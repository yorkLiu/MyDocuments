#!/usr/bin/env python3
"""301358 GIF 动画：从高点到7/13的下跌历程 + 关键事件 + 大宗交易"""
import json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as mpatches
import os

fm.fontManager.addfont('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')
plt.rcParams['font.family'] = 'WenQuanYi Zen Hei'
plt.rcParams['axes.unicode_minus'] = False

# 加载K线数据
with open('/data/hermes/workspace/301358_klines.json') as f:
    all_klines = json.load(f)

# 只取从2026年1月开始的约130条（覆盖完整下跌周期）
# 找到2026-01-01的索引
start_idx = 0
for i, k in enumerate(all_klines):
    if k['date'] >= '2026-01-01':
        start_idx = i
        break

klines = all_klines[start_idx:]
n = len(klines)
print(f"从{klines[0]['date']}到{klines[-1]['date']}, 共{n}条")

closes = np.array([k['close'] for k in klines])
highs = np.array([k['high'] for k in klines])
lows = np.array([k['low'] for k in klines])
opens = np.array([k['open'] for k in klines])
volumes = np.array([k['volume'] for k in klines])
dates = [k['date'] for k in klines]

# 关键事件
events = [
    {"date": "2026-02-09", "title": "2月9日 解禁3.74亿股", "desc": "49.13%限售解禁\n解禁前杀跌→见底59.04", "color": "#d32f2f", "y_offset": 5},
    {"date": "2026-03-16", "title": "3月16日 反弹高点83.14", "desc": "Q1业绩超预期反弹\n净利14亿 同比+1338%", "color": "#2e7d32", "y_offset": -6},
    {"date": "2026-04-03", "title": "4月3日 缩量回调底67.66", "desc": "机构借利好出货\n缩量回调-19%", "color": "#ff9800", "y_offset": -8},
    {"date": "2026-05-06", "title": "5月6日 年内最高109.64", "desc": "磷酸铁锂涨价高潮\n花旗目标价133.76", "color": "#d32f2f", "y_offset": 5},
    {"date": "2026-06-03", "title": "6月3日 宁德时代+津晟减持", "desc": "两大股东抛减持计划\n合计减持5.5%", "color": "#d32f2f", "y_offset": -6},
    {"date": "2026-06-26", "title": "6月26日 放量暴跌+减持开始", "desc": "宁德减持210万股\n大宗交易折价出货", "color": "#d32f2f", "y_offset": 5},
    {"date": "2026-07-10", "title": "7月10日 尾盘做图形", "desc": "收盘63.15=最低\n光脚阴线 破BOLL下轨\n大宗59.05 机构接货", "color": "#d32f2f", "y_offset": -8},
    {"date": "2026-07-13", "title": "7月13日 逼近59-61", "desc": "盘中最低60.88\n进入企稳区间\n距大宗价仅1.8元", "color": "#9c27b0", "y_offset": -10},
]

# 找到每个事件在klines中的索引
for ev in events:
    for i, d in enumerate(dates):
        if d == ev['date']:
            ev['idx'] = i
            ev['price'] = closes[i]
            break
    else:
        # 找最近的
        for i, d in enumerate(dates):
            if d >= ev['date']:
                ev['idx'] = i
                ev['price'] = closes[i] if i < n else closes[-1]
                break

# 预计算MA20
ma20 = np.convolve(closes, np.ones(20)/20, mode='valid')
ma20 = np.concatenate([np.full(19, np.nan), ma20])

# 预计算BOLL
boll_mid = ma20
boll_std = np.array([np.std(closes[max(0,i-19):i+1]) if i >= 19 else np.nan for i in range(n)])
boll_upper = boll_mid + 2 * boll_std
boll_lower = boll_mid - 2 * boll_std

# 支撑线价位
support_59 = 59.05  # 大宗交易价
support_60 = 60.00
support_61 = 61.00

# 输出目录
frames_dir = '/data/hermes/workspace/gif_frames'
os.makedirs(frames_dir, exist_ok=True)

# 总帧数：从第30根K线开始，每次前进3根，到最后
start_frame = 30
step = 3
frame_indices = list(range(start_frame, n, step))
# 最后几帧放慢
frame_indices += [n-1] * 5

total_frames = len(frame_indices)
print(f"总帧数: {total_frames}")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), gridspec_kw={'height_ratios': [3, 1]})
fig.subplots_adjust(hspace=0.05, top=0.93, bottom=0.07, left=0.08, right=0.95)

y_min = 55
y_max = 115

