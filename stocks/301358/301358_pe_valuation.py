#!/usr/bin/env python3
"""301358 PE估值分析图"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.gridspec import GridSpec

font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
fm.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'WenQuanYi Zen Hei'
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(24, 20))
gs = GridSpec(2, 2, height_ratios=[2, 2], hspace=0.3, wspace=0.25,
              left=0.06, right=0.97, top=0.95, bottom=0.04)

# === 1. PE多口径对比 ===
ax1 = fig.add_subplot(gs[0, 0])
pe_labels = ['PE(2025静态)\n12.77亿', 'PE(TTM)\n25.39亿', 'PE(2026E机构)\n43.87亿',
             'PE(2026E乐观)\n54.24亿', 'PE(2026E中性)\n48.82亿', 'PE(2026E保守)\n43.39亿']
pe_values = [36.3, 18.2, 10.6, 8.5, 9.5, 10.7]
colors_pe = ['#cc0000', '#ff6600', '#00aa00', '#00cc00', '#00aa00', '#00aa00']
bars = ax1.barh(pe_labels, pe_values, color=colors_pe, alpha=0.8, height=0.6)
for bar, val in zip(bars, pe_values):
    ax1.text(val + 0.3, bar.get_y() + bar.get_height()/2, f'{val:.1f}x',
             va='center', fontsize=13, fontweight='bold')

ax1.axvline(x=15, color='#ff6600', linestyle='--', linewidth=2, label='行业中枢 ~15x')
ax1.axvline(x=10, color='#0066cc', linestyle=':', linewidth=2, label='合理估值下限 ~10x')
ax1.set_xlabel('PE (倍)', fontsize=12)
ax1.set_title('PE多口径对比: 静态36x → TTM 18x → 2026E 10-11x\n当前股价对应的是"2026年高增长预期"的PE', fontsize=13, fontweight='bold')
ax1.legend(fontsize=10, loc='lower right')
ax1.set_xlim([0, 42])
ax1.grid(True, alpha=0.15, axis='x')

# === 2. 季度净利润趋势 ===
ax2 = fig.add_subplot(gs[0, 1])
quarters = ['2025Q1', '2025Q2', '2025Q3', '2025Q4', '2026Q1', '2026Q2E\n(乐观)', '2026Q2E\n(中性)', '2026Q2E\n(保守)']
profits = [0.94, 2.11, 3.40, 6.32, 13.56, 13.56, 10.85, 8.14]
colors_q = ['#cccccc', '#cccccc', '#cccccc', '#999999', '#cc0000', '#ff6600', '#ff6600', '#ff6600']
bars2 = ax2.bar(quarters, profits, color=colors_q, alpha=0.8, width=0.6)
for bar, val in zip(bars2, profits):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 0.3, f'{val:.2f}亿',
             ha='center', fontsize=11, fontweight='bold')

ax2.annotate('Q1同比+1343%!\n单季超2025全年', xy=(4, 13.56), xytext=(2.5, 15),
             fontsize=12, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=2))

ax2.set_ylabel('归母净利润 (亿)', fontsize=12)
ax2.set_title('季度归母净利润: 2025Q1→Q4加速, 2026Q1单季13.56亿=2025全年106%', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.1, axis='y')
ax2.set_ylim([0, 18])

# === 3. 当前股价 vs 合理估值区间 ===
ax3 = fig.add_subplot(gs[1, 0])

# 不同PE下对应的合理价格
pe_range = np.arange(5, 30, 0.5)
eps_2026_optimistic = 7.17  # 乐观EPS
eps_2026_agency = 5.20     # 机构EPS
eps_2026_conservative = 5.73  # 保守EPS
eps_ttm = 3.35
eps_2025 = 1.69

ax3.plot(pe_range, pe_range * eps_2026_optimistic, '-', color='#00cc00', linewidth=2.5, label=f'乐观EPS=7.17 (全年54.24亿)')
ax3.plot(pe_range, pe_range * eps_2026_agency, '-', color='#0066cc', linewidth=2.5, label=f'机构EPS=5.20 (全年43.87亿)')
ax3.plot(pe_range, pe_range * eps_2026_conservative, '-', color='#ff6600', linewidth=2.5, label=f'保守EPS=5.73 (全年43.39亿)')

ax3.axhline(y=60.58, color='#cc0000', linewidth=3, linestyle='-', label=f'当前价 60.58')
ax3.axhline(y=40.8, color='#990099', linewidth=2, linestyle='--', label=f'机构目标均价 40.8')

# 标注当前价在各EPS下对应的PE
for eps, label, color in [(eps_2026_optimistic, '乐观', '#00cc00'), (eps_2026_agency, '机构', '#0066cc'), (eps_2026_conservative, '保守', '#ff6600')]:
    pe_at_price = 60.58 / eps
    ax3.plot(pe_at_price, 60.58, 'o', color=color, markersize=10, zorder=5)
    ax3.annotate(f'{label}: PE={pe_at_price:.1f}x', xy=(pe_at_price, 60.58),
                 xytext=(pe_at_price+1, 58), fontsize=10, color=color, fontweight='bold')

ax3.fill_between(pe_range, pe_range * eps_2026_conservative, pe_range * eps_2026_optimistic,
                 color='#00aa00', alpha=0.08, label='2026E合理价格区间')

ax3.set_xlabel('PE (倍)', fontsize=12)
ax3.set_ylabel('股价 (元)', fontsize=12)
ax3.set_title('当前价60.58 vs 不同PE×EPS的合理价格\n当前价隐含PE=8.5x(乐观)~11.6x(机构)', fontsize=13, fontweight='bold')
ax3.legend(fontsize=9, loc='upper left')
ax3.grid(True, alpha=0.1)
ax3.set_xlim([5, 25])
ax3.set_ylim([20, 100])

# === 4. 估值判定总表 ===
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('off')
ax4.set_xlim([0, 10])
ax4.set_ylim([0, 10])

table_data = [
    ['估值口径', '净利(亿)', 'EPS(元)', 'PE(倍)', '判定'],
    ['2025静态', '12.77', '1.69', '36.3x', '❌ 高估'],
    ['TTM(年化)', '25.39', '3.35', '18.2x', '⚠️ 偏高'],
    ['2026E机构', '43.87', '5.20', '10.6x', '✅ 合理偏低'],
    ['2026E乐观', '54.24', '7.17', '8.5x', '✅ 低估'],
    ['2026E保守', '43.39', '5.73', '10.7x', '✅ 合理'],
    ['2026E悲观', '40.68', '5.37', '11.3x', '✅ 合理偏高'],
    ['', '', '', '', ''],
    ['机构目标均价', '—', '—', '40.8元', '⬇48%'],
    ['当前溢价vs目标', '—', '—', '+48.5%', '⚠️ 偏高'],
]

table = ax4.table(cellText=table_data[1:], colLabels=table_data[0],
                  cellLoc='center', loc='center', colWidths=[0.16, 0.13, 0.13, 0.13, 0.18])
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1.05, 2.0)

for j in range(5):
    table[0, j].set_facecolor('#333333')
    table[0, j].set_text_props(color='white', fontweight='bold')
for i in range(1, 7):
    table[i, 3].set_facecolor('#ffcccc')
table[3, 3].set_facecolor('#ccffcc')  # 机构预测行
table[8, 3].set_facecolor('#ffcccc')
table[9, 3].set_facecolor('#ffcccc')

ax4.set_title('估值综合判定: 当前60.58元\n对应2026E PE 10-11x 处于合理区间\n但vs机构目标价40.8仍有48%下行风险', 
              fontsize=13, fontweight='bold', pad=15)

plt.savefig('/data/hermes/workspace/301358_pe_valuation.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_pe_valuation.png')
