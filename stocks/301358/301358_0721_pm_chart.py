#!/usr/bin/env python3
"""301358 7/21 午后分析图"""
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

with open('/tmp/301358_t_pm.json') as f:
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

# 找午休分界
am_end = 0
for i, t in enumerate(times):
    if t.startswith('11:'):
        am_end = i
    if t.startswith('13:'):
        pm_start = i
        break

# 大单统计（分AM/PM）
am_big_buy = am_big_sell = 0
pm_big_buy = pm_big_sell = 0
for i in range(len(bars)):
    if real_vols[i] >= 100000:
        chg = prices[i] - (prices[i-1] if i > 0 else prices[i])
        direction = '买' if chg >= 0 else '卖'
        amt = real_vols[i] * prices[i] / 10000
        if i <= am_end:
            if direction == '买': am_big_buy += amt
            else: am_big_sell += amt
        else:
            if direction == '买': pm_big_buy += amt
            else: pm_big_sell += amt

fig = plt.figure(figsize=(22, 14))
gs = GridSpec(3, 2, figure=fig, height_ratios=[2, 1, 1], hspace=0.35, wspace=0.15,
              left=0.06, right=0.96, top=0.96, bottom=0.04)

# === 1. 分时图 ===
ax1 = fig.add_subplot(gs[0, 0])
x = np.arange(len(bars))
ax1.plot(x, prices, color='#cc0000', linewidth=1.5, zorder=5)
vwap = sum(p*v for p,v in zip(prices, real_vols))/sum(real_vols)
ax1.axhline(y=vwap, color='blue', linewidth=1.5, linestyle='--', alpha=0.6, label=f'VWAP {vwap:.2f}')
ax1.axhline(y=59.90, color='#888888', linewidth=1, linestyle=':', alpha=0.4, label='昨收59.90')
ax1.axhline(y=61.19, color='#ff6600', linewidth=1, linestyle='--', alpha=0.4, label='MA5=60.95')
ax1.axhline(y=62.48, color='#990099', linewidth=1, linestyle='--', alpha=0.4, label='MA10=62.48')

# 午休标记
ax1.axvline(x=am_end+0.5, color='#cccccc', linewidth=2, linestyle='-', alpha=0.5)
ax1.text(am_end/2, 63.5, '上午', ha='center', fontsize=10, alpha=0.5)
ax1.text((am_end+len(bars))/2+5, 63.5, '下午', ha='center', fontsize=10, alpha=0.5)

# 大单标记
for i in range(len(bars)):
    if real_vols[i] >= 100000:
        chg = prices[i] - (prices[i-1] if i > 0 else prices[i])
        color = '#00aa00' if chg >= 0 else '#cc0000'
        ax1.scatter(i, prices[i], s=60, color=color, zorder=10, edgecolors='black', linewidth=0.5)

# 标注最高点
max_idx = prices.index(max(prices))
ax1.annotate(f'最高 {max(prices):.2f}', xy=(max_idx, max(prices)), xytext=(max_idx+5, max(prices)+0.3),
             fontsize=10, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))

ax1.set_xticks(range(0, len(bars), 10))
ax1.set_xticklabels([times[i] for i in range(0, len(bars), 10)], fontsize=8, rotation=30)
ax1.set_ylabel('Price', fontsize=11)
ax1.set_title(f'7/21 分时图 — 最高62.97(+5%)后回落至62.19(+3.67%)', fontsize=12, fontweight='bold')
ax1.legend(fontsize=8, loc='upper left')
ax1.grid(True, alpha=0.1)

# === 2. 成交量 ===
ax2 = fig.add_subplot(gs[0, 1])
colors_vol = ['#cc0000' if i > 0 and prices[i] >= prices[i-1] else '#00aa00' for i in range(len(bars))]
ax2.bar(x, [v/10000 for v in real_vols], color=colors_vol, alpha=0.7, width=0.8)
ax2.set_xticks(range(0, len(bars), 10))
ax2.set_xticklabels([times[i] for i in range(0, len(bars), 10)], fontsize=8, rotation=30)
ax2.set_ylabel('Volume(万手)', fontsize=11)
ax2.set_title('成交量', fontsize=11, fontweight='bold')
ax2.grid(True, alpha=0.15, axis='y')

# === 3. AM vs PM 大单对比 ===
ax3 = fig.add_subplot(gs[1, 0])
cats = ['AM\n买入', 'AM\n卖出', 'AM\n净额', 'PM\n买入', 'PM\n卖出', 'PM\n净额', '全天\n净额']
vals = [am_big_buy, am_big_sell, am_big_buy-am_big_sell,
        pm_big_buy, pm_big_sell, pm_big_buy-pm_big_sell,
        am_big_buy+pm_big_buy-am_big_sell-pm_big_sell]
