#!/usr/bin/env python3
"""
301358 湖南裕能 90天综合K线分析图
- 日K线(红涨绿跌)
- 支撑位/压力位(筹码分布+均线+布林带)
- 成交量+换手率
- 主力意图标注
- 可比标的对比(宁德时代/德方纳米/富临精工/创业板指)
"""

import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import FancyBboxPatch
from datetime import datetime, timedelta
from matplotlib import font_manager

# 中文字体
for fp in ['/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', '/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc']:
    try:
        font_manager.fontManager.addfont(fp)
        break
    except:
        pass
plt.rcParams['font.family'] = 'WenQuanYi Zen Hei'
plt.rcParams['axes.unicode_minus'] = False

# 加载数据
def load_data(path):
    with open(path) as f:
        return json.load(f)

bars_301358 = load_data('/tmp/301358_daily_clean.json')
bars_300750 = load_data('/tmp/300750_daily.json')
bars_300769 = load_data('/tmp/300769_daily.json')
bars_300432 = load_data('/tmp/300432_daily.json')
bars_399006 = load_data('/tmp/399006_daily.json')

# 解析各标的
def parse_bars(raw_data, key):
    sd = raw_data['data'][key]
    if 'qfqday' in sd:
        bars = sd['qfqday']
    elif 'day' in sd:
        bars = sd['day']
    else:
        bars = list(sd.values())[0]
    dates, o, c, h, l, v = [], [], [], [], [], []
    for b in bars:
        dates.append(b[0])
        o.append(float(b[1])); c.append(float(b[2]))
        h.append(float(b[3])); l.append(float(b[4]))
        v.append(int(float(b[5])) if len(b) > 5 else 0)
    return dates, np.array(o), np.array(c), np.array(h), np.array(l), np.array(v)

dates, opens, closes, highs, lows, vols = [], [], [], [], [], []
for b in bars_301358:
    dates.append(b['date'])
    opens.append(b['open']); closes.append(b['close'])
    highs.append(b['high']); lows.append(b['low'])
    vols.append(b['volume'])

dates = np.array(dates)
opens, closes, highs, lows, vols = map(np.array, [opens, closes, highs, lows, vols])

# 转日期
dt_dates = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
n = len(dates)

# === 技术指标计算 ===
# 均线
def sma(data, period):
    result = np.full_like(data, np.nan, dtype=float)
    for i in range(period-1, len(data)):
        result[i] = np.mean(data[i-period+1:i+1])
    return result

ma5 = sma(closes, 5)
ma10 = sma(closes, 10)
ma20 = sma(closes, 20)
ma60 = sma(closes, 60)

# 布林带(20日, 2倍标准差)
bb_mid = ma20
bb_std = np.full_like(closes, np.nan, dtype=float)
for i in range(19, n):
    bb_std[i] = np.std(closes[i-19:i+1])
bb_upper = bb_mid + 2 * bb_std
bb_lower = bb_mid - 2 * bb_std

# 筹码分布(简化:用90天成交量加权价格分布)
price_min, price_max = lows.min(), highs.max()
bins = np.linspace(price_min, price_max, 80)
chip_dist = np.zeros(len(bins)-1)
for i in range(n):
    for j in range(len(bins)-1):
        if lows[i] <= bins[j+1] and highs[i] >= bins[j]:
            overlap = min(highs[i], bins[j+1]) - max(lows[i], bins[j])
            if overlap > 0:
                chip_dist[j] += vols[i] * overlap / (highs[i] - lows[i] + 0.001)

# 筹码峰值(支撑/压力)
chip_centers = (bins[:-1] + bins[1:]) / 2
# 找筹码集中峰
from scipy.signal import argrelextrema
try:
    peaks = argrelextrema(chip_dist, np.greater, order=5)[0]
except:
    peaks = []

# 支撑位/压力位判断
# 1. 筹码峰
# 2. 均线
# 3. 近期高低点
recent_30 = closes[-30:]
support_1 = np.percentile(recent_30, 10)  # 近30日10%分位
resist_1 = np.percentile(recent_30, 90)  # 近30日90%分位

