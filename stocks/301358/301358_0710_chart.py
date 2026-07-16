#!/usr/bin/env python3
"""301358 7/10更新版 K线图"""
import json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch

fm.fontManager.addfont('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')
plt.rcParams['font.family'] = 'WenQuanYi Zen Hei'
plt.rcParams['axes.unicode_minus'] = False

with open('/data/hermes/workspace/301358_klines.json') as f:
    all_klines = json.load(f)

# 取最近120日
klines = all_klines[-120:]
n = len(klines)

closes = [k['close'] for k in klines]
opens = [k['open'] for k in klines]
highs = [k['high'] for k in klines]
lows = [k['low'] for k in klines]
volumes = [k['volume'] for k in klines]
dates = [k['date'] for k in klines]

# 指标计算
c = np.array(closes)
h = np.array(highs)
l = np.array(lows)
v = np.array(volumes)

# BOLL
period = 20
mid = np.convolve(c, np.ones(period)/period, mode='valid')
std = np.array([c[max(0,i):i+period].std() for i in range(n-period+1)])
upper = mid + 2*std
lower = mid - 2*std

# MA
ma5 = np.convolve(c, np.ones(5)/5, mode='valid')
ma10 = np.convolve(c, np.ones(10)/10, mode='valid')
ma20 = np.convolve(c, np.ones(20)/20, mode='valid')
ma60 = np.convolve(c, np.ones(60)/60, mode='valid')

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(22, 14), gridspec_kw={'height_ratios': [3, 1]})
fig.subplots_adjust(hspace=0.05, top=0.94, bottom=0.05, left=0.07, right=0.93)
fig.suptitle('301358 湖南裕能 · 2026-07-10收盘分析  收盘63.15  跌-4.03%  RSI=32.97  KDJ J=-3.73',
             fontsize=16, fontweight='bold')

x = np.arange(n)

# K线
for i in range(n):
    color = '#d32f2f' if closes[i] >= opens[i] else '#2e7d32'
    ax1.plot([i, i], [lows[i], highs[i]], color=color, linewidth=0.7)
    bottom = min(opens[i], closes[i])
    height = abs(closes[i] - opens[i])
    if height < 0.01: height = 0.01
    rect = FancyBboxPatch((i-0.35, bottom), 0.7, height, boxstyle="round,pad=0",
                          facecolor=color, edgecolor=color, linewidth=0.5)
    ax1.add_patch(rect)

# MA线
ax1.plot(x[4:], ma5, color='#ff9800', linewidth=1, label=f'MA5={ma5[-1]:.2f}', alpha=0.8)
ax1.plot(x[9:], ma10, color='#2196f3', linewidth=1, label=f'MA10={ma10[-1]:.2f}', alpha=0.8)
ax1.plot(x[19:], ma20, color='#9c27b0', linewidth=1, label=f'MA20={ma20[-1]:.2f}', alpha=0.8)
ax1.plot(x[59:], ma60, color='#607d8b', linewidth=1, label=f'MA60={ma60[-1]:.2f}', alpha=0.8)

# BOLL
ax1.plot(x[19:], upper, color='#e91e63', linewidth=0.8, linestyle='--', alpha=0.5, label=f'BOLL上{upper[-1]:.2f}')
ax1.plot(x[19:], mid, color='#666', linewidth=0.8, linestyle='--', alpha=0.5, label=f'BOLL中{mid[-1]:.2f}')
ax1.plot(x[19:], lower, color='#e91e63', linewidth=0.8, linestyle='--', alpha=0.5, label=f'BOLL下{lower[-1]:.2f}★已破')
ax1.fill_between(x[19:], lower, upper, alpha=0.03, color='#e91e63')

# Fibonacci回撤位
peak = max(highs)
peak_i = highs.index(peak)
low_ipo = 30.14
fib618 = peak - (peak - low_ipo) * 0.618
ax1.axhline(y=fib618, color='#4caf50', linewidth=1, linestyle=':', alpha=0.6)
ax1.text(n-1, fib618, f' Fib 61.8%={fib618:.2f}', fontsize=8, color='#4caf50', va='bottom')

# 事件标注
events = [
    (dates.index("2026-06-03") if "2026-06-03" in dates else None, "6/03 宁德时代+津晟\n公告减持38亿", '#d32f2f'),
    (dates.index("2026-06-23") if "2026-06-23" in dates else None, "6/23 B浪反弹顶\n88.00", '#e91e63'),
    (dates.index("2026-07-08") if "2026-07-08" in dates else None, "7/08 放量暴跌\n-6.18%", '#d32f2f'),
    (dates.index("2026-07-10") if "2026-07-10" in dates else None, "7/10 收盘63.15\n破BOLL下轨\nKDJ J=-3.73", '#ff6f00'),
]
for ex, et, ec in events:
    if ex is not None:
        y_pos = highs[ex] + 4
        ax1.annotate(et, xy=(ex, y_pos), fontsize=8, color=ec, ha='center', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff9c4', alpha=0.8),
                    arrowprops=dict(arrowstyle='->', color=ec, lw=1.2))

# 成交量
colors_vol = ['#d32f2f' if closes[i] >= opens[i] else '#2e7d32' for i in range(n)]
ax2.bar(x, np.array(volumes)/10000, color=colors_vol, width=0.6, alpha=0.6)
v_avg = np.array(volumes[-20:]).mean()
ax2.axhline(y=v_avg/10000, color='#ff9800', linewidth=0.8, linestyle='--', label=f'20日均量={v_avg/10000:.0f}万手')
ax2.set_ylabel('成交量(万手)', fontsize=10)
ax2.set_xlabel('日期', fontsize=10)
ax2.legend(fontsize=8)

# X轴
step = max(1, n // 15)
ax1.set_xticks(x[::step])
ax1.set_xticklabels([])
ax2.set_xticks(x[::step])
ax2.set_xticklabels([dates[i] for i in range(0, n, step)], rotation=30, fontsize=8)

ax1.set_ylabel('价格(元)', fontsize=12)
ax1.legend(loc='upper right', fontsize=9, ncol=2)
ax1.grid(True, alpha=0.1)

plt.savefig('/data/hermes/workspace/301358_0710_chart.png', dpi=150, bbox_inches='tight')
print("✓ 7/10更新图表已保存")
print(f"\n关键数据汇总:")
print(f"  收盘: 63.15  跌幅: -4.03%")
print(f"  BOLL下轨: 63.67  已破↓")
print(f"  KDJ J: -3.73  极度超卖")
print(f"  RSI: 32.97")
print(f"  MACD绿柱放大: -2.212")
print(f"  均线: 完全空头排列")
print(f"  量能: 21万手 (vs 7/9 27万手, -23.3%)")
print(f"  Fib 61.8%: 60.51")
