#!/usr/bin/env python3
"""301358 7/10 分时交易时序图"""
import json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch

fm.fontManager.addfont('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')
plt.rcParams['font.family'] = 'WenQuanYi Zen Hei'
plt.rcParams['axes.unicode_minus'] = False

with open('/data/hermes/workspace/301358_0710_minutes.json') as f:
    minutes = json.load(f)

# 只取交易时段（去掉盘后零量数据）
minutes = [m for m in minutes if m.get('vol', 0) > 0 or m['time'] <= '1500']

times = [m['time'] for m in minutes]
prices = [m['price'] for m in minutes]
vols = [m.get('vol', 0) for m in minutes]
amts = [m.get('amt', 0) for m in minutes]

# 昨收
prev_close = 65.80  # 7/9收盘
# 开盘价
open_price = minutes[0]['price']

x = np.arange(len(minutes))

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(22, 16), gridspec_kw={'height_ratios': [3, 1, 1]})
fig.subplots_adjust(hspace=0.08, top=0.94, bottom=0.05, left=0.07, right=0.93)
fig.suptitle('301358 湖南裕能 · 2026-07-10 分时交易时序分析\n收盘63.15 (-4.03%) | 光脚阴线 | 尾盘异常砸盘',
             fontsize=16, fontweight='bold')

# ===== 图1：分时价格走势 =====
ax1.set_title('分时价格走势（黄线=均价，白线=价格）', fontsize=12)
ax1.axhline(y=prev_close, color='#ff9800', linewidth=1, linestyle='--', alpha=0.5, label=f'昨收{prev_close:.2f}')
ax1.fill_between(x, prev_close, prices, where=[p >= prev_close for p in prices],
                 color='#d32f2f', alpha=0.08)
ax1.fill_between(x, prev_close, prices, where=[p < prev_close for p in prices],
                 color='#2e7d32', alpha=0.08)

# 价格线
ax1.plot(x, prices, color='#1565c0', linewidth=1.5, label='价格')

# 均价线
cum_amt = np.cumsum(amts)
cum_vol = np.cumsum(vols)
avg_prices = cum_amt / (cum_vol * 100)  # 均价 = 累计额/累计量(手*100股)
ax1.plot(x, avg_prices, color='#ff9800', linewidth=1.5, linestyle='-', label='均价')

