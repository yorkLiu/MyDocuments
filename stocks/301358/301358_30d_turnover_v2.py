#!/usr/bin/env python3
"""301358 30日换手率与成交量分析图（修正版：流通股本7.69亿）"""
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

url = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sz301358,day,,,30,qfq"
req = urllib.request.Request(url)
with urllib.request.urlopen(req, timeout=10) as resp:
    k_data = json.loads(resp.read().decode())
klines = k_data['data']['sz301358']['qfqday']

float_shares = 7.69e8  # 修正：流通股本7.69亿股
dates = []
closes = []
vols = []
turnovers = []
amounts = []
chgs = []
prev_close = None
for k in klines:
    d = k[0]
    c = float(k[2])
    vol = float(k[5])  # 手
    vol_shares = vol * 100
    turnover = vol_shares / float_shares * 100
    if prev_close:
        chg = (c - prev_close) / prev_close * 100
    else:
        chg = 0
    prev_close = c
    dates.append(d[5:])
    closes.append(c)
    vols.append(vol / 10000)
    turnovers.append(turnover)
    amounts.append(vol * c * 100 / 1e8)
    chgs.append(chg)

x = np.arange(len(dates))
today_idx = len(dates) - 1
avg_30 = sum(turnovers)/30
avg_vol_30 = sum(vols)/30
avg_amt_30 = sum(amounts)/30

fig = plt.figure(figsize=(24, 20))
gs = GridSpec(3, 2, height_ratios=[2, 2, 1], hspace=0.35, wspace=0.15,
              left=0.06, right=0.97, top=0.96, bottom=0.03)

# === 1. 30日成交量柱状图 ===
ax1 = fig.add_subplot(gs[0, :])
colors1 = ['#cc0000' if c < 0 else '#00aa00' for c in chgs]
bars1 = ax1.bar(x, vols, color=colors1, alpha=0.8, width=0.7)
bars1[today_idx].set_edgecolor('black')
bars1[today_idx].set_linewidth(3)

for window, color, label in [(5, '#ff6600', '5日均量'), (10, '#0066cc', '10日均量'), (30, '#990099', '30日均量')]:
    ma = np.convolve(vols, np.ones(window)/window, mode='valid')
    ma_x = np.arange(window-1, len(vols))
    ax1.plot(ma_x, ma, '-', color=color, linewidth=2, label=label)

ax1.annotate(f'7/22 今日\n{vols[today_idx]:.0f}万手\n换手{turnovers[today_idx]:.2f}%',
             xy=(today_idx, vols[today_idx]), xytext=(today_idx-6, vols[today_idx]+6),
             fontsize=12, color='black', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='black', lw=2))

max_idx = vols.index(max(vols))
ax1.annotate(f'{dates[max_idx]} 最大量\n{vols[max_idx]:.0f}万手 换手{turnovers[max_idx]:.2f}%',
             xy=(max_idx, vols[max_idx]), xytext=(max_idx+1, vols[max_idx]+3),
             fontsize=11, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=2))

ax1.set_xticks(x)
ax1.set_xticklabels(dates, fontsize=8, rotation=45)
ax1.set_ylabel('Volume (万手)', fontsize=12)
ax1.set_title(f'30日成交量: 今日{vols[today_idx]:.0f}万手 = 30日均量{avg_vol_30:.0f}万手的{vols[today_idx]/avg_vol_30*100:.0f}%', fontsize=14, fontweight='bold')
ax1.legend(fontsize=11, loc='upper right')
ax1.axhline(y=avg_vol_30, color='#990099', linewidth=1, linestyle='--', alpha=0.3)
ax1.grid(True, alpha=0.1, axis='y')
ax1.set_ylim([0, max(vols)*1.25])

# === 2. 30日换手率折线图 ===
ax2 = fig.add_subplot(gs[1, :])
ax2.plot(x, turnovers, '-o', color='#cc6600', linewidth=2, markersize=6, zorder=5)
ax2.fill_between(x, turnovers, 0, color='#ff9966', alpha=0.15)

for window, color, label in [(5, '#ff6600', '5日均'), (10, '#0066cc', '10日均'), (30, '#990099', '30日均')]:
    ma = np.convolve(turnovers, np.ones(window)/window, mode='valid')
    ma_x = np.arange(window-1, len(turnovers))
    ax2.plot(ma_x, ma, '-', color=color, linewidth=2, label=label)

ax2.plot(today_idx, turnovers[today_idx], 'o', markersize=15, color='black', zorder=10)
ax2.annotate(f'今日 {turnovers[today_idx]:.2f}%\n30日均{avg_30:.2f}%的{turnovers[today_idx]/avg_30*100:.0f}%',
             xy=(today_idx, turnovers[today_idx]), xytext=(today_idx-8, turnovers[today_idx]+0.8),
             fontsize=12, color='black', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='black', lw=2))

