#!/usr/bin/env python3
"""301358 7/14 多维分析（含大宗交易）"""
import json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.gridspec as gridspec

fm.fontManager.addfont('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 读取分时数据
with open('301358_0714_minutes_latest.json') as f:
    raw = json.load(f)

prev_close = 61.54
data = []
for i, m in enumerate(raw):
    parts = m.split()
    cum_v = int(parts[2])
    inc_v = cum_v - (int(raw[i-1].split()[2]) if i > 0 else 0)
    cum_a = float(parts[3])
    inc_a = cum_a - (float(raw[i-1].split()[3]) if i > 0 else 0)
    data.append({'time': parts[0], 'price': float(parts[1]),
                'inc_vol': inc_v, 'cum_vol': cum_v,
                'inc_amt': inc_a, 'cum_amt': cum_a})

prices = [d['price'] for d in data]
inc_vols = [d['inc_vol'] for d in data]
times = [d['time'] for d in data]

# 大宗交易数据
block_trade = {
    'date': '2026-07-02',
    'price': 59.05,
    'discount': 6.49,
    'volume': 330000,
    'amount': 1.95,
    'seller': '宁德时代',
    'buyer': '未知机构',
    'cumulative_sold': 5435032,  # 210.5万(竞价)+33万(大宗)=243.5万股
    'remaining_plan': 25300206 - 5435032,  # 剩余约1986万股
    'reduction_window': '2026-06-26 ~ 2026-09-25',
}

# 实时quote
current_price = 60.71
current_change = -0.83
current_change_pct = -1.35
current_high = 61.80
current_low = 60.23
current_vol = 50160  # 手
current_amount = 30614  # 万
vwap = current_amount * 10000 / (current_vol * 100)

fig = plt.figure(figsize=(24, 16))
gs = gridspec.GridSpec(4, 2, figure=fig, hspace=0.35, wspace=0.25,
                       left=0.05, right=0.97, top=0.93, bottom=0.04)

fig.suptitle(f'301358 湖南裕能 7/14 多维分析（截至10:20）\n'
             f'当前{current_price:.2f}(-{abs(current_change_pct):.2f}%) | 最低{current_low:.2f} | '
             f'大宗折价6.49% | 宁德时代减持剩余{block_trade["remaining_plan"]/10000:.0f}万股(78.5%) | '
             f'板块资金流入电子器件+52.44亿',
             fontsize=14, fontweight='bold', color='#1a237e')

# ---- 1. 分时走势 + 大宗交易价 ----
ax1 = fig.add_subplot(gs[0, :])
x = np.arange(len(data))
ax1.fill_between(x, prev_close, prices, where=[p < prev_close for p in prices],
                 color='#00e676', alpha=0.1)
ax1.fill_between(x, prev_close, prices, where=[p >= prev_close for p in prices],
                 color='#ff1744', alpha=0.1)
ax1.plot(x, prices, color='#1565c0', linewidth=2, marker='o', markersize=2)

# 大宗交易价线
ax1.axhline(y=59.05, color='#d32f2f', linewidth=2, linestyle='--', alpha=0.7, label='大宗59.05(宁德售)')
ax1.text(0, 59.05, f' 大宗59.05\n折价6.49%', fontsize=9, color='#d32f2f',
        fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='#ffcdd2', alpha=0.9))

# 关键价位
ax1.axhline(y=prev_close, color='#ff9800', linewidth=0.8, linestyle='--', alpha=0.4, label='昨收61.54')
ax1.axhline(y=current_low, color='#d32f2f', linewidth=1, linestyle=':', alpha=0.5, label=f'最低{current_low}')
ax1.axhline(y=60.97, color='#2e7d32', linewidth=0.8, linestyle=':', alpha=0.4, label='7/13最低60.97')

# VWAP
cum_amts = np.cumsum([d['inc_amt'] for d in data])
cum_vols = np.cumsum([d['inc_vol'] for d in data])
vwap_line = cum_amts / (cum_vols * 100)
ax1.plot(x, vwap_line, color='#ff9800', linewidth=1, alpha=0.6, label=f'VWAP {vwap_line[-1]:.2f}')

# 标注
min_idx = prices.index(min(prices))
ax1.annotate(f'最低{min(prices):.2f}\n@{times[min_idx]}', 
            xy=(min_idx, min(prices)), fontsize=8, color='#d32f2f', fontweight='bold', ha='center',
            xytext=(min_idx-8, min(prices)-1.5),
            arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=1.5),
            bbox=dict(boxstyle='round', facecolor='#ffcdd2', alpha=0.9))

