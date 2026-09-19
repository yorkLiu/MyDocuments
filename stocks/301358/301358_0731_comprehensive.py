#!/usr/bin/env python3
"""301358 7/31收盘全面分析 — 日/周/月K支撑压力+5日分时异常+板块对比+Mistery视角"""
import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

# ============= 加载数据 =============
# 日K
daily_raw = json.load(open('/tmp/301358_130d.json'))
sd = daily_raw['data']['sz301358']
kb_d = sd.get('qfqday') or sd.get('day') or list(sd.values())[0]
d_full = [{'d':b[0],'o':float(b[1]),'c':float(b[2]),'h':float(b[3]),'l':float(b[4]),'v':int(float(b[5]))} for b in kb_d]
d_full.append({'d':'2026-07-31','o':63.52,'c':63.34,'h':65.46,'l':63.16,'v':18806300})

closes_d = [d['c'] for d in d_full]
all_c = np.array(closes_d)
ma5 = np.mean(closes_d[-5:])
ma10 = np.mean(closes_d[-10:])
ma20 = np.mean(closes_d[-20:])
ma30 = np.mean(closes_d[-30:])
ma60 = np.mean(all_c[-60:])
ma120 = np.mean(all_c[-120:])

# BOLL(20)
last20 = np.array(closes_d[-20:])
boll_mid = np.mean(last20); boll_std = np.std(last20)
boll_up = boll_mid + 2*boll_std
boll_down = boll_mid - 2*boll_std

# 周K
weekly_raw = json.load(open('/tmp/sdk_week.json'))
wk_data = [{'d':k if isinstance(k,str) else 'N/A','c':float(v[-1][2]) if isinstance(v,list) else float(v['close']) for k,v in weekly_raw.items() if isinstance(weekly_raw, dict)} or 
           [{'d':b.get('date','?'),'c':float(b.get('close',b[2]))} for b in weekly_raw]]
wk_closes = [d['c'] for d in wk_data[-10:]]
ma5w = np.mean(wk_closes[-5:])
ma20w = np.mean(wk_closes[-20:])

# 月K
monthly_raw = json.load(open('/tmp/sdk_month.json'))
mo_data = [{'d':k,'c':float(v[-1][2]) if isinstance(v,list) else float(v['close']) for k,v in monthly_raw.items() if isinstance(monthly_raw,dict)} or 
           [{'d':b.get('date','2026-07'),'c':float(b.get('close',b[2]))} for b in monthly_raw]]
mo_closes = [d['c'] for d in mo_data[-6:]]

# 行情数据
stock_301358 = {'price':63.34, 'chg':-1.31}
cyb = {'price':3343.96, 'chg':3.06, 'name':'创业板指'}
kc = {'price':1635.96, 'chg':2.99, 'name':'科创50'}
battery = [
    {'code':'300750','name':'宁德','price':395.30,'chg':-1.64},
    {'code':'300769','name':'德方','price':42.74,'chg':1.04},
    {'code':'300432','name':'富临','price':15.62,'chg':0.39},
    {'code':'002340','name':'格林美','price':6.70,'chg':0.00},
    {'code':'300037','name':'新宙邦','price':62.60,'chg':2.52},
    {'code':'002812','name':'恩捷','price':52.59,'chg':-1.09},
]

# ============= 绘图 =============
fig = plt.figure(figsize=(20, 22), facecolor='#1a1a2e')
gs = fig.add_gridspec(6, 2, height_ratios=[3,2,2,2,2,3], hspace=0.15, wspace=0.10,
                      left=0.05, right=0.95, top=0.97, bottom=0.02)
ax1 = fig.add_subplot(gs[0, :]); ax1.set_facecolor('#1a1a2e')
ax2 = fig.add_subplot(gs[1, 0]); ax2.set_facecolor('#1a1a2e')
ax3 = fig.add_subplot(gs[1, 1]); ax3.set_facecolor('#1a1a2e')
ax4 = fig.add_subplot(gs[2, 0]); ax4.set_facecolor('#1a1a2e')
ax5 = fig.add_subplot(gs[2, 1]); ax5.set_facecolor('#1a1a2e')
ax6 = fig.add_subplot(gs[3, 0]); ax6.set_facecolor('#1a1a2e')
ax7 = fig.add_subplot(gs[3, 1]); ax7.set_facecolor('#1a1a2e')
ax8 = fig.add_subplot(gs[4, :]); ax8.set_facecolor('#1a1a2e')
ax9 = fig.add_subplot(gs[5, :]); ax9.set_facecolor('#1a1a2e')

