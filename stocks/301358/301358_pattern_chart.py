#!/usr/bin/env python3
"""301358 K线形态+量能+位置完整分析图"""
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

with open('/tmp/301358_klines_60d_0720.json') as f:
    k_data = json.load(f)
klines = k_data['data']['sz301358']['qfqday']

# 修正7/20收盘数据
recent = klines[-21:]  # 取21条，修正最后一条
# 替换7/20: [date, open, close, high, low, vol]
# close=59.90, high=61.20, low=58.08
recent[-1] = ['2026-07-20', '60.01', '59.90', '61.20', '58.08', '195420']

# 取最后20天
recent = recent[-20:]

dates = []
opens, closes, highs, lows, vols = [], [], [], [], []
for k in recent:
    dates.append(k[0][5:])  # MM-DD
    opens.append(float(k[1]))
    closes.append(float(k[2]))
    highs.append(float(k[3]))
    lows.append(float(k[4]))
    vols.append(float(k[5]))

# 成交额
amts = [v*c/100000000 for v, c in zip(vols, closes)]

# 均线
def ma(data, period):
    result = [None] * len(data)
    for i in range(period-1, len(data)):
        result[i] = sum(data[i-period+1:i+1]) / period
    return result

ma5 = ma(closes, 5)
ma10 = ma(closes, 10)
ma20_list = ma(closes, 20)

# 量能均线
ma5v = ma(vols, 5)
ma10v = ma(vols, 10)

# === 画图 ===
fig = plt.figure(figsize=(20, 16))
gs = GridSpec(4, 2, figure=fig, height_ratios=[3, 1, 1.2, 1], hspace=0.3, wspace=0.15,
              left=0.06, right=0.97, top=0.96, bottom=0.04)

# --- 1. K线+均线 ---
ax1 = fig.add_subplot(gs[0, :])
x = np.arange(len(dates))
width = 0.6

# K线
for i in range(len(dates)):
    color = '#cc0000' if closes[i] >= opens[i] else '#00aa00'
    ax1.plot([i, i], [lows[i], highs[i]], color=color, linewidth=1.2, zorder=3)
    bottom = min(opens[i], closes[i])
    height = max(abs(closes[i] - opens[i]), 0.05)
    rect = plt.Rectangle((i-width/2, bottom), width, height,
                         facecolor=color, edgecolor=color, zorder=4)
    ax1.add_patch(rect)

# 均线
ax1.plot(x, ma5, '-', color='#ff6600', linewidth=1.5, alpha=0.8, label='MA5')
ax1.plot(x, ma10, '-', color='#0066cc', linewidth=1.5, alpha=0.8, label='MA10')
if ma20_list[-1] is not None:
    ax1.plot(x, ma20_list, '-', color='#990099', linewidth=1.5, alpha=0.6, label='MA20')

# 关键价位
ax1.axhline(y=57.54, color='#000099', linewidth=1, linestyle='--', alpha=0.4)
ax1.text(len(dates)-0.3, 57.54-1, '57.54\n大宗价\n铁底', fontsize=8, color='#000099', ha='right')
ax1.axhline(y=58.80, color='#00aa00', linewidth=1, linestyle=':', alpha=0.4)
ax1.text(0.3, 58.80, '58.80 7/17低', fontsize=8, color='#00aa00')
ax1.axhline(y=60, color='#888888', linewidth=0.5, linestyle=':', alpha=0.3)
ax1.axhline(y=63.37, color='#cc0000', linewidth=0.5, linestyle=':', alpha=0.3)
ax1.text(0.3, 63.37, '63.37 7/15高 阻力', fontsize=8, color='#cc0000')
ax1.axhline(y=76, color='#cc0000', linewidth=0.5, linestyle=':', alpha=0.2)
ax1.text(0.3, 76, '76 6/25 平台(20日最高区)', fontsize=7, color='#cc0000', alpha=0.5)

# 标注收盘价
for i in range(len(dates)):
    if i == len(dates)-1 or i % 2 == 0:
        ax1.text(i, closes[i]+0.5, f'{closes[i]:.1f}', ha='center', fontsize=8, fontweight='bold')

# 下跌趋势线
ax1.plot([0, len(dates)-1], [85, 58.8], '--', color='#999999', linewidth=1, alpha=0.4, label='下跌趋势线(6/23→7/17)')

# 阶段标注
ax1.axvspan(0, 4, color='#ff0000', alpha=0.04)
ax1.text(2, 92, '高位区\n6/23-6/30\n75-88', ha='center', fontsize=9, color='#cc0000', alpha=0.6)
ax1.axvspan(5, 9, color='#ff6600', alpha=0.04)
ax1.text(7, 92, '暴跌区\n7/1-7/9\n72→63', ha='center', fontsize=9, color='#ff6600', alpha=0.6)
ax1.axvspan(10, 13, color='#ffff00', alpha=0.04)
ax1.text(11.5, 92, '减速区\n7/10-7/14\n62±1', ha='center', fontsize=9, color='#999900', alpha=0.6)
ax1.axvspan(14, 16, color='#00aa00', alpha=0.04)
ax1.text(15, 92, '反复区\n7/15-7/17\n63→59', ha='center', fontsize=9, color='#00aa00', alpha=0.6)
ax1.axvspan(17, 19, color='#0066aa', alpha=0.04)
ax1.text(18, 92, '企稳区?\n7/20\n60±1', ha='center', fontsize=9, color='#0066cc', alpha=0.6)

ax1.set_xticks(x)
ax1.set_xticklabels(dates, fontsize=10, rotation=30)
ax1.set_ylabel('Price', fontsize=12)
ax1.set_title('301358 湖南裕能 — 20天K线形态+均线+量能位置分析', fontsize=14, fontweight='bold')
ax1.legend(loc='upper right', fontsize=10)
ax1.grid(True, alpha=0.12)
ax1.set_ylim([55, 95])

