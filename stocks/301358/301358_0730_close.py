#!/usr/bin/env python3
"""301358 7/30收盘综合分析 — 消息面/主力成本/筹码峰/股东/板块对比/主力意图"""
import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

for fp in ['/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc']:
    try:
        font_manager.fontManager.addfont(fp); break
    except: pass
plt.rcParams['font.family'] = 'WenQuanYi Zen Hei'
plt.rcParams['axes.unicode_minus'] = False

BG = '#1a1a2e'; TEXT = '#E0E0E0'; GRID = '#2a2a4a'
UP = '#E74C3C'; DOWN = '#2ECC71'

# === 分时数据 ===
with open('/tmp/301358_t_0730.json') as f:
    raw = json.load(f)
bars = raw if isinstance(raw, list) else raw.get('data', [])
times, prices, vols, amts = [], [], [], []
prev_v = 0; prev_a = 0
for it in bars:
    t = it['time']; p = it['price']
    v = it['volume'] - prev_v; a = it['amount'] - prev_a
    prev_v = it['volume']; prev_a = it['amount']
    times.append(t); prices.append(p); vols.append(v); amts.append(a)
prices = np.array(prices); vols = np.array(vols); amts = np.array(amts)

# === 日K数据 ===
with open('/tmp/301358_60d.json') as f:
    kd = json.load(f)
sd = kd['data']['sz301358']
kb = sd.get('qfqday') or sd.get('day') or list(sd.values())[0]
daily = [{'d':b[0],'o':float(b[1]),'c':float(b[2]),'h':float(b[3]),'l':float(b[4]),
          'v':int(float(b[5])) if len(b)>5 else 0} for b in kb]
# 补7/30
daily.append({'d':'2026-07-30','o':64.30,'c':64.18,'h':65.60,'l':63.57,'v':158655})
closes = [d['c'] for d in daily]
ma5 = np.mean(closes[-5:]); ma10 = np.mean(closes[-10:]); ma20 = np.mean(closes[-20:]); ma30 = np.mean(closes[-30:])

print(f"数据: 分时{len(bars)}条, 日K{len(daily)}条, MA5={ma5:.2f} MA20={ma20:.2f}")
print(f"7/30: 开64.30 收64.18 H65.60 L63.57 量15.87万手")

# === 绘图 ===
fig = plt.figure(figsize=(28, 28), facecolor=BG)
gs = fig.add_gridspec(5, 2, height_ratios=[3, 1.5, 2, 2, 3],
                      hspace=0.10, wspace=0.08,
                      left=0.05, right=0.96, top=0.97, bottom=0.02)

# --- 子图1: 分时 ---
ax1 = fig.add_subplot(gs[0, :]); ax1.set_facecolor(BG)
x = np.arange(len(prices))
ax1.plot(x, prices, color='#FFD700', linewidth=1.5, zorder=3)
ax1.axhline(y=64.60, color='#888', linestyle='--', linewidth=1, alpha=0.5, label='昨收 64.60')
cum_a = np.cumsum(amts); cum_v = np.cumsum(vols)
avg = np.where(cum_v > 0, cum_a / cum_v / 100, prices[0])
ax1.plot(x, avg, color='#4ECDC4', linewidth=1, alpha=0.7, label='均价线')

for i in range(len(prices)-1):
    c = UP if prices[i] >= 64.60 else DOWN
    ax1.fill_between([x[i], x[i+1]], prices[i], 64.60, alpha=0.05, color=c)