# 标注关键时段
# 开盘砸盘段
seg1_end = next(i for i, m in enumerate(minutes) if m['time'] == '0935')
ax1.axvspan(0, seg1_end, alpha=0.08, color='#d32f2f')
ax1.annotate('开盘砸盘\n65.60→64.38\n(-1.9% 仅5分钟)', xy=(seg1_end/2, 65.0),
            fontsize=8, color='#d32f2f', ha='center', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#ffcdd2', alpha=0.8))

# 午盘跳水段
noon_start = next(i for i, m in enumerate(minutes) if m['time'] == '1300')
noon_end = next(i for i, m in enumerate(minutes) if m['time'] == '1330')
ax1.axvspan(noon_start, noon_end, alpha=0.08, color='#d32f2f')
ax1.annotate('午盘跳水\n64.72→63.62\n(-1.7%)', xy=((noon_start+noon_end)/2, 64.3),
            fontsize=8, color='#d32f2f', ha='center', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#ffcdd2', alpha=0.8))

# 尾盘砸盘
tail_start = next(i for i, m in enumerate(minutes) if m['time'] == '1455')
tail_end = next(i for i, m in enumerate(minutes) if m['time'] == '1500')
ax1.axvspan(tail_start, tail_end, alpha=0.15, color='#d32f2f')
ax1.annotate('★尾盘精准砸盘\n63.35→63.15\n(0.3% 最后一分钟)', xy=((tail_start+tail_end)/2, 63.8),
            fontsize=9, color='#d32f2f', ha='center', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#ffcdd2', alpha=0.9))

# 标注全天最低点
low_idx = prices.index(min(prices))
ax1.annotate(f'最低{min(prices):.2f}\n=收盘价\n光脚阴线', xy=(low_idx, min(prices)),
            fontsize=9, color='#d32f2f', fontweight='bold', ha='center',
            xytext=(low_idx, min(prices)+2),
            arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=1.5),
            bbox=dict(boxstyle='round', facecolor='#fff9c4', alpha=0.9))

ax1.set_ylabel('价格(元)', fontsize=11)
ax1.legend(loc='upper right', fontsize=10)
ax1.grid(True, alpha=0.1)

# X轴时间标注
time_indices = list(range(0, len(minutes), max(1, len(minutes)//12)))
xlabels = [times[i] for i in time_indices]
ax1.set_xticks(x[time_indices])
ax1.set_xticklabels([])

# ===== 图2：每分钟成交量 =====
ax2.set_title('每分钟成交量（红=放量卖, 绿=缩量）', fontsize=12)
avg_vol = np.mean(vols)
vol_colors = []
for i in range(len(vols)):
    if vols[i] > avg_vol * 2:
        vol_colors.append('#d32f2f')
    elif vols[i] > avg_vol * 1.5:
        vol_colors.append('#ff9800')
    else:
        vol_colors.append('#666')

ax2.bar(x, np.array(vols)/10000, color=vol_colors, width=0.7, alpha=0.7)
ax2.axhline(y=avg_vol/10000, color='#2196f3', linewidth=0.8, linestyle='--', alpha=0.5, label=f'均量{avg_vol/10000:.2f}万手')
ax2.axhline(y=avg_vol*2/10000, color='#d32f2f', linewidth=0.8, linestyle=':', alpha=0.5, label=f'2倍均量{avg_vol*2/10000:.2f}万手')

# 标注尾盘大单
tail_idx = next(i for i, m in enumerate(minutes) if m['time'] == '1500')
ax2.annotate(f'尾盘大单\n{vols[tail_idx]/10000:.2f}万手\n(4.7倍均量)', xy=(tail_idx, vols[tail_idx]/10000),
            fontsize=8, color='#d32f2f', fontweight='bold', ha='center',
            xytext=(tail_idx-15, vols[tail_idx]/10000+0.3),
            arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=1),
            bbox=dict(boxstyle='round', facecolor='#ffcdd2', alpha=0.9))

# 标注开盘大单
ax2.annotate(f'开盘大单\n{vols[1]/10000:.2f}万手\n(11倍均量)', xy=(1, vols[1]/10000),
            fontsize=8, color='#d32f2f', fontweight='bold', ha='center',
            xytext=(10, vols[1]/10000+0.2),
            arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=1),
            bbox=dict(boxstyle='round', facecolor='#ffcdd2', alpha=0.9))

ax2.set_ylabel('成交量(万手)', fontsize=11)
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, alpha=0.1)
ax2.set_xticks(x[time_indices])
ax2.set_xticklabels([])

# ===== 图3：累计资金流向估算 =====
ax3.set_title('累计价格vs均价偏离（价-均价，判断买卖力量对比）', fontsize=12)
price_minus_avg = np.array(prices) - np.array(avg_prices)
colors_area = ['#d32f2f' if p > 0 else '#2e7d32' for p in price_minus_avg]
ax3.fill_between(x, 0, price_minus_avg, where=[p > 0 for p in price_minus_avg],
                 color='#d32f2f', alpha=0.3, label='价格>均价(卖压)')
ax3.fill_between(x, 0, price_minus_avg, where=[p < 0 for p in price_minus_avg],
                 color='#2e7d32', alpha=0.3, label='价格<均价(买力)')
ax3.axhline(y=0, color='#333', linewidth=0.5)
ax3.plot(x, price_minus_avg, color='#1565c0', linewidth=1)

ax3.set_ylabel('价-均价(元)', fontsize=11)
ax3.set_xlabel('时间', fontsize=11)
ax3.legend(loc='upper right', fontsize=9)
ax3.grid(True, alpha=0.1)
ax3.set_xticks(x[time_indices])
ax3.set_xticklabels(xlabels, rotation=30, fontsize=8)

plt.savefig('/data/hermes/workspace/301358_0710_intraday.png', dpi=150, bbox_inches='tight')
print("✓ 7/10分时交易时序图已保存")

# 打印分析摘要
print(f"\n{'='*60}")
print("7/10 分时交易异常点汇总")
print(f"{'='*60}")

# 开盘集中抛压
seg1 = [m for m in minutes if m['time'] <= '0935']
seg1_vol = sum(m.get('vol',0) for m in seg1)
total_vol = sum(m.get('vol',0) for m in minutes)
print(f"\n1. 开盘5分钟集中抛压:")
print(f"   0930-0935: 成交{seg1_vol/10000:.1f}万手 占全天{seg1_vol/total_vol*100:.1f}%")
print(f"   价格: 65.60→64.38 (-1.9%)")

# 尾盘砸盘
tail = [m for m in minutes if m['time'] >= '1455' and m['time'] <= '1500']
tail_vol = sum(m.get('vol',0) for m in tail)
print(f"\n2. 尾盘5分钟砸盘:")
print(f"   1455-1500: 成交{tail_vol/10000:.1f}万手 占全天{tail_vol/total_vol*100:.1f}%")
print(f"   价格: 63.35→63.15 (-0.3%)")
print(f"   最后一分钟(1500): {vols[tail_idx]/10000:.2f}万手 = 均量的{vols[tail_idx]/avg_vol:.1f}倍")

# 1458-1459 零成交
print(f"\n3. 1458-1459 零成交:")
m1458 = [m for m in minutes if m['time'] in ('1458','1459')]
for m in m1458:
    print(f"   {m['time']}  量{m.get('vol',0)}手  额{m.get('amt',0):.0f}")

# 均价分析
final_avg = avg_prices[-1]
close = prices[-1]
print(f"\n4. 均价分析:")
print(f"   全天均价: {final_avg:.2f}")
print(f"   收盘价: {close:.2f}")
print(f"   价-均价: {close - final_avg:.2f} (收盘低于均价={'卖压主导' if close < final_avg else '买力主导'})")

# 各时段量占比
print(f"\n5. 各时段成交量占比:")
segs = [
    ('0930-1000', '0930', '1000'),
    ('1000-1130', '1000', '1130'),
    ('1300-1400', '1300', '1400'),
    ('1400-1500', '1400', '1500'),
]
for name, s, e in segs:
    seg = [m for m in minutes if s <= m['time'] <= e]
    sv = sum(m.get('vol',0) for m in seg)
    print(f"   {name}: {sv/10000:.1f}万手 ({sv/total_vol*100:.1f}%)")
