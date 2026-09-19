#!/usr/bin/env python3
"""301358 7/22 主力意图+量价关系 分析图"""
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

# 加载7/22分时数据
with open('/tmp/301358_t_22.json') as f:
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

# 大单统计
big_buys = []  # (time_idx, amount, price)
big_sells = []
for i in range(len(bars)):
    if real_vols[i] >= 100000:
        chg = prices[i] - (prices[i-1] if i > 0 else prices[i])
        amt = real_vols[i] * prices[i] / 10000
        if chg >= 0:
            big_buys.append((i, amt, prices[i], times[i]))
        else:
            big_sells.append((i, amt, prices[i], times[i]))

total_big_buy = sum(b[1] for b in big_buys)
total_big_sell = sum(b[1] for b in big_sells)

# 东方财富资金流历史
flow_data = [
    ('7/07', -4195, 72.00, -1.88),
    ('7/08', -18888, 67.55, -6.18),
    ('7/09', -20964, 65.80, -2.59),
    ('7/10', -8695, 63.15, -4.03),
    ('7/13', -3940, 61.54, -2.55),
    ('7/14', -1612, 61.98, 0.71),
    ('7/15', 21539, 63.37, 2.24),
    ('7/16', -585, 61.24, -3.36),
    ('7/17', -7740, 59.47, -2.89),
    ('7/20', -613, 59.90, 0.72),
    ('7/21', 7542, 62.26, 3.94),
    ('7/22*', -1815, 60.90, -2.18),
]

fig = plt.figure(figsize=(22, 20))
gs = GridSpec(4, 2, figure=fig, height_ratios=[2, 1.2, 1, 1], hspace=0.35, wspace=0.15,
              left=0.06, right=0.96, top=0.97, bottom=0.03)

# === 1. 7/22 分时图 ===
ax1 = fig.add_subplot(gs[0, 0])
x = np.arange(len(bars))
ax1.plot(x, prices, color='#cc0000', linewidth=1.5, zorder=5)
vwap = sum(p*v for p,v in zip(prices, real_vols))/sum(real_vols)
ax1.axhline(y=vwap, color='blue', linewidth=1.5, linestyle='--', alpha=0.6, label=f'VWAP {vwap:.2f}')
ax1.axhline(y=62.26, color='#888888', linewidth=1, linestyle=':', alpha=0.4, label='昨收62.26')
ax1.axhline(y=61.79, color='#ff6600', linewidth=1, linestyle=':', alpha=0.4, label=f'开61.79')

# 大单标记
for i in range(len(bars)):
    if real_vols[i] >= 100000:
        chg = prices[i] - (prices[i-1] if i > 0 else prices[i])
        color = '#00aa00' if chg >= 0 else '#cc0000'
        size = min(200, real_vols[i]/1000)
        ax1.scatter(i, prices[i], s=size, color=color, zorder=10, edgecolors='black', linewidth=0.5)

# 标注关键大单
ax1.annotate(f'09:31 卖48.8万股\n3004万 61.54', xy=(0, 61.54), xytext=(3, 62.3),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
max_idx = prices.index(max(prices))
ax1.annotate(f'09:38 买20.6万股\n62.01 全天最高', xy=(max_idx, max(prices)), xytext=(max_idx+3, 62.6),
             fontsize=9, color='#00aa00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00aa00', lw=1.5))
ax1.annotate(f'09:43 卖40.5万股\n2482万 砸盘', xy=(11, 61.32), xytext=(14, 62.0),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
ax1.annotate(f'10:31 卖26.2万股\n跌破61', xy=(59, 60.91), xytext=(62, 61.6),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))

ax1.set_xticks(range(0, len(bars), 10))
ax1.set_xticklabels([times[i] for i in range(0, len(bars), 10)], fontsize=8, rotation=30)
ax1.set_ylabel('Price', fontsize=11)
ax1.set_title(f'7/22 分时图 — 低开砸盘+大单净卖出-1815万（昨+7542万→今-1815万）', fontsize=12, fontweight='bold')
ax1.legend(fontsize=8, loc='upper right')
ax1.grid(True, alpha=0.1)
ax1.set_ylim([60.5, 62.8])

# === 2. 大单买入 vs 卖出 ===
ax2 = fig.add_subplot(gs[0, 1])
buy_amts = [b[1] for b in big_buys]
sell_amts = [s[1] for s in big_sells]
categories = ['大单买入\n总计', '大单卖出\n总计', '净额']
values = [total_big_buy, total_big_sell, total_big_buy - total_big_sell]
colors2 = ['#00aa00', '#cc0000', '#0066cc' if values[2] > 0 else '#cc0000']
bars2 = ax2.bar(categories, [v/10000 for v in values], color=colors2, alpha=0.8, width=0.6)
for i, v in enumerate(values):
    label = f'{v/10000:+.2f}亿' if i == 2 else f'{v/10000:.2f}亿'
    ax2.text(i, v/10000 + 0.05, label, ha='center', fontsize=12, fontweight='bold')

