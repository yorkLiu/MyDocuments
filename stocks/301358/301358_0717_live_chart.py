#!/usr/bin/env python3
"""301358 7/17 实时分析图 — 截至11:23 午盘前"""
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

with open('/tmp/301358_tl_latest.json') as f:
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
amts = [b['amount'] for b in bars]
total_vol = sum(real_vols)
vwap = sum(p*v for p,v in zip(prices, real_vols)) / total_vol

fig = plt.figure(figsize=(20, 18))
gs = GridSpec(2, 2, figure=fig, height_ratios=[2, 1.8], hspace=0.25, wspace=0.2,
              left=0.07, right=0.95, top=0.95, bottom=0.04)

# ========== 1. 分时走势 ==========
ax1 = fig.add_subplot(gs[0, :])
x = np.arange(len(bars))
colors_vol = []
for i in range(len(bars)):
    if i > 0 and prices[i] >= prices[i-1]:
        colors_vol.append('#cc0000')
    else:
        colors_vol.append('#00aa00')

ax1_bar = ax1.twinx()
ax1_bar.bar(x, [v/10000 for v in real_vols], color=colors_vol, alpha=0.25, width=0.8)

ax1.plot(x, prices, color='#cc0000', linewidth=1.8, zorder=5)
ax1.axhline(y=vwap, color='blue', linewidth=1.5, linestyle='--', alpha=0.6, label=f'VWAP {vwap:.2f}')
ax1.axhline(y=60, color='#00aa00', linewidth=2, linestyle=':', alpha=0.5, label='60 line')
ax1.axhline(y=60.31, color='#006600', linewidth=1.5, linestyle='--', alpha=0.4, label='7/16 low 60.31 (broken)')
ax1.axhline(y=57.54, color='#000099', linewidth=1.5, linestyle='--', alpha=0.3, label='7/10 block 57.54')
ax1.axhline(y=61.24, color='#888888', linewidth=1, linestyle=':', alpha=0.3, label='7/16 close 61.24')

# 5段着色背景
seg_colors = ['#fff8e8', '#fff8e8', '#ffeeee', '#ffeeee', '#e8fff8']
seg_ranges = [(0,4), (4,15), (15,31), (31,81), (81,len(bars))]
for (s,e), c in zip(seg_ranges, seg_colors):
    ax1.axvspan(s-0.5, e-0.5, color=c, alpha=0.3, zorder=0)

# 大单标记
for i in range(len(bars)):
    if real_vols[i] >= 200000:
        dir_color = '#cc0000' if i > 0 and prices[i] < prices[i-1] else '#00aa00'
        ax1.scatter(i, prices[i], s=80, color=dir_color, zorder=10, edgecolors='black', linewidth=0.8)

tick_idx = [i for i, t in enumerate(times) if t.endswith(':00') or t.endswith(':30')]
ax1.set_xticks([i for i in tick_idx])
ax1.set_xticklabels([times[i] for i in tick_idx], fontsize=9, rotation=30)
ax1.set_ylabel('Price', fontsize=12)
ax1.set_title('301358 Hunan Yuneng 7/17 Intraday (as of 11:23) — V-SHAPED RECOVERY\n'
              '58.85 low → 60.69 now | VWAP 60.60 | Big order net -2604wan (narrowing)',
              fontsize=14, fontweight='bold')
ax1.legend(fontsize=9, loc='upper right')
ax1.grid(True, alpha=0.15)

# 关键节点标注
ax1.annotate('OPEN 61.08', xy=(0, 61.08), xytext=(5, 62.2),
             fontsize=8, color='#cc0000', arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1))
ax1.annotate('BREAK 60\n10:00\n28.6wan SHI', xy=(30, 59.97), xytext=(35, 61.5),
             fontsize=8, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
ax1.annotate('LOW 58.85\n10:54', xy=(78, 58.85), xytext=(72, 57.8),
             fontsize=8, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
ax1.annotate('V-REVERSE\n11:06-11:08\n80.6wan BUY', xy=(83, 61.7), xytext=(70, 62.8),
             fontsize=10, color='#00aa00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00aa00', lw=2),
             bbox=dict(boxstyle='round', facecolor='#f0fff0'))

# ========== 2a. 5阶段VWAP对比 ==========
ax2 = fig.add_subplot(gs[1, 0])
seg_labels = ['Open', 'Rush', 'Crash', 'Bottom', 'Recover']
seg_vwaps = []
seg_vols_pct = []
for s, e in [(0,4), (4,15), (15,31), (31,81), (81,len(bars))]:
    e = min(e, len(bars))
    sp = prices[s:e]
    sv = real_vols[s:e]
    v_sum = sum(sv)
    sw = sum(p*v for p,v in zip(sp, sv))/v_sum if v_sum else 0
    seg_vwaps.append(sw)
    seg_vols_pct.append(v_sum/total_vol*100)

colors_seg = ['#cc0000', '#ff6600', '#cc0000', '#990000', '#00aa00']
bars2 = ax2.bar(seg_labels, seg_vwaps, color=colors_seg, alpha=0.8, width=0.5)
ax2.set_ylabel('VWAP', fontsize=11)
ax2.set_title('5-Stage VWAP & Volume Share\nKey: Bottom VWAP 59.62 vs Recover VWAP 60.77',
              fontsize=12, fontweight='bold')
ax2.axhline(y=57.54, color='#000099', linewidth=1, linestyle='--', alpha=0.5, label='block 57.54')
ax2.axhline(y=60.31, color='#006600', linewidth=1, linestyle='--', alpha=0.5, label='7/16 low 60.31')
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.15, axis='y')

for b, w, p in zip(bars2, seg_vwaps, seg_vols_pct):
    ax2.text(b.get_x() + b.get_width()/2, w + 0.2, f'{w:.2f}\n{p:.1f}%',
             ha='center', fontsize=9, fontweight='bold')

# ========== 2b. 价格分布对比 ==========
ax3 = fig.add_subplot(gs[1, 1])
bins_17 = {}
for i in range(len(bars)):
    bucket = round(prices[i])
    bins_17[bucket] = bins_17.get(bucket, 0) + real_vols[i]

bins_16_pct = {61: 45.3, 62: 40.2, 63: 11.8, 64: 2.7}
all_p = sorted(set(list(bins_17.keys()) + list(bins_16_pct.keys())))
r_17 = [bins_17.get(p, 0)/total_vol*100 for p in all_p]
r_16 = [bins_16_pct.get(p, 0) for p in all_p]

x3 = np.arange(len(all_p))
width = 0.35
ax3.bar(x3 - width/2, r_16, width, color='#ff6600', alpha=0.6, label='7/16')
ax3.bar(x3 + width/2, r_17, width, color='#cc0000', alpha=0.8, label='7/17')
ax3.set_xticks(x3)
ax3.set_xticklabels([f'{p}' for p in all_p], fontsize=11)
ax3.set_xlabel('Price', fontsize=11)
ax3.set_ylabel('Volume %', fontsize=11)
ax3.set_title('7/16 vs 7/17 Distribution Comparison\n7/17: 62 zone recover to 29%, 59 zone only 14%',
              fontsize=12, fontweight='bold')
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.15, axis='y')

for i, (r16, r17) in enumerate(zip(r_16, r_17)):
    if r16 > 0:
        ax3.text(i - width/2, r16 + 1, f'{r16:.0f}%', ha='center', fontsize=8, color='#ff6600')
    ax3.text(i + width/2, r17 + 1, f'{r17:.0f}%', ha='center', fontsize=8, color='#cc0000')

plt.savefig('/data/hermes/workspace/301358_0717_live_analysis.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_0717_live_analysis.png')
