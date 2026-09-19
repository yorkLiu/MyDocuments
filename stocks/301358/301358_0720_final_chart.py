#!/usr/bin/env python3
"""301358 7/20 收盘前完整分析(截至14:48)"""
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

with open('/tmp/301358_t4.json') as f:
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

pm_start = next((i for i, t in enumerate(times) if t >= '13:01'), len(bars))

fig = plt.figure(figsize=(22, 18))
gs = GridSpec(2, 2, figure=fig, height_ratios=[2.5, 1.2], hspace=0.28, wspace=0.2,
              left=0.06, right=0.96, top=0.95, bottom=0.04)

# === 1. 全天分时 ===
ax1 = fig.add_subplot(gs[0, :])
x = np.arange(len(bars))
colors_vol = ['#cc0000' if i > 0 and prices[i] >= prices[i-1] else '#00aa00' for i in range(len(bars))]
ax1_v = ax1.twinx()
ax1_v.bar(x, [v/10000 for v in real_vols], color=colors_vol, alpha=0.25, width=0.8)

ax1.plot(x, prices, color='#cc0000', linewidth=2, zorder=5)
ax1.axhline(y=vwap, color='blue', linewidth=1.5, linestyle='--', alpha=0.6, label=f'VWAP {vwap:.2f}')
ax1.axhline(y=59.47, color='#888888', linewidth=1.5, linestyle=':', alpha=0.5, label='7/17 close 59.47')
ax1.axhline(y=60.31, color='#006600', linewidth=1, linestyle='--', alpha=0.3, label='7/16 low 60.31')
ax1.axhline(y=57.54, color='#000099', linewidth=1.5, linestyle='--', alpha=0.3, label='7/13 block 57.54')

for i in range(len(bars)):
    if real_vols[i] >= 100000:
        color = '#00aa00' if i > 0 and prices[i] >= prices[i-1] else '#cc0000'
        ax1.scatter(i, prices[i], s=60, color=color, zorder=10, edgecolors='black', linewidth=0.5)

ax1.axvline(x=pm_start, color='#ff6600', linewidth=2, linestyle='--', alpha=0.5)

tick_idx = [i for i, t in enumerate(times) if t.endswith(':00') or t.endswith(':30') or i == len(bars)-1]
ax1.set_xticks([i for i in tick_idx])
ax1.set_xticklabels([times[i] for i in tick_idx], fontsize=9, rotation=30)
ax1.set_ylabel('Price', fontsize=12)
ax1.set_title('301358 7/20 (as of 14:48) 3 STAGES: AM surge + PM crash + LATE rebound\n'
              'AM +121% val → PM crash to 58.18 (-4.7% from high) → 14:40 SUPER BUY 19.64wan → back to 59.49',
              fontsize=13, fontweight='bold')
ax1.legend(fontsize=9, loc='upper right')
ax1.grid(True, alpha=0.12)

# 关键节点标注
ax1.annotate('AM HIGH 61.15\n(10:10)', xy=(41, 61.15), xytext=(25, 62.3),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
ax1.annotate('13:39 砸盘\n18.43wan → 58.77', xy=(166, 58.77), xytext=(110, 57.5),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
ax1.annotate('13:56 LOW 58.18\n距57.54仅0.64元\n最危险时刻', xy=(187, 58.18), xytext=(140, 56.5),
             fontsize=10, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=2),
             bbox=dict(boxstyle='round', facecolor='#fff0f0'))
ax1.annotate('14:40 SUPER BUY!\n19.64万股大单反弹\n+0.28元', xy=(231, 58.80), xytext=(190, 60.5),
             fontsize=10, color='#00aa00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00aa00', lw=2),
             bbox=dict(boxstyle='round', facecolor='#f0fff0'))
ax1.annotate('NOW 59.49\nback to ~ VWAP', xy=(229, 59.49), xytext=(210, 61),
             fontsize=10, color='#000099', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#000099', lw=1))

# === 2a. 5个阶段大单对比 ===
ax2 = fig.add_subplot(gs[1, 0])
# 按时段统计
stages = [
    ('AM拉高\n09:30-10:11', 0, 42),
    ('AM回落\n10:12-11:30', 42, pm_start),
    ('PM开盘\n13:01-13:39', pm_start, 167),
    ('PM探底\n13:40-14:00', 167, 191),
    ('PM反弹\n14:01-14:48', 191, len(bars)),
]
stage_buys = []
stage_sells = []
labels = []
for label, s, e in stages:
    e = min(e, len(bars))
    if s >= len(bars) or s >= e: 
        stage_buys.append(0)
        stage_sells.append(0)
        labels.append(label)
        continue
    buy = sell = 0
    for i in range(s, e):
        if real_vols[i] >= 100000:
            direction = '卖' if i > 0 and prices[i] < prices[i-1] else '买'
            amt = real_vols[i]*prices[i]/10000
            if direction == '买': buy += amt
            else: sell += amt
    stage_buys.append(buy)
    stage_sells.append(sell)
    labels.append(label)

x2 = np.arange(len(stages))
width = 0.35
ax2.bar(x2 - width/2, stage_buys, width, color='#00aa00', alpha=0.7, label='Buy')
ax2.bar(x2 + width/2, stage_sells, width, color='#cc0000', alpha=0.7, label='Sell')
for i, (b, s) in enumerate(zip(stage_buys, stage_sells)):
    n = b - s
    color = '#00aa00' if n > 0 else '#cc0000'
    ax2.text(i, max(b, s) + 500, f'{n:+.0f}', ha='center', fontsize=10, color=color, fontweight='bold')
ax2.set_xticks(x2)
ax2.set_xticklabels(labels, fontsize=9)
ax2.set_ylabel('Amount (wan)', fontsize=11)
ax2.set_title('Big Order by 5 stages\n+9157wan AM buy → -2262wan PM crash → +2438wan PM rebound',
              fontsize=11, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.15, axis='y')

# === 2b. 筹码分布 ===
ax3 = fig.add_subplot(gs[1, 1])
bins = {}
for i in range(len(bars)):
    bucket = round(prices[i]*2)/2
    bins[bucket] = bins.get(bucket, 0) + real_vols[i]
all_p = sorted(bins.keys())
pcts = [bins[p]/total_vol*100 for p in all_p]

# 对比7/17和7/16
bins_17 = {58.5: 0, 59: 24.4, 59.5: 43.9, 60: 24.7, 61: 7.0, 61.5: 0}
bins_16 = {61: 45.3, 62: 40.2, 63: 11.8, 64: 2.7}

x3 = np.arange(len(all_p))
width = 0.25
r_20 = pcts
r_17 = [bins_17.get(p, 0) for p in all_p]
r_16 = [bins_16.get(p, 0) for p in all_p]

ax3.bar(x3 - width, r_16, width, color='#ff6600', alpha=0.6, label='7/16')
ax3.bar(x3, r_17, width, color='#cc0000', alpha=0.7, label='7/17')
ax3.bar(x3 + width, r_20, width, color='#0066cc', alpha=0.8, label='7/20')

ax3.set_xticks(x3)
ax3.set_xticklabels(['%.1f' % p for p in all_p], fontsize=10)
ax3.set_xlabel('Price', fontsize=11)
ax3.set_ylabel('Volume %', fontsize=11)
ax3.set_title('3-day chip distribution\n7/20 broadest base 58-61,59.5-60 core=46.3%',
              fontsize=11, fontweight='bold')
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.15, axis='y')

plt.savefig('/data/hermes/workspace/301358_0720_final.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_0720_final.png')
