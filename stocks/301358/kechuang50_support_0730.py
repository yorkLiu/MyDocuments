#!/usr/bin/env python3
"""科创50支撑分析 — Mistery视角 — 7/30收盘"""
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

# === 日K数据 ===
with open('/tmp/kechuang50_130d.json') as f:
    kd = json.load(f)
sd = kd['data']['sh000688']
kb = sd.get('qfqday') or sd.get('day') or list(sd.values())[0]
daily = [{'d':b[0],'o':float(b[1]),'c':float(b[2]),'h':float(b[3]),'l':float(b[4]),
          'v':int(float(b[5])) if len(b)>5 else 0} for b in kb]
closes = [d['c'] for d in daily]
ma5 = np.mean(closes[-5:]); ma10 = np.mean(closes[-10:]); ma20 = np.mean(closes[-20:]); 
ma60 = np.mean(closes[-60:]); ma120 = np.mean(closes[-120:])

print(f"数据: 日K{len(daily)}条, MA5={ma5:.0f} MA20={ma20:.0f} MA60={ma60:.0f} MA120={ma120:.0f}")

# === 绘图 ===
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(28, 18), gridspec_kw={'height_ratios':[3,1]}, facecolor=BG)
ax1.set_facecolor(BG); ax2.set_facecolor(BG)

