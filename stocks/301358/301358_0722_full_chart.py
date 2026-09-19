#!/usr/bin/env python3
"""301358 7/22 午盘全景分析 — 主力意图+量价+减持+新闻"""
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

# 7/22分时数据
with open('/tmp/301358_t_latest.json') as f:
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

# 大单统计（AM/PM分段）
am_end = max(i for i, t in enumerate(times) if t.startswith('11:')) if any(t.startswith('11:') for t in times) else len(bars)

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

# 东方财富12天资金流
flow_data = [
    ('7/07', -4195, 72.00, -1.88, 0.65, -4.35),
    ('7/08', -18888, 67.55, -6.18, 17.53, -10.37),
    ('7/09', -20964, 65.80, -2.59, 13.40, -4.04),
    ('7/10', -8695, 63.15, -4.03, 6.99, -5.00),
    ('7/13', -3940, 61.54, -2.55, 0.54, -4.03),
    ('7/14', -1612, 61.98, 0.71, 1.12, 1.99),
    ('7/15', 21539, 63.37, 2.24, -16.87, 5.10),
    ('7/16', -585, 61.24, -3.36, -0.90, -0.17),
    ('7/17', -7740, 59.47, -2.89, 5.80, -1.16),
    ('7/20', -613, 59.90, 0.72, -0.56, 0.44),
    ('7/21', 7542, 62.26, 3.94, -4.92, 4.97),
    ('7/22*', -3100, 61.12, -1.83, 0, 0),
]

fig = plt.figure(figsize=(24, 22))
gs = GridSpec(4, 2, figure=fig, height_ratios=[2, 1.2, 1, 1.2], hspace=0.35, wspace=0.15,
              left=0.05, right=0.97, top=0.97, bottom=0.03)

# === 1. 7/22 分时图 ===
ax1 = fig.add_subplot(gs[0, 0])
x = np.arange(len(bars))
ax1.plot(x, prices, color='#cc0000', linewidth=1.5, zorder=5)
vwap = sum(p*v for p,v in zip(prices, real_vols))/sum(real_vols)
ax1.axhline(y=vwap, color='blue', linewidth=1.5, linestyle='--', alpha=0.6, label=f'VWAP {vwap:.2f}')
ax1.axhline(y=62.26, color='#888888', linewidth=1, linestyle=':', alpha=0.4, label='昨收62.26')
ax1.axhline(y=61.79, color='#ff6600', linewidth=1, linestyle=':', alpha=0.4, label=f'开61.79')
ax1.axhline(y=61.28, color='#0066cc', linewidth=1, linestyle=':', alpha=0.4, label=f'VWAP 61.28')

for i in range(len(bars)):
    if real_vols[i] >= 100000:
        chg = prices[i] - (prices[i-1] if i > 0 else prices[i])
        color = '#00aa00' if chg >= 0 else '#cc0000'
        size = min(250, real_vols[i]/800)
        ax1.scatter(i, prices[i], s=size, color=color, zorder=10, edgecolors='black', linewidth=0.5)

# 标注关键时点
ax1.annotate(f'09:31 卖48.8万股\n3004万 61.54\n开盘第一笔就砸', xy=(0, 61.54), xytext=(3, 62.4),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
max_idx = prices.index(max(prices))
ax1.annotate(f'09:38 62.01 全天最高\n买20.6万股 1276万', xy=(max_idx, max(prices)), xytext=(max_idx+3, 62.7),
             fontsize=9, color='#00aa00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00aa00', lw=1.5))
min_idx = prices.index(min(prices))
ax1.annotate(f'10:34 60.85 全天最低\n卖20.1万股 1224万', xy=(min_idx, min(prices)), xytext=(min_idx+3, 60.2),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))

ax1.set_xticks(range(0, len(bars), 10))
ax1.set_xticklabels([times[i] for i in range(0, len(bars), 10)], fontsize=8, rotation=30)
ax1.set_ylabel('Price', fontsize=11)
ax1.set_title(f'7/22分时图: 低开→开盘砸→拉62→回落60.85→收盘前回升60.90→60.93→61.12', fontsize=12, fontweight='bold')
ax1.legend(fontsize=8, loc='upper right')
ax1.grid(True, alpha=0.1)
ax1.set_ylim([60.0, 62.8])

