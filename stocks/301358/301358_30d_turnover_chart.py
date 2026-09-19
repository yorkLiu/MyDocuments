#!/usr/bin/env python3
"""301358 30日换手率与成交量分析图"""
import json, urllib.request, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.gridspec import GridSpec

font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
fm.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'WenQuanYi Zen Hei'
plt.rcParams['axes.unicode_minus'] = False

# 拉30日K线
url = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sz301358,day,,,30,qfq"
req = urllib.request.Request(url)
with urllib.request.urlopen(req, timeout=10) as resp:
    k_data = json.loads(resp.read().decode())
klines = k_data['data']['sz301358']['qfqday']

float_shares = 3.4e8
dates = []
closes = []
vols = []
turnovers = []
amounts = []
prev_close = None
for k in klines:
    d = k[0]
    o, c, h, l = float(k[1]), float(k[2]), float(k[3]), float(k[4])
    vol = float(k[5])  # 手
    vol_shares = vol * 100
    turnover = vol_shares / float_shares * 100
    if prev_close:
        chg = (c - prev_close) / prev_close * 100
    else:
        chg = 0
    prev_close = c
    dates.append(d[5:])  # MM-DD
    closes.append(c)
    vols.append(vol / 10000)  # 万手
    turnovers.append(turnover)
    amounts.append(vol * c * 100 / 1e8)
    chgs = chgs if 'chgs' in dir() else []
    chgs.append(chg)

x = np.arange(len(dates))
today_idx = len(dates) - 1

fig = plt.figure(figsize=(24, 20))
gs = GridSpec(3, 2, height_ratios=[2, 2, 1], hspace=0.35, wspace=0.15,
              left=0.06, right=0.97, top=0.96, bottom=0.03)

# === 1. 30日成交量柱状图 ===
ax1 = fig.add_subplot(gs[0, :])
colors1 = ['#cc0000' if c < 0 else '#00aa00' for c in chgs]
bars1 = ax1.bar(x, vols, color=colors1, alpha=0.8, width=0.7)
# 今日高亮
bars1[today_idx].set_edgecolor('black')
bars1[today_idx].set_linewidth(3)

# 均线
for window, color, label in [(5, '#ff6600', '5日均量'), (10, '#0066cc', '10日均量'), (30, '#990099', '30日均量')]:
    ma = np.convolve(vols, np.ones(window)/window, mode='valid')
    ma_x = np.arange(window-1, len(vols))
    ax1.plot(ma_x, ma, '-', color=color, linewidth=2, label=label)

# 标注今日
ax1.annotate(f'7/22 今日\n{vols[today_idx]:.0f}万手\n换手{turnovers[today_idx]:.2f}%\n30日最低!',
             xy=(today_idx, vols[today_idx]), xytext=(today_idx-6, vols[today_idx]+5),
             fontsize=12, color='black', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='black', lw=2))

# 标注最大量日
max_idx = vols.index(max(vols))
ax1.annotate(f'{dates[max_idx]}  最大量\n{vols[max_idx]:.0f}万手 换手{turnovers[max_idx]:.2f}%',
             xy=(max_idx, vols[max_idx]), xytext=(max_idx+1, vols[max_idx]+3),
             fontsize=11, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=2))

# 标注7/15拉升日
if len(dates) > 26:
    idx_715 = 24  # approx
    ax1.annotate(f'7/15 拉升日\n{vols[idx_715]:.0f}万手 换手{turnovers[idx_715]:.2f}%',
                 xy=(idx_715, vols[idx_715]), xytext=(idx_715-4, vols[idx_715]+5),
                 fontsize=10, color='#00aa00', fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color='#00aa00', lw=1.5))

ax1.set_xticks(x)
ax1.set_xticklabels(dates, fontsize=9, rotation=40)
ax1.set_ylabel('Volume (万手)', fontsize=12)
ax1.set_title(f'30日成交量: 今日15万手 = 30日均量25万手的61% = 30日最低水平', fontsize=14, fontweight='bold')
ax1.legend(fontsize=11, loc='upper right')
ax1.axhline(y=sum(vols)/30, color='#990099', linewidth=1, linestyle='--', alpha=0.3)
ax1.grid(True, alpha=0.1, axis='y')
ax1.set_ylim([0, max(vols)*1.2])

# === 2. 30日换手率折线图 ===
ax2 = fig.add_subplot(gs[1, :])
ax2.plot(x, turnovers, '-o', color='#cc6600', linewidth=2, markersize=6, zorder=5)
ax2.fill_between(x, turnovers, 0, color='#ff9966', alpha=0.15)

# 均线
for window, color, label in [(5, '#ff6600', '5日均'), (10, '#0066cc', '10日均'), (30, '#990099', '30日均')]:
    ma = np.convolve(turnovers, np.ones(window)/window, mode='valid')
    ma_x = np.arange(window-1, len(turnovers))
    ax2.plot(ma_x, ma, '-', color=color, linewidth=2, label=label)

# 今日标注
ax2.plot(today_idx, turnovers[today_idx], 'o', markersize=15, color='black', zorder=10)
ax2.annotate(f'今日 {turnovers[today_idx]:.2f}%\n30日最低!\n(7/14并列最低{turnovers[today_idx-8]:.2f}%)',
             xy=(today_idx, turnovers[today_idx]), xytext=(today_idx-8, turnovers[today_idx]+1.5),
             fontsize=12, color='black', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='black', lw=2))

