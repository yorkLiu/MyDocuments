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

# 加载数据
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
ma60 = np.mean(all_c[-60:])
boll_mid = np.mean(np.array(closes_d[-20:]))
boll_std = np.std(np.array(closes_d[-20:]))
boll_up = boll_mid + 2*boll_std
boll_down = boll_mid - 2*boll_std

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), facecolor=BG)
ax1.set_facecolor(BG); ax2.set_facecolor(BG)

# 日K线图 (最近30天)
last30 = d_full[-30:]
x = np.arange(len(last30))
for i, d in enumerate(last30):
    o, c, h, l = d['o'], d['c'], d['h'], d['l']
    color = UP if c >= o else DOWN
    ax1.plot([i, i], [l, h], color=color, linewidth=1)
    rect = plt.Rectangle((i-0.3, min(o,c)), 0.6, max(abs(c-o),0.01), facecolor=color, edgecolor=color, alpha=0.7)
    ax1.add_patch(rect)

for ma, c, lbl in [(ma5,'#FFD700','MA5'), (ma20,'#4ECDC4','MA20'), (ma60,'#9B59B6','MA60')]:
    ax1.axhline(y=ma, color=c, linestyle='--', linewidth=1, alpha=0.6, label=lbl+f'={ma:.1f}')

ax1.axhline(y=boll_down, color='#FFD700', linestyle=':', linewidth=1, alpha=0.5, label='BOLL下轨')
ax1.set_title('301358 日K线 (30日) — 7/31收盘63.34(-1.31%)', color=TEXT, fontsize=12, fontweight='bold')
ax1.set_xlim(-1, len(last30))
ax1.set_ylim(55, 75)
ax1.legend(loc='upper left', fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=TEXT)
ax1.grid(True, color=GRID, alpha=0.3)
ax1.tick_params(colors=TEXT, labelsize=8)
for s in ax1.spines.values(): s.set_color(GRID)

# 关键点位标注
ax1.text(25, 65, '60日MA=77.33\n(远期压力)', color='#9B59B6', fontsize=7, bbox=dict(boxstyle='round', facecolor=BG, alpha=0.7))
ax1.text(25, 63, 'MA20=63.74\n(短期支撑)', color='#4ECDC4', fontsize=7, bbox=dict(boxstyle='round', facecolor=BG, alpha=0.7))
ax1.text(25, 57, 'BOLL下轨=56.57\n(长期支撑)', color='#FFD700', fontsize=7, bbox=dict(boxstyle='round', facecolor=BG, alpha=0.7))

# 成交量
ax2.bar(x, [d['v']/10000 for d in last30], width=0.7, color=[UP if d['c']>=d['o'] else DOWN for d in last30], alpha=0.3)
ax2.set_xlabel('日期', color=TEXT, fontsize=9)
ax2.set_ylabel('成交量(万手)', color=TEXT, fontsize=9)
ax2.set_title('成交量', color=TEXT, fontsize=10)
ax2.tick_params(colors=TEXT, labelsize=8)
for s in ax2.spines.values(): s.set_color(GRID)

plt.tight_layout()
plt.savefig('/data/hermes/workspace/MyDocuments/stocks/301358/301358_0731_kline.png', dpi=150, facecolor=BG, edgecolor='none')
print('Chart saved')

# 计算关键指标
print(f'\n=== 日K指标 ===')
print(f'收盘价: {closes_d[-1]:.2f} MA5:{ma5:.2f} MA10:{ma10:.2f} MA20:{ma20:.2f} MA60:{ma60:.2f}')
print(f'BOLL: 上{boll_up:.2f} 中{boll_mid:.2f} 下{boll_down:.2f}')
print(f'相对大盘: 创业板指+3.06%, 301358-1.31% → 偏离-4.37个百分点 (大盘涨它跌!)')