# 对比7/21
ax2.axhline(y=7542/10000, color='#0066cc', linewidth=1.5, linestyle='--', alpha=0.5, label='7/21净额+7542万')
ax2.axhline(y=-613/10000, color='#888888', linewidth=1, linestyle=':', alpha=0.4, label='7/20净额-613万')

ax2.set_ylabel('Amount(亿)', fontsize=11)
ax2.set_title(f'7/22 大单: 买{total_big_buy/10000:.2f}亿 vs 卖{total_big_sell/10000:.2f}亿 = 净{-1815/10000:.2f}亿', fontsize=12, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.15, axis='y')

# === 3. 12天主力资金流K线 ===
ax3 = fig.add_subplot(gs[1, 0])
flow_dates = [f[0] for f in flow_data]
flow_vals = [f[1] for f in flow_data]
flow_prices = [f[2] for f in flow_data]
flow_pct = [f[3] for f in flow_data]

colors3 = ['#cc0000' if v < 0 else '#00aa00' for v in flow_vals]
bars3 = ax3.bar(range(len(flow_dates)), [v/10000 for v in flow_vals], color=colors3, alpha=0.8, width=0.6)
for i, v in enumerate(flow_vals):
    y = v/10000
    ax3.text(i, y + (0.15 if y > 0 else -0.15), f'{y:+.1f}', ha='center',
             va='bottom' if y > 0 else 'top', fontsize=9, fontweight='bold')

ax3.set_xticks(range(len(flow_dates)))
ax3.set_xticklabels(flow_dates, fontsize=10)
ax3.set_ylabel('主力净额(亿)', fontsize=11)
ax3.set_title('12天主力资金流 — 7/22大单翻负-1815万(7/21+7542万→今-1815万)', fontsize=12, fontweight='bold')
ax3.axhline(y=0, color='black', linewidth=0.5)
ax3.grid(True, alpha=0.15, axis='y')

# === 4. 股价+资金流叠加 ===
ax4 = fig.add_subplot(gs[1, 1])
x4 = np.arange(len(flow_data))
ax4.bar(x4, [v/10000 for v in flow_vals], color=colors3, alpha=0.4, width=0.6, label='主力净额')
ax4_twin = ax4.twinx()
ax4_twin.plot(x4, flow_prices, '-o', color='#cc0000', linewidth=2.5, markersize=8, label='收盘价', zorder=5)

ax4.set_xticks(x4)
ax4.set_xticklabels(flow_dates, fontsize=10)
ax4.set_ylabel('主力净额(亿)', fontsize=11)
ax4_twin.set_ylabel('Price', fontsize=11, color='#cc0000')
ax4.set_title('价格 vs 主力资金流 — "拉一天砸两天"的画框节奏', fontsize=12, fontweight='bold')
ax4.axhline(y=0, color='black', linewidth=0.5)
ax4.legend(fontsize=9, loc='upper left')
ax4_twin.legend(fontsize=9, loc='upper right')
ax4.grid(True, alpha=0.1)

# === 5. 7/22 vs 7/21 逐时段对比 ===
ax5 = fig.add_subplot(gs[2, 0])
# 7/22按30min分桶
bins_722 = {'9:30-10:00': [0, 0], '10:00-10:42': [0, 0]}
# 第一桶9:31-10:00 = idx 0-29
# 第二桶10:01-10:42 = idx 30-end
for i in range(min(30, len(bars))):
    chg = prices[i] - (prices[i-1] if i > 0 else prices[i])
    if chg >= 0: bins_722['9:30-10:00'][0] += real_vols[i] * prices[i] / 10000
    else: bins_722['9:30-10:00'][1] += real_vols[i] * prices[i] / 10000
for i in range(30, len(bars)):
    chg = prices[i] - (prices[i-1] if i > 0 else prices[i])
    if chg >= 0: bins_722['10:00-10:42'][0] += real_vols[i] * prices[i] / 10000
    else: bins_722['10:00-10:42'][1] += real_vols[i] * prices[i] / 10000

cats = ['7/21 AM\n买入', '7/21 AM\n卖出', '7/21 PM\n买入', '7/21 PM\n卖出',
        '7/22 9:30-10:00\n买入', '7/22 9:30-10:00\n卖出', '7/22 10:00-10:42\n买入', '7/22 10:00-10:42\n卖出']
# 7/21数据(从之前缓存)
vals = [36016, 26752, 4616, 7440, bins_722['9:30-10:00'][0], bins_722['9:30-10:00'][1],
        bins_722['10:00-10:42'][0], bins_722['10:00-10:42'][1]]