# === 2. 12天主力资金流柱状图 ===
ax2 = fig.add_subplot(gs[0, 1])
flow_dates = [f[0] for f in flow_data]
flow_vals = [f[1] for f in flow_data]
flow_prices = [f[2] for f in flow_data]
colors2 = ['#cc0000' if v < 0 else '#00aa00' for v in flow_vals]
bars2 = ax2.bar(range(len(flow_dates)), [v/10000 for v in flow_vals], color=colors2, alpha=0.8, width=0.6)
for i, v in enumerate(flow_vals):
    y = v/10000
    ax2.text(i, y + (0.1 if y > 0 else -0.1), f'{y:+.1f}', ha='center',
             va='bottom' if y > 0 else 'top', fontsize=9, fontweight='bold')
ax2.set_xticks(range(len(flow_dates)))
ax2.set_xticklabels(flow_dates, fontsize=10, rotation=20)
ax2.set_ylabel('主力净额(亿)', fontsize=11)
ax2.set_title('12天主力资金流: 7/22大单翻负-0.31亿 → 验证"拉一天砸两天"', fontsize=12, fontweight='bold')
ax2.axhline(y=0, color='black', linewidth=0.5)
# 画趋势线
cumsum = 0
cumsums = []
for v in flow_vals:
    cumsum += v/10000
    cumsums.append(cumsum)
ax2_twin = ax2.twinx()
ax2_twin.plot(range(len(flow_dates)), cumsums, '-o', color='#990099', linewidth=2, markersize=6, label='累计净额')
ax2_twin.set_ylabel('累计净额(亿)', fontsize=11, color='#990099')
ax2_twin.legend(fontsize=10, loc='upper right')
ax2.grid(True, alpha=0.15, axis='y')

# === 3. 收盘价叠加主力净额 ===
ax3 = fig.add_subplot(gs[1, 0])
x3 = np.arange(len(flow_data))
ax3.bar(x3, [v/10000 for v in flow_vals], color=colors2, alpha=0.4, width=0.6, label='主力净额')
ax3_twin = ax3.twinx()
ax3_twin.plot(x3, flow_prices, '-o', color='#cc0000', linewidth=2.5, markersize=8, label='收盘价', zorder=5)
ax3.set_xticks(x3)
ax3.set_xticklabels(flow_dates, fontsize=10, rotation=20)
ax3.set_ylabel('主力净额(亿)', fontsize=11)
ax3_twin.set_ylabel('Price', fontsize=11, color='#cc0000')
ax3.set_title('价格+资金流: 主力净额翻负→次日价格下跌规律', fontsize=12, fontweight='bold')
ax3.axhline(y=0, color='black', linewidth=0.5)

# 标注"拉→砸"周期
ax3.annotate('拉', xy=(6, 2.5), fontsize=16, color='#00aa00', fontweight='bold', ha='center')
ax3.annotate('砸', xy=(7, 2.5), fontsize=16, color='#cc0000', fontweight='bold', ha='center')
ax3.annotate('拉', xy=(10, 2.5), fontsize=16, color='#00aa00', fontweight='bold', ha='center')
ax3.annotate('砸', xy=(11, 2.5), fontsize=16, color='#cc0000', fontweight='bold', ha='center')

ax3.legend(fontsize=9, loc='upper left')
ax3_twin.legend(fontsize=9, loc='upper right')
ax3.grid(True, alpha=0.1)

# === 4. 7/22 vs 7/21 大单对比 ===
ax4 = fig.add_subplot(gs[1, 1])
cats4 = ['7/21大单买入', '7/21大单卖出', '7/21净额',
         '7/22 AM买入', '7/22 AM卖出', '7/22 AM净额',
         '7/22 PM买入(估)', '7/22 PM卖出(估)', '7/22全天净额']
