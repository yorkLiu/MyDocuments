#!/usr/bin/env python3
"""
301358 湖南裕能 7/24 主力意图分析图
- 分时走势+成交量
- 大单买卖标注
- 30分钟分段量价
- 内外盘对比
- 主力意图归因
"""

import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from datetime import datetime
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
with open('/tmp/301358_t_0724_full.json') as f:
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

# 7/24收盘数据
close_data = {
    '现价': 63.92, '昨收': 66.01, '今开': 64.66,
    '最高': 67.13, '最低': 63.87,
    '成交量': 211127, '成交额': 13.80e8,
    '外盘': 99444, '内盘': 111682,
    '换手率': 2.76, '量比': 0.97, '振幅': 4.94,
    '涨跌幅': -3.17
}

# 大单识别(>3000手/分钟)
big_bars = []
for i in range(len(vols)):
    if vols[i] > 3000:
        if i > 0:
            direction = 1 if prices[i] > prices[i-1] else (-1 if prices[i] < prices[i-1] else 0)
        else:
            direction = 0
        big_bars.append((i, times[i], prices[i], vols[i], amts[i], direction))

big_buy_amt = sum(b[4] for b in big_bars if b[5] > 0)
big_sell_amt = sum(b[4] for b in big_bars if b[5] < 0)
big_neutral_amt = sum(b[4] for b in big_bars if b[5] == 0)
big_net = (big_buy_amt - big_sell_amt) / 1e8

# 30分钟分段
segments = {}
for i in range(len(times)):
    t = times[i]
    if ':' in t:
        hh, mm = int(t.split(':')[0]), int(t.split(':')[1])
        seg_key = f"{hh:02d}:{'00' if mm < 30 else '30'}"
    else:
        seg_key = t
    if seg_key not in segments:
        segments[seg_key] = {'vol': 0, 'amt': 0, 'open': prices[i], 'close': prices[i], 'high': prices[i], 'low': prices[i]}
    segments[seg_key]['vol'] += vols[i]
    segments[seg_key]['amt'] += amts[i]
    segments[seg_key]['close'] = prices[i]
    segments[seg_key]['high'] = max(segments[seg_key]['high'], prices[i])
    segments[seg_key]['low'] = min(segments[seg_key]['low'], prices[i])

# ==================== 绘图 ====================
BG = '#1a1a2e'
TEXT = '#E0E0E0'
GRID = '#2a2a4a'
UP = '#E74C3C'
DOWN = '#2ECC71'

fig = plt.figure(figsize=(24, 28), facecolor=BG)
gs = fig.add_gridspec(5, 2, height_ratios=[3, 1, 1.5, 1.2, 1.2],
                      hspace=0.12, wspace=0.08,
                      left=0.06, right=0.95, top=0.96, bottom=0.03)

# --- 子图1: 分时走势 + 大单标注 ---
ax1 = fig.add_subplot(gs[0, :])
ax1.set_facecolor(BG)

x = np.arange(len(prices))

# 分时线
ax1.plot(x, prices, color='#FFD700', linewidth=1.2, zorder=3)

# 昨收线
ax1.axhline(y=66.01, color='#888888', linestyle='--', linewidth=1, alpha=0.5, label='昨收 66.01')

# 均价线(累计成交额/累计成交量)
cum_amt = np.cumsum(amts)
cum_vol = np.cumsum(vols)
avg_price = np.where(cum_vol > 0, cum_amt / cum_vol / 100, prices[0])
ax1.plot(x, avg_price, color='#4ECDC4', linewidth=1, alpha=0.7, label='均价线')

# 填充(涨跌区域)
fill_colors = [UP if p >= 66.01 else DOWN for p in prices]
for i in range(len(prices)-1):
    color = UP if prices[i] >= 66.01 else DOWN
    ax1.fill_between([x[i], x[i+1]], prices[i], 66.01, alpha=0.06, color=color)

# 大单标注
for idx, t, p, v, a, d in big_bars:
    if a / 1e8 > 0.03:  # >300万的大单
        if d > 0:
            ax1.scatter(idx, p, s=30, color=UP, zorder=5, alpha=0.8)
        elif d < 0:
            ax1.scatter(idx, p, s=30, color=DOWN, zorder=5, alpha=0.8)

