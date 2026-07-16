#!/usr/bin/env python3
"""301358 减持进度+大宗交易+分时对比图"""
import json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch

fm.fontManager.addfont('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')
plt.rcParams['font.family'] = 'WenQuanYi Zen Hei'
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(2, 2, figsize=(22, 14))
fig.subplots_adjust(hspace=0.3, wspace=0.25, top=0.93, bottom=0.06, left=0.07, right=0.95)
fig.suptitle('301358 湖南裕能 · 7/10 主力意图深度拆解（分时做图形 + 大宗交易接货 + 减持进度）',
             fontsize=16, fontweight='bold')

# ===== 图1（左上）：宁德时代减持进度 =====
ax1 = axes[0, 0]
ax1.set_title('宁德时代减持进度（窗口期6/26-9/25）', fontsize=12, fontweight='bold')

# 时间轴
days_total = 92  # 3个月窗口
days_passed = 14  # 6/26到7/10
progress_plan = 8.3  # 计划完成百分比
progress_time = 15.2  # 时间已过百分比

categories = ['时间进度', '减持进度']
values = [progress_time, progress_plan]
colors_bar = ['#ff9800', '#d32f2f']
bars = ax1.barh(categories, values, color=colors_bar, height=0.5)
ax1.set_xlim(0, 100)
ax1.set_xlabel('百分比(%)', fontsize=10)

# 标注
for bar, val in zip(bars, values):
    ax1.text(val + 1, bar.get_y() + bar.get_height()/2,
             f'{val:.1f}%', va='center', fontsize=11, fontweight='bold')

ax1.axvline(x=progress_time, color='#ff9800', linewidth=0.8, linestyle='--', alpha=0.5)
ax1.axvline(x=progress_plan, color='#d32f2f', linewidth=0.8, linestyle='--', alpha=0.5)

# 文字框
text1 = (
    f'减持计划: 不超过2530万股(3%)\n'
    f'已减持: 210.5万股(0.25%)\n'
    f'剩余: 2320万股(2.75%)\n'
    f'持股: 5774.11万股(6.85%)\n'
    f'近3月7笔大宗仅52.9万股\n'
    f'大宗仅占减持计划的1.14%\n'
    f'妃5年浮盈超23倍\n'
    f'成本极低，任何价位都是暴利'
)
ax1.text(0.98, 0.95, text1, transform=ax1.transAxes, fontsize=8,
        va='top', ha='right', family='monospace',
        bbox=dict(boxstyle='round', facecolor='#fff9c4', alpha=0.9))

ax1.text(50, -0.6, '时间已过15.2% 但减持仅完成8.3%\n进度落后 = 后续需加速 = 卖压持续',
         fontsize=9, ha='center', color='#d32f2f', fontweight='bold')

# ===== 图2（右上）：7/10 大宗交易 vs 集中竞价 =====
ax2 = axes[0, 1]
ax2.set_title('7/10 双轨交易：集中竞价(做图形) vs 大宗交易(真接货)', fontsize=12, fontweight='bold')

# 两个市场对比
labels = ['集中竞价\n(二级市场)', '大宗交易\n(场外)']
prices = [63.15, 59.05]
volumes = [20.42, 0.226]  # 万股
amounts = [13.0, 0.1335]  # 亿

x_pos = np.arange(len(labels))
width = 0.3

# 价格对比
bars1 = ax2.bar(x_pos - width/2, prices, width, color=['#1565c0', '#2e7d32'], label='成交价')
ax2.set_ylabel('价格(元)', fontsize=10, color='#1565c0')
ax2.set_ylim(0, 80)
for bar, p in zip(bars1, prices):
    ax2.text(bar.get_x() + bar.get_width()/2, p + 1, f'{p:.2f}元',
             ha='center', fontsize=10, fontweight='bold')

# 折价标注
ax2.annotate('', xy=(1-width/2, 59.05), xytext=(1-width/2, 63.15),
            arrowprops=dict(arrowstyle='<->', color='#d32f2f', lw=2))
ax2.text(1, 61, '折价6.49%\n便宜4.10元/股', fontsize=9, color='#d32f2f',
        fontweight='bold', ha='center',
        bbox=dict(boxstyle='round', facecolor='#ffcdd2', alpha=0.8))

# 成交量对比 (次轴)
ax2r = ax2.twinx()
bars2 = ax2r.bar(x_pos + width/2, [204200, 2260], width, color=['#ff9800', '#4caf50'], alpha=0.6, label='成交量(万股)')
ax2r.set_ylabel('成交量(万股)', fontsize=10, color='#ff9800')
for bar, v in zip(bars2, [204.2, 22.6]):
    ax2r.text(bar.get_x() + bar.get_width()/2, v + 5000, f'{v:.1f}万股',
             ha='center', fontsize=9, color='#333')

ax2.set_xticks(x_pos)
ax2.set_xticklabels(labels, fontsize=10)
ax2.legend(loc='upper left', fontsize=8)
ax2r.legend(loc='upper right', fontsize=8)

