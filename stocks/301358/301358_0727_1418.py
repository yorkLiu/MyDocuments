#!/usr/bin/env python3
"""
301358 湖南裕能 7/27 主力尾盘拉升分析图
"""

import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

for fp in ['/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', '/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc']:
    try:
        font_manager.fontManager.addfont(fp)
        break
    except:
        pass
plt.rcParams['font.family'] = 'WenQuanYi Zen Hei'
plt.rcParams['axes.unicode_minus'] = False

# 加载分时数据
with open('/tmp/301358_t_0727.json') as f:
    raw = json.load(f)
bars = raw if isinstance(raw, list) else raw.get('data', [])

times, prices, vols, amts = [], [], [], []
prev_vol = 0
prev_amt = 0
for it in bars:
    t = it.get('time', '')
    p = it.get('price', 0)
    v = it.get('volume', 0)
    a = it.get('amount', 0)
    vd = v - prev_vol
    ad = a - prev_amt
    prev_vol = v
    prev_amt = a
    times.append(t)
    prices.append(p)
    vols.append(vd)
    amts.append(ad)

prices = np.array(prices)
vols = np.array(vols)
amts = np.array(amts)

BG = '#1a1a2e'
TEXT = '#E0E0E0'
GRID = '#2a2a4a'
UP = '#E74C3C'
DOWN = '#2ECC71'

fig = plt.figure(figsize=(24, 22), facecolor=BG)
gs = fig.add_gridspec(4, 2, height_ratios=[3, 1, 1.5, 1.5],
                      hspace=0.12, wspace=0.08,
                      left=0.06, right=0.95, top=0.96, bottom=0.03)

# --- 子图1: 分时走势 + 14:18标注 ---
ax1 = fig.add_subplot(gs[0, :])
ax1.set_facecolor(BG)

x = np.arange(len(prices))

# 分时线
ax1.plot(x, prices, color='#FFD700', linewidth=1.2, zorder=3)

# 昨收线
ax1.axhline(y=63.92, color='#888888', linestyle='--', linewidth=1, alpha=0.5, label='昨收 63.92')

# 均价线
cum_amt = np.cumsum(amts)
cum_vol = np.cumsum(vols)
avg_price = np.where(cum_vol > 0, cum_amt / cum_vol / 100, prices[0])
ax1.plot(x, avg_price, color='#4ECDC4', linewidth=1, alpha=0.7, label='均价线')

# 14:18转折线
idx_1418 = None
for i, t in enumerate(times):
    if t == '14:18':
        idx_1418 = i
        break

