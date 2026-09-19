#!/usr/bin/env python3
"""301358 最近10天 K线+主力资金流 复合图"""
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

# === K线数据 ===
with open('/tmp/301358_klines_60d_0720.json') as f:
    k_data = json.load(f)
klines = k_data['data']['sz301358']['qfqday']
recent_k = klines[-10:]

dates = []
opens = []
closes = []
highs = []
lows = []
vols = []
for k in recent_k:
    dates.append(k[0][5:])  # MM-DD
    opens.append(float(k[1]))
    closes.append(float(k[2]))
    highs.append(float(k[3]))
    lows.append(float(k[4]))
    vols.append(float(k[5]))

# === 东方财富资金流数据 ===
# 格式: 日期, 主力净额, 小单净额, 中单净额(?), 大单净额(?), ...
# 字段: f51=date, f52=主力净额, f53=小单, f54=中单, f55=大单, f56=超大单
# 实际格式: date, main_net, small_net, medium_net, large_net, super_net, main_pct, small_pct, medium_pct, large_pct, super_pct, close, chg
em_data = [
    ("07-07", -41945286, 7148816, 34796464, 5959239, -47904525, 72.00),
    ("07-08", -188878196, 244111888, -55233680, -144451248, -44426948, 67.55),
    ("07-09", -209640064, 234894496, -25254432, -70794928, -138845136, 65.80),
    ("07-10", -86945099, 93206400, -6261312, -66690093, -20255006, 63.15),
    ("07-13", -39399970, 5716272, 33683696, 3665409, -43065379, 61.54),
    ("07-14", -16117289, 10493296, 5624000, -34680751, 18563462, 61.98),
    ("07-15", 215389142, -252501728, 37112576, 139053632, 76335510, 63.37),
    ("07-16", -5845658, -11147552, 16993216, -3741040, -2104618, 61.24),
    ("07-17", -77401834, 70415504, 6986320, -63293350, -14108484, 59.47),
    ("07-20", -6125776, -6572128, 12697904, 5103390, -11229166, 59.90),
]

em_dates = [d[0] for d in em_data]
main_nets = [d[1]/1e8 for d in em_data]  # 转亿
small_nets = [d[2]/1e8 for d in em_data]
medium_nets = [d[3]/1e8 for d in em_data]
# 大单+超大单 组合
large_nets = [d[4]/1e8 for d in em_data]
super_nets = [d[5]/1e8 for d in em_data]
big_nets = [l+s for l, s in zip(large_nets, super_nets)]

# === 画图 ===
fig = plt.figure(figsize=(18, 14))
gs = GridSpec(3, 1, figure=fig, height_ratios=[2.5, 1, 1.5], hspace=0.2,
              left=0.07, right=0.96, top=0.95, bottom=0.05)

# --- 1. K线图 ---
ax1 = fig.add_subplot(gs[0])
x = np.arange(len(dates))
width = 0.5

for i in range(len(dates)):
    color = '#cc0000' if closes[i] >= opens[i] else '#00aa00'
    # 影线
    ax1.plot([i, i], [lows[i], highs[i]], color=color, linewidth=1.5, zorder=3)
    # 实体
    bottom = min(opens[i], closes[i])
    height = abs(closes[i] - opens[i])
    if height == 0: height = 0.1
    rect = plt.Rectangle((i-width/2, bottom), width, height, 
                         facecolor=color, edgecolor=color, zorder=4)
    ax1.add_patch(rect)

# 标注收盘价
for i in range(len(dates)):
    ax1.text(i, closes[i]+0.3, f'{closes[i]:.2f}', ha='center', fontsize=8, fontweight='bold')

ax1.set_xticks(x)
ax1.set_xticklabels(dates, fontsize=11)
ax1.set_ylabel('Price (yuan)', fontsize=12)
ax1.set_title('301358 湖南裕能 最近10天 K线 + 主力资金流', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.15)

# 关键价位
ax1.axhline(y=57.54, color='#000099', linewidth=1, linestyle='--', alpha=0.4)
ax1.text(len(dates)-0.5, 57.54, '57.54 大宗价', fontsize=8, color='#000099', va='bottom')
ax1.axhline(y=60, color='#888888', linewidth=0.5, linestyle=':', alpha=0.3)