cols = ['#00aa00', '#cc0000', '#00aa00', '#cc0000', '#00aa00', '#cc0000', '#00aa00', '#cc0000']
ax5.bar(cats, [v/10000 for v in vals], color=cols, alpha=0.8)
for i, v in enumerate(vals):
    ax5.text(i, v/10000 + 0.1, f'{v/10000:.1f}亿', ha='center', fontsize=9, fontweight='bold', rotation=15)
ax5.set_xticklabels(cats, fontsize=8, rotation=20, ha='right')
ax5.set_ylabel('Amount(亿)', fontsize=11)
ax5.set_title('7/21 vs 7/22 逐时段对比 — 昨天买今天卖', fontsize=12, fontweight='bold')
ax5.grid(True, alpha=0.15, axis='y')

# === 6. 价格分布 ===
ax6 = fig.add_subplot(gs[2, 1])
bins_p = {}
for i in range(len(bars)):
    p = round(prices[i])
    bins_p[p] = bins_p.get(p, 0) + real_vols[i]
total = sum(bins_p.values())
sorted_bins = sorted(bins_p.items())
labels6 = [f'{p}元' for p, v in sorted_bins]
vols6 = [v/10000 for p, v in sorted_bins]
pcts6 = [v/total*100 for p, v in sorted_bins]
colors6 = ['#00aa00', '#ff6600', '#cc0000']
bars6 = ax6.barh(labels6, vols6, color=colors6[:len(vols6)], alpha=0.8, height=0.6)
for i, (v, p) in enumerate(zip(vols6, pcts6)):
    ax6.text(v+1, i, f'{v:.0f}万手 ({p:.1f}%)', va='center', fontsize=10, fontweight='bold')
ax6.set_xlabel('Volume(万手)', fontsize=11)
ax6.set_title(f'7/22价格分布: 61元58.3% / 62元41.7% → 60元以下0%', fontsize=12, fontweight='bold')
ax6.grid(True, alpha=0.12, axis='x')

# === 7. 大盘对比 ===
ax7 = fig.add_subplot(gs[3, 0])
compare = ['上证\n+0.36%', '深证\n+0.04%', '科创50\n-0.35%', '创业板\n-1.07%',
           '宁德\n-1.31%', '中芯国际\n-1.94%', '寒武纪\n-0.67%', '301358\n-2.18%']
comp_vals = [0.36, 0.04, -0.35, -1.07, -1.31, -1.94, -0.67, -2.18]
cols7 = ['#00aa00' if v > 0 else '#cc0000' if v < -1 else '#ff6600' for v in comp_vals]
ax7.barh(range(len(compare)), comp_vals, color=cols7, alpha=0.8, height=0.6)
for i, v in enumerate(comp_vals):
    ax7.text(v + (0.05 if v > 0 else -0.05), i, f'{v:+.2f}%', va='center',
             ha='left' if v > 0 else 'right', fontsize=10, fontweight='bold')
ax7.set_yticks(range(len(compare)))
ax7.set_yticklabels(compare, fontsize=10)
ax7.axvline(x=0, color='black', linewidth=0.5)
ax7.set_xlabel('涨幅 (%)', fontsize=11)
ax7.set_title('7/22 大盘对比 — 301358跌幅-2.18%全场最弱之一', fontsize=12, fontweight='bold')
ax7.invert_yaxis()
ax7.grid(True, alpha=0.12, axis='x')

# === 8. 关键价位 ===
ax8 = fig.add_subplot(gs[3, 1])
levels = ['铁底\n57.54', '20日最低\n58.80', '今日最低\n60.85', 'MA5\n~61.5', 'VWAP\n61.41',
          '今日开盘\n61.79', '昨收\n62.26', 'MA10\n~62.5', '今日最高\n62.01']
vals8 = [57.54, 58.80, 60.85, 61.5, 61.41, 61.79, 62.26, 62.5, 62.01]
cols8 = ['#00aa00', '#00aa00', '#ff6600', '#ff6600', '#0066cc', '#ff6600', '#888888', '#990099', '#cc0000']
ax8.barh(range(len(levels)), vals8, color=cols8, alpha=0.8, height=0.6)
for i, v in enumerate(vals8):
    ax8.text(v + 0.05, i, f'{v:.2f}', va='center', fontsize=10, fontweight='bold')
ax8.set_yticks(range(len(levels)))
ax8.set_yticklabels(levels, fontsize=10)
ax8.axvline(x=60.90, color='#cc0000', linewidth=2, linestyle='--', label='当前60.90')
ax8.set_xlabel('Price', fontsize=11)
ax8.set_title('关键价位 — 当前60.90跌破MA5和VWAP', fontsize=12, fontweight='bold')
ax8.legend(fontsize=10)
ax8.grid(True, alpha=0.12, axis='x')

plt.savefig('/data/hermes/workspace/301358_0722_analysis.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_0722_analysis.png')
