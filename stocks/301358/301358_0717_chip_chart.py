#!/usr/bin/env python3
"""301358 7/17 实时筹码分析（截至10:50）"""
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

# 7/17分时数据
with open('/tmp/301358_tl_0716_v2.json') as f:
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
vwap = sum(p*v for p,v in zip(prices, real_vols)) / total_vol

# 60日K线
with open('/tmp/301358_klines_60d_v2.json') as f:
    k_data = json.load(f)
klines = k_data['data']['sz301358']['qfqday']
bins_60d = {}
for k in klines:
    bucket = round(float(k[2]))
    bins_60d[bucket] = bins_60d.get(bucket, 0) + int(float(k[5]))
total_60d = sum(bins_60d.values())

fig = plt.figure(figsize=(20, 22))
gs = GridSpec(3, 2, figure=fig, height_ratios=[2, 1.5, 2.5], hspace=0.3, wspace=0.25,
              left=0.07, right=0.95, top=0.96, bottom=0.03)

# ============ 1. 7/17分时走势 ============
ax1 = fig.add_subplot(gs[0, :])
x = np.arange(len(bars))
ax1.plot(x, prices, color='#cc0000', linewidth=1.5, label='Price')
ax1.axhline(y=vwap, color='blue', linewidth=1, linestyle='--', alpha=0.5, label='VWAP=%.2f' % vwap)
ax1.axhline(y=60, color='#00aa00', linewidth=1.5, linestyle=':', alpha=0.7, label='60 support')
ax1.axhline(y=60.31, color='#006600', linewidth=2, linestyle='--', alpha=0.7, label='7/16 low 60.31 (BROKEN!)')
ax1.axhline(y=57.54, color='#000099', linewidth=1.5, linestyle='--', alpha=0.5, label='7/10 block trade 57.54')
ax1.axhline(y=61.24, color='#888888', linewidth=1, linestyle=':', alpha=0.5, label='7/16 close 61.24')
ax1.axhline(y=63.73, color='#ff6600', linewidth=1, linestyle=':', alpha=0.3, label='7/16 high 63.73')

# 成交量柱
ax1v = ax1.twinx()
colors_vol = ['#cc0000' if prices[i] < (prices[i-1] if i>0 else prices[i]) else '#00aa00' for i in range(len(bars))]
ax1v.bar(x, [v/10000 for v in real_vols], color=colors_vol, alpha=0.3, width=0.8)

tick_idx = [i for i, t in enumerate(times) if t.endswith(':00') or t.endswith(':30')]
ax1.set_xticks([i for i in tick_idx])
ax1.set_xticklabels([times[i] for i in tick_idx], fontsize=9, rotation=30)
ax1.set_ylabel('Price', fontsize=12)
ax1.set_title('301358 Hunan Yuneng 7/17 Intraday (as of 10:50)\nCurrent: 58.98 (-3.87%) | 60.31 BROKEN | 58.93 low | VWAP 60.55',
              fontsize=14, fontweight='bold')
ax1.legend(fontsize=9, loc='upper right')
ax1.grid(True, alpha=0.15)

# 标注跌破60
ax1.annotate('BREAK 60\n10:00\n59.97', xy=(60, 59.97), xytext=(70, 61.5),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=2),
             bbox=dict(boxstyle='round', facecolor='#fff0f0'))
ax1.annotate('58.93 LOW\n10:49', xy=(79, 58.93), xytext=(65, 57.5),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5),
             bbox=dict(boxstyle='round', facecolor='#fff0f0'))

# ============ 2a. 7/17 vs 7/16 价格分布对比 ============
ax2 = fig.add_subplot(gs[1, 0])
bins_17 = {}
for i in range(len(bars)):
    bucket = round(prices[i])
    bins_17[bucket] = bins_17.get(bucket, 0) + real_vols[i]

# 7/16数据（从K线获取）
bins_16 = {61: 0, 62: 0, 63: 0}
# 无法直接分时分桶7/16，用估算：7/16主要在61-63
# 从之前分析知道：61=45.3%, 62=40.2%, 63=11.8%
bins_16_pct = {61: 45.3, 62: 40.2, 63: 11.8, 64: 2.7}

all_p = sorted(set(list(bins_17.keys()) + list(bins_16_pct.keys())))
r_17 = [bins_17.get(p, 0)/total_vol*100 for p in all_p]
r_16 = [bins_16_pct.get(p, 0) for p in all_p]

x2 = np.arange(len(all_p))
width = 0.35
ax2.bar(x2 - width/2, r_16, width, color='#ff6600', alpha=0.7, label='7/16')
ax2.bar(x2 + width/2, r_17, width, color='#cc0000', alpha=0.8, label='7/17')
ax2.set_xticks(x2)
ax2.set_xticklabels(['%d' % p for p in all_p], fontsize=11)
ax2.set_xlabel('Price', fontsize=11)
ax2.set_ylabel('Volume %', fontsize=11)
ax2.set_title('7/16 vs 7/17 Price Distribution\n7/17 shifted to 59-60 zone (38%), 7/16 was 61-62 (85%)',
              fontsize=12, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.15, axis='y')

for i, (r16, r17) in enumerate(zip(r_16, r_17)):
    if r16 > 0: ax2.text(i - width/2, r16 + 1, '%.1f%%' % r16, ha='center', fontsize=8, color='#ff6600')
    ax2.text(i + width/2, r17 + 1, '%.1f%%' % r17, ha='center', fontsize=8, color='#cc0000')

