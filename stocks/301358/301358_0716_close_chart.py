#!/usr/bin/env python3
"""301358 7/16 全天分时分析图"""
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

with open('/tmp/301358_tl_0716_close.json') as f:
    data = json.load(f)
bars = data['data']

prices = [float(b['price']) for b in bars]
times = [b['time'] for b in bars]
pre_close = 63.37

real_vols = []
amts = []
for i in range(len(bars)):
    if i == 0:
        real_vols.append(int(bars[i]['volume']))
        amts.append(bars[i]['amount'])
    else:
        real_vols.append(max(int(bars[i]['volume']) - int(bars[i-1]['volume']), 0))
        amts.append(bars[i]['amount'] - bars[i-1]['amount'])

# 标注午休时段
# 11:30之后到13:00是午休
pm_start_idx = None
for i, t in enumerate(times):
    if t >= '13:01':
        pm_start_idx = i
        break

fig = plt.figure(figsize=(18, 20))
gs = GridSpec(4, 2, figure=fig, height_ratios=[3, 1.5, 1.2, 1.5], hspace=0.25, wspace=0.2,
              left=0.07, right=0.95, top=0.95, bottom=0.04)

# ====== 1. 分时走势 ======
ax1 = fig.add_subplot(gs[0, :])
ax1.plot(range(len(prices)), prices, color='#cc0000', linewidth=1.2)
ax1.axhline(y=pre_close, color='gray', linewidth=1, linestyle='--', alpha=0.5, label='Prev close 63.37')
ax1.axhline(y=63.15, color='#0066cc', linewidth=1, linestyle=':', alpha=0.5, label='63.15 (7/10 close)')
ax1.axhline(y=60.31, color='#00aa00', linewidth=1.5, linestyle=':', alpha=0.6, label='60.31 (today low / support)')

# 标注午休
ax1.axvspan(pm_start_idx-1, pm_start_idx, alpha=0.1, color='gray', label='Lunch break')

# 区域着色
ax1.fill_between(range(len(prices)), pre_close, prices, where=[p < pre_close for p in prices],
                 color='#cc0000', alpha=0.1)

# 关键点标注
key_points = [
    (1, 61.06, '09:31 Crash\n-3.67% in 1min\n1.41M vol', 'left'),
    (np.argmin(prices), min(prices), '60.31 LOW\n09:39', 'bottom'),
    (np.argmax(prices), max(prices), '63.73 HIGH\n11:16\n(+3.97% from low)', 'top'),
    (pm_start_idx, 62.60, '13:01 PM open\n34wan dump\n2nd T+0 sell', 'right'),
    (len(prices)-1, prices[-1], 'Close 61.24\n-3.36%', 'right'),
]