min_idx = turnovers.index(min(turnovers))
ax2.annotate(f'{dates[min_idx]} 30日最低{turnovers[min_idx]:.2f}%',
             xy=(min_idx, turnovers[min_idx]), xytext=(min_idx-4, turnovers[min_idx]+1.2),
             fontsize=11, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))

max_t_idx = turnovers.index(max(turnovers))
ax2.annotate(f'{dates[max_t_idx]} 最高{turnovers[max_t_idx]:.2f}%\n(单日暴涨+12.85%)',
             xy=(max_t_idx, turnovers[max_t_idx]), xytext=(max_t_idx+1, turnovers[max_t_idx]-1),
             fontsize=11, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))

ax2.set_xticks(x)
ax2.set_xticklabels(dates, fontsize=8, rotation=45)
ax2.set_ylabel('Turnover Rate (%)', fontsize=12)
ax2.set_title(f'30日换手率: 今日2.20% vs 30日均3.29% = 仅在均值的67%水平（但非30日最低）', fontsize=14, fontweight='bold')
ax2.legend(fontsize=11, loc='upper right')
ax2.grid(True, alpha=0.1, axis='y')

ax2.axvspan(0, 12, color='#00aa00', alpha=0.05)
ax2.axvspan(12, 18, color='#ff6600', alpha=0.05)
ax2.axvspan(18, len(x)-1, color='#cc0000', alpha=0.05)
ax2.text(6, max(turnovers)*0.95, '高位放量区\n(6/9-6/24)', fontsize=10, ha='center', color='#00aa00')
ax2.text(15, max(turnovers)*0.95, '缩量下跌\n(6/26-7/09)', fontsize=10, ha='center', color='#ff6600')
ax2.text(23, max(turnovers)*0.95, '底部缩量横盘\n(7/10-7/22)', fontsize=10, ha='center', color='#cc0000')

# === 3. 收盘价叠加成交量 ===
ax3 = fig.add_subplot(gs[2, 0])
ax3b = ax3.twinx()
colors3 = ['#cc0000' if c < 0 else '#00aa00' for c in chgs]
ax3b.bar(x, vols, color=colors3, alpha=0.3, width=0.7)
ax3.plot(x, closes, '-o', color='#cc0000', linewidth=2.5, markersize=5, zorder=5)
ax3.set_xticks(x)
ax3.set_xticklabels(dates, fontsize=7, rotation=45)
ax3.set_ylabel('Close', fontsize=11, color='#cc0000')
ax3b.set_ylabel('Volume (万手)', fontsize=11)
ax3.set_title('价格+量: 85→60下跌中量缩价跌, 底部缩量横盘', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.1)
ax3.axhline(y=60, color='#666666', linewidth=1, linestyle=':', alpha=0.5)

# === 4. 30日数据表 ===
ax4 = fig.add_subplot(gs[2, 1])
ax4.axis('off')
ax4.set_xlim([0, 10])
ax4.set_ylim([0, 10])

table_data = [
    ['指标', '今日7/22', '5日均', '10日均', '30日均', '30日最大', '30日最小'],
    ['成交量(万手)', f'{vols[-1]:.0f}', f'{sum(vols[-5:])/5:.0f}', f'{sum(vols[-10:])/10:.0f}', f'{avg_vol_30:.0f}', f'{max(vols):.0f}', f'{min(vols):.0f}'],
    ['换手率(%)', f'{turnovers[-1]:.2f}', f'{sum(turnovers[-5:])/5:.2f}', f'{sum(turnovers[-10:])/10:.2f}', f'{avg_30:.2f}', f'{max(turnovers):.2f}', f'{min(turnovers):.2f}'],
    ['成交额(亿)', f'{amounts[-1]:.2f}', f'{sum(amounts[-5:])/5:.2f}', f'{sum(amounts[-10:])/10:.2f}', f'{avg_amt_30:.2f}', f'{max(amounts):.2f}', f'{min(amounts):.2f}'],
    ['今日/30日均', f'{vols[-1]/avg_vol_30*100:.0f}%', '-', '-', '100%', f'{max(vols)/avg_vol_30*100:.0f}%', f'{min(vols)/avg_vol_30*100:.0f}%'],
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
        if j == 1:
            table[i, j].set_facecolor('#ffcccc')

ax4.set_title('30日量能统计对比 (流通股本7.69亿)', fontsize=12, fontweight='bold', pad=20)

plt.savefig('/data/hermes/workspace/301358_30d_turnover_v2.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_30d_turnover_v2.png')
