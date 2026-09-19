#!/usr/bin/env python3
"""301358 30min K线 + MACD + 量能 分析图"""
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

with open('/tmp/301358_30m_latest.json') as f:
    data = json.load(f)

bars = data['data']['sz301358']['m30']

parsed = []
for b in bars:
    t = b[0]
    day = t[:8]
    o = float(b[1]); c = float(b[2]); h = float(b[3]); l = float(b[4]); v = float(b[5])
    a = 0.0
    if len(b) > 7 and isinstance(b[7], (int, float)):
        a = float(b[7])
    parsed.append({'t': t, 'day': day, 'o': o, 'c': c, 'h': h, 'l': l, 'v': v, 'a': a})

from collections import defaultdict
daily = defaultdict(list)
for p in parsed:
    daily[p['day']].append(p)
sorted_days = sorted(daily.keys())

# 最近5天
recent = [p for d in sorted_days[-5:] for p in daily[d]]
n = len(recent)
x = list(range(n))

prices_o = [p['o'] for p in recent]
prices_c = [p['c'] for p in recent]
prices_h = [p['h'] for p in recent]
prices_l = [p['l'] for p in recent]
vols = [p['v']/10000 for p in recent]
amts = [p['a'] for p in recent]
t_times = [p['t'][10:14] for p in recent]
t_days = [p['day'] for p in recent]

# MACD
def ema(data, period):
    result = [data[0]]
    alpha = 2.0 / (period + 1)
    for i in range(1, len(data)):
        result.append(data[i] * alpha + result[-1] * (1 - alpha))
    return result

ema12 = ema(prices_c, 12)
ema26 = ema(prices_c, 26)
dif = [a - b for a, b in zip(ema12, ema26)]
dea = ema(dif, 9)
macd = [2 * (d - e) for d, e in zip(dif, dea)]

# MA
ma2 = np.convolve(prices_c, np.ones(2)/2, mode='same')
ma5 = np.convolve(prices_c, np.ones(5)/5, mode='same')
ma10 = np.convolve(prices_c, np.ones(10)/10, mode='same')
ma20 = np.convolve(prices_c, np.ones(20)/20, mode='same')

fig = plt.figure(figsize=(24, 20))
gs = GridSpec(3, 1, height_ratios=[4, 1.5, 2.2], hspace=0.18,
              left=0.06, right=0.97, top=0.97, bottom=0.02)

# === 1. K线图 ===
ax1 = fig.add_subplot(gs[0])

day_starts = {}
for i, p in enumerate(recent):
    if p['day'] not in day_starts:
        day_starts[p['day']] = i

for i in range(n):
    o, c, h, l = prices_o[i], prices_c[i], prices_h[i], prices_l[i]
    color = '#cc0000' if c >= o else '#00aa00'
    ax1.plot([i, i], [l, h], '-', color=color, linewidth=1)
    bw = 0.35
    bottom = min(o, c)
    height = max(abs(c - o), 0.01)
    ax1.bar(i - bw/2, height, width=bw*0.7, bottom=bottom, color=color, alpha=0.9)

ax1.plot(x, ma5, '-', color='#0099ff', linewidth=1.5, label='MA5(2.5h)', alpha=0.8)
ax1.plot(x, ma10, '-', color='#9933cc', linewidth=1.5, label='MA10(5h)', alpha=0.8)
# ma20 后面补nan
ma20_plot = [np.nan]*9 + list(ma20[9:])
ax1.plot(x[:len(ma20_plot)], [p if p == p and p is not None else np.nan for p in ma20_plot],
         '-', color='#ff9900', linewidth=1.5, label='MA20(10h)', alpha=0.8)

# 日分隔线
for d, idx in sorted(day_starts.items()):
    ax1.axvline(x=idx, color='#999999', linewidth=0.5, linestyle='--', alpha=0.3)
    date_label = d[4:6] + '/' + d[6:8]
    if idx > 0:
        y_top = max(prices_h) * 1.015
        ax1.text(idx, y_top, date_label, ha='center', va='bottom', fontsize=10,
                 fontweight='bold', color='#666666')

# 关键价位
ax1.axhline(y=60.00, color='#990099', linewidth=1.5, linestyle='--', alpha=0.5)
ax1.text(n-1, 60.00, '  60.00整数关', va='center', fontsize=9, color='#990099')
ax1.axhline(y=58.08, color='#cc6600', linewidth=1.2, linestyle=':', alpha=0.5)
ax1.text(n-1, 58.08, '  58.08铁底', va='center', fontsize=9, color='#cc6600')
ax1.axhline(y=62.26, color='#0066cc', linewidth=1.2, linestyle=':', alpha=0.4)
ax1.text(n-1, 62.26, '  62.26=7/21收盘', va='center', fontsize=9, color='#0066cc')

# 标注7/22日内高低
last_day_idx = day_starts.get(sorted_days[-1], 0)
last_day_bars = [i for i in range(n) if recent[i]['day'] == sorted_days[-1]]
if last_day_bars:
    hi_idx = max(last_day_bars, key=lambda i: prices_h[i])
    lo_idx = min(last_day_bars, key=lambda i: prices_l[i])
    ax1.annotate('7/22高 62.26', xy=(hi_idx, prices_h[hi_idx]),
                 xytext=(hi_idx-3, prices_h[hi_idx]+0.4),
                 fontsize=10, color='#cc0000', fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
    ax1.annotate('7/22低 60.12', xy=(lo_idx, prices_l[lo_idx]),
                 xytext=(lo_idx-1, prices_l[lo_idx]-0.5),
                 fontsize=10, color='#00aa00', fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color='#00aa00', lw=1.5))

