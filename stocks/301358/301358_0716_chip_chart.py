#!/usr/bin/env python3
"""301358 7/16 筹码交易分布深度分析图"""
import json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.gridspec import GridSpec

font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
fm.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'WenQuanYi Zen Hei'
plt.rcParams['axes.unicode_minus'] = False

# 7/16分时数据
with open('/tmp/301358_tl_0716_final.json') as f:
    tl_data = json.load(f)
bars = tl_data['data']
real_vols = []
for i in range(len(bars)):
    if i == 0:
        real_vols.append(int(bars[i]['volume']))
    else:
        real_vols.append(max(int(bars[i]['volume']) - int(bars[i-1]['volume']), 0))
prices = [float(b['price']) for b in bars]
times = [b['time'] for b in bars]
total_vol = sum(real_vols)

# 0.5元分桶
bins_05 = {}
for i in range(len(bars)):
    bucket = round(prices[i] * 2) / 2
    bins_05[bucket] = bins_05.get(bucket, 0) + real_vols[i]

# 60日K线
with open('/tmp/301358_klines_60d.json') as f:
    k_data = json.load(f)
klines = k_data['data']['sz301358']['qfqday']
bins_60d = {}
for k in klines:
    close = float(k[2])
    vol = int(float(k[5]))
    bucket = round(close)
    bins_60d[bucket] = bins_60d.get(bucket, 0) + vol
total_60d = sum(bins_60d.values())

# 分时段
rally_start = None
pm_start = None
for i, b in enumerate(bars):
    if b['time'] >= '10:30' and rally_start is None:
        rally_start = i
    if b['time'] >= '13:01' and pm_start is None:
        pm_start = i

# 各段分桶
def segment_bins(start, end):
    bins = {}
    for i in range(start, end):
        bucket = round(prices[i])
        bins[bucket] = bins.get(bucket, 0) + real_vols[i]
    return bins

crash_bins = segment_bins(0, 30)       # 09:30-09:59
rally_bins = segment_bins(rally_start, pm_start-1)  # 10:30-11:30
pm_bins = segment_bins(pm_start, len(bars))         # 13:01-15:00

fig = plt.figure(figsize=(20, 24))
gs = GridSpec(4, 2, figure=fig, height_ratios=[2, 2, 1.8, 2.5], hspace=0.3, wspace=0.25,
              left=0.07, right=0.95, top=0.96, bottom=0.03)

# ============ 1. 7/16全天筹码分布（横向直方图）============
ax1 = fig.add_subplot(gs[0, :])
sorted_prices = sorted(bins_05.keys())
vol_pct = [bins_05[p]/total_vol*100 for p in sorted_prices]

colors = []
for p in sorted_prices:
    if p < 61: colors.append('#00aa00')      # 获利区
    elif p < 62: colors.append('#88cc00')    # 底部
    elif p < 63: colors.append('#ffaa00')    # 横盘
    elif p < 64: colors.append('#ff6600')    # 拉升
    else: colors.append('#cc0000')           # 套牢

y_pos = np.arange(len(sorted_prices))
ax1.barh(y_pos, vol_pct, color=colors, alpha=0.8, height=0.7)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(['%.1f-%.1f' % (p, p+0.5) for p in sorted_prices], fontsize=10)
ax1.set_xlabel('Volume %', fontsize=12)
ax1.set_title('7/16 Full Day Volume Distribution by Price\nKey: 61-62=58.3% (bottom), 62-63=28.4% (sideways), 63-64=10.7% (rally zone)',
              fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.15, axis='x')

# 标注
for i, (p, v) in enumerate(zip(sorted_prices, vol_pct)):
    ax1.text(v + 0.5, i, '%.1f%%' % v, va='center', fontsize=10, fontweight='bold')

# 60日筹码在右侧虚线
ax1_r = ax1.twiny()
for p in sorted(bins_60d.keys()):
    if p < 65:
        ax1_r.barh(p/0.5-0.5, bins_60d.get(p,0)/total_60d*100, alpha=0.15, color='blue', height=0.3)
ax1_r.set_xlim(ax1.get_xlim())
ax1_r.set_xlabel('60d volume % (blue overlay)', fontsize=9, color='blue')