# 最低换手日
min_idx = turnovers.index(min(turnovers))
if min_idx != today_idx:
    ax2.annotate(f'{dates[min_idx]} 最低{turnovers[min_idx]:.2f}%',
                 xy=(min_idx, turnovers[min_idx]), xytext=(min_idx-3, turnovers[min_idx]+1),
                 fontsize=10, color='#cc0000', fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))

# 异常高换手日
max_t_idx = turnovers.index(max(turnovers))
ax2.annotate(f'{dates[max_t_idx]} 最高{turnovers[max_t_idx]:.2f}%\n(6/22单日+12.85%暴涨日)',
             xy=(max_t_idx, turnovers[max_t_idx]), xytext=(max_t_idx+1, turnovers[max_t_idx]-2),
             fontsize=11, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))

ax2.set_xticks(x)
ax2.set_xticklabels(dates, fontsize=9, rotation=40)
ax2.set_ylabel('Turnover Rate (%)', fontsize=12)
ax2.set_title(f'30日换手率: 今日4.41% vs 30日均7.22% = 仅在均值的61%水平', fontsize=14, fontweight='bold')
ax2.legend(fontsize=11, loc='upper right')
ax2.grid(True, alpha=0.1, axis='y')

# 分三阶段背景
ax2.axvspan(0, 12, color='#00aa00', alpha=0.05)  # 高位区
ax2.axvspan(12, 18, color='#ff6600', alpha=0.05)  # 下跌区
ax2.axvspan(18, len(x)-1, color='#cc0000', alpha=0.05)  # 底部横盘区
ax2.text(6, max(turnovers)*0.95, '高位放量区\n(6/10-6/24)', fontsize=10, ha='center', color='#00aa00')
ax2.text(15, max(turnovers)*0.95, '缩量下跌\n(6/26-7/09)', fontsize=10, ha='center', color='#ff6600')
ax2.text(24, max(turnovers)*0.95, '底部缩量横盘\n(7/13-7/22)', fontsize=10, ha='center', color='#cc0000')

# === 3. 收盘价叠加成交量 ===
ax3 = fig.add_subplot(gs[2, 0])
ax3b = ax3.twinx()
colors3 = ['#cc0000' if c < 0 else '#00aa00' for c in chgs]
ax3b.bar(x, vols, color=colors3, alpha=0.3, width=0.7)
ax3.plot(x, closes, '-o', color='#cc0000', linewidth=2.5, markersize=5, zorder=5)
ax3.set_xticks(x)
ax3.set_xticklabels(dates, fontsize=8, rotation=40)
ax3.set_ylabel('Close', fontsize=11, color='#cc0000')
ax3b.set_ylabel('Volume (万手)', fontsize=11)
ax3.set_title('价格+量: 88→58下跌中量缩价跌，底部缩量横盘', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.1)

# 标注关键价位
ax3.axhline(y=60, color='#666666', linewidth=1, linestyle=':', alpha=0.5)
ax3.text(len(x)-1, 60, '60', fontsize=9, color='#666666')
ax3.axhline(y=62, color='#666666', linewidth=1, linestyle=':', alpha=0.5)
ax3.text(len(x)-1, 62, '62', fontsize=9, color='#666666')
ax3.axhline(y=85.86, color='#ff6600', linewidth=1, linestyle=':', alpha=0.3)
ax3.text(7, 85.86, '6/22高峰85.86', fontsize=9, color='#ff6600')

# === 4. 30日数据表 ===
ax4 = fig.add_subplot(gs[2, 1])
ax4.axis('off')
ax4.set_xlim([0, 10])
ax4.set_ylim([0, 10])

table_data = [
    ['指标', '今日7/22', '5日均', '10日均', '30日均', '30日最大', '30日最小'],
    ['成交量(万手)', f'{vols[-1]:.0f}', f'{sum(vols[-5:])/5:.0f}', f'{sum(vols[-10:])/10:.0f}', f'{sum(vols)/30:.0f}', f'{max(vols):.0f}', f'{min(vols):.0f}'],
    ['换手率(%)', f'{turnovers[-1]:.2f}', f'{sum(turnovers[-5:])/5:.2f}', f'{sum(turnovers[-10:])/10:.2f}', f'{sum(turnovers)/30:.2f}', f'{max(turnovers):.2f}', f'{min(turnovers):.2f}'],
    ['成交额(亿)', f'{amounts[-1]:.2f}', f'{sum(amounts[-5:])/5:.2f}', f'{sum(amounts[-10:])/10:.2f}', f'{sum(amounts)/30:.2f}', f'{max(amounts):.2f}', f'{min(amounts):.2f}'],
    ['今日/均值比', f'{vols[-1]/(sum(vols)/30)*100:.0f}%', '-', '-', '100%', f'{max(vols)/(sum(vols)/30)*100:.0f}%', f'{min(vols)/(sum(vols)/30)*100:.0f}%'],
]

table = ax4.table(cellText=table_data[1:], colLabels=table_data[0],
                  cellLoc='center', loc='center', colWidths=[0.15, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.1, 2.2)

for j in range(7):
    table[0, j].set_facecolor('#333333')
    table[0, j].set_text_props(color='white', fontweight='bold')
for i in range(1, 5):
    for j in range(7):
        if i == 1:  # 成交量行
            if j == 1: table[i, j].set_facecolor('#ffcccc')
        if i == 2:  # 换手率行
            if j == 1: table[i, j].set_facecolor('#ffcccc')

ax4.set_title('30日量能统计对比 — 今日处于30日最低水平', fontsize=12, fontweight='bold', pad=20)

plt.savefig('/data/hermes/workspace/301358_30d_turnover.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_30d_turnover.png')