if idx_1418:
    ax1.axvline(x=idx_1418, color='#FF6B6B', linestyle='-', linewidth=2, alpha=0.7)
    ax1.text(idx_1418+0.5, 66.5, '14:18\n转折点', color='#FF6B6B', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#3a1a1a', alpha=0.9, edgecolor='#FF6B6B'))

# 14:18后高亮区域
if idx_1418:
    ax1.axvspan(idx_1418, len(prices)-1, alpha=0.08, color=UP, label='14:18后尾盘拉升区')

# 关键事件标注
idx_high = np.argmax(prices)
ax1.annotate(f'最高 {prices[idx_high]:.2f}', xy=(idx_high, prices[idx_high]),
            xytext=(idx_high+5, prices[idx_high]+0.4),
            fontsize=9, color=UP, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=UP, lw=1.2),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#3a1a1a', alpha=0.9, edgecolor=UP))

idx_low = np.argmin(prices)
ax1.annotate(f'最低 {prices[idx_low]:.2f}', xy=(idx_low, prices[idx_low]),
            xytext=(idx_low-15, prices[idx_low]-0.8),
            fontsize=9, color=DOWN, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=DOWN, lw=1.2),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a3a1a', alpha=0.9, edgecolor=DOWN))

# 13:00低点标注(午后跳水)
idx_13low = None
min_13 = 999
for i in range(len(times)):
    if times[i].startswith('13:'):
        if prices[i] < min_13:
            min_13 = prices[i]
            idx_13low = i

if idx_13low:
    ax1.annotate(f'午后低点 {min_13:.2f}', xy=(idx_13low, min_13),
                xytext=(idx_13low-20, min_13-1.5),
                fontsize=9, color=DOWN,
                arrowprops=dict(arrowstyle='->', color=DOWN, lw=1),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a3a1a', alpha=0.9, edgecolor=DOWN))

# 收盘标注
ax1.annotate(f'收盘 65.80 (+2.94%)', xy=(len(prices)-1, 65.80),
            xytext=(len(prices)-25, 65.80+1.5), fontsize=10, color=UP, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=UP, lw=1.2),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#3a1a1a', alpha=0.9, edgecolor=UP))

# 67.52压力位
ax1.axhline(y=67.52, color='#E74C3C', linestyle=':', linewidth=1.5, alpha=0.5)
ax1.text(len(prices)+1, 67.52, 'MA20/布林中轨 67.52', color='#E74C3C', fontsize=8)

# 63.92昨收
ax1.axhline(y=63.92, color='#888888', linestyle='--', linewidth=1, alpha=0.4)

ax1.set_xlim(-3, len(prices)+20)
ax1.set_title('301358 湖南裕能 — 7/27 分时走势 & 14:18尾盘拉升分析', 
              color=TEXT, fontsize=15, fontweight='bold', pad=15)
ax1.legend(loc='upper left', fontsize=9, facecolor=BG, edgecolor=GRID, labelcolor=TEXT)
ax1.grid(True, color=GRID, alpha=0.3)
ax1.tick_params(colors=TEXT, labelsize=8)
for spine in ax1.spines.values():
    spine.set_color(GRID)

tick_positions = list(range(0, len(prices), 30))
tick_labels = [times[i] if i < len(times) else '' for i in tick_positions]
ax1.set_xticks(tick_positions)
ax1.set_xticklabels(tick_labels, rotation=30, ha='right', fontsize=8)

# --- 子图2: 分钟成交量 ---
ax2 = fig.add_subplot(gs[1, :], sharex=ax1)
ax2.set_facecolor(BG)

for i in range(len(vols)):
    if i > 0:
        color = UP if prices[i] >= prices[i-1] else DOWN
    else:
        color = UP
    # 14:18后加大alpha
    alpha = 0.9 if (idx_1418 and i >= idx_1418) else 0.5
    ax2.bar(i, vols[i]/10000, width=0.8, color=color, alpha=alpha)

# 14:18线
if idx_1418:
    ax2.axvline(x=idx_1418, color='#FF6B6B', linestyle='-', linewidth=2, alpha=0.7)

ax2.set_ylabel('成交量(万手)', color=TEXT, fontsize=9)
ax2.set_title('分钟成交量 (红=主动涨 绿=主动跌, 14:18后高亮)', color=TEXT, fontsize=10)
ax2.grid(True, color=GRID, alpha=0.3)
ax2.tick_params(colors=TEXT, labelsize=7)
for spine in ax2.spines.values():
    spine.set_color(GRID)

# --- 子图3: 14:18前后对比统计 ---
ax3 = fig.add_subplot(gs[2, :])
ax3.set_facecolor(BG)
ax3.axis('off')

# 计算14:18前后数据
before_data = [(times[i], prices[i], vols[i], amts[i]) for i in range(len(times)) if idx_1418 and i < idx_1418]
after_data = [(times[i], prices[i], vols[i], amts[i]) for i in range(len(times)) if idx_1418 and i >= idx_1418]

before_vol = sum(x[2] for x in before_data)
before_amt = sum(x[3] for x in before_data)
after_vol = sum(x[2] for x in after_data)
after_amt = sum(x[3] for x in after_data)

# 大单分析
big_buy_before = 0
big_sell_before = 0
big_buy_after = 0
big_sell_after = 0

for i in range(len(times)):
    if vols[i] > 3000:
        if i > 0:
            d = 1 if prices[i] > prices[i-1] else (-1 if prices[i] < prices[i-1] else 0)
        else:
            d = 0
        if idx_1418 and i < idx_1418:
            if d > 0: big_buy_before += amts[i]
            elif d < 0: big_sell_before += amts[i]
        elif idx_1418 and i >= idx_1418:
            if d > 0: big_buy_after += amts[i]
            elif d < 0: big_sell_after += amts[i]

table_data = [
    ['指标', '14:18之前(全天前234分钟)', '14:18之后(尾盘22分钟)', '对比'],
    ['成交量', f'{before_vol/10000:.2f}万手', f'{after_vol/10000:.2f}万手', f'尾盘占比{after_vol/(before_vol+after_vol)*100:.1f}%'],
    ['成交额', f'{before_amt/1e8:.2f}亿', f'{after_amt/1e8:.2f}亿', f'尾盘占比{after_amt/(before_amt+after_amt)*100:.1f}%'],
    ['价格区间', f'{min(x[1] for x in before_data):.2f}-{max(x[1] for x in before_data):.2f}', 
     f'{min(x[1] for x in after_data):.2f}-{max(x[1] for x in after_data):.2f}', ''],
    ['大单主动买入', f'{big_buy_before/1e8:.2f}亿', f'{big_buy_after/1e8:.2f}亿', ''],
    ['大单主动卖出', f'{big_sell_before/1e8:.2f}亿', f'{big_sell_after/1e8:.2f}亿', ''],
    ['大单净额', f'{(big_buy_before-big_sell_before)/1e8:+.2f}亿', f'{(big_buy_after-big_sell_after)/1e8:+.2f}亿', ''],
    ['价格走势', '64.30-65.59 震荡', '64.92→65.82 持续上行', '尾盘单边拉升'],
]

table = ax3.table(cellText=table_data, cellLoc='center', loc='center',
                  colWidths=[0.15, 0.28, 0.28, 0.22])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.8)
for j in range(4):
    table[0, j].set_facecolor('#2a2a5a')
    table[0, j].set_text_props(color='#FFFFFF', fontweight='bold')

for i in range(1, len(table_data)):
    for j in range(4):
        cell = table[i, j]
        if i == 6:  # 大单净额
            cell.set_facecolor('#1a3a1a')
            cell.set_text_props(color=DOWN if 'after' not in table_data[i][j] else UP, fontweight='bold')
        elif j > 0 and i in [1, 2]:
            cell.set_facecolor('#2a2a3a')
            cell.set_text_props(color=TEXT)
        elif j > 0 and i == 7:
            cell.set_facecolor('#1a3a1a')
            cell.set_text_props(color=UP, fontweight='bold')
        else:
            cell.set_facecolor('#2a2a3a')
            cell.set_text_props(color=TEXT)

ax3.set_title('14:18 前后量价对比', color=TEXT, fontsize=12, pad=10)

# --- 子图4: 归因分析 ---
ax4 = fig.add_subplot(gs[3, :])
ax4.set_facecolor(BG)
ax4.axis('off')

analysis_text = """7/27 14:18后尾盘拉升归因分析

一、数据事实
  14:18后22分钟成交1.03亿元(占全天8.5%)，其中大单主动买入0.66亿 vs 卖出0.27亿 = 净买入0.39亿
  价格从64.92单边拉升至65.82(+1.39%)，无回调
  全天外盘54.2% > 内盘45.8%，净买入+1.02亿元(与7/24的-0.78亿完全反转)

二、消息面排查
  ① 7/27全天大盘强势：创业板指+2.94%收最高3583.06，4900只个股上涨，沪深放量1.35万亿(+1242亿)
     → 外资看多中国(花旗上调至超配、高盛做多中国AI价值链)→全市场风险偏好回升  [来源:上证报/央广网]
  ② 宁德时代+4.56%突破400元→锂电产业链龙头带动板块β  [来源:东方财富]
  ③ 磷酸铁锂涨价函8/1生效倒计时5天→ strands: 每经7/21报道"涨价成闭门会议主要议题，湖南裕能率先调价+2000元/吨"
  ④ 碳酸锂期货7/27报14.48万/吨→vs 7/24的14.48万基本持平→非碳酸锂驱动
  ⑤ 未发现7/27当天有301358个股级别的直接公告/新闻

三、核心判断
  14:18的买盘不是个股独立消息驱动→是三重共振的结果：
  ① 大盘尾盘集体拉升(创业板指收在最高3583.06=尾盘同步走高)
  ② 锂电板块跟随宁德时代突破400元的β带动
  ③ 涨价函8/1生效倒计时→资金提前布局"涨价兑现"预期
  ④ 主力可能利用大盘尾盘强势完成"修复7/24避雷针"的技术动作

四、关键疑问
  14:18后大单净买入0.39亿→vs 7/24全天大单净流出-0.69亿→完全反转
  这是主力在"回补"7/24卖出的筹码?还是利用大盘尾盘强势做"T+0"?
  → 需观察7/28是否放量延续：放量站上66=真做多；缩量回落=仅尾盘投机"""

ax4.text(0.03, 0.97, analysis_text, transform=ax4.transAxes,
         fontsize=10, color=TEXT, va='top', ha='left',
         family='WenQuanYi Zen Hei',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#2a2a4a', alpha=0.9, edgecolor=GRID))
ax4.set_title('14:18尾盘拉升深度归因', color=TEXT, fontsize=13, pad=10)

plt.savefig('/data/hermes/workspace/301358_0727_1418.png', dpi=150,
            facecolor=BG, edgecolor='none', bbox_inches='tight')
print("图表已保存: /data/hermes/workspace/301358_0727_1418.png")
print(f"\n14:18前: 量{before_vol/10000:.2f}万手 额{before_amt/1e8:.2f}亿")
print(f"14:18后: 量{after_vol/10000:.2f}万手 额{after_amt/1e8:.2f}亿 (占比{after_amt/(before_amt+after_amt)*100:.1f}%)")
print(f"14:18前大单净: {(big_buy_before-big_sell_before)/1e8:+.2f}亿")
print(f"14:18后大单净: {(big_buy_after-big_sell_after)/1e8:+.2f}亿")
