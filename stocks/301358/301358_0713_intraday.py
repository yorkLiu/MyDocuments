#!/usr/bin/env python3
"""301358 7/13 盘中分时图"""
import json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

fm.fontManager.addfont('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')
plt.rcParams['font.family'] = 'WenQuanYi Zen Hei'
plt.rcParams['axes.unicode_minus'] = False

# 7/13 分时数据
raw_mins = [
    "0930 62.79 562 3528798.00", "0931 62.47 6779 42635792.61",
    "0932 62.37 9823 61631525.82", "0933 62.85 12536 78608668.69",
    "0934 62.57 14667 91984560.87", "0935 62.81 16879 105829431.54",
    "0936 62.47 18328 114898130.36", "0937 62.02 19846 124339678.61",
    "0938 61.85 21886 137002607.95", "0939 62.12 23491 146962403.23",
    "0940 61.95 25287 158074130.31", "0941 61.89 28131 175650356.94",
    "0942 61.76 29762 185728493.27", "0943 61.68 31492 196428640.69",
    "0944 61.80 33244 207255986.11", "0945 62.24 34807 216949731.84",
    "0946 62.05 36174 225444252.70", "0947 61.70 37029 230736301.57",
    "0948 61.65 38444 239452405.07", "0949 61.68 39614 246667180.73",
    "0950 61.67 40901 254601815.36", "0951 61.56 42410 263893376.90",
    "0952 61.51 43847 272734084.54", "0953 61.41 45201 281041618.21",
    "0954 61.31 46217 287273474.05", "0955 61.31 47606 295799863.09",
    "0956 61.15 48405 300692004.32", "0957 61.13 50261 312032223.05",
    "0958 60.97 51706 320851703.40", "0959 61.19 53781 333511053.00",
    "1000 61.30 54723 339276968"
]

times = []
prices = []
cum_vols = []
cum_amts = []
for m in raw_mins:
    parts = m.split()
    times.append(parts[0])
    prices.append(float(parts[1]))
    cum_vols.append(int(parts[2]))
    cum_amts.append(float(parts[3]))

# 每分钟增量
inc_vols = [cum_vols[0]] + [cum_vols[i] - cum_vols[i-1] for i in range(1, len(cum_vols))]

prev_close = 63.15
avg_prices = [cum_amts[i] / (cum_vols[i] * 100) for i in range(len(cum_vols))]

x = np.arange(len(times))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 10), gridspec_kw={'height_ratios': [3, 1]})
fig.subplots_adjust(hspace=0.08, top=0.93, bottom=0.07, left=0.07, right=0.93)
fig.suptitle('301358 湖南裕能 7/13 盘中分时 (截至10:00)\n当前61.00(-3.40%) 最低60.88 逼近59-61企稳区',
             fontsize=15, fontweight='bold')

# ===== 价格图 =====
ax1.axhline(y=prev_close, color='#ff9800', linewidth=1, linestyle='--', alpha=0.6, label='昨收63.15')
ax1.fill_between(x, prev_close, prices, where=[p >= prev_close for p in prices],
                 color='#d32f2f', alpha=0.06)
ax1.fill_between(x, prev_close, prices, where=[p < prev_close for p in prices],
                 color='#2e7d32', alpha=0.08)

ax1.plot(x, prices, color='#1565c0', linewidth=1.5, label='价格')
ax1.plot(x, avg_prices, color='#ff9800', linewidth=1.5, label='均价')

# 关键支撑线
ax1.axhline(y=61.00, color='#9c27b0', linewidth=1, linestyle=':', alpha=0.5)
ax1.text(0, 61.00, ' 61.00心理关', fontsize=8, color='#9c27b0', va='bottom')

ax1.axhline(y=59.05, color='#2e7d32', linewidth=2, linestyle='-', alpha=0.7)
ax1.text(0, 59.05, ' 大宗价59.05(机构接货) → 核心支撑', fontsize=9, color='#2e7d32',
        fontweight='bold', va='center',
        bbox=dict(boxstyle='round', facecolor='#c8e6c9', alpha=0.8))

