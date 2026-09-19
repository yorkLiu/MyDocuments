#!/usr/bin/env python3
"""301358 7/21 实时分析图"""
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

with open('/tmp/301358_t_now.json') as f:
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

# 大单净额
big_buy = big_sell = 0
for i in range(len(bars)):
    if real_vols[i] >= 100000:
        chg = prices[i] - (prices[i-1] if i > 0 else prices[i])
        direction = '买' if chg >= 0 else '卖'
        amt = real_vols[i] * prices[i] / 10000
        if direction == '买': big_buy += amt
        else: big_sell += amt

# 20天K线
klines_data = [
    ("06-24", 83.00, 84.85, 85.48, 79.12),
    ("06-25", 83.53, 82.30, 84.70, 81.10),
    ("06-26", 82.00, 75.80, 83.58, 75.68),
    ("06-29", 74.54, 74.99, 76.08, 71.80),
    ("06-30", 74.66, 75.87, 76.80, 73.10),
    ("07-01", 75.11, 76.80, 78.87, 72.00),
    ("07-02", 76.00, 75.41, 78.98, 75.12),
    ("07-03", 76.18, 73.39, 76.80, 73.31),
    ("07-06", 73.00, 73.38, 76.30, 71.74),
    ("07-07", 74.47, 72.00, 74.88, 71.49),
    ("07-08", 71.64, 67.55, 72.29, 67.50),
    ("07-09", 67.49, 65.80, 67.79, 63.00),
    ("07-10", 65.60, 63.15, 66.59, 63.15),
    ("07-13", 62.79, 61.54, 63.76, 60.88),
    ("07-14", 61.50, 61.98, 61.98, 59.72),
    ("07-15", 62.20, 63.37, 65.05, 60.50),
    ("07-16", 63.00, 61.24, 63.80, 60.31),
    ("07-17", 61.08, 59.47, 62.44, 58.80),
    ("07-20", 60.01, 59.90, 61.20, 58.08),
    ("07-21", 59.90, 60.76, 62.25, 59.37),
]
k_dates = [k[0] for k in klines_data]
k_opens = [k[1] for k in klines_data]
k_closes = [k[2] for k in klines_data]
k_highs = [k[3] for k in klines_data]
k_lows = [k[4] for k in klines_data]

fig = plt.figure(figsize=(20, 16))
gs = GridSpec(4, 2, figure=fig, height_ratios=[3, 1, 1.2, 1.2], hspace=0.3, wspace=0.15,
              left=0.06, right=0.96, top=0.96, bottom=0.04)

# --- 1. 分时图 ---
ax1 = fig.add_subplot(gs[0, 0])
x = np.arange(len(bars))
ax1.plot(x, prices, color='#cc0000', linewidth=1.5, zorder=5)
ax1.axhline(y=vwap, color='blue', linewidth=1.5, linestyle='--', alpha=0.6, label=f'VWAP {vwap:.2f}')
ax1.axhline(y=59.90, color='#888888', linewidth=1, linestyle=':', alpha=0.4, label='7/20收盘59.90')
ax1.axhline(y=61.19, color='#ff6600', linewidth=1, linestyle='--', alpha=0.4, label='MA5=60.95')
ax1.axhline(y=62.48, color='#990099', linewidth=1, linestyle='--', alpha=0.4, label='MA10=62.48')

# 大单标记
for i in range(len(bars)):
    if real_vols[i] >= 100000:
        chg = prices[i] - (prices[i-1] if i > 0 else prices[i])
        color = '#00aa00' if chg >= 0 else '#cc0000'
        ax1.scatter(i, prices[i], s=60, color=color, zorder=10, edgecolors='black', linewidth=0.5)

