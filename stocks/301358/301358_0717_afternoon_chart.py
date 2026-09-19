#!/usr/bin/env python3
"""301358 7/17 截至14:40 收盘前完整分析图"""
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

with open('/tmp/301358_tl_latest2.json') as f:
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

with open('/tmp/301358_klines_60d_v2.json') as f:
    k_data = json.load(f)
klines = k_data['data']['sz301358']['qfqday']

fig = plt.figure(figsize=(22, 26))
gs = GridSpec(3, 2, figure=fig, height_ratios=[2.5, 1.5, 2.8], hspace=0.3, wspace=0.2,
              left=0.06, right=0.96, top=0.96, bottom=0.02)

# ============ 1. 全天分时走势 ============
ax1 = fig.add_subplot(gs[0, :])
x = np.arange(len(bars))
colors_vol = ['#cc0000' if i > 0 and prices[i] >= prices[i-1] else '#00aa00' for i in range(len(bars))]
ax1_v = ax1.twinx()
ax1_v.bar(x, [v/10000 for v in real_vols], color=colors_vol, alpha=0.25, width=0.8)

ax1.plot(x, prices, color='#cc0000', linewidth=1.5, zorder=5)
ax1.axhline(y=vwap, color='blue', linewidth=1.5, linestyle='--', alpha=0.6, label=f'VWAP {vwap:.2f}')
ax1.axhline(y=60, color='#00aa00', linewidth=2, linestyle=':', alpha=0.4, label='60 line')
ax1.axhline(y=60.31, color='#006600', linewidth=1.5, linestyle='--', alpha=0.3, label='7/16 low 60.31')
ax1.axhline(y=57.54, color='#000099', linewidth=1.5, linestyle='--', alpha=0.3, label='7/10 block 57.54')
ax1.axhline(y=61.24, color='#888888', linewidth=1, linestyle=':', alpha=0.3, label='7/16 close 61.24')

# 5段着色
seg_colors_bg = ['#fff8e8', '#fff8e8', '#ffeeee', '#e8fff8', '#fff0f0', '#ffeeee', '#e8fff8']
seg_ranges_idx = [(0,4), (4,15), (15,31), (31,81), (81,111), (111,141), (141,len(bars))]
for (s,e), c in zip(seg_ranges_idx, seg_colors_bg):
    ax1.axvspan(s-0.5, e-0.5, color=c, alpha=0.25, zorder=0)

# 大单标记
for i in range(len(bars)):
    if real_vols[i] >= 200000:
        color = '#00aa00' if i > 0 and prices[i] >= prices[i-1] else '#cc0000'
        ax1.scatter(i, prices[i], s=50, color=color, zorder=10, edgecolors='black', linewidth=0.5)

tick_idx = [i for i, t in enumerate(times) if t.endswith(':00') or t.endswith(':30')]
ax1.set_xticks([i for i in tick_idx])
ax1.set_xticklabels([times[i] for i in tick_idx], fontsize=9, rotation=30)
ax1.set_ylabel('Price', fontsize=12)
ax1.set_title('301358 Hunan Yuneng 7/17 Full Day (as of 14:40) — NOW: 60.23 (-1.65%)\n'
              '58.85 low (10:54) → 60.69 bounce (11:23) → 59.21 re-test PM (13:49) → 60+ stabilize (14:00+)',
              fontsize=13, fontweight='bold')
ax1.legend(fontsize=9, loc='upper right')
ax1.grid(True, alpha=0.12)

# 关键标注
ax1.annotate('Open 61.08\n诱多', xy=(0, 61.08), xytext=(3, 62.0),
             fontsize=8, color='#cc0000', arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1))
