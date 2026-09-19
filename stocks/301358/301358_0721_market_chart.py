#!/usr/bin/env python3
"""7/21 大盘+半导体+301358 对比分析图"""
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

fig = plt.figure(figsize=(22, 18))
gs = GridSpec(3, 2, figure=fig, height_ratios=[1.5, 1, 1], hspace=0.35, wspace=0.2,
              left=0.06, right=0.96, top=0.96, bottom=0.04)

# === 1. 板块涨幅对比 ===
ax1 = fig.add_subplot(gs[0, 0])
sectors = ['科创50\n+5.29%', '华虹公司\n+13.43%', '中微公司\n+9.66%', '华峰测控\n+10.60%',
           '寒武纪\n+7.28%', '兆易创新\n+7.24%', '中芯国际\n+6.83%',
           '创业板指\n+3.94%', '宁德时代\n+2.94%', '深证成指\n+2.58%',
           '301358\n+4.17%', '沪深300\n+1.40%', '上证50\n+0.71%', '上证指数\n+0.37%',
           '隆基绿能\n-1.25%']
values = [5.29, 13.43, 9.66, 10.60, 7.28, 7.24, 6.83, 3.94, 2.94, 2.58, 4.17, 1.40, 0.71, 0.37, -1.25]
colors = ['#cc0000' if v > 3 else '#ff6600' if v > 0 else '#00aa00' for v in values]
bars = ax1.barh(range(len(sectors)), values, color=colors, alpha=0.8, height=0.7)
for i, v in enumerate(values):
    ax1.text(v + 0.3, i, f'{v:+.2f}%', va='center', fontsize=10, fontweight='bold')
ax1.set_yticks(range(len(sectors)))
ax1.set_yticklabels(sectors, fontsize=10)
ax1.set_xlabel('涨幅 (%)', fontsize=11)
ax1.set_title('7/21 实时板块涨幅全景 — 半导体霸屏', fontsize=14, fontweight='bold')
ax1.axvline(x=0, color='black', linewidth=0.5)
ax1.axvline(x=3.94, color='#cc0000', linewidth=0.8, linestyle='--', alpha=0.3)
ax1.invert_yaxis()
ax1.grid(True, alpha=0.12, axis='x')

# === 2. 半导体龙头走势 ===
ax2 = fig.add_subplot(gs[0, 1])
stocks = ['华虹公司\n+13.43%', '华峰测控\n+10.60%', '中微公司\n+9.66%', '寒武纪\n+7.28%',
          '兆易创新\n+7.24%', '中芯国际\n+6.83%', '301358\n+4.17%', '宁德时代\n+2.94%']
vals = [13.43, 10.60, 9.66, 7.28, 7.24, 6.83, 4.17, 2.94]
colors2 = ['#cc0000' if v > 7 else '#ff6600' if v > 4 else '#cc8800' for v in vals]
ax2.bar(range(len(stocks)), vals, color=colors2, alpha=0.8, width=0.6)
for i, v in enumerate(vals):
    ax2.text(i, v + 0.3, f'+{v:.2f}%', ha='center', fontsize=10, fontweight='bold')
ax2.set_xticks(range(len(stocks)))
ax2.set_xticklabels(stocks, fontsize=9, rotation=20)
ax2.set_ylabel('涨幅 (%)', fontsize=11)
ax2.set_title('半导体龙头 vs 301358 vs 宁德时代', fontsize=14, fontweight='bold')
ax2.axhline(y=5.29, color='#0066cc', linewidth=1.5, linestyle='--', alpha=0.5, label='科创50 +5.29%')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.12, axis='y')

