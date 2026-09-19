#!/usr/bin/env python3
"""301358 7/16 早盘分时分析图"""
import json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
fm.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'WenQuanYi Zen Hei'
plt.rcParams['axes.unicode_minus'] = False

with open('/tmp/301358_tl_0716.json') as f:
    data = json.load(f)
bars = data['data']

times = [b['time'] for b in bars]
prices = [float(b['price']) for b in bars]

real_vols = []
amts = []
for i in range(len(bars)):
    if i == 0:
        real_vols.append(int(bars[i]['volume']))
        amts.append(bars[i]['amount'])
    else:
        diff_v = int(bars[i]['volume']) - int(bars[i-1]['volume'])
        real_vols.append(max(diff_v, 0))
        amts.append(bars[i]['amount'] - bars[i-1]['amount'])

pre_close = 63.37

fig, axes = plt.subplots(3, 1, figsize=(14, 14), height_ratios=[3, 1, 1])
fig.suptitle('301358 7/16 Early Session Analysis (09:30-09:52) — Gap Down + Volume Spike',
             fontsize=15, fontweight='bold')

# ----- Subplot 1: Price + Volume -----
ax1 = axes[0]
ax1.plot(range(len(prices)), prices, color='#cc0000', linewidth=2, marker='o', markersize=3)
ax1.axhline(y=pre_close, color='gray', linewidth=1, linestyle='--', label='Prev close 63.37')
ax1.axhline(y=63.15, color='#0066cc', linewidth=1, linestyle=':', label='63.15 support (7/10 close)')
ax1.axhline(y=61.98, color='#00aa00', linewidth=1, linestyle=':', label='61.98 (7/14 close)')

# 标注关键点
ax1.annotate('09:30 Open 63.00\n09:31 Crash to 61.06\n(-3.67% in 1 min, 1.41M vol)',
             xy=(1, 61.06), xytext=(5, 62.5),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000'),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff0f0', edgecolor='#cc0000'))

ax1.annotate('09:35-09:41\nLow 60.31-60.94\nBottom testing',
             xy=(8, 60.77), xytext=(12, 61.8),
             fontsize=9, color='#ff6600', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#ff6600'),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff5e6', edgecolor='#ff6600'))

ax1.annotate('09:44 Bounce\n61.76 (+1.8% from low)',
             xy=(14, 61.76), xytext=(16, 62.5),
             fontsize=9, color='#00aa00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00aa00'),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#e6ffe6', edgecolor='#00aa00'))

ax1.set_ylabel('Price (RMB)', fontsize=12)
ax1.set_title('Intraday Price (09:30-09:52, pre_close=63.37)', fontsize=12, fontweight='bold')
ax1.set_xticks(range(0, len(times), 3))
ax1.set_xticklabels([times[i] for i in range(0, len(times), 3)], fontsize=8, rotation=30)
ax1.legend(fontsize=8, loc='upper right')
ax1.grid(True, alpha=0.15)

# ----- Subplot 2: Volume -----
ax2 = axes[1]
colors_vol = ['#cc0000' if prices[i] < pre_close else '#00aa00' for i in range(len(prices))]
ax2.bar(range(len(real_vols)), [v/10000 for v in real_vols], color=colors_vol, alpha=0.8, width=0.7)
ax2.set_ylabel('Volume (10k shares)', fontsize=11)
ax2.set_title('Per-Minute Volume (Red=down, Green=up)', fontsize=11, fontweight='bold')
ax2.set_xticks(range(0, len(times), 3))
ax2.set_xticklabels([times[i] for i in range(0, len(times), 3)], fontsize=8, rotation=30)
ax2.grid(True, alpha=0.15, axis='y')

# 标注09:31巨量
ax2.annotate('09:31: 141wan\n(max volume)', xy=(1, 141), xytext=(4, 120),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000'))

# ----- Subplot 3: Comparison with market -----
ax3 = axes[2]
ax3.axis('off')

data_text = [
    ('301358', '-3.08%', '3.58', '63.00->60.31->61.42', '#cc0000'),
    ('SH Index', '-0.88%', '2.76', '3956->3920', '#ff6600'),
    ('SZ Index', '-1.17%', '2.79', '14780->14607', '#ff6600'),
    ('ChiNext', '-1.62%', '2.77', '3805->3743', '#cc0000'),
    ('CATL', '-0.90%', '1.60', '373->369', '#ff6600'),
    ('GEM', '-1.10%', '2.23', '6.38->6.31', '#ff6600'),
]

ax3.text(0.5, 0.95, '7/16 09:52 Market Comparison', fontsize=13, ha='center', fontweight='bold',
         transform=ax3.transAxes)

y_pos = 0.82
for name, chg, vr, detail, color in data_text:
    ax3.text(0.05, y_pos, name, fontsize=11, fontweight='bold', transform=ax3.transAxes)
    ax3.text(0.25, y_pos, chg, fontsize=11, color=color, fontweight='bold', transform=ax3.transAxes)
    ax3.text(0.40, y_pos, 'VR=' + vr, fontsize=10, transform=ax3.transAxes)
    ax3.text(0.55, y_pos, detail, fontsize=10, transform=ax3.transAxes, color=color)
    y_pos -= 0.1

# 结论
ax3.text(0.05, 0.15, 'Key: 301358 -3.08% vs ChiNext -1.62%', fontsize=11, fontweight='bold',
         color='#cc0000', transform=ax3.transAxes)
ax3.text(0.05, 0.08, 'Underperform ChiNext by -1.46%, VolumeRatio 3.58 = massive sell-off', fontsize=10,
         color='#cc0000', transform=ax3.transAxes)
ax3.text(0.05, 0.02, 'Support: 60.31 (today low) | 55.72 (Jul 14 low) | Key: can 63.15 hold?', fontsize=10,
         color='#333', transform=ax3.transAxes)

plt.tight_layout()
plt.savefig('/data/hermes/workspace/301358_0716_morning.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_0716_morning.png')