# 标注减持事件
ax1.annotate('7/10 大宗\n59.05元', xy=(3, 63.15), xytext=(2, 68),
             fontsize=8, color='#000099',
             arrowprops=dict(arrowstyle='->', color='#000099', lw=1))
ax1.annotate('7/13 大宗\n57.54元', xy=(4, 61.54), xytext=(3.5, 66),
             fontsize=8, color='#000099',
             arrowprops=dict(arrowstyle='->', color='#000099', lw=1))
ax1.annotate('7/15 调价函\n利好+1.9%', xy=(6, 63.37), xytext=(5, 68),
             fontsize=8, color='#cc0000',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1))
ax1.annotate('7/20 净买入\n+16990万', xy=(9, 59.90), xytext=(8.3, 55),
             fontsize=8, color='#00aa00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00aa00', lw=1.5))

# --- 2. 成交量 ---
ax2 = fig.add_subplot(gs[1])
vol_colors = ['#cc0000' if closes[i] >= opens[i] else '#00aa00' for i in range(len(dates))]
ax2.bar(x, [v/10000 for v in vols], color=vol_colors, alpha=0.7, width=0.6)
ax2.set_xticks(x)
ax2.set_xticklabels(dates, fontsize=11)
ax2.set_ylabel('Volume (万手)', fontsize=11)
ax2.set_title('Daily Volume', fontsize=11)
ax2.grid(True, alpha=0.15, axis='y')

# --- 3. 主力资金流 ---
ax3 = fig.add_subplot(gs[2])

# 主力净额柱状图
colors_flow = ['#cc0000' if v > 0 else '#00aa00' for v in main_nets]
bars = ax3.bar(x, main_nets, color=colors_flow, alpha=0.7, width=0.6, label='主力净额')

# 大单+超大单叠加
ax3.bar(x, big_nets, color='#ff6600', alpha=0.3, width=0.4, label='大单+超大单')

# 累计线
cum_main = np.cumsum(main_nets)
ax3_2 = ax3.twinx()
ax3_2.plot(x, cum_main, 'o-', color='#000099', linewidth=2.5, markersize=6, label='累计主力净额', zorder=5)
for i, v in enumerate(cum_main):
    ax3_2.text(i, v+0.05, f'{v:.2f}', ha='center', fontsize=8, color='#000099', fontweight='bold')

ax3.axhline(y=0, color='black', linewidth=0.5)
ax3.set_xticks(x)
ax3.set_xticklabels(dates, fontsize=11)
ax3.set_ylabel('Daily Net (亿)', fontsize=11)
ax3_2.set_ylabel('Cumulative (亿)', fontsize=11, color='#000099')
ax3.set_title('Main Force Net Flow (红色=inflow / 绿色=outflow) & Cumulative', fontsize=12, fontweight='bold')
ax3.legend(fontsize=10, loc='upper left')
ax3_2.legend(fontsize=10, loc='upper right')
ax3.grid(True, alpha=0.15, axis='y')

# 标注关键日
ax3.annotate('7/15\n主力+2.15亿\n(唯一净流入)', xy=(6, main_nets[6]), xytext=(5.5, 2.5),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
ax3.annotate('7/09\n主力-2.10亿\n(最大流出)', xy=(2, main_nets[2]), xytext=(1, -2.8),
             fontsize=9, color='#00aa00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00aa00', lw=1.5))
ax3.annotate('7/20\n主力-0.06亿\n(东方财富口径)\n但大单+16990万(分时)', xy=(9, main_nets[9]), xytext=(7.5, -1.5),
             fontsize=8, color='#ff6600', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#ff6600', lw=1))

plt.savefig('/data/hermes/workspace/301358_10d_flow_kline.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_10d_flow_kline.png')

# 打印资金流表格
print('\n=== 10天资金流明细 ===')
print(f'{"日期":>6}  {"收盘":>6}  {"涨跌":>6}  {"主力净额":>10}  {"大单+超大":>10}  {"累计主力":>10}')
cum = 0
for i, d in enumerate(em_data):
    cum += d[1]/1e8
    print(f'{d[0]:>6}  {closes[i]:6.2f}  {(closes[i]/closes[i-1]-1)*100 if i>0 else 0:+5.1f}%  {d[1]/1e8:+8.3f}亿  {big_nets[i]:+8.3f}亿  {cum:+8.3f}亿')