# 标注
idx_low = np.argmin(prices)
ax1.annotate(f'最低 {prices[idx_low]:.2f}\n{times[idx_low]}', xy=(idx_low, prices[idx_low]),
            xytext=(idx_low+15, prices[idx_low]-1.5), fontsize=10, color=DOWN, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=DOWN, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a3a1a', alpha=0.9, edgecolor=DOWN))

idx_high = np.argmax(prices)
ax1.annotate(f'最高 {prices[idx_high]:.2f}\n{times[idx_high]}', xy=(idx_high, prices[idx_high]),
            xytext=(idx_high+5, prices[idx_high]+0.8), fontsize=10, color=UP, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=UP, lw=1.2),
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#3a1a1a', alpha=0.9, edgecolor=UP))

# 13:08拉升
for i,t in enumerate(times):
    if t == '13:08':
        ax1.annotate(f'13:08 午后拉升\n+0.59元', xy=(i, prices[i]),
                    xytext=(i-40, prices[i]+1.5), fontsize=10, color=UP, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color=UP, lw=1.5),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#3a1a1a', alpha=0.9, edgecolor=UP))
        break

for px, c, lbl in [(60.00, '#2ECC71', '支撑60'), (61.17, '#27AE60', '支撑61.17'),
                    (64.60, '#888', '昨收64.60'), (65.22, '#E74C3C', 'MA20=65.22'), (67.52, '#C0392B', '压力67.52')]:
    ax1.axhline(y=px, color=c, linestyle=':', linewidth=1.2, alpha=0.4)
    ax1.text(len(prices)+1, px, lbl, color=c, fontsize=8)

ax1.set_xlim(-2, len(prices)+25)
ax1.set_title('301358 湖南裕能 — 7/30收盘分时 (收64.18 -0.65%, 创业板指暴跌-3.97%中个股抗跌)',
              color=TEXT, fontsize=15, fontweight='bold', pad=15)
ax1.legend(loc='upper right', fontsize=9, facecolor=BG, edgecolor=GRID, labelcolor=TEXT)
ax1.grid(True, color=GRID, alpha=0.3)
ax1.tick_params(colors=TEXT, labelsize=8)
for s in ax1.spines.values(): s.set_color(GRID)
tp = list(range(0, len(prices), 15))
ax1.set_xticks(tp)
ax1.set_xticklabels([times[i] if i < len(times) else '' for i in tp], rotation=30, ha='right', fontsize=8)

# 成交量
ax1b = ax1.twinx(); ax1b.set_facecolor(BG)
ax1b.bar(x, vols/10000, width=0.8, color=[UP if prices[i] >= 64.60 else DOWN for i in range(len(vols))], alpha=0.2)
ax1b.set_ylabel('成交量(万手)', color='#888', fontsize=9)
ax1b.tick_params(colors='#888', labelsize=7)
ax1b.set_ylim(0, max(vols/10000)*3)
for s in ax1b.spines.values(): s.set_color(GRID)

# --- 子图2: 日K线(15天) + MA ---
ax2 = fig.add_subplot(gs[1, :]); ax2.set_facecolor(BG)
last15 = daily[-15:]
for i, d in enumerate(last15):
    o, c, h, l = d['o'], d['c'], d['h'], d['l']
    color = UP if c >= o else DOWN
    ax2.plot([i, i], [l, h], color=color, linewidth=1.2, alpha=0.8)
    rect = plt.Rectangle((i-0.3, min(o,c)), 0.6, max(abs(c-o),0.01), facecolor=color, edgecolor=color, alpha=0.85)
    ax2.add_patch(rect)
    chg = (c - o) / o * 100
    ax2.text(i, h+0.3, f'{d["d"][8:]}\n{chg:+.1f}%', ha='center', fontsize=7, color=color, fontweight='bold')

ax2.axhline(y=ma5, color='#FFD700', linestyle='--', linewidth=1, alpha=0.6, label=f'MA5={ma5:.2f}')
ax2.axhline(y=ma10, color='#4ECDC4', linestyle='--', linewidth=1, alpha=0.6, label=f'MA10={ma10:.2f}')
ax2.axhline(y=ma20, color='#E74C3C', linestyle='--', linewidth=1, alpha=0.6, label=f'MA20={ma20:.2f}')
ax2.axhline(y=61.17, color='#2ECC71', linestyle=':', linewidth=1, alpha=0.5, label='支撑61.17')
ax2.set_xlim(-0.5, len(last15)-0.5)
ax2.set_ylim(55, 75)
ax2.set_title('近15日K线 (7/10-7/30) + 均线系统', color=TEXT, fontsize=12, fontweight='bold')
ax2.legend(loc='upper left', fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=TEXT, ncol=4)
ax2.grid(True, color=GRID, alpha=0.3)
ax2.tick_params(colors=TEXT, labelsize=8)
for s in ax2.spines.values(): s.set_color(GRID)

# --- 子图3: 60日筹码分布 ---
ax3 = fig.add_subplot(gs[2, 0]); ax3.set_facecolor(BG)
wp = []
for b in kb[-60:]:
    avg = (float(b[1])+float(b[2])+float(b[3])+float(b[4]))/4
    vv = int(float(b[5])) if len(b)>5 else 100000
    wp.extend([avg] * min(vv//10000, 30))
wp = np.array(wp)
bins = np.arange(55, 95, 1)
counts, edges = np.histogram(wp, bins=bins)
centers = (edges[:-1]+edges[1:])/2
max_c = max(counts) if max(counts) > 0 else 1
colors = [UP if centers[i] <= 64.18 else DOWN for i in range(len(counts))]
ax3.barh(centers, counts*30/max_c, height=0.9, color=colors, alpha=0.5)
ax3.axhline(y=64.18, color='#FFD700', linewidth=2, label=f'当前价 64.18')
ax3.axhline(y=88.75, color='#9B59B6', linestyle='--', linewidth=1.5, label='裕富减持均价 88.75')
ax3.axhline(y=60.00, color='#2ECC71', linestyle=':', linewidth=1.2, label='画框底 60')
# 标注筹码峰
for i in range(len(counts)):
    if counts[i] > max_c * 0.25:
        ax3.text(counts[i]*30/max_c + 0.5, centers[i], f'{centers[i]:.0f}', fontsize=7, color=TEXT, va='center')
ax3.set_xlabel('筹码密度', color=TEXT, fontsize=9)
ax3.set_ylabel('价格(元)', color=TEXT, fontsize=9)
ax3.set_title('60日筹码分布 (红=获利盘 绿=套牢盘)', color=TEXT, fontsize=11, fontweight='bold')
ax3.legend(loc='upper right', fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=TEXT)
ax3.grid(True, color=GRID, alpha=0.3)
ax3.tick_params(colors=TEXT, labelsize=8)
ax3.set_ylim(55, 95)
for s in ax3.spines.values(): s.set_color(GRID)

# --- 子图4: 电池板块强弱对比 ---
ax4 = fig.add_subplot(gs[2, 1]); ax4.set_facecolor(BG)
stocks = ['301358\n湖南裕能', '300750\n宁德时代', '300769\n德方纳米', '300432\n富临精工', 
          '002340\n格林美', '300037\n新宙邦', '002812\n恩捷股份', '399006\n创业板指']
chg_0730 = [-0.65, +1.27, -2.62, -0.95, +0.15, -1.07, -0.36, -3.97]
colors4 = [UP if c > 0 else (DOWN if c < 0 else '#888') for c in chg_0730]
x4 = np.arange(len(stocks))
bars4 = ax4.bar(x4, chg_0730, 0.6, color=colors4, alpha=0.7)
for i, v in enumerate(chg_0730):
    ax4.text(i, v+0.1 if v > 0 else v-0.2, f'{v:+.2f}%', ha='center', fontsize=9, color=colors4[i], fontweight='bold')
ax4.axhline(y=0, color='#888', linewidth=0.5)
ax4.set_xticks(x4)
ax4.set_xticklabels(stocks, fontsize=8, color=TEXT)
ax4.set_ylabel('涨跌幅(%)', color=TEXT, fontsize=9)
ax4.set_title('7/30电池板块涨跌对比: 301358仅-0.65% vs 创业板-3.97% → 严重抗跌', color=TEXT, fontsize=10, fontweight='bold')
ax4.grid(True, color=GRID, alpha=0.3, axis='y')
ax4.tick_params(colors=TEXT, labelsize=8)
for s in ax4.spines.values(): s.set_color(GRID)

# --- 子图5: 股东持股变化 ---
ax5 = fig.add_subplot(gs[3, 0]); ax5.set_facecolor(BG)
# 股东持股比例变化
holders = ['宁德时代', '上海津晟', '湖南裕富']
before = [7.10, 7.89, 5.32]  # Q1初
after = [6.85, 7.89, 4.90]   # 7/30
xh = np.arange(len(holders))
w = 0.35
ax5.bar(xh - w/2, before, w, color='#3498DB', alpha=0.7, label='减持前')
ax5.bar(xh + w/2, after, w, color='#E74C3C', alpha=0.7, label='当前(7/30)')
for i in range(len(holders)):
    delta = after[i] - before[i]
    ax5.text(i, max(before[i], after[i]) + 0.3, f'{delta:+.2f}%', ha='center', fontsize=10,
             color='#E74C3C' if delta < 0 else '#2ECC71', fontweight='bold')
ax5.set_xticks(xh)
ax5.set_xticklabels(holders, fontsize=10, color=TEXT)
ax5.set_ylabel('持股比例(%)', color=TEXT, fontsize=9)
ax5.set_title('三大股东持股比例变化 (蓝=减持前 红=当前)', color=TEXT, fontsize=11, fontweight='bold')
ax5.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=TEXT)
ax5.grid(True, color=GRID, alpha=0.3, axis='y')
ax5.tick_params(colors=TEXT, labelsize=8)
for s in ax5.spines.values(): s.set_color(GRID)
# 加标注
ax5.text(0.5, -0.15, '湖南裕富7/29提前终止减持\n剩余63.22万股不再减持',
         transform=ax5.transAxes, fontsize=8, color='#2ECC71', ha='center', fontweight='bold')

# --- 子图6: 7日涨跌 + 大盘对比 ---
ax6 = fig.add_subplot(gs[3, 1]); ax6.set_facecolor(BG)
labels6 = ['7/24', '7/27', '7/28', '7/29', '7/30']
chg6_301 = [-1.1, +0.8, -2.8, +2.3, -0.65]  # 用实际K线的open→close
chg6_cyb = [-2.65, +2.94, -7.35, +1.55, -3.97]
chg6_catl = [-1.5, +4.56, -2.29, +1.27, +1.27]
x6 = np.arange(len(labels6))
w6 = 0.25
colors_301 = '#FFD700'; colors_cyb = '#4ECDC4'; colors_catl = '#9B59B6'
ax6.bar(x6 - w6, chg6_301, w6, color=colors_301, alpha=0.85, label='301358')
ax6.bar(x6, chg6_cyb, w6, color=colors_cyb, alpha=0.85, label='创业板指')
ax6.bar(x6 + w6, chg6_catl, w6, color=colors_catl, alpha=0.85, label='宁德时代')
ax6.axhline(y=0, color='#888', linewidth=0.5)
for i, v in enumerate(chg6_301):
    ax6.text(i-w6, v+0.15 if v > 0 else v-0.4, f'{v:+.1f}%', ha='center', fontsize=8, color=colors_301, fontweight='bold')
ax6.set_xticks(x6)
ax6.set_xticklabels(labels6, fontsize=9, color=TEXT)
ax6.set_ylabel('涨跌幅(%)', color=TEXT, fontsize=9)
ax6.set_title('5日涨跌对比: 7/30 301358(-0.65%) vs 创业板(-3.97%) → 超越大盘3.32%', color=TEXT, fontsize=10, fontweight='bold')
ax6.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=TEXT)
ax6.grid(True, color=GRID, alpha=0.3, axis='y')
ax6.tick_params(colors=TEXT, labelsize=8)
for s in ax6.spines.values(): s.set_color(GRID)

# --- 子图7: 综合分析文字 ---
ax7 = fig.add_subplot(gs[4, :]); ax7.set_facecolor(BG); ax7.axis('off')
summary = """【7/30收盘综合分析 — GMT+08:00 15:17 收盘后】

═══ 一、消息面 ═══
  ① 7/29盘后公告(2026-060): 湖南裕富提前终止减持计划(原395万股,实际减332万股@88.75元,剩余63.22万股不再减) → 利空出清1/3,利好信号
  ② 7/30创业板暴跌-3.97%: AI硬件/半导体/CPO大幅领跌,创业板指抹平年内全部涨幅(曾涨35%) → 系统性利空
  ③ 磷酸铁锂涨价函8/1生效倒计时2天: 湖南裕能率先调价+2000元/吨 → 基本面支撑
  ④ 宁德时代6/26首减210.5万股(0.25%),已降至6.85%,触及1%整数倍 → 减持窗口进行中(至9/25,余56天)

═══ 二、主力成本估算 ═══
  60日加权均价(主力成本区): 70.5元  |  30日加权均价: 65.8元  |  7月密集区: 62-66元
  当前价64.18 < 30日均价65.8 < 60日均价70.5 → 主力整体浮亏,短期成本线在65-66

═══ 三、筹码峰分析 ═══
  最大峰: 74-76元(7.3%+6.8%=14.1%) → 90天最大套牢区,反弹巨大压力
  次大峰: 60-64元(14.8%) → 当前价格区域=主力7月建仓+护盘区
  特征: 双峰形态,60-64底部+74-76顶部,中间65-70筹码稀疏=反弹空间大但上方压力大
  裕富减持均价88.75元 = 高位精准减持,低位(63元)宣布不再卖

═══ 四、股东人数与持仓变化 ═══
  股东人数: 2026Q1 4.95万户(较2025年末+23.11%) → 筹码分散,散户涌入
  户均持股: 1.54万股(较上期1.89万降18.5%) → 户均降低=散户化
  三大股东:  宁德时代 7.10%→6.85%(已减0.25%,剩余2.75%额度)
    上海津晟 7.89%(暂未减,额度2.5%)
    湖南裕富 5.32%→4.90%(已终止,剩余0.08%不再减)
  结论: 大股东在减,散户在接,筹码从集中走向分散

═══ 五、与电池板块类比 ═══
  7/30涨跌:  301358 -0.65% | 宁德时代 +1.27% | 德方纳米 -2.62% | 富临精工 -0.95% | 创业板指 -3.97%
  ★ 301358严重抗跌: -0.65% vs 创业板-3.97% = 超越大盘3.32个百分点
  ★ 宁德时代逆势+1.27%(电池龙头独立行情,减持窗口内需维护价格)
  ★ 德方纳米-2.62%最弱(正极材料二线,无减持护盘)
  板块结论: 301358在电池板块中属于"强抗跌型",强于德方/富临,弱于宁德(宁德有逆势买入逻辑)

═══ 六、主力意图与后续操作预判 ═══
  【主力行为链 7/23-7/30】
  7/23 +8.3% 拉高 → 7/24 -1.1% 试盘失败出货 → 7/27 +0.8% 尾盘修复
  → 7/28 -2.8% 冲高跳水完成T+0出货 → 7/29 +2.3% 探底60.95后V型反弹
  → 7/30 -0.65% 创业板暴跌中仅微跌=有资金护盘

  【当前主力状态】
  - 大单净额 -0.86亿(小幅流出,但远小于7/28的-1.37亿)
  - 外盘50.8%(接近平衡,不像7/28的44.7%卖方主导)
  - 成交量15.87万手(60日12%分位=极度缩量)
  - 振幅3.1%(远小于7/28的6.24%=波动收敛)

  【主力意图判断】
  1. 维护60-66画框: 7/29探底60.95+裕富终止减持=底部有"政策底+资金底"双重支撑
  2. 不急于拉升: 缩量-0.65%=主力在创业板暴跌中选择"不卖也不买",耐心等待大盘企稳
  3. 减持节奏: 宁德6/26首减仅0.25%(用3.3%额度),余56天+2.75%额度→平均每周约0.16%
  4. 大股东博弈: 裕富终止=释放"股东认为价格偏低"信号;宁德仍减持=但需好价格出货
  → 两方大股东共识: 当前不是最佳减持价格,需要先稳住再择机减

  【后续操作概率】
  A. 大盘企稳→放量上攻66+ → 概率30% → 需要8月1日涨价落地+创业板止跌
  B. 继续60-66画框内缩量震荡 → 概率55% → 等待大盘方向明确(最可能)
  C. 创业板继续崩→跌破60探58 → 概率15% → 极端情景,需创业板再跌3%+"""

ax7.text(0.02, 0.98, summary, transform=ax7.transAxes,
         fontsize=9.5, color=TEXT, va='top', ha='left',
         family='WenQuanYi Zen Hei',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#2a2a4a', alpha=0.9, edgecolor=GRID))

outpath = '/data/hermes/workspace/MyDocuments/stocks/301358/301358_0730_close.png'
plt.savefig(outpath, dpi=150, facecolor=BG, edgecolor='none', bbox_inches='tight')
plt.close()
import os
print(f"OK: {outpath} size={os.path.getsize(outpath)}")