# 阶段标注
ax1.axvspan(0, 12, color='#fff8e8', alpha=0.3)
ax1.text(6, 62.3, '①拉升\n09:31-09:47', ha='center', fontsize=9, alpha=0.7)
ax1.axvspan(12, len(bars), color='#f0f0f0', alpha=0.3)
ax1.text(len(bars)//2+12, 62.3, '②回落\n09:48-09:57', ha='center', fontsize=9, alpha=0.7)

ax1.set_xticks(range(0, len(bars), 5))
ax1.set_xticklabels([times[i] for i in range(0, len(bars), 5)], fontsize=8, rotation=30)
ax1.set_ylabel('Price', fontsize=11)
ax1.set_title('7/21 分时图 — 冲高62.08后回落至60.75', fontsize=12, fontweight='bold')
ax1.legend(fontsize=8, loc='upper left')
ax1.grid(True, alpha=0.1)

# --- 2. 成交量 ---
ax2 = fig.add_subplot(gs[0, 1])
colors_vol = ['#cc0000' if i > 0 and prices[i] >= prices[i-1] else '#00aa00' for i in range(len(bars))]
ax2.bar(x, [v/10000 for v in real_vols], color=colors_vol, alpha=0.7, width=0.8)
ax2.axhline(y=0, color='black', linewidth=0.5)
ax2.set_xticks(range(0, len(bars), 5))
ax2.set_xticklabels([times[i] for i in range(0, len(bars), 5)], fontsize=8, rotation=30)
ax2.set_ylabel('Volume(万手)', fontsize=11)
ax2.set_title('成交量', fontsize=11, fontweight='bold')
ax2.grid(True, alpha=0.15, axis='y')

# --- 3. 20日K线+MA ---
ax3 = fig.add_subplot(gs[1, :])
x3 = np.arange(len(k_dates))
width = 0.6
for i in range(len(k_dates)):
    color = '#cc0000' if k_closes[i] >= k_opens[i] else '#00aa00'
    ax3.plot([i, i], [k_lows[i], k_highs[i]], color=color, linewidth=1.2, zorder=3)
    bottom = min(k_opens[i], k_closes[i])
    height = max(abs(k_closes[i]-k_opens[i]), 0.05)
    rect = plt.Rectangle((i-width/2, bottom), width, height,
                         facecolor=color, edgecolor=color, zorder=4)
    ax3.add_patch(rect)

# MA
ma5_arr = []
ma10_arr = []
for i in range(len(k_closes)):
    if i >= 4:
        ma5_arr.append(sum(k_closes[i-4:i+1])/5)
    else:
        ma5_arr.append(None)
    if i >= 9:
        ma10_arr.append(sum(k_closes[i-9:i+1])/10)
    else:
        ma10_arr.append(None)

ax3.plot(x3, ma5_arr, '-', color='#ff6600', linewidth=1.5, alpha=0.8, label='MA5')
ax3.plot(x3, ma10_arr, '-', color='#0066cc', linewidth=1.5, alpha=0.8, label='MA10')

# 关键价位
ax3.axhline(y=57.54, color='#000099', linewidth=1, linestyle='--', alpha=0.3, label='大宗铁底57.54')
ax3.axhline(y=63.37, color='#cc0000', linewidth=0.5, linestyle=':', alpha=0.3, label='7/15高点63.37')
ax3.axhline(y=76, color='#cc0000', linewidth=0.5, linestyle=':', alpha=0.2, label='7/1高点76')

# 标注
ax3.annotate('7/21\n冲高62.08', xy=(19, 62.08), xytext=(17, 66),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
ax3.annotate('7/20收盘59.90', xy=(18, 59.90), xytext=(16, 65),
             fontsize=9, color='#888888', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#888888', lw=1))

ax3.set_xticks(range(0, len(k_dates), 2))
ax3.set_xticklabels([k_dates[i] for i in range(0, len(k_dates), 2)], fontsize=10, rotation=30)
ax3.set_ylabel('Price', fontsize=12)
ax3.set_title('20日K线 — 7/21冲高62.08逼近MA10(62.48)', fontsize=12, fontweight='bold')
ax3.legend(fontsize=9, loc='upper right')
ax3.grid(True, alpha=0.12)
ax3.set_ylim([55, 70])

# --- 4. 大单净额 ---
ax4 = fig.add_subplot(gs[2, 0])
big_buy_nets = []
cum_buy = cum_sell = 0
for i in range(len(bars)):
    if real_vols[i] >= 100000:
        chg = prices[i] - (prices[i-1] if i > 0 else prices[i])
        direction = '买' if chg >= 0 else '卖'
        amt = real_vols[i] * prices[i] / 10000
        if direction == '买': cum_buy += amt
        else: cum_sell += amt
    big_buy_nets.append(cum_buy - cum_sell)

colors4 = ['#cc0000' if n > 0 else '#00aa00' for n in big_buy_nets]
ax4.bar(range(len(big_buy_nets)), [n/10000 for n in big_buy_nets], color=colors4, alpha=0.7, width=0.6)
ax4.axhline(y=0, color='black', linewidth=0.5)
ax4.set_xticks(range(0, len(bars), 5))
ax4.set_xticklabels([times[i] for i in range(0, len(bars), 5)], fontsize=8, rotation=30)
ax4.set_ylabel('Net Buy (万)', fontsize=11)
ax4.set_title(f'累计大单净额: {big_buy_nets[-1]/10000:+.0f}万', fontsize=11, fontweight='bold')
ax4.grid(True, alpha=0.15, axis='y')

# --- 5. 7/21 vs 7/20 对比 ---
ax5 = fig.add_subplot(gs[2, 1])
days = ['7/20\nAM', '7/20\nPM', '7/21\nAM']
vols_day = [1213, 212, 642]  # 万手
nets_day = [9157, -2262, 3392]  # 万
x5 = np.arange(3)
ax5_bar = ax5.bar(x5 - 0.2, [v/100 for v in vols_day], 0.35, color='#0066cc', alpha=0.7, label='Volume(亿)')
ax5_twin = ax5.twinx()
ax5_twin.bar(x5 + 0.2, [n/100 for n in nets_day], 0.35, color=['#00aa00','#cc0000','#00aa00'], alpha=0.7, label='Big Net(亿)')
ax5.set_xticks(x5)
ax5.set_xticklabels(days, fontsize=11)
ax5.set_ylabel('Volume(亿)', fontsize=11)
ax5_twin.set_ylabel('Big Net(亿)', fontsize=11)
ax5.set_title('7/20 AM vs PM vs 7/21 AM\n量+大单对比', fontsize=11, fontweight='bold')
ax5_twin.legend(fontsize=9, loc='upper right')
ax5.grid(True, alpha=0.15, axis='y')

# --- 6. 均线位置 ---
ax6 = fig.add_subplot(gs[3, :])
metrics = ['距MA5\n(60.95)', '距MA10\n(62.48)', '距MA20\n(69.48)', '距大宗\n(57.54)', '距7/15高\n(63.37)']
values = [(60.75-60.95)/60.95*100, (60.75-62.48)/62.48*100, (60.75-69.48)/69.48*100, (60.75-57.54)/57.54*100, (60.75-63.37)/63.37*100]
colors6 = ['#cc0000' if v < 0 else '#00aa00' for v in values]
ax6.barh(metrics, values, color=colors6, alpha=0.7, height=0.6)
for i, v in enumerate(values):
    ax6.text(v+0.2 if v >= 0 else v-0.2, i, f'{v:+.2f}%', va='center', fontsize=10, fontweight='bold')
ax6.axhline(y=0, color='black', linewidth=0.5)
ax6.set_xlabel('Deviation from MA (%)', fontsize=11)
ax6.set_title('当前价60.75 距各均线偏差', fontsize=12, fontweight='bold')
ax6.grid(True, alpha=0.15, axis='x')

plt.savefig('/data/hermes/workspace/301358_0721_realtime.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_0721_realtime.png')