# 7/21数据(东方财富): main=7542万, big_order=737万, super=6804万
# 7/22分时: AM买入约21300万, 卖出约24500万, 净-3200万
vals4 = [7542+0, 0, 7542, am_big_buy, am_big_sell, am_big_buy-am_big_sell,
         0, 0, -3100]
# 7/21: 买7542万(净), 7/22: 净-3100万
# 简化展示
cats4_simple = ['7/21\n主力净额', '7/22\n主力净额', '7/22\nAM大单买入', '7/22\nAM大单卖出', '7/22\nAM大单净额']
vals4_simple = [7542, -3100, am_big_buy, am_big_sell, am_big_buy-am_big_sell]
colors4 = ['#00aa00', '#cc0000', '#00aa00', '#cc0000', '#cc0000']
ax4.bar(cats4_simple, [v/10000 for v in vals4_simple], color=colors4, alpha=0.8, width=0.6)
for i, v in enumerate(vals4_simple):
    ax4.text(i, v/10000 + (0.1 if v > 0 else -0.2), f'{v/10000:+.2f}亿', ha='center',
             fontsize=11, fontweight='bold')
ax4.axhline(y=0, color='black', linewidth=0.5)
ax4.set_xticklabels(cats4_simple, fontsize=9, rotation=10)
ax4.set_ylabel('Amount(亿)', fontsize=11)
ax4.set_title('7/21→7/22 大单反转: +0.75亿→-0.31亿 = 拉完就砸', fontsize=12, fontweight='bold')
ax4.grid(True, alpha=0.15, axis='y')

# === 5. 7/22 价格分布 ===
ax5 = fig.add_subplot(gs[2, 0])
bins_p = {}
for i in range(len(bars)):
    p = round(prices[i])
    bins_p[p] = bins_p.get(p, 0) + real_vols[i]
total = sum(bins_p.values())
sorted_bins = sorted(bins_p.items())
labels5 = [f'{p}元' for p, v in sorted_bins]
vols5 = [v/10000 for p, v in sorted_bins]
pcts5 = [v/total*100 for p, v in sorted_bins]
colors5 = ['#00aa00', '#ff6600', '#cc0000', '#990099']
bars5 = ax5.barh(labels5, vols5, color=colors5[:len(vols5)], alpha=0.8, height=0.6)
for i, (v, p) in enumerate(zip(vols5, pcts5)):
    ax5.text(v+1, i, f'{v:.0f}万手 ({p:.1f}%)', va='center', fontsize=10, fontweight='bold')
ax5.set_xlabel('Volume(万手)', fontsize=11)
is60 = 60 in bins_p
ax5.set_title(f'7/22价格分布: 61元63.6% / 62元33.8%{" / 60元2.7%" if is60 else ""} = 61-62成交97%+', fontsize=12, fontweight='bold')
ax5.grid(True, alpha=0.12, axis='x')

# === 6. 大盘对比 ===
ax6 = fig.add_subplot(gs[2, 1])
compare = ['上证\n+0.50%', '科创50\n+1.54%', '寒武纪\n+1.48%', '华虹\n+0.89%',
           '中芯国际\n-0.31%', '创业板\n-0.13%', '宁德时代\n-1.47%', '301358\n-1.83%']
comp_vals = [0.50, 1.54, 1.48, 0.89, -0.31, -0.13, -1.47, -1.83]
cols6 = ['#00aa00' if v > 0.3 else '#ff6600' if v > -0.5 else '#cc0000' for v in comp_vals]
ax6.barh(range(len(compare)), comp_vals, color=cols6, alpha=0.8, height=0.6)
for i, v in enumerate(comp_vals):
    ax6.text(v + (0.05 if v > 0 else -0.05), i, f'{v:+.2f}%', va='center',
             ha='left' if v > 0 else 'right', fontsize=10, fontweight='bold')
ax6.set_yticks(range(len(compare)))
ax6.set_yticklabels(compare, fontsize=10)
ax6.axvline(x=0, color='black', linewidth=0.5)
ax6.set_xlabel('涨幅 (%)', fontsize=11)
ax6.set_title('7/22大盘对比: 301358跌-1.83% 弱于宁德(大盘不差个股自身弱)', fontsize=12, fontweight='bold')
ax6.invert_yaxis()
ax6.grid(True, alpha=0.12, axis='x')

