#!/usr/bin/env python3
"""301358 7/20 早盘实时分析图"""
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

# 7/20 分时数据
with open('/tmp/301358_tl_0720.json') as f:
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

# 7/17 价格分布（从K线记录而非分时文件）
# 7/17: O:61.08 C:59.47 H:62.44 L:58.80, 按区间估算
bins_17_pct_manual = {59: 24.4, 60: 43.9, 61: 24.7, 62: 7.0}
total_vol17 = 20000000  # 20万手近似

# K线
with open('/tmp/301358_klines_60d_0720.json') as f:
    k_data = json.load(f)
klines = k_data['data']['sz301358']['qfqday']

fig = plt.figure(figsize=(22, 24))
gs = GridSpec(3, 2, figure=fig, height_ratios=[2.5, 1.5, 2.5], hspace=0.3, wspace=0.2,
              left=0.06, right=0.96, top=0.96, bottom=0.02)

# ============ 1. 7/20 分时走势 ============
ax1 = fig.add_subplot(gs[0, :])
x = np.arange(len(bars))
colors_vol = ['#cc0000' if i > 0 and prices[i] >= prices[i-1] else '#00aa00' for i in range(len(bars))]
ax1_v = ax1.twinx()
ax1_v.bar(x, [v/10000 for v in real_vols], color=colors_vol, alpha=0.25, width=0.8)

ax1.plot(x, prices, color='#cc0000', linewidth=2, zorder=5)
ax1.axhline(y=vwap, color='blue', linewidth=1.5, linestyle='--', alpha=0.6, label=f'7/20 VWAP {vwap:.2f}')

# 7/17 对比线
prev_close = 59.47
ax1.axhline(y=prev_close, color='#888888', linewidth=1.5, linestyle=':', alpha=0.5, label=f'7/17 close {prev_close}')
ax1.axhline(y=60.31, color='#006600', linewidth=1, linestyle='--', alpha=0.3, label='7/16 low 60.31')
ax1.axhline(y=57.54, color='#000099', linewidth=1.5, linestyle='--', alpha=0.3, label='7/13 block 57.54')

# 大单标记
for i in range(len(bars)):
    if real_vols[i] >= 200000:
        color = '#00aa00' if i > 0 and prices[i] >= prices[i-1] else '#cc0000'
        ax1.scatter(i, prices[i], s=80, color=color, zorder=10, edgecolors='black', linewidth=0.8)

tick_idx = [i for i, t in enumerate(times) if t.endswith(':00') or t.endswith(':30') or i == len(bars)-1]
ax1.set_xticks([i for i in tick_idx])
ax1.set_xticklabels([times[i] for i in tick_idx], fontsize=9, rotation=30)
ax1.set_ylabel('Price', fontsize=12)
ax1.set_title('301358 Hunan Yuneng 7/20 AM (as of 10:05) — REBOUND +2.1% to 60.72\n'
              'Volume RATIO 2.38 vs 7/17 1.05 | Big Order NET +8293wan (FLIP from sell)',
              fontsize=13, fontweight='bold')
ax1.legend(fontsize=9, loc='lower right')
ax1.grid(True, alpha=0.12)

# 标注
ax1.annotate('OPEN 60.01\n+0.9% gap up', xy=(0, 60.01), xytext=(3, 58.8),
             fontsize=9, color='#00aa00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00aa00', lw=1.5))
ax1.annotate('09:31 SUPER BUY\n79.84wan 4806wan', xy=(1, 60.19), xytext=(5, 61.5),
             fontsize=10, color='#00aa00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00aa00', lw=2),
             bbox=dict(boxstyle='round', facecolor='#f0fff0'))
ax1.annotate('09:32 SELL\n43.14wan 2575wan', xy=(2, 59.68), xytext=(8, 58.5),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
ax1.annotate('09:37 60.84\nHIGH', xy=(7, 60.84), xytext=(12, 61.8),
             fontsize=9, color='#cc0000',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1))

# ============ 2a. 7/20 vs 7/17 大单对比 ============
ax2 = fig.add_subplot(gs[1, 0])
# 7/20
buy20 = 23299
sell20 = 15006
net20 = buy20 - sell20
# 7/17 全天
buy17 = 26623
sell17 = 32682
net17 = buy17 - sell17

labels = ['7/17 Full Day', '7/20 AM(35min)']
buys = [buy17, buy20]
sells = [sell17, sell20]
nets = [net17, net17]

x2 = np.arange(2)
width = 0.35
ax2.bar(x2 - width/2, buys, width, color='#00aa00', alpha=0.7, label='Buy')
ax2.bar(x2 + width/2, sells, width, color='#cc0000', alpha=0.7, label='Sell')
ax2.text(0, max(buy17, sell17)+1000, f'{net17:+.0f}', ha='center', fontsize=11, color='#cc0000', fontweight='bold')
ax2.text(1, max(buy20, sell20)+1000, f'{net20:+.0f}', ha='center', fontsize=11, color='#00aa00', fontweight='bold')
ax2.set_xticks(x2)
ax2.set_xticklabels(labels, fontsize=10)
ax2.set_ylabel('Amount (wan)', fontsize=11)
ax2.set_title('Big Order: 7/17 NET SELL -6059wan → 7/20 NET BUY +8293wan\nFLIP! In 35 min, more buy than full day 7/17',
              fontsize=11, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.15, axis='y')