# 当前价
current_price = closes[-1]
current_date = dates[-1]

# 支撑位
support_levels = []
# 筹码峰支撑
for p in peaks:
    if chip_centers[p] < current_price:
        support_levels.append((chip_centers[p], chip_dist[p], '筹码峰'))
# 布林下轨
if not np.isnan(bb_lower[-1]):
    support_levels.append((bb_lower[-1], 0, 'BOLL下轨'))
# 近期低点
support_levels.append((support_1, 0, '30日10%分位'))
# MA60
if not np.isnan(ma60[-1]):
    support_levels.append((ma60[-1], 0, 'MA60'))

# 压力位
resist_levels = []
for p in peaks:
    if chip_centers[p] > current_price:
        resist_levels.append((chip_centers[p], chip_dist[p], '筹码峰'))
if not np.isnan(bb_upper[-1]):
    resist_levels.append((bb_upper[-1], 0, 'BOLL上轨'))
resist_levels.append((resist_1, 0, '30日90%分位'))
# 近期高点
recent_high = np.max(highs[-30:])
resist_levels.append((recent_high, 0, '30日最高'))

# 去重排序
support_levels = sorted(set([(round(s[0],2), s[2]) for s in support_levels]), reverse=True)
resist_levels = sorted(set([(round(r[0],2), r[2]) for r in resist_levels]))

# === 量能分析 ===
vol_ma5 = sma(vols.astype(float), 5)
vol_ma20 = sma(vols.astype(float), 20)

# 换手率估算(流通股本7.69亿)
float_shares = 7.69e8
turnover = vols * 100 / float_shares * 100  # 百分比

# === 主力意图标注(关键事件) ===
events = []
# 找大涨大跌日
for i in range(n):
    chg = (closes[i] - closes[i-1]) / closes[i-1] * 100 if i > 0 else 0
    if chg > 5:
        events.append((dt_dates[i], f'+{chg:.1f}%', 'red', 'top'))
    elif chg < -5:
        events.append((dt_dates[i], f'{chg:.1f}%', 'green', 'bottom'))

# 标注已知事件
event_labels = {
    '2026-05-13': '主力净流出1.67亿',
    '2026-05-25': '主力净流出4.93亿\n跌3.71%',
    '2026-06-03': '宁德+津晟\n减持公告',
    '2026-06-26': '减持窗口开启',
    '2026-07-17': '涨价函公告\n+终止铜冶炼',
    '2026-07-22': '240亿扩产\n主力翻负',
    '2026-07-23': '+8.96%暴涨\n大宗13笔50万股',
}

# === 可比标的归一化 ===
def normalize(data_dict, key):
    _, o, c, h, l, v = parse_bars(data_dict, key)
    # 归一化到301358第一根收盘价
    base = c[0]
    return c / base * closes[0]

cmp_300750 = normalize(load_data('/tmp/300750_daily.json'), 'sz300750')
cmp_300769 = normalize(load_data('/tmp/300769_daily.json'), 'sz300769')
cmp_300432 = normalize(load_data('/tmp/300432_daily.json'), 'sz300432')

# 创业板指
_, _, c399006, _, _, _ = parse_bars(load_data('/tmp/399006_daily.json'), 'sz399006')
# 对齐日期
cmp_399006 = c399006[:n] / c399006[0] * closes[0]

# 可比对齐(取最后99根)
cmp_dates_300750 = parse_bars(load_data('/tmp/300750_daily.json'), 'sz300750')[0]
# 因为所有标的都是99根同期,直接用

# ======================== 绘图 ========================
fig = plt.figure(figsize=(24, 36), facecolor='#1a1a2e')
gs = fig.add_gridspec(6, 2, height_ratios=[3, 1, 1.5, 1, 1, 0.8], 
                       hspace=0.15, wspace=0.08,
                       left=0.07, right=0.93, top=0.96, bottom=0.03)

# 颜色(红涨绿跌)
UP = '#E74C3C'  # 红色
DOWN = '#2ECC71'  # 绿色
GRID = '#2a2a4a'
TEXT = '#E0E0E0'
BG = '#1a1a2e'