# === 7. 减持时间轴 ===
ax7 = fig.add_subplot(gs[3, 0])
ax7.set_xlim([0, 10])
ax7.set_ylim([0, 5])
ax7.axis('off')

# 时间线
dates_tl = ['6/3', '6/4', '6/26', '7/13', '7/17', '7/22\n今天', '8/1', '8月中\n(估)', '9/25']
events_tl = [
    '6/3: 减持公告\n宁德3%+津晟2.5%\n合计5.5%(4638万股)',
    '6/4: 跌停-10%\n从88→73',
    '6/26: 减持1%\n持股降至6.85%\n大宗57.54',
    '7/13: 大宗交易\n约242万股\n完成约9.6%',
    '7/17: 240亿扩产\n+H股上市',
    '7/22: 当前\n减持约10.8%\n画框58-62',
    '8/1: 涨价函生效\n+2000元/吨',
    '8月中:\n半年报发布\n(预计)',
    '9/25: 减持截止\n剩余~4400万股'
]
colors_tl = ['#cc0000', '#cc0000', '#ff6600', '#ff6600', '#ff6600', '#cc0000', '#00aa00', '#0066cc', '#cc0000']

x_pos = np.linspace(0.5, 9.5, 9)
for i, (d, e, c) in enumerate(zip(dates_tl, events_tl, colors_tl)):
    y_pos = 3.5 if i % 2 == 0 else 1.5
    ax7.plot(x_pos[i], 3, 'o', markersize=15, color=c, zorder=5)
    ax7.plot([x_pos[i], x_pos[i]], [3, y_pos+0.3 if y_pos > 3 else y_pos-0.3], color=c, linewidth=1, alpha=0.5)
    offset = 0.5 if y_pos > 3 else -0.5
    ax7.text(x_pos[i], y_pos + offset, f'{d}\n{e}', ha='center', va='top' if y_pos > 3 else 'bottom',
             fontsize=8, color=c, fontweight='bold')

ax7.plot([0.2, 9.8], [3, 3], '-', color='#cccccc', linewidth=2)
ax7.set_title('减持时间轴: 6/3公告→9/25截止 | 已完成约10.8% | 剩余89.2%待减', fontsize=12, fontweight='bold')

# === 8. 关键数据汇总表 ===
ax8 = fig.add_subplot(gs[3, 1])
ax8.axis('off')
ax8.set_xlim([0, 10])
ax8.set_ylim([0, 10])

table_data = [
    ['指标', '7/21', '7/22(盘中)', '变化'],
    ['收盘价', '62.26 (+3.95%)', '61.12 (-1.83%)', '-1.14元'],
    ['最高', '62.97', '62.01', '上轨下移'],
    ['最低', '59.70', '60.85', '+1.15'],
    ['VWAP', '61.43', '61.28', '-0.15'],
    ['东方财富主力', '+7542万', '-3100万(估)', '🚨翻负!'],
    ['量比', '1.61', '1.11', '缩量'],
    ['宁德', '+2.70%', '-1.47%', '电池弱'],
    ['科创50', '+6.53%', '+1.54%', '半导体高位'],
    ['画框', '突破上轨62.97', '回落框内61', '假突破确认'],
]

table = ax8.table(cellText=table_data[1:], colLabels=table_data[0],
                  cellLoc='center', loc='center',
                  colWidths=[0.2, 0.25, 0.25, 0.2])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.8)

for j in range(4):
    table[0, j].set_facecolor('#333333')
    table[0, j].set_text_props(color='white', fontweight='bold')
for i in range(1, len(table_data)):
    for j in range(4):
        if i == 6:  # 主力翻负行
            table[i, j].set_facecolor('#ffcccc')
        elif i % 2 == 0:
            table[i, j].set_facecolor('#f0f0f0')

ax8.set_title('7/21→7/22 核心数据对比', fontsize=12, fontweight='bold', pad=20)

plt.savefig('/data/hermes/workspace/301358_0722_full.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_0722_full.png')