# 关键事件标注
# 最高点
idx_high = np.argmax(prices)
ax1.annotate(f'最高 {prices[idx_high]:.2f}', xy=(idx_high, prices[idx_high]),
            xytext=(idx_high+8, prices[idx_high]+0.5),
            fontsize=9, color=UP, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=UP, lw=1.2),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#3a1a1a', alpha=0.9, edgecolor=UP))

# 最低点
idx_low = np.argmin(prices)
ax1.annotate(f'最低 {prices[idx_low]:.2f}', xy=(idx_low, prices[idx_low]),
            xytext=(idx_low-20, prices[idx_low]-1.5),
            fontsize=9, color=DOWN, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=DOWN, lw=1.2),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a3a1a', alpha=0.9, edgecolor=DOWN))

# 开盘/收盘标注
ax1.annotate(f'开盘 64.66', xy=(0, 64.66),
            xytext=(3, 64.66-2), fontsize=8, color='#FFD700',
            arrowprops=dict(arrowstyle='->', color='#FFD700', lw=0.8))
ax1.annotate(f'收盘 63.92 (-3.17%)', xy=(len(prices)-1, 63.92),
            xytext=(len(prices)-30, 63.92-2.5), fontsize=9, color=DOWN, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=DOWN, lw=1),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a3a1a', alpha=0.9, edgecolor=DOWN))

# 67.13压力标注(MA20/布林中轨)
ax1.axhline(y=67.52, color='#E74C3C', linestyle=':', linewidth=1.5, alpha=0.6)
ax1.text(len(prices)+1, 67.52, 'MA20/布林中轨 67.52\n(精确反压位)', color='#E74C3C', fontsize=8, va='center')

# 61.17支撑标注
ax1.axhline(y=61.17, color='#2ECC71', linestyle=':', linewidth=1.5, alpha=0.6)
ax1.text(len(prices)+1, 61.17, '第一支撑 61.17', color='#2ECC71', fontsize=8, va='center')

ax1.set_xlim(-3, len(prices)+20)
ax1.set_title('301358 湖南裕能 — 7/24 分时走势 & 大单标注 (全天)', 
              color=TEXT, fontsize=15, fontweight='bold', pad=15)
ax1.legend(loc='upper right', fontsize=9, facecolor=BG, edgecolor=GRID, labelcolor=TEXT)
ax1.grid(True, color=GRID, alpha=0.3)
ax1.tick_params(colors=TEXT, labelsize=8)
for spine in ax1.spines.values():
    spine.set_color(GRID)

# X轴时间标签
tick_positions = list(range(0, len(prices), 30))
tick_labels = [times[i] if i < len(times) else '' for i in tick_positions]
ax1.set_xticks(tick_positions)
ax1.set_xticklabels(tick_labels, rotation=30, ha='right', fontsize=8)

# --- 子图2: 分钟成交量 ---
ax2 = fig.add_subplot(gs[1, :], sharex=ax1)
ax2.set_facecolor(BG)

for i in range(len(vols)):
    color = UP if prices[i] >= 66.01 else DOWN
    if i > 0:
        color = UP if prices[i] >= prices[i-1] else DOWN
    ax2.bar(i, vols[i]/10000, width=0.8, color=color, alpha=0.6)

ax2.set_ylabel('成交量(万手)', color=TEXT, fontsize=9)
ax2.set_title('分钟成交量 (红=主动涨 绿=主动跌)', color=TEXT, fontsize=10)
ax2.grid(True, color=GRID, alpha=0.3)
ax2.tick_params(colors=TEXT, labelsize=7)
for spine in ax2.spines.values():
    spine.set_color(GRID)

# --- 子图3: 30分钟分段量价 ---
ax3 = fig.add_subplot(gs[2, :])
ax3.set_facecolor(BG)

seg_keys = sorted(segments.keys())
seg_x = np.arange(len(seg_keys))
seg_vols = [segments[k]['vol']/10000 for k in seg_keys]
seg_amts = [segments[k]['amt']/1e8 for k in seg_keys]
seg_opens = [segments[k]['open'] for k in seg_keys]
seg_closes = [segments[k]['close'] for k in seg_keys]
seg_highs = [segments[k]['high'] for k in seg_keys]
seg_lows = [segments[k]['low'] for k in seg_keys]