ax1.set_ylabel('Price (元)', fontsize=12)
ax1.set_title('301358 30分钟K线 — 7/15至7/22\n7/21拉高(收62.26) → 7/22低开阴跌(收60.58) MACD 死叉', 
              fontsize=14, fontweight='bold')
ax1.legend(loc='upper right', fontsize=10)
ax1.set_xticks([])
ax1.grid(True, alpha=0.15)
all_h = [h for h in prices_h]
all_l = [l for l in prices_l]
ax1.set_ylim([min(all_l)*0.99, max(all_h)*1.02])

# === 2. 成交量 ===
ax2 = fig.add_subplot(gs[1])
colors_vol = ['#cc0000' if c >= o else '#00aa00' for o, c in zip(prices_o, prices_c)]
ax2.bar(x, vols, color=colors_vol, alpha=0.7, width=0.6)

# VOL MA5
vol_ma5 = np.convolve(vols, np.ones(5)/5, mode='same')
ax2.plot(x, vol_ma5, '-', color='#ff9900', linewidth=1.5, label='VOL_MA5')

# 标注7/22缩量
if last_day_bars:
    avg_recent_vol = np.mean(vols[-16:-8]) if len(vols) >= 16 else np.mean(vols)
    ax2.annotate('7/22缩量17w\n(5日最低)', xy=(last_day_bars[-1], vols[last_day_bars[-1]]),
                 xytext=(last_day_bars[-1]-3, max(vols)*0.9),
                 fontsize=10, color='#0066cc', fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color='#0066cc', lw=1.5))

for d, idx in sorted(day_starts.items()):
    ax2.axvline(x=idx, color='#999999', linewidth=0.5, linestyle='--', alpha=0.3)

ax2.set_ylabel('Volume (万手)', fontsize=11)
ax2.set_title('30min成交量: 7/22缩至17万手=近5日最低(7/21为22万手)', fontsize=12, fontweight='bold')
ax2.legend(fontsize=10, loc='upper right')
ax2.grid(True, alpha=0.15, axis='y')

# === 3. MACD ===
ax3 = fig.add_subplot(gs[2])
# MACD柱
colors_macd = ['#cc0000' if m > 0 else '#00aa00' for m in macd]
ax3.bar(x, macd, color=colors_macd, alpha=0.5, width=0.5)
ax3.plot(x, dif, '-', color='#ff6600', linewidth=1.5, label='DIF')
ax3.plot(x, dea, '-', color='#0066ff', linewidth=1.5, label='DEA')

# 标注死叉
for i in range(1, len(macd)):
    if macd[i-1] >= 0 and macd[i] < 0:
        ax3.annotate('死叉', xy=(i, 0), fontsize=11, color='#00aa00', fontweight='bold',
                     arrowprops=dict(arrowstyle='->', color='#00aa00', lw=1.5),
                     xytext=(i+1, -0.3))
    elif macd[i-1] <= 0 and macd[i] > 0:
        ax3.annotate('金叉', xy=(i, 0), fontsize=11, color='#cc0000', fontweight='bold',
                     arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5),
                     xytext=(i+1, 0.3))

# 标注MACD从红到绿的转折
if macd[-1] < 0:
    last_red_idx = None
    for i in range(len(macd)-1, -1, -1):
        if macd[i] > 0:
            last_red_idx = i
            break
    if last_red_idx is not None:
        ax3.axvline(x=last_red_idx + 0.5, color='#990099', linewidth=1.5, linestyle='--')
        ax3.text(last_red_idx + 1, min(macd)*0.8, 'MACD\n翻绿', fontsize=10,
                 color='#990099', fontweight='bold', ha='center')

for d, idx in sorted(day_starts.items()):
    ax3.axvline(x=idx, color='#999999', linewidth=0.5, linestyle='--', alpha=0.3)

ax3.axhline(y=0, color='black', linewidth=0.5)
ax3.set_ylabel('MACD', fontsize=11)
ax3.set_xlabel('30min bars (7/15 - 7/22)', fontsize=11)
ax3.set_title('30min MACD: DIF=-0.096 DEA=-0.019 死叉后绿柱连续4根扩大中', 
              fontsize=12, fontweight='bold')
ax3.legend(fontsize=10, loc='upper right')
ax3.grid(True, alpha=0.15)

# x轴标签：用日期+时间
tick_labels = []
tick_positions = []
for i, p in enumerate(recent):
    hm = p['t'][10:14]
    if hm == '0930' or hm == '1330':
        date_label = p['day'][4:6] + '/' + p['day'][6:8]
        tick_labels.append(date_label)
        tick_positions.append(i)
    elif hm == '1100':
        tick_labels.append('11:00')
        tick_positions.append(i)
    elif hm == '1500':
        tick_labels.append('15:00')
        tick_positions.append(i)
ax3.set_xticks(tick_positions)
ax3.set_xticklabels(tick_labels, fontsize=9, rotation=30)

plt.savefig('/data/hermes/workspace/301358_30m_chart_v2.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_30m_chart_v2.png')