for idx, price, text, pos in key_points:
    if pos == 'left':
        ax1.annotate(text, xy=(idx, price), xytext=(idx+8, price + (1.5 if price < pre_close else -1)),
                     fontsize=8, fontweight='bold', color='#cc0000',
                     arrowprops=dict(arrowstyle='->', color='#cc0000'),
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff0f0', edgecolor='#cc0000'))
    elif pos == 'bottom':
        ax1.annotate(text, xy=(idx, price), xytext=(idx+10, price + 3),
                     fontsize=8, fontweight='bold', color='#00aa00',
                     arrowprops=dict(arrowstyle='->', color='#00aa00'),
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='#e6ffe6', edgecolor='#00aa00'))
    elif pos == 'top':
        ax1.annotate(text, xy=(idx, price), xytext=(idx+10, price - 2),
                     fontsize=8, fontweight='bold', color='#cc0000',
                     arrowprops=dict(arrowstyle='->', color='#cc0000'),
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff0f0', edgecolor='#cc0000'))
    elif pos == 'right':
        ax1.annotate(text, xy=(idx, price), xytext=(idx-20, price + (2 if price < pre_close else -1)),
                     fontsize=8, fontweight='bold', color='#ff6600',
                     arrowprops=dict(arrowstyle='->', color='#ff6600'),
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff5e6', edgecolor='#ff6600'))

# 阶段背景
phases = [
    (0, 2, '#cc0000', 0.05, '1.Crash'),
    (2, 30, '#ff6600', 0.05, '2.Bottom'),
    (30, 60, '#cccccc', 0.05, '3.Sideway'),
    (60, 121, '#00aa00', 0.05, '4.Rally'),
    (122, 152, '#cc0000', 0.05, '5.PM Sell'),
    (152, 182, '#ff6600', 0.05, '6.Drift'),
    (182, len(bars), '#333333', 0.05, '7.Close'),
]

for s, e, color, alpha, label in phases:
    ax1.axvspan(s, e, alpha=alpha, color=color)
    mid = (s + e) / 2
    y_top = max(prices) + 0.5
    ax1.text(mid, y_top, label, fontsize=7, ha='center', color=color, alpha=0.7)

ax1.set_ylabel('Price (RMB)', fontsize=12)
ax1.set_title('301358 7/16 Full Day Ticker — Crash + V-Recovery + PM Sell-off\n(Open 63.00 -> Low 60.31 -> High 63.73 -> Close 61.24, -3.36%)',
              fontsize=14, fontweight='bold')
ax1.legend(fontsize=8, loc='upper right')
ax1.grid(True, alpha=0.1)

# ====== 2. 成交量 ======
ax2 = fig.add_subplot(gs[1, :])
colors_vol = ['#cc0000' if prices[i] < pre_close else '#00aa00' for i in range(len(prices))]
ax2.bar(range(len(real_vols)), [v/10000 for v in real_vols], color=colors_vol, alpha=0.7, width=0.7)
ax2.axvspan(pm_start_idx-1, pm_start_idx, alpha=0.1, color='gray')
ax2.set_ylabel('Volume (10k shares)', fontsize=10)
ax2.set_title('Per-Minute Volume (Red=down, Green=up)', fontsize=11, fontweight='bold')
ax2.grid(True, alpha=0.1, axis='y')

# 标注关键大单
big_bars = [(i, real_vols[i]) for i in range(len(real_vols)) if real_vols[i] > 150000]
for idx, vol in big_bars:
    ax2.annotate('%.0fwan' % (vol/10000), xy=(idx, vol/10000), xytext=(idx, vol/10000+5),
                 fontsize=7, ha='center', color='#cc0000', fontweight='bold')

# ====== 3. 阶段成交分布 ======
ax3 = fig.add_subplot(gs[2, 0])
seg_labels = ['1.Crash\n09:30-09:31', '2.Bottom\n09:32-09:59', '3.Sideway\n10:00-10:29',
              '4.Rally\n10:30-11:30', '5.PM Sell\n13:01-13:30', '6.Drift\n13:31-14:30', '7.Close\n14:31-15:00']
seg_vols = [1522300, 5823700, 1799500, 3965100, 1736500, 1548500, 3631100]
seg_colors = ['#cc0000', '#ff6600', '#cccccc', '#00aa00', '#cc0000', '#ff6600', '#333333']

x = np.arange(len(seg_labels))
ax3.barh(x, [v/10000 for v in seg_vols], color=seg_colors, alpha=0.8, height=0.6)
ax3.set_yticks(x)
ax3.set_yticklabels(seg_labels, fontsize=8)
ax3.set_xlabel('Volume (10k)', fontsize=10)
ax3.set_title('Volume by Phase', fontsize=11, fontweight='bold')
ax3.invert_yaxis()
ax3.grid(True, alpha=0.1, axis='x')

# 百分比标注
total_v = sum(seg_vols)
for i, v in enumerate(seg_vols):
    ax3.text(v/10000 + 5, i, '%.1f%%' % (v/total_v*100), va='center', fontsize=9, fontweight='bold')

# ====== 4. 大盘对比 ======
ax4 = fig.add_subplot(gs[2, 1])
ax4.axis('off')

compare = [
    ('301358', '-3.36%', '0.96', '#cc0000'),
    ('SH Index', '-1.85%', '0.91', '#ff6600'),
    ('SZ Index', '-1.97%', '0.91', '#ff6600'),
    ('ChiNext', '-2.95%', '0.93', '#cc0000'),
    ('CATL', '-1.82%', '0.57', '#ff6600'),
    ('GEM', '-1.10%', '0.71', '#ff6600'),
    ('Tianhua', '-1.67%', '0.66', '#ff6600'),
    ('Putailai', '-3.69%', '0.69', '#cc0000'),
]

y = 0.83
ax4.text(0.5, 0.95, '7/16 Close Market Comparison', fontsize=13, ha='center', fontweight='bold',
         transform=ax4.transAxes)
ax4.text(0.05, y, 'Stock', fontsize=10, fontweight='bold', transform=ax4.transAxes)
ax4.text(0.30, y, 'Change%', fontsize=10, fontweight='bold', transform=ax4.transAxes)
ax4.text(0.50, y, 'VolRatio', fontsize=10, fontweight='bold', transform=ax4.transAxes)
ax4.text(0.70, y, 'vs 301358', fontsize=10, fontweight='bold', transform=ax4.transAxes)
y -= 0.07
for name, chg, vr, color in compare:
    diff = float(chg.replace('%','')) - (-3.36)
    vs_text = 'outperform %+.2f%%' % diff if diff > 0 else 'underperform %+.2f%%' % diff
    ax4.text(0.05, y, name, fontsize=10, transform=ax4.transAxes)
    ax4.text(0.30, y, chg, fontsize=10, color=color, fontweight='bold', transform=ax4.transAxes)
    ax4.text(0.50, y, vr, fontsize=10, transform=ax4.transAxes)
    ax4.text(0.70, y, vs_text, fontsize=8, color=('#00aa00' if diff > 0 else '#cc0000'), transform=ax4.transAxes)
    y -= 0.08

# ====== 5. K线形态分析 ======
ax5 = fig.add_subplot(gs[3, :])
ax5.axis('off')

kline_data = """
7/16 K-line: Long Upper Shadow + Small Body = Bearish Shooting Star

  High  63.80  ───┐
                  │  ← Long upper shadow (63.80 - 63.00 = 0.80)
  Open  63.00  ───┤
  Close 61.24  ───┤  ← Body (63.00 - 61.24 = -1.76, RED)
  Low   60.31  ───┤  ← Long lower shadow (61.24 - 60.31 = 0.93)
                  │
                  Total range: 63.80 - 60.31 = 3.49 (amplitude 5.51%)
"""

ax5.text(0.05, 0.85, '7/16 K-line Pattern Analysis', fontsize=13, fontweight='bold', transform=ax5.transAxes)

# K线形态描述
ax5.text(0.05, 0.70,
         'Open 63.00  |  High 63.80  |  Low 60.31  |  Close 61.24\n'
         'Body: 63.00 -> 61.24 (RED, -1.76)\n'
         'Upper shadow: 63.80 - 63.00 = 0.80\n'
         'Lower shadow: 61.24 - 60.31 = 0.93\n'
         'Amplitude: 5.51%  |  Volume ratio: 0.96 (below average)',
         fontsize=11, family='monospace', transform=ax5.transAxes,
         bbox=dict(boxstyle='round', facecolor='#f5f5f5', edgecolor='#ccc'))

# Mistery conclusion
ax5.text(0.05, 0.30,
         'Mistery View: Today is a classic "Shooting Star with Long Lower Shadow"\n\n'
         '1. Upper shadow 0.80 = Main force sold at 63+ (2nd T+0)\n'
         '2. Lower shadow 0.93 = Bottom support at 60.31 (held 5hrs)\n'
         '3. Volume ratio 0.96 = BELOW average (no panic selling)\n'
         '4. Close 61.24 = Below 7/14 close 61.98, below 7/10 close 63.15\n\n'
         'Verdict: BEARISH short-term (63.73 is the ceiling),\n'
         '         BULLISH mid-term (60.31 support held, main force T+0 completed).\n'
         '         Key: Can 60.31 hold tomorrow?',
         fontsize=11, transform=ax5.transAxes, color='#333',
         bbox=dict(boxstyle='round', facecolor='#fff5e6', edgecolor='#ff6600'))

plt.savefig('/data/hermes/workspace/301358_0716_close_analysis.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_0716_close_analysis.png')