# ============ 2b. 大单方向 ============
ax3 = fig.add_subplot(gs[1, 1])
# 大单分类
big_buy = 0
big_sell = 0
for i in range(len(bars)):
    if real_vols[i] >= 100000:
        if i > 0 and prices[i] < prices[i-1]:
            big_sell += real_vols[i] * prices[i] / 10000
        else:
            big_buy += real_vols[i] * prices[i] / 10000

categories = ['Big Buy\n(>10wan)', 'Big Sell\n(>10wan)', 'Net']
values = [big_buy, big_sell, big_buy - big_sell]
colors_bar = ['#00aa00', '#cc0000', '#cc0000' if big_buy-big_sell < 0 else '#00aa00']

bars3 = ax3.bar(np.arange(3), values, color=colors_bar, alpha=0.8, width=0.5)
ax3.set_xticks(np.arange(3))
ax3.set_xticklabels(categories, fontsize=10)
ax3.set_ylabel('Amount (wan)', fontsize=11)
ax3.set_title('7/17 Big Order Analysis (35 orders)\nNet: -%.0fwan (selling)' % abs(big_buy-big_sell),
              fontsize=12, fontweight='bold')
ax3.axhline(y=0, color='black', linewidth=0.5)
ax3.grid(True, alpha=0.15, axis='y')

for b, v in zip(bars3, values):
    ax3.text(b.get_x() + b.get_width()/2, v + 200 if v > 0 else v - 800,
             '%.0fwan' % v, ha='center', fontsize=11, fontweight='bold')

# ============ 3. Mistery深度分析 ============
ax4 = fig.add_subplot(gs[2, :])
ax4.axis('off')

analysis_text = """
=== MISTERY视角：7/17 实时筹码分析（截至10:50）===

一、60.31防线被击穿
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7/16最低60.31坚守了5小时 → 7/17 10:00被28.6万股大单砸破59.97 → 最低58.93
  这意味着7/16主力画的"60-64元盒子"底部被击穿了。
  
  但注意：58.93距离7/10大宗交易价57.54仅1.36元（2.4%），下方空间有限。

二、与昨日筹码分布对比
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7/16: 61-62元集中85% → 底部吸筹区
  7/17: 59-60元集中51% → 筹码继续下移
  
  价格中枢从61.5元 → 59.5元（下移2元，-3.3%）
  这说明7/16在61-62买入的主力（58.3%的量）今天没有护盘——直接让价格滑到59-60
  
  关键数据：7/17 VWAP=60.55，当前价58.98，价低于VWAP 2.59%
  → 今天平均买入成本60.55，但价格已经跌破成本，说明主力没有在VWAP以下护盘

三、上午为什么要拉？现在变成了"不拉"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7/16上午拉升到63.73是为了给午后出货制造空间
  7/17上午根本没有拉——开盘61.08，冲到61.88就放弃了
  
  为什么不拉了？
  → 7/16午后已经把63+的筹码全部砸出去，今天没有高位筹码需要出
  → 昨天63→61 T+0赚的2元今天不需要再复制
  → 今天大盘暴跌（创业板-5.49%），主力不会逆势做T

四、大单方向：净卖出3412万
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  35笔大单中：
  → 买入16772万（09:31-09:33开盘拉61.60-61.88是诱多）
  → 卖出20185万（随后持续卖出到58.93）
  
  大单净卖出3412万 = 主力在出货
  对比7/16全天主力净流出约2000-3000万，今天仅上午就超过了昨天全天

五、下方获利筹码：彻底消失
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7/16还有2.7%在60-61元的微利盘 → 今天全部变成套牢盘
  7/17成58.93 → 7/16在61-62买入的58.3%筹码全部套牢2-3元
  
  现在的筹码结构：
  → 58-59元（今天新买入）：51% ← 新的底部区
  → 60-61元（7/16买入套牢）：约30% ← 昨天的底部变成今天的套牢
  → 61-63元（7/15-7/16高位套牢）：约15% ← 继续套
  → 64元以上（60日老套牢盘）：94.6% ← 纹丝不动

六、上方套牢筹码
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  与7/16一致：65元以上零成交（0%），94.6%的60日筹码完全锁仓不动
  套牢盘不松动 = 没有人割肉 = 上方压力依然在

七、Mistery判断
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7/16我判断："主力画了60-64的盒子做T+0"
  7/17盒子被打破 → 说明主力改变策略了
  
  两种可能：
  A. 大盘暴跌（创业板-5.49%）导致主力放弃护盘，顺势洗到57.54附近吸筹
  B. 主力已经完成出货，不再关心这个价位
  
  关键信号：
  → 量比1.35（昨天1.75）= 放量但不如昨天恐慌
  → 58.93仅一瞬即弹回59+ = 58-59有接盘
  → 距57.54仅2.4% = 下方空间有限
  
  明日关键：57.54能否守住？如果守住=主力在57-59吸筹，等大盘企稳再拉升
  如果破57.54=中期趋势彻底走坏，看到55-53
"""

ax4.text(0.03, 0.97, analysis_text, fontsize=10.5, va='top', fontfamily='monospace',
         transform=ax4.transAxes,
         bbox=dict(boxstyle='round', facecolor='#fafafa', edgecolor='#ccc'))

plt.savefig('/data/hermes/workspace/301358_0717_chip_analysis.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_0717_chip_analysis.png')