max_idx = prices.index(max(prices))
ax1.annotate(f'最高{max(prices):.2f}\n@{times[max_idx]}', 
            xy=(max_idx, max(prices)), fontsize=8, color='#2e7d32', ha='center',
            xytext=(max_idx+2, max(prices)+0.8),
            arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=1),
            bbox=dict(boxstyle='round', facecolor='#c8e6c9', alpha=0.9))

ax1.set_ylabel('价格(元)', fontsize=11)
ax1.set_title('① 分时走势 + 大宗交易价59.05（宁德折价6.49%售出）', fontsize=12, fontweight='bold')
ax1.set_ylim(58.0, 63.5)
ax1.legend(loc='upper left', fontsize=8)
ax1.grid(True, alpha=0.08)
step = max(1, len(data) // 12)
ax1.set_xticks(x[::step])
ax1.set_xticklabels([times[i] for i in range(0, len(times), step)], rotation=30, fontsize=8)

# ---- 2. 量能 + 大单 ----
ax2 = fig.add_subplot(gs[1, :])
ax2_bar = ax2.bar(x, [v/1000 for v in inc_vols], color='#1565c0', alpha=0.6, label='增量(千手)')
ax2_twin = ax2.twinx()
ax2_twin.plot(x, prices, color='#d32f2f', linewidth=1.5, label='价格')

# 标注大单
for i, d in enumerate(data):
    if d['inc_vol'] >= 2500:
        color = '#d32f2f' if d['price'] < data[max(0,i-1)]['price'] else '#2e7d32'
        ax2.scatter(i, d['inc_vol']/1000, s=60, c=color, marker='v' if color=='#d32f2f' else '^', zorder=5)

ax2.set_ylabel('增量成交量(千手)', fontsize=10)
ax2_twin.set_ylabel('价格(元)', fontsize=10)
ax2.set_title('② 量能 + 大单标注 (>2500手) — 0931放量3662手推升至61.66', fontsize=12, fontweight='bold')
ax2.legend(loc='upper left', fontsize=8)
ax2_twin.legend(loc='upper right', fontsize=8)
ax2.grid(True, alpha=0.08, axis='y')
ax2.set_ylim(0, 5)

# ---- 3. 宁德时代减持进度 ----
ax3 = fig.add_subplot(gs[2, 0])
# 减持计划
total_plan = 25300206
sold_concentrated = 2105032  # 竞价
sold_block = 330000  # 大宗
total_sold = sold_concentrated + sold_block
remaining = total_plan - total_sold
pct_sold = total_sold / total_plan * 100
pct_remaining = remaining / total_plan * 100

# 饼图
labels = [f'已售\n{total_sold/10000:.0f}万股\n{pct_sold:.1f}%'] * 1 + [f'剩余\n{remaining/10000:.0f}万股\n{pct_remaining:.1f}%']
sizes = [total_sold, remaining]
colors_red = ['#d32f2f', '#ff9800']
colors_blue = ['#1565c0', '#e3f2fd']

wedges, texts, autotexts = ax3.pie(sizes, labels=labels, autopct='%1.1f%%',
                                   colors=['#d32f2f', '#e3f2fd'], startangle=90,
                                   textprops={'fontsize': 9})
ax3.set_title('③ 宁德时代减持进度\n(计划2530万股, 窗口6/26-9/25)', fontsize=11, fontweight='bold')

# 详细信息
info_text = (
    f"减持计划: {total_plan/10000:.0f}万股\n"
    f"竞价减持: {sold_concentrated/10000:.0f}万股 (6/26)\n"
    f"大宗交易: {sold_block/10000:.0f}万股 (7/2)\n"
    f"已售合计: {total_sold/10000:.0f}万股 ({pct_sold:.1f}%)\n"
    f"剩余额度: {remaining/10000:.0f}万股 ({pct_remaining:.1f}%)\n"
    f"折价率: 6.49%\n"
    f"成交价: 59.05元\n"
    f"预估金额: {block_trade['amount']}亿元"
)
ax3.text(0.5, -0.15, info_text, transform=ax3.transAxes, fontsize=9,
        verticalalignment='top', horizontalalignment='center',
        bbox=dict(boxstyle='round', facecolor='#fff3e0', alpha=0.8),
        family='monospace')

# ---- 4. 大宗交易 vs 市场价 ----
ax4 = fig.add_subplot(gs[2, 1])
# 时间轴
block_dates = ['2026-06-26', '2026-07-02', '2026-07-14']
block_prices = [63.15, 59.05, current_price]
block_labels = ['竞价减持\n6/26', '大宗交易\n7/2', '当前价\n7/14']

x_pos = [0, 1, 2]
colors_bar = ['#d32f2f', '#ff9800', '#1565c0']
bars = ax4.bar(x_pos, block_prices, color=colors_bar, alpha=0.7, edgecolor='black', linewidth=1.5)

for i, (bp, bl) in enumerate(zip(block_prices, block_labels)):
    ax4.text(i, bp + 0.5, f'{bp:.2f}', ha='center', fontsize=10, fontweight='bold')
    ax4.text(i, bp - 1.5, bl, ha='center', fontsize=8)

ax4.set_ylabel('价格(元)', fontsize=11)
ax4.set_title('④ 关键价位对比\n(竞价63.15→大宗59.05→当前60.71)', fontsize=11, fontweight='bold')
ax4.set_xticks([])
ax4.set_ylim(55, 68)
ax4.grid(True, axis='y', alpha=0.1)

# ---- 5. 板块资金流 ----
ax5 = fig.add_subplot(gs[3, 0])
# 电池/储能概念板块
sector_data = [
    ('电子器件', 52.44, 1.20),
    ('电池', 8.5, 0.8),  # 估算
    ('储能', 5.2, 0.6),  # 估算
    ('湖南裕能', 1.5, -1.35),
]

sectors = [s[0] for s in sector_data]
inflows = [s[1] for s in sector_data]
changes = [s[2] for s in sector_data]

x_sec = np.arange(len(sectors))
color_sec = ['#d32f2f' if i > 0 else '#ff9800' for i in range(len(sectors))]
bars = ax5.bar(x_sec, inflows, color=color_sec, alpha=0.7, edgecolor='black', linewidth=1)

for i, (sec, inf, chg) in enumerate(sector_data):
    ax5.text(i, inf + 0.3, f'{inf:+.1f}亿\n({chg:+.2f}%)', ha='center', fontsize=8, fontweight='bold')

ax5.set_ylabel('主力资金净流入(亿元)', fontsize=10)
ax5.set_title('⑤ 板块资金流对比\n(电子器件+52.44亿, 电池+8.5亿)', fontsize=11, fontweight='bold')
ax5.set_xticks(x_sec)
ax5.set_xticklabels(sectors)
ax5.grid(True, alpha=0.1, axis='y')

# ---- 6. 多维度信号面板 ----
ax6 = fig.add_subplot(gs[3, 1])
ax6.axis('off')

signals = [
    ['维度', '信号', '数据', '判断'],
    ['量价', '缩量', '3.42万手/32分钟', '抛压衰竭'],
    ['双底', '60.95-60.97', '差0.02元', '确认中'],
    ['主力', '净流出1548万', 'vs 7/10的3.2亿', '退场'],
    ['大宗', '59.05折价6.49%', '宁德售给机构', '机构接货'],
    ['板块', '电子器件+52亿', '电池+8.5亿', '板块强势'],
    ['技术', 'VWAP 61.27', '现价60.71<VWAP', '弱势'],
    ['减持', '剩余78.5%', '1986万股', '继续施压'],
    ['估值', 'PE 12.1倍', '59元=PE11.3', '估值底'],
]

# 表格
table_data = [[cell for cell in row[1:]] for row in signals]
headers = [row[0] for row in signals]
table = ax6.table(cellText=table_data, rowLabels=headers, colLabels=['维度', '信号', '数据', '判断'],
                  loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2.0)

# 表头加粗
for j in range(4):
    if (0, j) in table._cells:
        table[0, j].set_text_props(fontweight='bold', color='white', fontsize=10)
        table[0, j].set_facecolor('#1a237e')

# 信号列着色
for i in range(len(headers)):
    signal = signals[i+1][1]
    if '缩量' in signal or '确认' in signal or '退场' in signal or '接货' in signal:
        table[i+1, 1].set_facecolor('#e8f5e9')
    elif '弱势' in signal or '施压' in signal:
        table[i+1, 1].set_facecolor('#ffcdd2')
    elif '估值底' in signal:
        table[i+1, 1].set_facecolor('#c8e6c9')

ax6.set_title('⑥ 多维度信号面板', fontsize=11, fontweight='bold', pad=20)

plt.savefig('301358_0714_multidimensional.png', dpi=150, bbox_inches='tight')
print("OK saved")