colors3 = ['#00aa00', '#cc0000', '#0066cc' if vals[2]>0 else '#cc0000',
           '#00aa00', '#cc0000', '#0066cc' if vals[5]>0 else '#cc0000',
           '#0066cc' if vals[6]>0 else '#cc0000']
ax3.bar(cats, [v/10000 for v in vals], color=colors3, alpha=0.8, width=0.6)
for i, v in enumerate(vals):
    ax3.text(i, v/10000+0.05, f'{v/10000:.2f}亿', ha='center', fontsize=9, fontweight='bold')
ax3.axhline(y=0, color='black', linewidth=0.5)
ax3.set_ylabel('Amount(亿)', fontsize=11)
ax3.set_title('AM vs PM 大单对比', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.15, axis='y')

# === 4. 301358 vs 大盘 ===
ax4 = fig.add_subplot(gs[1, 1])
times_compare = ['7/20\n收盘', '7/21\nAM高点', '7/21\n13:33当前']
p301358 = [59.90, 62.08, 62.19]
kc50 = [1731.12, 1809.60, 1830.84]
cyb = [3421.99, 3578.85, 3612.60]
ningde = [375.33, 387.49, 381.20]

x4 = np.arange(3)
ax4.plot(x4, p301358, '-o', color='#cc0000', linewidth=2.5, markersize=10, label='301358', zorder=5)
for i, v in enumerate(p301358):
    ax4.text(i, v+0.5, f'{v:.2f}', ha='center', fontsize=10, color='#cc0000', fontweight='bold')
ax4_twin = ax4.twinx()
ax4_twin.plot(x4, kc50, '-s', color='#0066cc', linewidth=2, markersize=8, label='科创50', alpha=0.8)
ax4_twin.plot(x4, cyb, '-^', color='#ff6600', linewidth=2, markersize=8, label='创业板', alpha=0.8)
ax4_twin.plot(x4, ningde, '--d', color='#888888', linewidth=1.5, markersize=6, label='宁德', alpha=0.6)

ax4.set_xticks(x4)
ax4.set_xticklabels(times_compare, fontsize=10)
ax4.set_ylabel('301358', fontsize=11, color='#cc0000')
ax4_twin.set_ylabel('Index', fontsize=11)
ax4.set_title('301358 vs 大盘走势对比', fontsize=12, fontweight='bold')
ax4.legend(fontsize=9, loc='upper left')
ax4_twin.legend(fontsize=9, loc='lower left')
ax4.grid(True, alpha=0.1)

# === 5. 价格分布 ===
ax5 = fig.add_subplot(gs[2, 0])
bins = {}
for i in range(len(bars)):
    p = round(prices[i])
    bins[p] = bins.get(p, 0) + real_vols[i]
total = sum(bins.values())
sorted_bins = sorted(bins.items())
prices_lbl = [f'{p}元' for p, v in sorted_bins]
vols = [v/10000 for p, v in sorted_bins]
pcts = [v/total*100 for p, v in sorted_bins]
colors5 = ['#00aa00', '#ff6600', '#cc0000', '#990099']
ax5.barh(prices_lbl, vols, color=colors5[:len(vols)], alpha=0.8, height=0.6)
for i, (v, p) in enumerate(zip(vols, pcts)):
    ax5.text(v+1, i, f'{v:.0f}万手 ({p:.1f}%)', va='center', fontsize=10, fontweight='bold')
ax5.set_xlabel('Volume(万手)', fontsize=11)
ax5.set_title('价格分布 — 61-62元占82%', fontsize=12, fontweight='bold')
ax5.grid(True, alpha=0.12, axis='x')

# === 6. 关键价位 ===
ax6 = fig.add_subplot(gs[2, 1])
levels = ['最低59.70', '昨收59.90', 'MA5\n60.95', 'VWAP\n61.43', '当前62.19', 'MA10\n62.48', '最高62.97']
values = [59.70, 59.90, 60.95, 61.43, 62.19, 62.48, 62.97]
colors6 = ['#00aa00', '#888888', '#ff6600', '#0066cc', '#cc0000', '#990099', '#cc0000']
ax6.barh(levels, values, color=colors6, alpha=0.8, height=0.6)
for i, v in enumerate(values):
    ax6.text(v+0.1, i, f'{v:.2f}', va='center', fontsize=10, fontweight='bold')
ax6.set_xlabel('Price', fontsize=11)
ax6.set_title('关键价位全景', fontsize=12, fontweight='bold')
ax6.set_xlim([58, 64])
ax6.grid(True, alpha=0.12, axis='x')

plt.savefig('/data/hermes/workspace/301358_0721_pm.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_0721_pm.png')