ax1.axhline(y=59.04, color='#2e7d32', linewidth=1, linestyle=':', alpha=0.4)
ax1.text(len(times)-1, 59.04, ' 59.04(段C底) ', fontsize=8, color='#2e7d32', va='center', ha='right')

# 标注最低点
low_idx = prices.index(min(prices))
ax1.annotate(f'最低{min(prices):.2f}\n已破61!', xy=(low_idx, min(prices)),
            fontsize=10, color='#d32f2f', fontweight='bold', ha='center',
            xytext=(low_idx-3, min(prices)-1.5),
            arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=1.5),
            bbox=dict(boxstyle='round', facecolor='#ffcdd2', alpha=0.9))

# 标注开盘跳水
ax1.axvspan(0, 2, alpha=0.08, color='#d32f2f')
ax1.annotate('开盘跳水\n62.79→62.37', xy=(1, 62.5),
            fontsize=8, color='#d32f2f', ha='center',
            bbox=dict(boxstyle='round', facecolor='#ffcdd2', alpha=0.8))

# 标注0937跳水
idx_0937 = times.index('0937')
ax1.axvspan(idx_0937, idx_0937+1, alpha=0.08, color='#d32f2f')
ax1.annotate('破62\n0937: 62.02', xy=(idx_0937, 62.02),
            fontsize=8, color='#d32f2f', ha='center',
            xytext=(idx_0937-2, 62.8),
            arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=1),
            bbox=dict(boxstyle='round', facecolor='#ffcdd2', alpha=0.8))

# 标注0945反弹
idx_0945 = times.index('0945')
ax1.annotate('0945反弹62.24\n但没量', xy=(idx_0945, 62.24),
            fontsize=8, color='#ff9800', ha='center',
            xytext=(idx_0945+2, 62.8),
            arrowprops=dict(arrowstyle='->', color='#ff9800', lw=1),
            bbox=dict(boxstyle='round', facecolor='#fff9c4', alpha=0.8))

ax1.set_ylabel('价格(元)', fontsize=11)
ax1.legend(loc='upper right', fontsize=10)
ax1.grid(True, alpha=0.1)
ax1.set_ylim(58.5, 64.5)

step = max(1, len(times) // 12)
ax1.set_xticks(x[::step])
ax1.set_xticklabels([])

# ===== 成交量图 =====
avg_vol = np.mean(inc_vols)
vol_colors = []
for v in inc_vols:
    if v > avg_vol * 2:
        vol_colors.append('#d32f2f')
    elif v > avg_vol * 1.5:
        vol_colors.append('#ff9800')
    else:
        vol_colors.append('#888')

ax2.bar(x, np.array(inc_vols)/10000, color=vol_colors, width=0.7, alpha=0.7)
ax2.axhline(y=avg_vol/10000, color='#2196f3', linewidth=0.8, linestyle='--', alpha=0.5,
           label=f'均量{avg_vol/10000:.2f}万手')

# 标注开盘大单
ax2.annotate(f'开盘大单\n{inc_vols[1]/10000:.2f}万手', xy=(1, inc_vols[1]/10000),
            fontsize=8, color='#d32f2f', fontweight='bold', ha='center',
            xytext=(5, inc_vols[1]/10000+0.3),
            arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=1),
            bbox=dict(boxstyle='round', facecolor='#ffcdd2', alpha=0.9))

# 标注缩量下跌
ax2.annotate('0956-0958缩量跌破61\n抛压在减弱', xy=(28, inc_vols[28]/10000),
            fontsize=8, color='#2e7d32', ha='center',
            xytext=(20, inc_vols[28]/10000+0.5),
            arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=1),
            bbox=dict(boxstyle='round', facecolor='#c8e6c9', alpha=0.9))

ax2.set_ylabel('每分钟成交量(万手)', fontsize=11)
ax2.set_xlabel('时间', fontsize=11)
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, alpha=0.1)
ax2.set_xticks(x[::step])
ax2.set_xticklabels([times[i] for i in range(0, len(times), step)], rotation=30, fontsize=8)

plt.savefig('/data/hermes/workspace/301358_0713_intraday.png', dpi=150, bbox_inches='tight')
print("OK saved")
