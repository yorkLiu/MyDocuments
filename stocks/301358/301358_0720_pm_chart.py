#!/usr/bin/env python3
"""301358 7/20 截至13:40 午后暴跌分析图"""
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

with open('/tmp/301358_t3.json') as f:
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

# 午后分界
pm_start = next((i for i, t in enumerate(times) if t >= '13:01'), len(bars))

fig = plt.figure(figsize=(22, 16))
gs = GridSpec(2, 2, figure=fig, height_ratios=[2.5, 1.2], hspace=0.25, wspace=0.2,
              left=0.06, right=0.96, top=0.95, bottom=0.05)

# ============ 1. 全天分时 ============
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

# 大单标记
for i in range(len(bars)):
    if real_vols[i] >= 100000:
        color = '#00aa00' if i > 0 and prices[i] >= prices[i-1] else '#cc0000'
        ax1.scatter(i, prices[i], s=60, color=color, zorder=10, edgecolors='black', linewidth=0.5)

# 午后分界
ax1.axvline(x=pm_start, color='#ff6600', linewidth=2, linestyle='--', alpha=0.5, label='午休')

tick_idx = [i for i, t in enumerate(times) if t.endswith(':00') or t.endswith(':30') or i == len(bars)-1]
ax1.set_xticks([i for i in tick_idx])
ax1.set_xticklabels([times[i] for i in tick_idx], fontsize=9, rotation=30)
ax1.set_ylabel('Price', fontsize=12)
ax1.set_title('301358 7/20 (as of 13:40) — AM surge to 61.15 → PM crash to 58.77\n'
              'AM big order NET +10021wan → PM FLIP to -2262wan | Volume RATIO dropped to 1.11',
              fontsize=13, fontweight='bold')
ax1.legend(fontsize=9, loc='upper right')
ax1.grid(True, alpha=0.12)

ax1.annotate('AM HIGH 61.15\n(10:10) big buying', xy=(41, 61.15), xytext=(30, 62.5),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
ax1.annotate('LUNCH 60.20\nholding above 60', xy=(pm_start-1, 60.20), xytext=(pm_start+10, 61.5),
             fontsize=9, color='#ff6600',
             arrowprops=dict(arrowstyle='->', color='#ff6600', lw=1))
ax1.annotate('PM CRASH\n13:39 18.43wan砸盘\n59.22→58.92→58.77', xy=(161, 58.77), xytext=(130, 57.0),
             fontsize=10, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=2),
             bbox=dict(boxstyle='round', facecolor='#fff0f0'))
ax1.annotate('NOW 58.77\n距57.54仅1.23元(2%)', xy=(161, 58.77), xytext=(140, 60),
             fontsize=9, color='#006600', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#006600', lw=1))

# ============ 2a. AM vs PM 大单 ============
ax2 = fig.add_subplot(gs[1, 0])
labels = ['AM\n09:30-11:30', 'PM\n13:01-13:40']
buys = [9326, 695]
sells = [18479, 2957]
nets = [b-s for b, s in zip(buys, sells)]

x2 = np.arange(2)
width = 0.35
ax2.bar(x2 - width/2, buys, width, color='#00aa00', alpha=0.7, label='Buy')
ax2.bar(x2 + width/2, sells, width, color='#cc0000', alpha=0.7, label='Sell')
for i, n in enumerate(nets):
    color = '#00aa00' if n > 0 else '#cc0000'
    ax2.text(i, max(buys[i], sells[i]) + 500, f'{n:+.0f}', ha='center', fontsize=12, color=color, fontweight='bold')
ax2.set_xticks(x2)
ax2.set_xticklabels(labels, fontsize=11)
ax2.set_ylabel('Amount (wan)', fontsize=11)
ax2.set_title('AM buy -> PM SELL flip\nAM was net +9157wan, PM already -2262wan in 40min',
              fontsize=11, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.15, axis='y')

# ============ 2b. AM vs PM 量价 ============
ax3 = fig.add_subplot(gs[1, 1])
am_vol = sum(real_vols[:pm_start])
pm_vol = sum(real_vols[pm_start:])
am_pct = am_vol / total_vol * 100
pm_pct = pm_vol / total_vol * 100

ax3_p = ax3.twinx()
categories = ['AM\n09:30-11:30', 'PM\n13:01-13:40']
vol_pcts = [am_pct, pm_pct]
price_ranges = [max(prices[:pm_start]) - min(prices[:pm_start]),
                max(prices[pm_start:]) - min(prices[pm_start:])]

bars3 = ax3.bar(np.arange(2), vol_pcts, color=['#0066cc', '#cc0000'], alpha=0.6, width=0.5)
ax3_p.plot(np.arange(2), price_ranges, 'o-', color='#ff6600', linewidth=2, markersize=10, label='Price Range')
ax3.set_xticks(np.arange(2))
ax3.set_xticklabels(categories, fontsize=11)
ax3.set_ylabel('Vol % of day', fontsize=11)
ax3_p.set_ylabel('Price Range (yuan)', fontsize=11, color='#ff6600')

for i, (vp, pr) in enumerate(zip(vol_pcts, price_ranges)):
    ax3.text(i, vp + 1, f'{vp:.1f}%', ha='center', fontsize=11, fontweight='bold')
    ax3_p.text(i, pr + 0.1, f'{pr:.2f}', ha='center', fontsize=10, color='#ff6600', fontweight='bold')

ax3.set_title('AM 85% vol vs PM 15% vol but wider range\nPM 40min: range 1.43 (vs AM 1.95)',
              fontsize=11, fontweight='bold')
ax3.grid(True, alpha=0.15, axis='y')

plt.savefig('/data/hermes/workspace/301358_0720_pm_crash.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_0720_pm_crash.png')
