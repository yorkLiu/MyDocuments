#!/usr/bin/env python3
"""301358 7/20 主力操作复盘图 — 按复盘框架"""
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

with open('/tmp/301358_t5.json') as f:
    data = json.load(f)
bars = data['data']
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

fig = plt.figure(figsize=(22, 20))
gs = GridSpec(4, 2, figure=fig, height_ratios=[3, 1, 1, 1], hspace=0.35, wspace=0.2,
              left=0.06, right=0.96, top=0.97, bottom=0.04)

# === 1. 全天分时+大单+阶段 ===
ax1 = fig.add_subplot(gs[0, :])
x = np.arange(len(bars))
colors_vol = ['#cc0000' if i > 0 and prices[i] >= prices[i-1] else '#00aa00' for i in range(len(bars))]
ax1_v = ax1.twinx()
ax1_v.bar(x, [v/10000 for v in real_vols], color=colors_vol, alpha=0.25, width=0.8)

ax1.plot(x, prices, color='#cc0000', linewidth=2, zorder=5)
ax1.axhline(y=vwap, color='blue', linewidth=1.5, linestyle='--', alpha=0.6, label=f'VWAP {vwap:.2f}')
ax1.axhline(y=59.47, color='#888888', linewidth=1, linestyle=':', alpha=0.4, label='7/17 close 59.47')
ax1.axhline(y=57.54, color='#000099', linewidth=1.5, linestyle='--', alpha=0.3, label='7/13 block 57.54')

# 阶段背景
stages = [
    (0, 42, '#fff8e8', '①拉高出货'),
    (42, 120, '#f0f0f0', '②横盘阴跌'),
    (120, 167, '#fff0f0', '③午后砸盘'),
    (167, 191, '#ffe0e0', '④恐慌探底'),
    (191, len(bars), '#e8fff0', '⑤反弹拉尾'),
]
for s, e, color, label in stages:
    ax1.axvspan(s, e, color=color, alpha=0.4, zorder=0)
    mid = (s+e)/2
    ax1.text(mid, 62.5, label, ha='center', fontsize=10, fontweight='bold', alpha=0.7)

# 大单标记
for i in range(len(bars)):
    if real_vols[i] >= 150000:
        color = '#00aa00' if i > 0 and prices[i] >= prices[i-1] else '#cc0000'
        ax1.scatter(i, prices[i], s=80, color=color, zorder=10, edgecolors='black', linewidth=0.5)

tick_idx = [i for i, t in enumerate(times) if t.endswith(':00') or t.endswith(':30') or i == len(bars)-1]
ax1.set_xticks([i for i in tick_idx])
ax1.set_xticklabels([times[i] for i in tick_idx], fontsize=8, rotation=30)
ax1.set_ylabel('Price', fontsize=12)
ax1.set_title('301358 7/20 主力操作复盘 — 5阶段全景\n'
              '09:31 79.84wan开盘买入 → 10:10/11:15 61.15双顶出货 → 13:39 18.43wan砸盘 → 14:40 19.64wan护盘 → 14:50拉尾',
              fontsize=13, fontweight='bold')
ax1.legend(fontsize=9, loc='upper right')
ax1.grid(True, alpha=0.12)

# 关键节点标注
ax1.annotate('09:31 79.84万股\n4806万 超大买', xy=(1, 60.19), xytext=(5, 62),
             fontsize=9, color='#00aa00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00aa00', lw=1.5))
ax1.annotate('10:10 61.14\n第1次冲顶', xy=(41, 61.14), xytext=(25, 62.5),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1))
ax1.annotate('11:11 61.15\n第2次冲顶\n双顶=出货', xy=(82, 61.15), xytext=(55, 62.5),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
ax1.annotate('13:39 18.43万股\n砸盘1086万', xy=(166, 58.92), xytext=(120, 57),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=2),
             bbox=dict(boxstyle='round', facecolor='#fff0f0'))
ax1.annotate('13:56 58.18\n全天最低\n距57.54仅0.64', xy=(187, 58.18), xytext=(140, 56.3),
             fontsize=10, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=2),
             bbox=dict(boxstyle='round', facecolor='#fff0f0'))
ax1.annotate('14:40 19.64万股\n护盘1155万\n反弹起点', xy=(231, 58.80), xytext=(185, 60.5),
             fontsize=10, color='#00aa00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00aa00', lw=2),
             bbox=dict(boxstyle='round', facecolor='#f0fff0'))
ax1.annotate('14:50-14:57\n5连大单拉尾\n+4171万', xy=(237, 59.99), xytext=(200, 61.5),
             fontsize=9, color='#00aa00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00aa00', lw=1.5))

# === 2. 5阶段大单净额 ===
ax2 = fig.add_subplot(gs[1, :])
seg_names = ['①拉高\n09:30-10:11', '②阴跌\n10:12-11:30', '③砸盘\n13:01-13:39', '④探底\n13:40-14:00', '⑤反弹\n14:01-15:00']
seg_ranges = [(0,42), (42,120), (120,167), (167,191), (191,len(bars))]
seg_buys = []
seg_sells = []
seg_nets = []
for s, e in seg_ranges:
    e = min(e, len(bars))
    buy = sell = 0
    for i in range(s, e):
        if real_vols[i] >= 100000:
            direction = '卖' if i > 0 and prices[i] < prices[i-1] else '买'
            amt = real_vols[i]*prices[i]/10000
            if direction == '买': buy += amt
            else: sell += amt
    seg_buys.append(buy)
    seg_sells.append(sell)
    seg_nets.append(buy - sell)