# 区域标注
ax1.axhline(y=0.5, color='#00aa00', linewidth=2, linestyle='--', alpha=0.5)
ax1.axhline(y=3.5, color='#ffaa00', linewidth=2, linestyle='--', alpha=0.5)
ax1.text(15, -0.3, 'PROFIT\nZONE', fontsize=9, color='#00aa00', fontweight='bold')
ax1.text(15, 1.5, 'BOTTOM\n58.3%', fontsize=9, color='#88cc00', fontweight='bold')
ax1.text(15, 3.5, 'SIDEWAYS\n28.4%', fontsize=9, color='#ffaa00', fontweight='bold')

# ============ 2. 上午拉升 vs 午后下跌 筹码对比 ============
ax2 = fig.add_subplot(gs[1, :])
all_p = sorted(set(list(rally_bins.keys()) + list(pm_bins.keys())))
rally_total = sum(rally_bins.values())
pm_total = sum(pm_bins.values())

rally_pct = [rally_bins.get(p,0)/rally_total*100 for p in all_p]
pm_pct = [pm_bins.get(p,0)/pm_total*100 for p in all_p]

x = np.arange(len(all_p))
width = 0.35

bars_r = ax2.bar(x - width/2, rally_pct, width, color='#00aa00', alpha=0.8, label='Rally 10:30-11:30 (Auto buy)')
bars_p = ax2.bar(x + width/2, pm_pct, width, color='#cc0000', alpha=0.8, label='PM Selloff 13:01-15:00 (PM sell)')

ax2.set_xticks(x)
ax2.set_xticklabels(['%d' % p for p in all_p], fontsize=11)
ax2.set_xlabel('Price (RMB)', fontsize=12)
ax2.set_ylabel('Volume %', fontsize=12)
ax2.set_title('Morning Rally vs Afternoon Selloff — Chip Distribution Comparison\n63+ chips bought in AM (39.5%) were dumped to 61 in PM (75.3% < 62)',
              fontsize=13, fontweight='bold')
ax2.legend(fontsize=10, loc='upper right')
ax2.grid(True, alpha=0.15, axis='y')

for i, (r, p) in enumerate(zip(rally_pct, pm_pct)):
    ax2.text(i - width/2, r + 1, '%.1f%%' % r, ha='center', fontsize=9, fontweight='bold', color='#006600')
    ax2.text(i + width/2, p + 1, '%.1f%%' % p, ha='center', fontsize=9, fontweight='bold', color='#cc0000')

# 箭头标注筹码转移
ax2.annotate('', xy=(1, 20), xytext=(2, 40),
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=2))
ax2.text(1.5, 32, 'Chip\nTransfer\n63→61\n(-3.9%)', fontsize=9, ha='center',
         color='#cc0000', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='#fff0f0', edgecolor='#cc0000'))

# ============ 3. 各阶段成交量占比 ============
ax3 = fig.add_subplot(gs[2, 0])
seg_labels = ['1.Crash\n09:30-09:31', '2.Bottom\n09:32-09:59', '3.Sideway\n10:00-10:29',
              '4.Rally\n10:30-11:30', '5.PM Sell\n13:01-13:30', '6.Drift\n13:31-14:30', '7.Close\n14:31-15:00']
seg_vols = [1522300, 5823700, 1799500, 3965100, 1736500, 1548500, 3631100]
seg_colors = ['#cc0000', '#ff6600', '#cccccc', '#00aa00', '#cc0000', '#ff6600', '#333333']

x3 = np.arange(len(seg_labels))
ax3.barh(x3, [v/10000 for v in seg_vols], color=seg_colors, alpha=0.8, height=0.6)
ax3.set_yticks(x3)
ax3.set_yticklabels(seg_labels, fontsize=8)
ax3.set_xlabel('Volume (10k shares)', fontsize=10)
ax3.set_title('Volume by Phase', fontsize=11, fontweight='bold')
ax3.invert_yaxis()
ax3.grid(True, alpha=0.1, axis='x')

for i, v in enumerate(seg_vols):
    ax3.text(v/10000 + 5, i, '%.1f%%' % (v/total_vol*100), va='center', fontsize=9, fontweight='bold')

# ============ 4. 60日 vs 7/16 筹码对比 ============
ax4 = fig.add_subplot(gs[2, 1])
# 只展示63元以下的对比（关键区域）
compare_prices = [61, 62, 63, 64]+list(range(66, 80, 2))+[80, 85, 90, 100, 110]
compare_prices = [p for p in compare_prices if p in bins_60d or p in bins_05]
cp = sorted(set(list(bins_05.keys()) + [p for p in bins_60d.keys() if p <= 67]))

r_pct_60 = [bins_60d.get(p, 0)/total_60d*100 for p in cp]
r_pct_16 = [bins_05.get(p, 0)/total_vol*100 for p in cp]