# === 3. 7月半导体大事件时间线 ===
ax3 = fig.add_subplot(gs[1, :])
events = [
    ('7/2', '寒武纪破万亿市值', '#cc0000'),
    ('7/7', '科创50逆市活跃\n半导体占83.7%权重', '#ff6600'),
    ('7/9', '科创50暴涨8.41%\n今年最大单日涨幅', '#cc0000'),
    ('7/9', '高盛报告:做多中国AI\n从韩国切换到中国', '#0000cc'),
    ('7/14', '拓荆科技创新高\n一年涨400%', '#cc0000'),
    ('7/16', '长鑫科技295亿IPO申购\n虹吸效应资金撤离', '#00aa00'),
    ('7/20', '301358 60±2画框\n主力净买入1.7亿', '#ff6600'),
    ('7/21', '半导体全面爆发\n科创50+5.29%', '#cc0000'),
]
x_pos = np.arange(len(events))
for i, (date, desc, color) in enumerate(events):
    ax3.scatter(i, 0, s=200, color=color, zorder=5, edgecolors='black', linewidth=1)
    y_offset = 0.5 if i % 2 == 0 else -0.5
    ax3.annotate(f'{date}\n{desc}', xy=(i, 0), xytext=(i, y_offset),
                 fontsize=9, ha='center', va='center' if y_offset < 0 else 'bottom',
                 arrowprops=dict(arrowstyle='->', color=color, lw=1.2))
ax3.set_xlim(-0.5, len(events) - 0.5)
ax3.set_ylim(-1.2, 1.2)
ax3.axhline(y=0, color='#888888', linewidth=2)
ax3.set_title('7月半导体大事件时间线 — 申购结束后的资金回流', fontsize=14, fontweight='bold')
ax3.set_yticks([])
ax3.set_xticks(x_pos)
ax3.set_xticklabels([e[0] for e in events], fontsize=11)
ax3.grid(True, alpha=0.08, axis='x')

# === 4. 301358 走势 vs 大盘 ===
ax4 = fig.add_subplot(gs[2, 0])
days = ['7/15', '7/16', '7/17', '7/20', '7/21\n当前']
p301358 = [63.37, 61.24, 59.47, 59.90, 62.40]
sh_idx = [3837.66, 3798.99, 3783.00, 3784.37, 3810.37]
cyb = [3514.52, 3420.75, 3431.47, 3421.99, 3578.85]
kc50 = [1723.50, 1690.33, 1680.21, 1731.12, 1809.60]

x4 = np.arange(len(days))
ax4.plot(x4, p301358, '-o', color='#cc0000', linewidth=2.5, markersize=8, label='301358', zorder=5)
ax4_twin = ax4.twinx()
ax4_twin.plot(x4, kc50, '-s', color='#0066cc', linewidth=2, markersize=7, label='科创50', alpha=0.7)
ax4_twin.plot(x4, cyb, '-^', color='#ff6600', linewidth=2, markersize=7, label='创业板', alpha=0.7)
ax4_twin.plot(x4, sh_idx, '--', color='#888888', linewidth=1.5, markersize=5, label='上证', alpha=0.5)

ax4.set_xticks(x4)
ax4.set_xticklabels(days, fontsize=10)
ax4.set_ylabel('301358 Price', fontsize=11, color='#cc0000')
ax4_twin.set_ylabel('Index', fontsize=11)
ax4.set_title('301358 vs 大盘/科创 — 7/21放量突破跟随科创', fontsize=13, fontweight='bold')
ax4.legend(fontsize=10, loc='upper left')
ax4_twin.legend(fontsize=10, loc='upper right')
ax4.grid(True, alpha=0.1)

# === 5. 半导体上涨三大引擎 ===
ax5 = fig.add_subplot(gs[2, 1])
engines = ['AI算力需求爆发\n(寒武纪破万亿)', '高盛唱多中国AI\n(韩国→中国切换)', '长鑫IPO虹吸结束\n(资金回流半导体)',
           '半导体7月涨价\n(TI/英飞凌/意法调价)', '国产替代加速\n(产能将超韩国)', '科创50权重83.7%\n半导体=科创50']
weights = [30, 25, 20, 10, 10, 5]
colors5 = ['#cc0000', '#ff6600', '#0066cc', '#cc8800', '#990099', '#888888']
wedges, texts, autotexts = ax5.pie(weights, labels=engines, autopct='%1d%%',
                                    colors=colors5, startangle=90,
                                    textprops={'fontsize': 9})
for t in autotexts:
    t.set_fontsize(11)
    t.set_fontweight('bold')
ax5.set_title('半导体暴涨六大引擎（权重占比）', fontsize=13, fontweight='bold')

plt.savefig('/data/hermes/workspace/301358_0721_market.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_0721_market.png')