# --- 2. 成交量 ---
ax2 = fig.add_subplot(gs[1, :])
vol_colors = ['#cc0000' if closes[i] >= opens[i] else '#00aa00' for i in range(len(dates))]
ax2.bar(x, [v/10000 for v in vols], color=vol_colors, alpha=0.7, width=0.6, label='Volume')
ax2.plot(x, [v/10000 if v else None for v in ma5v], '-', color='#ff6600', linewidth=1.5, alpha=0.7, label='MA5量')
ax2.plot(x, [v/10000 if v else None for v in ma10v], '-', color='#0066cc', linewidth=1.5, alpha=0.7, label='MA10量')
ax2.set_xticks(x)
ax2.set_xticklabels(dates, fontsize=10, rotation=30)
ax2.set_ylabel('Volume(万手)', fontsize=11)
ax2.set_title('Daily Volume + MA5/MA10', fontsize=11, fontweight='bold')
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.15, axis='y')

# --- 3. 量价关系散点 ---
ax3 = fig.add_subplot(gs[2, 0])
chg_pcts = [(closes[i]/closes[i-1]-1)*100 if i > 0 else 0 for i in range(len(closes))]
vol_norm = [v/10000 for v in vols]
ax3.scatter(vol_norm, chg_pcts, c=['#cc0000' if c >= 0 else '#00aa00' for c in chg_pcts],
            s=80, alpha=0.7, edgecolors='black', linewidth=0.5)
# 标注最新点
ax3.annotate(f'7/20\n{chg_pcts[-1]:+.1f}%', xy=(vol_norm[-1], chg_pcts[-1]),
             xytext=(vol_norm[-1]+3, chg_pcts[-1]+1), fontsize=9, fontweight='bold',
             arrowprops=dict(arrowstyle='->', lw=1))
ax3.set_xlabel('Volume(万手)', fontsize=11)
ax3.set_ylabel('Daily Change %', fontsize=11)
ax3.set_title('Volume vs Change %\n缩量上涨=底部信号?', fontsize=11, fontweight='bold')
ax3.axhline(y=0, color='gray', linewidth=0.5)
ax3.grid(True, alpha=0.15)

# --- 4. 振幅+换手趋势 ---
ax4 = fig.add_subplot(gs[2, 1])
amplitudes = [(highs[i]-lows[i])/opens[i]*100 for i in range(len(dates))]
ax4.bar(x, amplitudes, color=['#cc0000' if a > 5 else '#ff6600' if a > 3 else '#00aa00' for a in amplitudes], alpha=0.7, width=0.6)
ax4.axhline(y=5, color='gray', linewidth=0.5, linestyle='--')
ax4.axhline(y=3, color='gray', linewidth=0.5, linestyle=':')
ax4.set_xticks(x)
ax4.set_xticklabels(dates, fontsize=9, rotation=30)
ax4.set_ylabel('Amplitude %', fontsize=11)
ax4.set_title('Daily Amplitude (振幅)\n高振幅=分歧\低振幅=共识', fontsize=11, fontweight='bold')
ax4.grid(True, alpha=0.15, axis='y')

# --- 5. 下跌幅度统计 ---
ax5 = fig.add_subplot(gs[3, :])
# 从6/23最高88元起累计跌幅
base_price = 88.00
cum_drops = [(c - base_price) / base_price * 100 for c in closes]
ax5.fill_between(x, cum_drops, 0, where=[d < 0 for d in cum_drops], color='#00aa00', alpha=0.2)
ax5.plot(x, cum_drops, 'o-', color='#00aa00', linewidth=2, markersize=5)
for i in range(0, len(dates), 2):
    ax5.text(i, cum_drops[i]-1, f'{cum_drops[i]:.0f}%', ha='center', fontsize=8, color='#006600')
ax5.axhline(y=-20, color='#ff0000', linewidth=1, linestyle='--', alpha=0.5)
ax5.text(len(dates)-1, -21, '-20% 后市熊牛分界', fontsize=9, color='#ff0000', ha='right', alpha=0.5)
ax5.axhline(y=-30, color='#000099', linewidth=1, linestyle='--', alpha=0.5)
ax5.text(len(dates)-1, -31, '-30% 技术熊市', fontsize=9, color='#000099', ha='right', alpha=0.5)
ax5.set_xticks(x)
ax5.set_xticklabels(dates, fontsize=10, rotation=30)
ax5.set_ylabel('Drop from 88元 (%)', fontsize=11)
ax5.set_title('Cumulative Drop from 6/23 (88元) — 到底了吗?', fontsize=12, fontweight='bold')
ax5.grid(True, alpha=0.15, axis='y')

plt.savefig('/data/hermes/workspace/301358_pattern_position.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_pattern_position.png')

# 打印分析
print('\n=== 形态分析总结 ===')
print(f'20日最高: 88.00  最低: 58.80')
print(f'20日跌幅: {(min(lows)-88)/88*100:.1f}% (88→{min(lows):.2f})')
print(f'当前: {closes[-1]:.2f}  距最高: {(closes[-1]-88)/88*100:.1f}%')
print(f'当前: {closes[-1]:.2f}  距最低: {(closes[-1]-58.80)/58.80*100:.1f}%')
print(f'MA5: {ma5[-1]:.2f}  MA10: {ma10[-1]:.2f}  MA20: {ma20_list[-1]:.2f}')
print(f'量能: 今日{vols[-1]/10000:.0f}万手 vs 5日均{ma5v[-1]/10000:.0f}万手 vs 10日均{ma10v[-1]/10000:.0f}万手')