for frame_i, data_end in enumerate(frame_indices):
    ax1.clear()
    ax2.clear()
    
    end = data_end
    x = np.arange(end + 1)
    
    # 涨跌色: 红涨绿跌 (中国习惯)
    colors_candle = []
    for i in range(end + 1):
        if closes[i] >= opens[i]:
            colors_candle.append('#d32f2f')  # 红
        else:
            colors_candle.append('#2e7d32')  # 绿
    
    # K线柱体
    for i in range(end + 1):
        bottom = min(opens[i], closes[i])
        height = abs(closes[i] - opens[i])
        if height < 0.01:
            height = 0.02
        ax1.bar(i, height, bottom=bottom, width=0.6, color=colors_candle[i], edgecolor=colors_candle[i], linewidth=0.5)
        # 影线
        ax1.plot([i, i], [lows[i], highs[i]], color=colors_candle[i], linewidth=0.5)
    
    # MA20
    valid_ma = ~np.isnan(ma20[:end+1])
    if np.any(valid_ma):
        ax1.plot(x[valid_ma], ma20[:end+1][valid_ma], color='#ff9800', linewidth=1.2, alpha=0.8, label='MA20')
    
    # BOLL上下轨（只在最后几帧显示）
    if end >= n - 10:
        valid_bu = ~np.isnan(boll_upper[:end+1])
        valid_bl = ~np.isnan(boll_lower[:end+1])
        if np.any(valid_bu):
            ax1.plot(x[valid_bu], boll_upper[:end+1][valid_bu], color='#9c27b0', linewidth=0.8, linestyle='--', alpha=0.4)
        if np.any(valid_bl):
            ax1.plot(x[valid_bl], boll_lower[:end+1][valid_bl], color='#9c27b0', linewidth=0.8, linestyle='--', alpha=0.4)
    
    # 支撑线
    ax1.axhline(y=support_59, color='#2e7d32', linewidth=1.5, linestyle='-', alpha=0.5)
    ax1.text(0, support_59, ' 大宗价59.05(机构接货)', fontsize=8, color='#2e7d32', va='center',
            bbox=dict(boxstyle='round', facecolor='#c8e6c9', alpha=0.7))
    
    ax1.axhline(y=support_61, color='#9c27b0', linewidth=0.8, linestyle=':', alpha=0.3)
    ax1.axhline(y=support_60, color='#888', linewidth=0.5, linestyle=':', alpha=0.3)
    
    # 事件标注（只显示已经过去的事件）
    for ev in events:
        if ev['idx'] <= end:
            ax1.annotate(
                f"{ev['title']}\n{ev['desc']}",
                xy=(ev['idx'], ev['price']),
                fontsize=6.5,
                color=ev['color'],
                fontweight='bold',
                ha='left' if ev['idx'] < n//2 else 'right',
                xytext=(ev['idx'] + 3, ev['price'] + ev.get('y_offset', 0)),
                arrowprops=dict(arrowstyle='->', color=ev['color'], lw=0.8, alpha=0.7),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=ev['color'], alpha=0.85, linewidth=0.5)
            )
    
    # 当前价格指示
    if end < n:
        current_price = closes[end]
        ax1.axhline(y=current_price, color='#1565c0', linewidth=0.5, linestyle=':', alpha=0.3)
    
    # 标题
    current_date = dates[end] if end < n else dates[-1]
    current_change = (closes[end] - closes[max(0, end-1)]) / closes[max(0, end-1)] * 100
    ax1.set_title(f'301358 湖南裕能  {current_date}  收盘{closes[end]:.2f}  ({current_change:+.2f}%)',
                 fontsize=13, fontweight='bold')
    
    ax1.set_ylim(y_min, y_max)
    ax1.set_xlim(-2, n + 15)
    ax1.set_ylabel('价格(元)', fontsize=11)
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.08)
    
    # X轴日期标签
    step_label = max(1, n // 12)
    label_indices = list(range(0, n, step_label))
    ax1.set_xticks(label_indices)
    ax1.set_xticklabels([dates[i][5:] for i in label_indices], rotation=30, fontsize=7)
    
    # ===== 成交量 =====
    vol_colors = []
    for i in range(end + 1):
        if closes[i] >= opens[i]:
            vol_colors.append('#d32f2f')
        else:
            vol_colors.append('#2e7d32')
    
    ax2.bar(x, volumes[:end+1]/10000, color=vol_colors, width=0.6, alpha=0.7)
    vol_ma5 = np.convolve(volumes[:end+1], np.ones(5)/5, mode='valid')
    if len(vol_ma5) >= 5:
        ax2.plot(np.arange(4, end+1), vol_ma5/10000, color='#ff9800', linewidth=0.8, alpha=0.6)
    
    ax2.set_ylim(0, max(volumes)/10000 * 1.5)
    ax2.set_xlim(-2, n + 15)
    ax2.set_ylabel('成交量(万手)', fontsize=10)
    ax2.set_xlabel('日期', fontsize=10)
    ax2.grid(True, alpha=0.08)
    ax2.set_xticks(label_indices)
    ax2.set_xticklabels([dates[i][5:] for i in label_indices], rotation=30, fontsize=7)
    
    # 底部注释
    if end >= n - 1:
        ax2.text(n*0.5, max(volumes)/10000*0.5,
                '企稳区间59-61  |  大宗59.05(机构接货)  |  8/20中报  |  9/25减持结束',
                fontsize=10, ha='center', color='#333', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='#fff9c4', alpha=0.8))
    
    fig.canvas.draw()
    fig.savefig(f'{frames_dir}/frame_{frame_i:04d}.png', dpi=80, bbox_inches='tight')
    
    if frame_i % 10 == 0:
        print(f"  帧 {frame_i}/{total_frames} ({dates[end]})")

plt.close()
print(f"\n所有帧已保存到 {frames_dir}")
print("正在合成GIF...")