x2 = np.arange(5)
width = 0.35
bars_b = ax2.bar(x2 - width/2, seg_buys, width, color='#00aa00', alpha=0.7, label='Buy')
bars_s = ax2.bar(x2 + width/2, seg_sells, width, color='#cc0000', alpha=0.7, label='Sell')
for i, n in enumerate(seg_nets):
    color = '#00aa00' if n > 0 else '#cc0000'
    ax2.text(i, max(seg_buys[i], seg_sells[i]) + 300, f'{n:+.0f}万', ha='center', fontsize=11, color=color, fontweight='bold')
ax2.axhline(y=0, color='black', linewidth=0.5)
ax2.set_xticks(x2)
ax2.set_xticklabels(seg_names, fontsize=10)
ax2.set_ylabel('Amount (wan)', fontsize=11)
ax2.set_title('5阶段大单净额：①+9157万(买) → ②-2024万(卖) → ③-2262万(砸) → ④-866万(卖) → ⑤+12867万(买)',
              fontsize=12, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.15, axis='y')

# === 3. 0.5元筹码分布 ===
ax3 = fig.add_subplot(gs[2, 0])
bins = {}
for i in range(len(bars)):
    bucket = round(prices[i]*2)/2
    bins[bucket] = bins.get(bucket, 0) + real_vols[i]
all_p = sorted(bins.keys())
pcts = [bins[p]/total_vol*100 for p in all_p]
colors = ['#cc0000' if p >= 60 else '#0066cc' for p in all_p]
ax3.barh(np.arange(len(all_p)), pcts, color=colors, alpha=0.7)
ax3.set_yticks(np.arange(len(all_p)))
ax3.set_yticklabels(['%.1f' % p for p in all_p], fontsize=10)
ax3.set_xlabel('Volume %', fontsize=11)
ax3.set_title('7/20 筹码分布\n60以上47.2% vs 60以下52.8%', fontsize=11, fontweight='bold')
for i, p in enumerate(pcts):
    ax3.text(p+1, i, f'{p:.1f}%', va='center', fontsize=9)
ax3.grid(True, alpha=0.15, axis='x')

# === 4. AM vs PM 对比 ===
ax4 = fig.add_subplot(gs[2, 1])
pm_start = next((i for i, t in enumerate(times) if t >= '13:01'), len(bars))
am_vol = sum(real_vols[:pm_start])
pm_vol = sum(real_vols[pm_start:])
am_buy = sum(v*p/10000 for i, (v, p) in enumerate(zip(real_vols[:pm_start], prices[:pm_start])) if v >= 100000 and (i == 0 or prices[i] >= prices[i-1]))
pm_buy = sum(v*p/10000 for i, (v, p) in enumerate(zip(real_vols[pm_start:], prices[pm_start:])) if v >= 100000 and (i+pm_start == 0 or prices[i+pm_start] >= prices[i+pm_start-1]))

cats = ['AM\n09:30-11:30', 'PM\n13:01-15:00']
vols = [am_vol/total_vol*100, pm_vol/total_vol*100]
ax4.bar(cats, vols, color=['#0066cc', '#ff6600'], alpha=0.7, width=0.5)
for i, v in enumerate(vols):
    ax4.text(i, v+2, f'{v:.1f}%', ha='center', fontsize=13, fontweight='bold')
ax4.set_ylabel('% of day volume', fontsize=11)
ax4.set_title('AM vs PM 量能分布\nAM 74.4% vs PM 25.6%', fontsize=11, fontweight='bold')
ax4.grid(True, alpha=0.15, axis='y')

# === 5. 价格区统计 ===
ax5 = fig.add_subplot(gs[3, :])
# 按1元区间
price_bins = {}
for i in range(len(bars)):
    bucket = round(prices[i])
    price_bins[bucket] = price_bins.get(bucket, 0) + real_vols[i]
p_sorted = sorted(price_bins.keys())
p_pcts = [price_bins[p]/total_vol*100 for p in p_sorted]

x5 = np.arange(len(p_sorted))
colors5 = []
for p in p_sorted:
    if p >= 61: colors5.append('#cc0000')  # 出货区
    elif p >= 60: colors5.append('#ff6600')  # 中枢
    elif p >= 59: colors5.append('#0066cc')  # 吸筹区
    else: colors5.append('#00aa00')  # 恐慌区

ax5.bar(x5, p_pcts, color=colors5, alpha=0.7, width=0.6)
for i, p in enumerate(p_pcts):
    ax5.text(i, p+1, f'{p:.1f}%', ha='center', fontsize=11, fontweight='bold')
ax5.set_xticks(x5)
ax5.set_xticklabels(['%.0f元' % p for p in p_sorted], fontsize=12)
ax5.set_ylabel('% of day volume', fontsize=11)
ax5.set_title('成交价格分布\n恐慌区(58-) 吸筹区(59-60) 中枢(60) 出货区(61+)',
              fontsize=12, fontweight='bold')
ax5.grid(True, alpha=0.15, axis='y')

# 添加分区标注
ax5.axhline(y=max(p_pcts)*0.8, color='gray', linewidth=0.5, linestyle=':')
ax5.text(0, max(p_pcts)*0.85, '←恐慌吸筹', fontsize=10, color='#00aa00', fontweight='bold')
ax5.text(1, max(p_pcts)*0.85, '←主力吸筹', fontsize=10, color='#0066cc', fontweight='bold')
ax5.text(2, max(p_pcts)*0.85, '←做T中枢', fontsize=10, color='#ff6600', fontweight='bold')
ax5.text(3, max(p_pcts)*0.85, '←高位出货', fontsize=10, color='#cc0000', fontweight='bold')

plt.savefig('/data/hermes/workspace/301358_0720_review.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_0720_review.png')