ax4_twin = ax4.twinx()

bars_60 = ax4.barh(np.arange(len(cp))-0.15, r_pct_60, height=0.3, color='blue', alpha=0.5, label='60d')
bars_16 = ax4.barh(np.arange(len(cp))+0.15, r_pct_16, height=0.3, color='red', alpha=0.8, label='7/16')
ax4.set_yticks(np.arange(len(cp)))
ax4.set_yticklabels(['%d' % p for p in cp], fontsize=10)
ax4.set_xlabel('Volume %', fontsize=10)
ax4.set_title('60d (blue) vs 7/16 (red) Distribution\n65+ chips: 7/16 = 0% vs 60d = 94.6%',
              fontsize=11, fontweight='bold')
ax4.legend(fontsize=9, loc='lower right')
ax4.grid(True, alpha=0.1, axis='x')

# ============ 5. Mistery分析结论 ============
ax5 = fig.add_subplot(gs[3, :])
ax5.axis('off')

analysis_text = """
=== MISTERY视角：7/16筹码交易分布深度分析 ===

一、全天筹码分布总览
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  60.5-61.0元:    2.7%  ← 获利盘（7/14抄底者微利）
  61.0-61.5元:   31.8%  ← 底部主力吸筹区
  61.5-62.0元:   26.4%  ← 底部主力吸筹区
  62.0-62.5元:   19.9%  ← 横盘换手区
  62.5-63.0元:    8.5%  ← 横盘换手区
  63.0-63.5元:    7.4%  ← 午收区/拉升区
  63.5-64.0元:    3.2%  ← 最高点附近
  64元以上:       0.0%  ← 零成交！

二、上午为什么要拉？
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  09:31暴砸60.31后横盘到10:30，主力在60-61吸筹29.1%全天量。
  10:30开始拉升，11:09-11:16连续放量（19.8万+21.4万+39.8万股）冲到63.73。
  
  拉升目的：不是突破，是给午后出货制造空间。
  → 上午在63元上方成交156.7万股（9952万元）= 这些就是午后要砸的筹码
  → 拉到63.73让散户追涨进场，为午后开盘砸盘提供足够的买盘对手方
  → 午收63.09故意收在63附近，让市场以为"企稳"，午后开盘32万股（2142万）直接砸

三、午后为何不让它继续涨？
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  如果午后继续涨到64+，主力在63+的卖单会被套（因为上方64-65有7/15的套牢盘）。
  主力不会用自己的钱去解放别人的套牢盘。
  
  午后直接出货的逻辑：
  → 13:01开盘34万股砸到62.60 = 把上午63+买入的人立刻套住
  → 13:01-15:00缩量阴跌到61.24 = 不给上午追涨者离场机会
  → 量比0.96 = 没有新买盘来接，价格自然下滑
  → 收盘61.24 = 完美收盘位（在60.31上方0.93元，在63.73下方2.49元）

四、下方获利筹码是否松动？
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7/14收盘61.98，7/13最低60.88。7/14抄底者成本约61-62元。
  7/16收盘61.24，这些筹码微亏或持平——没有获利，所以不存在"获利了结松动"。
  
  60元以下成交=0股（0.0%）。60元是60日筹码的绝对底线，从未被触及。
  真正的"下方获利盘"极少——7/16全天只有2.7%在60.5-61.0元成交，这些是
  7/13-7/14在60.88抄底的人，微利0.5元（+0.8%）就跑了。

五、上方套牢筹码又如何？
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  65元以上成交：0股（0.0%）← 完全没有触及！
  64元以上成交：0股（0.0%）← 也没有！
  63元以上成交：290.9万股（14.5%）← 但这是7/16新买入的，不是解套卖出
  
  60日筹码中94.6%在64元以上——这些套牢盘今天完全没有交易。
  深度套牢区（80-110元）占总筹码64.7%，全部锁仓不动。
  
  结论：上方套牢盘依然纹丝不动，与7/15一样零松动。
  7/16的交易完全在60-64元区间（本轮调整底部区域）内部完成。
"""

ax5.text(0.03, 0.97, analysis_text, fontsize=10.5, va='top', fontfamily='monospace',
         transform=ax5.transAxes,
         bbox=dict(boxstyle='round', facecolor='#fafafa', edgecolor='#ccc'))

plt.savefig('/data/hermes/workspace/301358_0716_chip_analysis.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_0716_chip_analysis.png')