# K线
last80 = daily[-80:]
x = np.arange(len(last80))
for i, d in enumerate(last80):
    o, c, h, l = d['o'], d['c'], d['h'], d['l']
    color = UP if c >= o else DOWN
    ax1.plot([i, i], [l, h], color=color, linewidth=1, alpha=0.8)
    rect = plt.Rectangle((i-0.3, min(o,c)), 0.6, max(abs(c-o),0.5), facecolor=color, edgecolor=color, alpha=0.8)
    ax1.add_patch(rect)
    # 标注7月大跌关键点
    if d['d'] == '2026-07-10':
        ax1.annotate(f'7/10 -5.7%\n顶部确认', xy=(i, h), xytext=(i+3, h+80),
            fontsize=10, color=DOWN, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=DOWN, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a3a1a', alpha=0.9, edgecolor=DOWN))
    elif d['d'] == '2026-07-16':
        ax1.annotate(f'7/16 M头\n确认', xy=(i, l), xytext=(i+3, l-80),
            fontsize=10, color=DOWN, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=DOWN, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a3a1a', alpha=0.9, edgecolor=DOWN))
    elif d['d'] == '2026-07-21':
        ax1.annotate(f'7/21 +8.9%\n反弹', xy=(i, h), xytext=(i+2, h+50),
            fontsize=9, color=UP, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=UP, lw=1.2),
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#3a1a1a', alpha=0.9, edgecolor=UP))
    elif d['d'] == '2026-07-30':
        ax1.annotate(f'7/30 收1588\n-3.9%', xy=(i, c), xytext=(i+2, c-100),
            fontsize=10, color='#FFD700', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#FFD700', lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#3a3a1a', alpha=0.9, edgecolor='#FFD700'))

# 均线
for ma, c, lbl in [(ma5,'#FFD700','MA5'), (ma20,'#4ECDC4','MA20'), (ma60,'#9B59B6','MA60'), (ma120,'#E67E22','MA120')]:
    ma_vals = [np.mean(closes[max(0,len(closes)-80+i-ma_i):len(closes)-80+i+1]) for i, ma_i in enumerate([ma]*80)]
    ma_vals = [np.mean(closes[len(closes)-80+i-ma+1:len(closes)-80+i+1]) if i >= ma-1 else None for i in range(80)]
    valid_x = [x[i] for i in range(80) if ma_vals[i] is not None]
    valid_y = [ma_vals[i] for i in range(80) if ma_vals[i] is not None]
    ax1.plot(valid_x, valid_y, color=c, linewidth=1.2, alpha=0.7, label=f'{lbl}={ma:.0f}')

# === 关键支撑线 ===
supports = [
    (1588, '#FFD700', '当前价 1588'),
    (1577, '#E67E22', 'BOLL下轨 1577'),
    (1562, '#FF6B6B', '今日最低 1562'),
    (1492, '#4ECDC4', '2月收盘 1488\n3月起涨点'),
    (1249, '#2ECC71', '4月大底 1249\nMistery核心支撑'),
    (1715, '#888', 'Mistery旧支撑 1715\n(7/8提示1726-1730)'),
]
for px, c, lbl in supports:
    ax1.axhline(y=px, color=c, linestyle=':', linewidth=1.5, alpha=0.5)
    ax1.text(len(last80)+0.5, px, lbl, color=c, fontsize=9, fontweight='bold', va='center',
             bbox=dict(boxstyle='round,pad=0.2', facecolor=BG, alpha=0.7, edgecolor=c))

# 前高压力
ax1.axhline(y=2255, color='#C0392B', linestyle='--', linewidth=1.2, alpha=0.4)
ax1.text(2, 2255, '60日高 2255', color='#C0392B', fontsize=9, fontweight='bold')

ax1.set_xlim(-1, len(last80)+12)
ax1.set_ylim(1100, 2300)
ax1.set_title('科创50 (000688) — Mistery视角支撑位分析 | 7/30收1588(-3.9%) 距60日高-29.6%',
              color=TEXT, fontsize=15, fontweight='bold', pad=15)
ax1.legend(loc='upper left', fontsize=9, facecolor=BG, edgecolor=GRID, labelcolor=TEXT, ncol=5)
ax1.grid(True, color=GRID, alpha=0.3)
ax1.tick_params(colors=TEXT, labelsize=8)
for s in ax1.spines.values(): s.set_color(GRID)
# x轴日期
td = list(range(0, len(last80), 10))
ax1.set_xticks(td)
ax1.set_xticklabels([last80[i]['d'][5:] if i < len(last80) else '' for i in td], rotation=30, ha='right', fontsize=8)

# 成交量
vols = [d['v'] for d in last80]
vol_colors = [UP if d['c'] >= d['o'] else DOWN for d in last80]
ax2.bar(x, np.array(vols)/1e6, width=0.7, color=vol_colors, alpha=0.5)
ax2.axhline(y=np.mean(vols[-20:])/1e6, color='#FFD700', linestyle='--', linewidth=1, alpha=0.6, label='20日均量')
ax2.set_ylabel('成交量(亿手)', color=TEXT, fontsize=9)
ax2.set_title('成交量 — 7/30量比0.95 缩量下跌', color=TEXT, fontsize=11)
ax2.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=TEXT)
ax2.grid(True, color=GRID, alpha=0.3)
ax2.tick_params(colors=TEXT, labelsize=8)
for s in ax2.spines.values(): s.set_color(GRID)
ax2.set_xticks(td)
ax2.set_xticklabels([last80[i]['d'][5:] if i < len(last80) else '' for i in td], rotation=30, ha='right', fontsize=8)

# 添加Mistery观点文字框
mistery_text = """Mistery核心观点（来源：@Mimiwftt X/Twitter）

▸ "科创50月线依然处于强势主升浪" (7/4)
▸ "科创50最舒服的上车点1730-1726附近" (7/8)
▸ "下次阶段低吸位置在20日线附近(V型颈线位)" (7/4)
▸ "科创50跳空下跌,M头形成,提醒小心双顶" (7/16) ← 已兑现
▸ "4月1日1249是真正具备高性价比的买点" (7/11)
▸ "破位一般看3天,3天内不能收回才叫真破" (7/13)
▸ 月线见顶三条件: ①10月均线拐头向下 ②MACD月线死叉 ③放巨量不涨

当前验证: 7月月线-28% 收1588 (从2255跌29.6%)
关键位: ①1577布林下轨(已触及) ②1488-1492 2月起涨平台 ③1249 4月大底"""

fig.text(0.02, 0.02, mistery_text, fontsize=10, color=TEXT, va='bottom', ha='left',
         family='WenQuanYi Zen Hei',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#2a2a4a', alpha=0.9, edgecolor=GRID))

plt.tight_layout(rect=[0, 0.15, 1, 1])
outpath = '/data/hermes/workspace/MyDocuments/stocks/301358/kechuang50_support_0730.png'
plt.savefig(outpath, dpi=150, facecolor=BG, edgecolor='none', bbox_inches='tight')
plt.close()
import os
print(f"OK: {outpath} size={os.path.getsize(outpath)}")