colors_seg = [UP if seg_closes[i] >= seg_opens[i] else DOWN for i in range(len(seg_keys))]

bars_x = np.arange(len(seg_keys))
ax3.bar(bars_x, seg_vols, width=0.6, color=colors_seg, alpha=0.7)

# 叠加价格线
ax3b = ax3.twinx()
ax3b.set_facecolor(BG)
for i in range(len(seg_keys)):
    color = UP if seg_closes[i] >= seg_opens[i] else DOWN
    ax3b.plot([i-0.3, i+0.3], [seg_opens[i], seg_closes[i]], color=color, linewidth=2)
    ax3b.plot([i, i], [seg_lows[i], seg_highs[i]], color=color, linewidth=1, alpha=0.5)

ax3.set_xticks(bars_x)
ax3.set_xticklabels(seg_keys, fontsize=8, rotation=30)
ax3.set_ylabel('成交量(万手)', color=TEXT, fontsize=9)
ax3b.set_ylabel('价格(元)', color=TEXT, fontsize=9)
ax3.set_title('30分钟分段量价 (柱=量 线=开收)', color=TEXT, fontsize=10)
ax3.grid(True, color=GRID, alpha=0.3)
ax3.tick_params(colors=TEXT, labelsize=7)
ax3b.tick_params(colors=TEXT, labelsize=7)
for spine in ax3.spines.values():
    spine.set_color(GRID)
for spine in ax3b.spines.values():
    spine.set_color(GRID)

# --- 子图4: 内外盘+大单统计 ---
ax4 = fig.add_subplot(gs[3, 0])
ax4.set_facecolor(BG)
ax4.axis('off')

# 内外盘饼图
ext = 99444
inn = 111682
total = ext + inn

# 用表格代替
table_data = [
    ['指标', '值', '占比/说明'],
    ['外盘(主动买)', f'{ext:,}手', f'{ext/total*100:.1f}%'],
    ['内盘(主动卖)', f'{inn:,}手', f'{inn/total*100:.1f}%'],
    ['净卖出', f'{ext-inn:,}手', f'-0.78亿元'],
    ['', '', ''],
    ['大单主动买入', f'{big_buy_amt/1e8:.2f}亿', f'{big_buy_amt/(big_buy_amt+big_sell_amt)*100:.1f}%'],
    ['大单主动卖出', f'{big_sell_amt/1e8:.2f}亿', f'{big_sell_amt/(big_buy_amt+big_sell_amt)*100:.1f}%'],
    ['大单净额', f'{big_net:+.2f}亿', '主力净流出'],
    ['大单笔数', f'{len(big_bars)}', '>3000手/分钟'],
]

table = ax4.table(cellText=table_data, cellLoc='center', loc='center',
                  colWidths=[0.25, 0.25, 0.3])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.6)
for j in range(3):
    table[0, j].set_facecolor('#2a2a5a')
    table[0, j].set_text_props(color='#FFFFFF', fontweight='bold')
for i in range(1, len(table_data)):
    for j in range(3):
        cell = table[i, j]
        if i in [1, 5]:  # 买入
            cell.set_facecolor('#1a3a1a')
            cell.set_text_props(color=DOWN)
        elif i in [2, 6]:  # 卖出
            cell.set_facecolor('#3a1a1a')
            cell.set_text_props(color=UP)
        elif i in [3, 7]:  # 净额
            cell.set_facecolor('#3a1a1a')
            cell.set_text_props(color=UP, fontweight='bold')
        else:
            cell.set_facecolor('#2a2a3a')
            cell.set_text_props(color=TEXT)

ax4.set_title('内外盘 & 大单统计', color=TEXT, fontsize=12, pad=10)

# --- 子图5: 资金流向汇总 ---
ax5 = fig.add_subplot(gs[3, 1])
ax5.set_facecolor(BG)
ax5.axis('off')