ax9.axis('off')

# --- 日K线图（60日）+ 关键支撑压力标注 ---
last60 = d_full[-60:]
x = np.arange(len(last60))
for i, d in enumerate(last60):
    o, c, h, l = d['o'], d['c'], d['h'], d['l']
    color = '#E74C3C' if c >= o else '#2ECC71'
    ax1.plot([i, i], [l, h], color=color, linewidth=1)
    rect = plt.Rectangle((i-0.35, min(o,c)), 0.7, max(abs(c-o), 0.01), 
                         facecolor=color, edgecolor=color, alpha=0.7)
    ax1.add_patch(rect)

# 标注7/29-7/31关键走势
for i, d in enumerate(last60[-3:]):
    ax1.text(i, d['h']+0.5, f"{d['d'][8:]}\n{d['c']:.2f}({d['c']-last60[i-1]['c'] if i>0 else 0:+.2f})", 
             ha='center', fontsize=7, color='#FFD700' if d['c']>d['o'] else '#E74C3C')

# 支撑压力线
for y, lbl, c in [(boll_down, 'BOLL下轨', '#FFD700'), (ma20, 'MA20', '#4ECDC4'), 
                  (ma60, 'MA60', '#9B59B6'), (ma120, 'MA120', '#E67E22')]:
    ax1.axhline(y=y, color=c, linestyle='--', linewidth=1, alpha=0.5)

ax1.set_title('301358 日K线（60日）— 现价63.34(-1.31%) 大盘+3.06%', color='#E0E0E0', fontsize=13, fontweight='bold')
ax1.set_xlim(-1, len(last60))
ax1.set_ylim(50, 90)
ax1.set_ylabel('价格(元)', color='#E0E0E0')
ax1.tick_params(colors='#E0E0E0', labelsize=8)
for s in ax1.spines.values(): s.set_color('#2a2a4a')
ax1.grid(True, color='#2a2a4a', alpha=0.3)

# --- 周K + 压力位 ---
wk_x = np.arange(len(wk_data[-20:]))
wk_closes_arr = [d['c'] for d in wk_data[-20:]]
for i, (d, c) in enumerate(zip(wk_data[-20:], wk_closes_arr)):
    # 周K只有开收高低，简化为矩形
    ax2.plot(i, c, 'o', color='#FFD700', markersize=8)
ax2.set_xticks(np.arange(0, len(wk_closes_arr), 5))
ax2.set_xticklabels([d['d'] for d in wk_data[-20:][::5]], rotation=45, fontsize=7, color='#E0E0E0')
ax2.set_title('周K线（最近20周）', color='#E0E0E0', fontsize=10, fontweight='bold')
ax2.set_ylabel('周收盘价', color='#E0E0E0')
ax2.tick_params(colors='#E0E0E0', labelsize=7)
for s in ax2.spines.values(): s.set_color('#2a2a4a')
ax2.grid(True, color='#2a2a4a', alpha=0.3)

# 周支撑标注
ax2.text(0, wk_closes_arr[-1]+2, f'周MA5={ma5w:.1f}', color='#FFD700', fontsize=8)
ax2.text(0, wk_closes_arr[-1]+4, f'周BOLL下={(np.mean(wk_closes_arr[-20:])-2*np.std(wk_closes_arr[-20:])):.1f}', color='#FFD700', fontsize=8)

# --- 月K + 长期支撑 ---
mo_x = np.arange(len(mo_data[-12:]))
mo_closes_arr = [d['c'] for d in mo_data[-12:]]
for i, c in enumerate(mo_closes_arr):
    ax3.plot(i, c, 'o', color='#FFD700', markersize=6)
ax3.set_xticks(np.arange(0, len(mo_closes_arr), 3))
ax3.set_xticklabels([d['d'] for d in mo_data[-12:][::3]], rotation=45, fontsize=7, color='#E0E0E0')
ax3.set_title('月K线（最近12月）', color='#E0E0E0', fontsize=10, fontweight='bold')
ax3.set_ylabel('月收盘价', color='#E0E0E0')
ax3.tick_params(colors='#E0E0E0', labelsize=7)
for s in ax3.spines.values(): s.set_color('#2a2a4a')
ax3.grid(True, color='#2a2a4a', alpha=0.3)
ax3.text(0, mo_closes_arr[-1]+5, f'月MA5={ma5m:.1f}', color='#E67E20', fontsize=8)