text2 = (
    '关键发现：\n'
    '1. 集中竞价: 收盘63.15=最低\n'
    '   尾盘做图形(光脚阴线)\n'
    '2. 大宗交易: 均价59.05\n'
    '   机构折价6.49%接货\n'
    '3. 大宗价59.05 姬 Fib61.8%=60.51\n'
    '   机构接货价已在Fib支撑附近\n'
    '4. 买方=机构 不是散户/游资'
)
ax2.text(0.02, 0.95, text2, transform=ax2.transAxes, fontsize=8,
        va='top', ha='left', family='monospace',
        bbox=dict(boxstyle='round', facecolor='#c8e6c9', alpha=0.9))

# ===== 图3（左下）：分时图+尾盘做图形+大宗交易价 =====
ax3 = axes[1, 0]
with open('/data/hermes/workspace/301358_0710_minutes.json') as f:
    minutes = json.load(f)
minutes = [m for m in minutes if m.get('vol', 0) > 0 or m['time'] <= '1500']

x = np.arange(len(minutes))
prices_min = [m['price'] for m in minutes]

ax3.set_title('7/10 分时走势 + 尾盘做图形 + 大宗交易价位', fontsize=12, fontweight='bold')
ax3.axhline(y=65.80, color='#ff9800', linewidth=0.8, linestyle='--', alpha=0.5, label='昨收65.80')
ax3.fill_between(x, 65.80, prices_min, where=[p >= 65.80 for p in prices_min],
                 color='#d32f2f', alpha=0.06)
ax3.fill_between(x, 65.80, prices_min, where=[p < 65.80 for p in prices_min],
                 color='#2e7d32', alpha=0.06)
ax3.plot(x, prices_min, color='#1565c0', linewidth=1.5, label='分时价格')

# 大宗交易价位线
ax3.axhline(y=59.05, color='#2e7d32', linewidth=2, linestyle='-', alpha=0.7)
ax3.text(len(minutes)-5, 59.05, ' 大宗价59.05\n (机构接货价)', fontsize=8, color='#2e7d32',
        fontweight='bold', va='center',
        bbox=dict(boxstyle='round', facecolor='#c8e6c9', alpha=0.8))

# 尾盘做图形
tail_start = next(i for i, m in enumerate(minutes) if m['time'] == '1455')
ax3.axvspan(tail_start, len(minutes)-1, alpha=0.1, color='#d32f2f')
ax3.annotate('尾盘做图形\n63.35姬3.15\n0.31万手=1970万', xy=((tail_start+len(minutes)-1)/2, 63.8),
            fontsize=8, color='#d32f2f', ha='center', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#ffcdd2', alpha=0.9))

# 收盘价
ax3.axhline(y=63.15, color='#d32f2f', linewidth=1, linestyle=':', alpha=0.5)
ax3.text(0, 63.15, ' 收盘63.15(=最低)', fontsize=8, color='#d32f2f', va='bottom',
        fontweight='bold')

step = max(1, len(minutes) // 10)
ax3.set_xticks(x[::step])
ax3.set_xticklabels([minutes[i]['time'] for i in range(0, len(minutes), step)], rotation=30, fontsize=8)
ax3.set_ylabel('价格(元)', fontsize=10)
ax3.set_xlabel('时间', fontsize=10)
ax3.legend(loc='upper right', fontsize=9)
ax3.grid(True, alpha=0.1)

# ===== 图4（右下）：主力意图全景图 =====
ax4 = axes[1, 1]
ax4.set_title('主力意图全景：双轨操作模式', fontsize=12, fontweight='bold')
ax4.axis('off')

table_data = [
    ['操作维度', '集中竞价(台前)', '大宗交易(幕后)'],
    ['目的', '做K线恐吓散户', '低价接减持筹码'],
    ['价格', '收盘63.15(最低)', '59.05(折价6.49%)'],
    ['成交量', '20.4万手', '0.23万手(22.6万股)'],
    ['成交额', '13.0亿', '0.13亿'],
    ['买方', '散户(恐慌割肉)', '机构(折价接货)'],
    ['卖方', '主力(分批出货)', '宁德/津晟(大宗减持)'],
    ['效果', '光脚阴线+破BOLL', '机构在低位建仓'],
    ['信号', '恐吓散户卖出', '机构看好低位'],
]

table = ax4.table(cellText=table_data, cellLoc='center', loc='center',
                 colWidths=[0.2, 0.35, 0.35])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2.0)

# 表头颜色
for j in range(3):
    table[0, j].set_facecolor('#37474f')
    table[0, j].set_text_props(color='white', fontweight='bold')
# 数据行交替色
for i in range(1, len(table_data)):
    for j in range(3):
        if j == 0:
            table[i, j].set_facecolor('#eceff1')
        elif j == 1:
            table[i, j].set_facecolor('#ffebee' if i in [2,8] else '#fff')
        else:
            table[i, j].set_facecolor('#e8f5e9' if i in [2,8] else '#fff')

plt.savefig('/data/hermes/workspace/301358_0710_full picture.png', dpi=150, bbox_inches='tight')
print("full picture saved")