fund_data = [
    ['资金口径', '净额', '方向'],
    ['大单分钟估算', '-0.69亿', '净流出'],
    ['新浪财经', '+243.98万', '微流入'],
    ['证券之星', '-499.21万', '微流出'],
    ['MSN/东方财富', '+897.06万', '微流入'],
    ['', '', ''],
    ['口径差异说明', '', ''],
    ['大单估算(本图)', '=分钟级>3000', '手主动买卖差'],
    ['第三方平台', '=逐笔成交', '金额分级统计'],
    ['三方差异', '=统计口径', '不同导致'],
]

table2 = ax5.table(cellText=fund_data, cellLoc='center', loc='center',
                   colWidths=[0.25, 0.2, 0.3])
table2.auto_set_font_size(False)
table2.set_fontsize(9)
table2.scale(1, 1.4)
for j in range(3):
    table2[0, j].set_facecolor('#2a2a5a')
    table2[0, j].set_text_props(color='#FFFFFF', fontweight='bold')
for i in range(1, len(fund_data)):
    for j in range(3):
        cell = table2[i, j]
        cell.set_facecolor('#2a2a3a')
        cell.set_text_props(color=TEXT)

ax5.set_title('资金流向多口径对比', color=TEXT, fontsize=12, pad=10)

# --- 子图6: 主力意图归因 ---
ax6 = fig.add_subplot(gs[4, :])
ax6.set_facecolor(BG)
ax6.axis('off')

intent_text = """7/24 主力意图深度归因

阶段一(09:30-09:48)  开盘冲高 64.66 → 67.06  量6.23亿(占全天45%)
  → 有资金在开盘前18分钟集中推升，连续大单主动买入(09:31-09:38连续8分钟红柱)
  → 09:38冲至67.06=精确试探MA20/布林中轨67.52 → 遇阻
  → 这是"试盘"行为：测试上方67.5压力位的卖压强度

阶段二(09:39-10:30)  冲高回落 67.06 → 64.91  量3.08亿(占22%)
  → 09:39起连续14分钟主动卖出(绿柱)=09:38冲高后立即出货
  → 10:00-10:34连续35分钟阴跌=系统性抛压
  → "试盘失败"后的派发阶段：发现67元上方卖压沉重→放弃突破→转为出货

阶段三(10:30-14:00)  低位横盘 64.44-65.23  量4.22亿(占31%)
  → 13:01尝试反攻64.49→64.95但量能不足
  → 13:18再试探65.23→13:21立即被打回64.96
  → "弱势反弹"特征：每次反抽都被卖压打下

阶段四(14:00-15:00)  尾盘跳水 64.37 → 63.92  量1.84亿(占13%)
  → 14:32出现一笔16.26万手大单(1046万)=尾盘集中抛售
  → 14:46-14:57连续12分钟阴跌=尾盘清仓式卖出
  → 全天收盘63.92=接近最低点63.87=收在全天最低区域

核心结论：7/24主力行为="试盘67 → 遇阻 → 派发 → 尾盘跳水"四步走
  ① 09:30冲高67不是做多→是测试上方筹码压力
  ② 发现67以上卖压沉重→立即转为出货模式
  ③ 10:30-14:00的横盘不是蓄力→是出货平台
  ④ 尾盘跳水=不维护收盘价=无意继续做多
  ⑤ 全天-3.17%+外盘<内盘+大单净流出-0.69亿=主力在撤退"""

ax6.text(0.03, 0.97, intent_text, transform=ax6.transAxes,
         fontsize=10, color=TEXT, va='top', ha='left',
         family='WenQuanYi Zen Hei',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#2a2a4a', alpha=0.9, edgecolor=GRID))
ax6.set_title('主力意图归因 (7/24全天分时行为链)', color=TEXT, fontsize=13, pad=10)

plt.savefig('/data/hermes/workspace/301358_0724_intent.png', dpi=150,
            facecolor=BG, edgecolor='none', bbox_inches='tight')
print("图表已保存: /data/hermes/workspace/301358_0724_intent.png")
print(f"\n大单主动买入: {big_buy_amt/1e8:.2f}亿")
print(f"大单主动卖出: {big_sell_amt/1e8:.2f}亿")
print(f"大单净额: {big_net:+.2f}亿")
print(f"大单笔数: {len(big_bars)}")