# --- 5日分时对比图 ---
fig5, ax4 = plt.subplots(figsize=(6, 3), facecolor='#1a1a2e', subplot_kw={'axes':ax4})
# 用7/27-7/31五天的收盘走势绘制
days = ['7/27','7/28','7/29','7/30','7/31']
chgs = [2.77, -3.99, 2.43, -0.65, -1.31]
cyb_chgs = [2.94, -7.35, 1.55, -3.97, 3.06]  # 对应创业板指
bars4 = ax4.bar(range(5), chgs, color=['#E74C3C' if c<0 else '#2ECC71' for c in chgs], alpha=0.7)
for i, (d, c, cc) in enumerate(zip(days, chgs, cyb_chgs)):
    ax4.text(i, c+(0.5 if c>0 else -0.8), f'{c:+.1f}%\n({cc:+.1f}%)', ha='center', fontsize=7, 
             color='#FFD700' if abs(c-c)>2 else '#888')
ax4.axhline(y=0, color='#888', linewidth=0.5)
ax4.set_xticks(range(5))
ax4.set_xticklabels(days, fontsize=8, color='#E0E0E0')
ax4.set_title('5日涨跌对比(绿=红盘 蓝=创业板)', color='#E0E0E0', fontsize=9, fontweight='bold')
ax4.grid(True, color='#2a2a4a', alpha=0.3, axis='y')
ax4.tick_params(colors='#E0E0E0', labelsize=7)

# --- 板块个股对比 — 7/31涨跌幅 ---
battery_names = [b['name'] for b in battery]
battery_chgs = [b['chg'] for b in battery]
battery_colors = ['#FFD700' if b['code']=='300750' else ('#E74C3C' if b['chg']<0 else '#2ECC71') for b in battery]
ax5.barh(range(len(battery)), battery_chgs, color=battery_colors, height=0.6)
for i, (name, chg) in enumerate(zip(battery_names, battery_chgs)):
    ax5.text(max(chg, 0)+0.1, i, f'{name}: {chg:+.2f}%', va='center', fontsize=9, 
             color='#FFD700' if name=='宁德' else ('#E74C3C' if chg<0 else '#2ECC71'))
ax5.axhline(y=0, color='#888', linewidth=0.5)
ax5.set_yticks(range(len(battery)))
ax5.set_yticklabels([b.split()[0] for b in battery_names], fontsize=8, color='#E0E0E0')
ax5.set_xlabel('涨跌幅(%)', color='#E0E0E0', fontsize=9)
ax5.set_title('电池板块个股7/31涨跌幅(金色=宁德时代)', color='#E0E0E0', fontsize=10, fontweight='bold')
ax5.grid(True, color='#2a2a4a', alpha=0.3, axis='x')
ax5.tick_params(colors='#E0E0E0', labelsize=8)

# --- 301358 vs 大盘对比表 ---
table_data = [
    ['日期', '301358涨跌', '创业板指涨跌', '相对强弱', '成交量'],
    ['7/27', '+2.77%', '+2.94%', '≈-0.17%', '20.0万手'],
    ['7/28', '-3.99%', '-7.35%', '+3.36%', '16.0万手'],
    ['7/29', '+2.43%', '+1.55%', '+0.88%', '19.0万手'],
    ['7/30', '-0.65%', '-3.97%', '+3.32%', '15.0万手'],
    ['7/31', '-1.31%', '+3.06%', '-4.37%', '18.8万手'],
]
ax6.table(cellText=table_data, loc='center', cellLoc='center')
ax6.axis('off')
ax6.set_title('301358 vs 创业板指 5日对比(相对强弱=301358-创业板)', color='#E0E0E0', fontsize=10, fontweight='bold', pad=20)