# ============ 2b. 近8日K线 ============
ax3 = fig.add_subplot(gs[1, 1])
recent_ks = klines[-8:]
k_labels = [k[0][-5:] for k in recent_ks]
opens = [float(k[1]) for k in recent_ks]
closes = [float(k[2]) for k in recent_ks]
highs = [float(k[3]) for k in recent_ks]
lows = [float(k[4]) for k in recent_ks]
vols = [float(k[5]) for k in recent_ks]

x3 = np.arange(len(recent_ks))
for i in range(len(recent_ks)):
    up = closes[i] >= opens[i]
    color = '#cc0000' if up else '#00aa00'
    ax3.plot([i, i], [lows[i], highs[i]], color=color, linewidth=1, zorder=1)
    body_bottom = min(opens[i], closes[i])
    body_height = abs(closes[i] - opens[i])
    rect = plt.Rectangle((i-0.3, body_bottom), 0.6, max(body_height, 0.15),
                         facecolor=color if not up else 'white', edgecolor=color, linewidth=1.5, zorder=2)
    ax3.add_patch(rect)
    chg = (closes[i] - opens[i]) / opens[i] * 100
    ax3.text(i, lows[i]-1, f'{closes[i]:.1f}', ha='center', fontsize=8, color=color)
    ax3.text(i, highs[i]+0.5, f'{chg:+.1f}%', ha='center', fontsize=8, color=color)

# 7/20 K线(实时)
i_today = len(recent_ks)-1
ax3.scatter(i_today, 60.72, s=100, color='#cc0000', zorder=15, marker='*', label='Now 60.72')
ax3.scatter(i_today, 59.16, s=50, color='#00aa00', zorder=15, marker='v', label='Low 59.16')

ax3.set_xticks(x3)
ax3.set_xticklabels(k_labels, fontsize=9, rotation=15)
ax3.set_ylabel('Price', fontsize=11)
ax3.set_title('Recent 8 Days K-Line\n7/17 -2.6% → 7/20 +2.1% rebound, lower shadow 59.16',
              fontsize=11, fontweight='bold')
ax3.axhline(y=57.54, color='#000099', linewidth=1, linestyle='--', alpha=0.3)
ax3.axhline(y=60, color='#00aa00', linewidth=1, linestyle=':', alpha=0.3)
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.15, axis='y')

# ============ 3. 价格分布对比 3天 ============
ax4 = fig.add_subplot(gs[2, :])

# 三天价格分布
bins_20 = {}
for i in range(len(bars)):
    bucket = round(prices[i])
    bins_20[bucket] = bins_20.get(bucket, 0) + real_vols[i]
bins_20_pct = {p: bins_20[p]/total_vol*100 for p in bins_20}

bins_17 = {}
for p, pct in bins_17_pct_manual.items():
    bins_17[p] = int(pct * total_vol17 / 100)
bins_17_pct = {p: bins_17[p]/total_vol17*100 for p in bins_17}

bins_16_pct = {61: 45.3, 62: 40.2, 63: 11.8, 64: 2.7}

all_p = sorted(set(list(bins_20_pct.keys()) + list(bins_17_pct.keys()) + list(bins_16_pct.keys())))
r_16 = [bins_16_pct.get(p, 0) for p in all_p]
r_17 = [bins_17_pct.get(p, 0) for p in all_p]
r_20 = [bins_20_pct.get(p, 0) for p in all_p]

x4 = np.arange(len(all_p))
width = 0.25
ax4.bar(x4 - width, r_16, width, color='#ff6600', alpha=0.6, label='7/16')
ax4.bar(x4, r_17, width, color='#cc0000', alpha=0.7, label='7/17')
ax4.bar(x4 + width, r_20, width, color='#0066cc', alpha=0.8, label='7/20 AM')

ax4.set_xticks(x4)
ax4.set_xticklabels(['%d' % p for p in all_p], fontsize=12)
ax4.set_xlabel('Price', fontsize=12)
ax4.set_ylabel('Volume %', fontsize=12)
ax4.set_title('Price Distribution: 7/16 vs 7/17 vs 7/20 AM\n'
              '7/16: 61-62 floor(85%) | 7/17: 59-60 floor(67%) | 7/20: 60 floor(72%), 61 zone=28%',
              fontsize=12, fontweight='bold')
ax4.legend(fontsize=11)
ax4.grid(True, alpha=0.15, axis='y')

for i, (r16, r17, r20) in enumerate(zip(r_16, r_17, r_20)):
    if r16 > 0: ax4.text(i - width, r16 + 1, '%.0f' % r16, ha='center', fontsize=8, color='#ff6600')
    if r17 > 0: ax4.text(i, r17 + 1, '%.0f' % r17, ha='center', fontsize=8, color='#cc0000')
    if r20 > 0: ax4.text(i + width, r20 + 1, '%.0f' % r20, ha='center', fontsize=8, color='#0066cc')

plt.savefig('/data/hermes/workspace/301358_0720_am_analysis.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_0720_am_analysis.png')