# --- 子图1: K线图 + 均线 + 支撑压力 ---
ax1 = fig.add_subplot(gs[0, :])
ax1.set_facecolor(BG)

x = np.arange(n)
width = 0.6

for i in range(n):
    color = UP if closes[i] >= opens[i] else DOWN
    # 影线
    ax1.plot([x[i], x[i]], [lows[i], highs[i]], color=color, linewidth=0.8, zorder=1)
    # 实体
    body_bottom = min(opens[i], closes[i])
    body_height = abs(closes[i] - opens[i]) + 0.01
    rect = FancyBboxPatch((x[i]-width/2, body_bottom), width, body_height,
                          boxstyle='square,pad=0', facecolor=color, 
                          edgecolor=color, linewidth=0.5, zorder=2)
    ax1.add_patch(rect)

# 均线
for ma, label, color in [(ma5, 'MA5', '#FFD700'), (ma10, 'MA10', '#FF6B35'), 
                          (ma20, 'MA20', '#4ECDC4'), (ma60, 'MA60', '#A569BD')]:
    ax1.plot(x, ma, color=color, linewidth=1.2, label=label, alpha=0.8)

# 布林带
ax1.fill_between(x, bb_upper, bb_lower, alpha=0.08, color='#4ECDC4', label='BOLL带')

# 支撑位(绿色虚线)
for i, (price, label) in enumerate(support_levels[:4]):
    ax1.axhline(y=price, color='#2ECC71', linestyle='--', linewidth=1, alpha=0.6)
    ax1.text(x[-1]+1, price, f'支撑 {price:.2f} [{label}]', color='#2ECC71', 
             fontsize=8, va='center', alpha=0.9)

# 压力位(红色虚线)
for i, (price, label) in enumerate(resist_levels[:4]):
    ax1.axhline(y=price, color='#E74C3C', linestyle='--', linewidth=1, alpha=0.6)
    ax1.text(x[-1]+1, price, f'压力 {price:.2f} [{label}]', color='#E74C3C',
             fontsize=8, va='center', alpha=0.9)