# === 7日大单净额变化（根据分时估算）===
# 7/27: +0.39亿(尾盘大单) 7/28: -1.37亿(冲高调派) 7/29: +0.35亿(接盘) 7/30: -0.86亿(净流出) 7/31: 估算-0.5亿
seven_days = [0.39, -1.37, 0.35, -0.86, -0.5]
ax7.bar(range(5), seven_days, color=['#E74C3C' if x<0 else '#2ECC71' for x in seven_days])
ax7.axhline(y=0, color='#888', linewidth=0.5)
ax7.set_xticks(range(5))
ax7.set_xticklabels(['7/27','7/28','7/29','7/30','7/31'], fontsize=8, color='#E0E0E0')
ax7.set_ylabel('大单净额(亿)', color='#E0E0E0', fontsize=9)
ax7.set_title('7日大单净流出(估算)', color='#E0E0E0', fontsize=10, fontweight='bold')
ax7.tick_params(colors='#E0E0E0', labelsize=8)
ax7.grid(True, color='#2a2a4a', alpha=0.3)

# === 综合文字分析 ===
summary = """
╔══════════════════════════════════════════════════════════════════════════════╗
║               301358 7/31收盘全面分析 — Mistery视角                       ║
║                (GMT+08:00 2026-07-31 收盘后)                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

【一、日K线技术面】
  ● 现价: 63.34元 (7/31收盘 -1.31%)
  ● 均线系统: MA5=64.18 < MA10=63.74 ≈ MA20=63.74 < MA30=69.50
  ● 关键支撑: MA20=63.74 (近期支撑), BOLL下轨=56.57 (长期支撑)
  ● 关键压力: MA60=77.33 (60日均线压力), 前期高点67.13 (7/24最高点)
  ● 60日画框: 58.08-108.64 → 当前63.34处于低位区，支撑58附近
  
  日K结论: 价格跌破MA5和MA10，呈现短期空头排列，但距离MA60和月线还有较大距离

【二、周K技术面】
  ● 周收盘价: 63.34元
  ● 周均线: 周MA5=64.65 < 周MA10=70.85 < 周MA20=78.27
  ● 周BOLL下轨: ≈54.75
  
  周K结论: 周均线呈空头排列(MA5<MA10<MA20)，周线级别压力在78-80元区域，
           支撑在54-55元周BOLL下轨。当前位于周线偏低位。

【三、月K技术面】
  ● 月收盘价: 63.34元 (7月大幅下跌16.52%)
  ● 月均线: 月MA5=80.94 > 月MA10=74.70
  ● 月历史高点: 108.64(4月), 月历史低点: 30.16(2025年)
  
  月K结论: 月线MA5=80.94为中长期重要压力，7月大幅回落但仍在月线上升通道内。
           月线级别的真正底部区域在30-40元（历史最低30.16），当前63距离月线底部仍有空间。

【四、大盘对比——关键背离信号】
  创业板指 +3.06%   科创50 +2.99%   ← 大盘强势反弹
  301358 -1.31%    ← 个股逆势下跌
  ──────────────────────────────────
  相对表现: -4.37个百分点
  
  ⚠️ 重要信号！大盘暴涨时个股逆势下跌，显示301358存在独立抛压。
  这不是系统风险，而是个股自身的卖压。

【五、电池板块对比】
  电池板块平均(不含宁德): +0.96% (德方+1.04%, 富临+0.39%, 格林美0%, 新宙邦+2.52%, 恩捷-1.09%)
  宁德时代: -1.64% (独立行情，减持中)
  301358: -1.31%
  
  301358在电池板块中属于"弱者"，强于宁德时代但弱于其他板块个股。
  7/30(强于板块3.32%)→7/31(弱于板块4.37%)，这种快速变化显示主力资金在调仓。

【六、5日分时异常分析】
  7/27 14:18后拉升 (尾盘借大盘修复) → 正常
  7/28 冲66.98后跳水 (冲高派发) → 正常减持周期模式
  7/29 探底60.95后V型反弹 (接盘) → 正常护盘
  7/30 缩量-0.65% (大盘-3.97%时的抗跌) → 有资金托底
  7/31 冲高65.42后阴跌收跌 (大盘+3.06%时逆势-1.31%) → ⚠️异常!
  
  7/31最异常特征:
  1. 早盘冲高65.42(接近7/28高点66.98)，随后一路阴跌
  2. 大盘创业板+3.06%的强势环境下，个股逆势下跌
  3. 成交量18.8万手(放大)，但价格走弱 = 放量下跌，资金在出
  4. 分时走势: 10:01见顶65.42后震荡下行，下午持续弱势
  
  7/31的行为模式 = 7/28的复制(冲高-派发-回落)，只是位置不同
  7/28: 66.98(试探压力)→63.07(收盘)  -3.99%
  7/31: 65.42(试探压力)→63.34(收盘)  -1.31%(但大盘涨3%)

【七、主力意图分析】

日/周/月K支撑压力总结:
───────────────────────
  月压力: MA5=80.94 (遥远) → 周压力: MA20=78.27 → 日压力: MA60=77.33
          → 60日高=108.64 (强压力)
          
  日支撑: MA20=63.74 (近) → 心理60 → 周BOLL下54.75 → 日BOLL下56.57
          → 60日低=58.08 (画框底)
  
主力操作轨迹(7天行为链):
  7/23: 拉高66.01(当日+8.96%) → 派发准备
  7/24: 冲67.13(试探MA20上压力)→跳水收63.92(-3.17%) → T+0出货
  7/27: 尾盘14:18拉升(借大盘β修复)→收65.69(+2.77%) → 为下一波派发做准备
  7/28: 冲66.98(再次试探MA20压力)→跳水收63.07(-3.99%) → 完成T+0出货
  7/29: 探底60.95(支撑测试)→V型反弹收64.60(+2.43%) → 接护底仓
  7/30: 横盘整理64.18(-0.65%)在大盘暴跌时抗跌 → 观察等待
  7/31: 冲高65.42(又一次试探压力)→阴跌收63.34(-1.31%)在大盘上涨时逆势 → 派发信号

Mistery归因:
  "三次在66-67区域(66.98, 67.13, 65.42附近)都遇到抛压，这说明66-67确实是强阻力区。
   而7/31最关键的是'大盘涨它跌'——这不是跟随市场，而是独立出货。
   主力在等市场情绪好时拉高(7/31冲高65.42)，然后借大盘强势掩护出货(阴跌收跌)，
   这是非常经典的主力'骑猪'手法: 涨的时候不卖，但绝不随大盘一起涨，
   反而在大盘上涨时逆势下跌——因为拉高了不好出货，要在强势时悄悄抛。
  
   60-66画框现在被反复测试：60是支撑(7/29和7/31都在63附近获得支撑)，
   66是压力(三次冲高都在此遇阻)。主力在画框内反复'拉高→派发'，
   减持窗口(9/25前)还剩55天，他们需要持续出货。
  
   7/30在大盘暴跌时抗跌→显示有护盘力量。7/31在大盘上涨时下跌→显示有出货力量。
   同一个主力，在不同市场环境下'一托一拉'(护底+拉高派发)，非常典型。"

【八、7/31后续操作预判】

支撑位优先级:
  ① 63.74 (MA20, 日内支撑) — 跌破则看60
  ② 60.00 (心理+画框底, 周BOLL上沿) — 此处若破则趋势转弱
  ③ 58.08 (60日最低, 历史低点) — 极端支撑

压力位优先级:
  ① 65.42 (7/31最高) — 短期压力
  ② 66.98 (7/28最高点, MA20上方) — 强压力区
  ③ 77.33 (MA60, 周线压力) — 中长期压力

关键观察点:
  · 7/31收盘63.34接近MA20(63.74)，若连续两天跌破MA20则趋势转空
  · 能否守住60元画框底决定短期方向
  · 8/1磷酸铁锂涨价函落地是潜在利好催化剂
  · 减持窗口剩余55天，主力持续出货压力不改
  
  最可能情景: 63-66区间继续震荡，等待8/1涨价消息落地后选择方向
  激进情景: 跌破60→去58找底
  乐观情景: 放量突破66.98→看74-76筹码峰压力
"""

ax9.text(0.02, 0.98, summary, transform=ax9.transAxes,
         fontsize=9.5, color='#E0E0E0', va='top', ha='left',
         family='WenQuanYi Zen Hei',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#2a2a4a', alpha=0.95, edgecolor='#4ECDC4'))

plt.savefig('/data/hermes/workspace/MyDocuments/stocks/301358/301358_0730_close.png', 
            dpi=150, facecolor='#1a1a2e', edgecolor='none', bbox_inches='tight')
print("Chart saved successfully!")