ax1.annotate('BREAK 60\n10:00\n28.6wan', xy=(30, 59.97), xytext=(25, 61.3),
             fontsize=8, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
ax1.annotate('LOW 58.85\n10:54', xy=(78, 58.85), xytext=(65, 57.8),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
ax1.annotate('V-REVERSE\n11:06-08\n80.6wan BUY', xy=(84, 61.7), xytext=(90, 62.5),
             fontsize=9, color='#00aa00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00aa00', lw=2),
             bbox=dict(boxstyle='round', facecolor='#f0fff0'))
ax1.annotate('PM re-test\n59.21 @13:49', xy=(128, 59.21), xytext=(115, 58.2),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
ax1.annotate('STABILIZE\n14:00+\n60+ plat', xy=(150, 60.30), xytext=(165, 59.3),
             fontsize=9, color='#006600', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#006600', lw=1.5),
             bbox=dict(boxstyle='round', facecolor='#f0fff0'))

# ============ 2a. 5段大单对比 ============
ax2 = fig.add_subplot(gs[1, 0])
seg_labels = ['AM\nCrash\n09:30-10:50', 'AM\nBounce\n10:51-11:30',
              'PM\nCrash\n13:01-13:30', 'PM\nTest\n13:31-14:00',
              'PM\nStable\n14:01-14:40']
# PM开始位置
pm_start = None
for i, t in enumerate(times):
    if t >= '13:01':
        pm_start = i
        break

seg_defs = [(0,81), (81,pm_start), (pm_start,pm_start+30), (pm_start+30,pm_start+60), (pm_start+60,len(bars))]
seg_buys = []
seg_sells = []
for s, e in seg_defs:
    e = min(e, len(bars))
    buy = sell = 0
    for i in range(s, e):
        if real_vols[i] >= 100000:
            if i > 0 and prices[i] < prices[i-1]:
                sell += real_vols[i]*prices[i]/10000
            else:
                buy += real_vols[i]*prices[i]/10000
    seg_buys.append(buy)
    seg_sells.append(sell)

x2 = np.arange(5)
width = 0.35
ax2.bar(x2 - width/2, seg_buys, width, color='#00aa00', alpha=0.7, label='Buy')
ax2.bar(x2 + width/2, seg_sells, width, color='#cc0000', alpha=0.7, label='Sell')
seg_nets = [b-s for b,s in zip(seg_buys, seg_sells)]
for i, n in enumerate(seg_nets):
    color = '#cc0000' if n < 0 else '#00aa00'
    ax2.text(i, max(seg_buys[i], seg_sells[i]) + 300, f'{n:+.0f}', ha='center', fontsize=9, color=color, fontweight='bold')
ax2.set_xticks(x2)
ax2.set_xticklabels(seg_labels, fontsize=9)
ax2.set_ylabel('Amount (wan)', fontsize=11)
ax2.set_title('Big Order Net by Stage\nAM Crash: -3425wan | AM Bounce: +820wan | PM Crash: -2216wan | PM Test: -1136wan | PM Stable: -104wan',
              fontsize=11, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.15, axis='y')

# ============ 2b. 7/17 vs 7/16 价格分布 ============
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
ax3.set_xticklabels(['%d' % p for p in all_p], fontsize=11)
ax3.set_xlabel('Price', fontsize=11)
ax3.set_ylabel('Volume %', fontsize=11)
ax3.set_title('7/16 vs 7/17 Price Distribution\n7/17: 60 zone=43.9% (new floor) | 59 zone=24.4% (panic)',
              fontsize=11, fontweight='bold')
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.15, axis='y')

for i, (r16, r17) in enumerate(zip(r_16, r_17)):
    if r16 > 0: ax3.text(i - width/2, r16 + 1, '%.0f%%' % r16, ha='center', fontsize=8, color='#ff6600')
    ax3.text(i + width/2, r17 + 1, '%.0f%%' % r17, ha='center', fontsize=8, color='#cc0000')

# ============ 3. 近6日K线对比 ============
ax4 = fig.add_subplot(gs[2, :])
recent_ks = klines[-6:]
k_labels = [k[0][-5:] for k in recent_ks]  # MM-DD
opens = [float(k[1]) for k in recent_ks]
closes = [float(k[2]) for k in recent_ks]
highs = [float(k[3]) for k in recent_ks]
lows = [float(k[4]) for k in recent_ks]
vols = [float(k[5]) for k in recent_ks]

# K线
x4 = np.arange(len(recent_ks))
for i in range(len(recent_ks)):
    up = closes[i] >= opens[i]
    color = '#cc0000' if up else '#00aa00'
    # 影线
    ax4.plot([i, i], [lows[i], highs[i]], color=color, linewidth=1, zorder=1)
    # 实体
    body_bottom = min(opens[i], closes[i])
    body_height = abs(closes[i] - opens[i])
    rect = plt.Rectangle((i-0.3, body_bottom), 0.6, max(body_height, 0.15),
                         facecolor=color, edgecolor=color, zorder=2)
    ax4.add_patch(rect)
    # 标注收盘价
    ax4.text(i, lows[i]-0.3, f'{closes[i]:.2f}', ha='center', fontsize=9, color=color, fontweight='bold')
    # 涨跌幅
    chg = (closes[i] - opens[i]) / opens[i] * 100
    ax4.text(i, highs[i]+0.3, f'{chg:+.1f}%', ha='center', fontsize=9, color=color)

# 成交量副图
ax4_v = ax4.twinx()
ax4_v.bar(x4, [v/10000 for v in vols], color=['#cc0000' if c>=o else '#00aa00' for c,o in zip(closes, opens)],
          alpha=0.3, width=0.5)
ax4_v.set_ylabel('Volume (wan lots)', fontsize=11, color='#666666')
ax4_v.set_ylim(0, max(vols)/10000*2)

ax4.set_xticks(x4)
ax4.set_xticklabels(k_labels, fontsize=11)
ax4.set_ylabel('Price', fontsize=12)
ax4.set_title('Recent 6 Days K-Line Comparison\n7/16: -2.8% (big body -1.76) | 7/17: -3.4% so far, BUT long lower shadow 0.08 only',
              fontsize=12, fontweight='bold')
ax4.set_ylim(55, 68)
ax4.axhline(y=57.54, color='#000099', linewidth=1.5, linestyle='--', alpha=0.3, label='7/10 block 57.54')
ax4.axhline(y=60, color='#00aa00', linewidth=1, linestyle=':', alpha=0.3)
ax4.legend(fontsize=10)
ax4.grid(True, alpha=0.15, axis='y')

# 标注7/10大宗
ax4.annotate('7/10 block\n57.54', xy=(0, 57.54), xytext=(0.5, 56.5),
             fontsize=9, color='#000099', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#000099', lw=1.5))

plt.savefig('/data/hermes/workspace/301358_0717_afternoon_analysis.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_0717_afternoon_analysis.png')