# 事件标注
for date_str, label in event_labels.items():
    try:
        idx = list(dates).index(date_str)
        ax1.annotate(label, xy=(idx, highs[idx]), 
                    xytext=(idx, highs[idx]+3),
                    fontsize=7, color='#FFD700', ha='center',
                    arrowprops=dict(arrowstyle='->', color='#FFD700', lw=0.8),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#2a2a4a', alpha=0.8, edgecolor='#FFD700'))
    except ValueError:
        pass

# 大涨大跌标注
for dt, text, color, pos in events:
    idx = (dt - dt_dates[0]).days
    # 找最近的x
    try:
        i = dt_dates.index(dt)
        if pos == 'top':
            ax1.annotate(text, xy=(i, highs[i]), xytext=(i, highs[i]+2),
                        fontsize=6, color=color, ha='center', alpha=0.7)
    except:
        pass

ax1.set_xlim(-2, n+15)
ax1.set_title('301358 湖南裕能 — 90天日K线综合分析 (2026-03-02 → 2026-07-23)', 
              color=TEXT, fontsize=16, fontweight='bold', pad=15)
ax1.legend(loc='upper left', fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=TEXT)
ax1.grid(True, color=GRID, alpha=0.3)
ax1.tick_params(colors=TEXT, labelsize=8)
for spine in ax1.spines.values():
    spine.set_color(GRID)

# X轴日期
date_ticks = list(range(0, n, 10))
date_labels = [dates[i] for i in date_ticks]
ax1.set_xticks(date_ticks)
ax1.set_xticklabels(date_labels, rotation=30, ha='right', fontsize=8)

# 当前价标注
ax1.axhline(y=current_price, color='#FFFFFF', linestyle='-', linewidth=0.8, alpha=0.5)
ax1.text(x[-1]+1, current_price, f'当前 {current_price:.2f}', color='#FFFFFF',
         fontsize=9, va='center', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.2', facecolor='#E74C3C', alpha=0.7))

# --- 子图2: 成交量 ---
ax2 = fig.add_subplot(gs[1, :], sharex=ax1)
ax2.set_facecolor(BG)
for i in range(n):
    color = UP if closes[i] >= opens[i] else DOWN
    ax2.bar(x[i], vols[i]/10000, width=width, color=color, alpha=0.7)
ax2.plot(x, vol_ma5/10000, color='#FFD700', linewidth=1, label='量MA5')
ax2.plot(x, vol_ma20/10000, color='#4ECDC4', linewidth=1, label='量MA20')
ax2.set_ylabel('成交量(万手)', color=TEXT, fontsize=9)
ax2.legend(loc='upper left', fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=TEXT)
ax2.grid(True, color=GRID, alpha=0.3)
ax2.tick_params(colors=TEXT, labelsize=7)
for spine in ax2.spines.values():
    spine.set_color(GRID)

# --- 子图3: 筹码分布(横向) ---
ax3 = fig.add_subplot(gs[2, 0])
ax3.set_facecolor(BG)
ax3.barh(chip_centers, chip_dist/np.sum(chip_dist)*100, height=(bins[1]-bins[0])*0.8, 
         color='#4ECDC4', alpha=0.6)
ax3.axhline(y=current_price, color='#FFFFFF', linestyle='-', linewidth=1.5, label=f'当前价 {current_price:.2f}')
# 筹码峰标注
for p in peaks:
    ax3.annotate(f'峰:{chip_centers[p]:.1f}', xy=(chip_dist[p]/np.sum(chip_dist)*100, chip_centers[p]),
                xytext=(chip_dist[p]/np.sum(chip_dist)*100+0.3, chip_centers[p]),
                fontsize=7, color='#FFD700')
ax3.set_xlabel('筹码占比(%)', color=TEXT, fontsize=9)
ax3.set_ylabel('价格(元)', color=TEXT, fontsize=9)
ax3.set_title('筹码分布(90天成交量加权)', color=TEXT, fontsize=11)
ax3.legend(loc='upper right', fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=TEXT)
ax3.grid(True, color=GRID, alpha=0.3)
ax3.tick_params(colors=TEXT, labelsize=8)
for spine in ax3.spines.values():
    spine.set_color(GRID)

# --- 子图4: 换手率 ---
ax4 = fig.add_subplot(gs[2, 1])
ax4.set_facecolor(BG)
ax4.bar(x, turnover, width=width, color='#FF6B35', alpha=0.6)
ax4.axhline(y=3, color='#E74C3C', linestyle='--', linewidth=1, label='3%警戒线')
ax4.axhline(y=np.mean(turnover[turnover>0]), color='#FFD700', linestyle='--', linewidth=1, 
            label=f'均值{np.mean(turnover[turnover>0]):.2f}%')
ax4.set_title('换手率(%)', color=TEXT, fontsize=11)
ax4.set_xlabel('交易日', color=TEXT, fontsize=9)
ax4.legend(loc='upper right', fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=TEXT)
ax4.grid(True, color=GRID, alpha=0.3)
ax4.tick_params(colors=TEXT, labelsize=8)
for spine in ax4.spines.values():
    spine.set_color(GRID)

# --- 子图5: 可比标的归一化对比 ---
ax5 = fig.add_subplot(gs[3, :], sharex=ax1)
ax5.set_facecolor(BG)
ax5.plot(x, closes, color='#E74C3C', linewidth=2, label='301358 湖南裕能')
# 对齐长度
m = min(len(cmp_300750), len(closes))
ax5.plot(x[:m], cmp_300750[:m], color='#4ECDC4', linewidth=1.5, label='300750 宁德时代', alpha=0.8)
m2 = min(len(cmp_300769), m)
ax5.plot(x[:m2], cmp_300769[:m2], color='#FFD700', linewidth=1.5, label='300769 德方纳米', alpha=0.8)
m3 = min(len(cmp_300432), m2)
ax5.plot(x[:m3], cmp_300432[:m3], color='#A569BD', linewidth=1.5, label='300432 富临精工', alpha=0.8)
m4 = min(len(cmp_399006), m3)
ax5.plot(x[:m4], cmp_399006[:m4], color='#FF6B35', linewidth=1.5, label='399006 创业板指', alpha=0.8)

ax5.set_title('可比标的归一化对比(起点=301358首发收盘)', color=TEXT, fontsize=11)
ax5.legend(loc='upper left', fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=TEXT)
ax5.grid(True, color=GRID, alpha=0.3)
ax5.tick_params(colors=TEXT, labelsize=8)
for spine in ax5.spines.values():
    spine.set_color(GRID)

# --- 子图6: 支撑压力位表格 ---
ax6 = fig.add_subplot(gs[4, 0])
ax6.set_facecolor(BG)
ax6.axis('off')

# 表格数据
table_data = []
# 压力位
for price, label in resist_levels[:5]:
    dist = (price - current_price) / current_price * 100
    table_data.append(['压力', f'{price:.2f}', label, f'+{dist:.1f}%'])
# 当前价
table_data.append(['★当前', f'{current_price:.2f}', '2026-07-23收盘', '0%'])
# 支撑位
for price, label in support_levels[:5]:
    dist = (price - current_price) / current_price * 100
    table_data.append(['支撑', f'{price:.2f}', label, f'{dist:.1f}%'])

table = ax6.table(cellText=table_data, 
                   colLabels=['类型', '价格(元)', '依据', '距当前'],
                   cellLoc='center', loc='center',
                   colWidths=[0.15, 0.15, 0.4, 0.15])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.5)
# 颜色
for i in range(len(table_data)):
    for j in range(4):
        cell = table[i+1, j]
        if i < len(resist_levels[:5]):
            cell.set_facecolor('#3a1a1a')
            cell.set_text_props(color='#E74C3C')
        elif i == len(resist_levels[:5]):
            cell.set_facecolor('#2a2a4a')
            cell.set_text_props(color='#FFFFFF', fontweight='bold')
        else:
            cell.set_facecolor('#1a3a1a')
            cell.set_text_props(color='#2ECC71')
for j in range(4):
    table[0, j].set_facecolor('#2a2a5a')
    table[0, j].set_text_props(color='#FFFFFF', fontweight='bold')

ax6.set_title('支撑位 / 压力位 一览', color=TEXT, fontsize=12, pad=10)

# --- 子图7: 主力意图分析 ---
ax7 = fig.add_subplot(gs[4, 1])
ax7.set_facecolor(BG)
ax7.axis('off')

intent_text = """
主力意图分析 (90天)
━━━━━━━━━━━━━━━━━━━━━━━━━
① 3月-5月: 90→98元 主力拉升
   量能持续放大 + 换手3-5%
   → 建仓+拉高阶段

② 5月13日: 98→96元 放量跌
   主力净流出1.67亿
   → 首次大规模派发

③ 5月25日: 88→84元 跌3.7%
   主力净流出4.93亿
   → 暴力出货日

④ 6月3日: 宁德+津晟减持公告
   → 利空压制 75→60

⑤ 6月26日-7月22日: 60±2画框
   缩量+换手<3% → 减持期低迷

⑥ 7月23日: +8.96%暴涨
   主力净流入仅+1304万
   大宗13笔50万股(折价-9.1%)
   → 拉高+大宗减持组合拳

⑦ 7月24日: 冲高67→回落64
   缩量62% + 外盘<内盘
   → 试盘失败+回归画框
"""
ax7.text(0.05, 0.95, intent_text, transform=ax7.transAxes,
         fontsize=10, color=TEXT, va='top', ha='left',
         family='WenQuanYi Zen Hei',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#2a2a4a', alpha=0.8, edgecolor=GRID))
ax7.set_title('主力意图归因', color=TEXT, fontsize=12, pad=10)

# --- 子图8: 板块对比统计 ---
ax8 = fig.add_subplot(gs[5, :])
ax8.set_facecolor(BG)
ax8.axis('off')

# 计算各标的涨跌幅
def calc_stats(closes_arr, name):
    if len(closes_arr) < 2:
        return name, 0, 0, 0, 0
    total_ret = (closes_arr[-1] / closes_arr[0] - 1) * 100
    max_price = np.max(closes_arr)
    min_price = np.min(closes_arr)
    max_drawdown = (np.min(closes_arr[np.argmax(closes_arr):]) / np.max(closes_arr) - 1) * 100 if len(closes_arr) > 1 else 0
    vol_ratio = np.std(closes_arr) / np.mean(closes_arr) * 100
    return name, total_ret, max_drawdown, vol_ratio, closes_arr[-1]

stats_301358 = calc_stats(closes, '301358 湖南裕能')
stats_300750 = calc_stats(cmp_300750, '300750 宁德时代')
stats_300769 = calc_stats(cmp_300769, '300769 德方纳米')
stats_300432 = calc_stats(cmp_300432, '300432 富临精工')
stats_399006 = calc_stats(cmp_399006, '399006 创业板指')

stats_data = [stats_301358, stats_300750, stats_300769, stats_300432, stats_399006]
table2 = ax8.table(cellText=stats_data,
                    colLabels=['标的', '90天涨跌幅(%)', '最大回撤(%)', '波动率(%)', '最新归一化价'],
                    cellLoc='center', loc='center',
                    colWidths=[0.2, 0.15, 0.15, 0.15, 0.15])
table2.auto_set_font_size(False)
table2.set_fontsize(10)
table2.scale(1, 1.5)
for j in range(5):
    table2[0, j].set_facecolor('#2a2a5a')
    table2[0, j].set_text_props(color='#FFFFFF', fontweight='bold')
for i in range(len(stats_data)):
    for j in range(5):
        cell = table2[i+1, j]
        if i == 0:
            cell.set_facecolor('#3a1a1a')
            cell.set_text_props(color='#E74C3C', fontweight='bold')
        else:
            ret = stats_data[i][1]
            if ret > 0:
                cell.set_facecolor('#1a2a2a')
                cell.set_text_props(color='#2ECC71')
            else:
                cell.set_facecolor('#2a1a1a')
                cell.set_text_props(color='#E74C3C')

ax8.set_title('板块可比标的统计对比 (90天)', color=TEXT, fontsize=12, pad=10)

plt.savefig('/data/hermes/workspace/301358_90d_analysis.png', dpi=150, 
            facecolor=BG, edgecolor='none', bbox_inches='tight')
print("图表已保存: /data/hermes/workspace/301358_90d_analysis.png")

# 输出关键数据
print(f"\n=== 关键支撑/压力位 ===")
print(f"当前价: {current_price:.2f}")
print(f"\n压力位(由近及远):")
for p, l in resist_levels[:5]:
    print(f"  {p:.2f} [{l}]  +{(p-current_price)/current_price*100:.1f}%")
print(f"\n支撑位(由近及远):")
for p, l in support_levels[:5]:
    print(f"  {p:.2f} [{l}]  {(p-current_price)/current_price*100:.1f}%")

print(f"\n=== 筹码峰 ===")
for p in peaks:
    pct = chip_dist[p] / np.sum(chip_dist) * 100
    side = "压力" if chip_centers[p] > current_price else "支撑"
    print(f"  {chip_centers[p]:.2f}元 占比{pct:.1f}% → {side}")

print(f"\n=== 均线 ===")
print(f"MA5={ma5[-1]:.2f}  MA10={ma10[-1]:.2f}  MA20={ma20[-1]:.2f}  MA60={ma60[-1]:.2f}")
print(f"BOLL: 上轨={bb_upper[-1]:.2f}  中轨={bb_mid[-1]:.2f}  下轨={bb_lower[-1]:.2f}")

print(f"\n=== 可比标的90天涨跌 ===")
for s in stats_data:
    print(f"  {s[0]}: {s[1]:+.1f}%  回撤:{s[2]:.1f}%  波动:{s[3]:.1f}%")
