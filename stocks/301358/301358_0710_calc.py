#!/usr/bin/env python3
"""301358 7/10 完整技术指标计算"""
import json, numpy as np

with open('/data/hermes/workspace/301358_klines.json') as f:
    all_klines = json.load(f)

closes = np.array([k['close'] for k in all_klines])
volumes = np.array([k['volume'] for k in all_klines])
highs = np.array([k['high'] for k in all_klines])
lows = np.array([k['low'] for k in all_klines])
opens = np.array([k['open'] for k in all_klines])
dates = [k['date'] for k in all_klines]
n = len(closes)

print(f"K线总数: {n}")
print(f"日期范围: {dates[0]} ~ {dates[-1]}")
print(f"\n最后5日数据:")
for i in range(n-5, n):
    chg = (closes[i]/closes[i-1]-1)*100 if i>0 else 0
    print(f"  {dates[i]}  开{opens[i]:.2f}  收{closes[i]:.2f}  高{highs[i]:.2f}  低{lows[i]:.2f}  量{volumes[i]/10000:.0f}万手  涨跌{chg:+.2f}%")

print(f"\n{'='*60}")
print(f"7/10 关键数据")
print(f"{'='*60}")

i = n - 1  # 7/10
print(f"收盘: {closes[i]:.2f}")
print(f"开盘: {opens[i]:.2f}")
print(f"最高: {highs[i]:.2f}")
print(f"最低: {lows[i]:.2f}")
print(f"成交量: {volumes[i]/10000:.0f}万手")
print(f"成交额: {closes[i]*volumes[i]/100000000:.1f}亿")
print(f"涨跌幅: {(closes[i]/closes[i-1]-1)*100:.2f}%")

# MA
for p in [5, 10, 20, 60, 120]:
    if i >= p-1:
        ma = closes[i-p+1:i+1].mean()
        dist = (closes[i]/ma - 1)*100
        print(f"MA{p}: {ma:.2f}  (价格偏离{dist:+.1f}%)")

# BOLL
p = 20
mid = closes[i-p+1:i+1].mean()
std = closes[i-p+1:i+1].std()
upper = mid + 2*std
lower = mid - 2*std
print(f"\nBOLL: 上{upper:.2f}  中{mid:.2f}  下{lower:.2f}")
print(f"  收盘vs下轨: {closes[i]:.2f} vs {lower:.2f} ({'已破' if closes[i] < lower else '未破'})")
print(f"  距下轨: {(closes[i]/lower-1)*100:+.2f}%")

# KDJ
low_9 = lows[i-8:i+1].min()
high_9 = highs[i-8:i+1].max()
if high_9 == low_9:
    rsv = 50
else:
    rsv = (closes[i] - low_9) / (high_9 - low_9) * 100
# 递推KDJ
k_prev = 50
d_prev = 50
for j in range(max(0, i-20), i+1):
    l9 = lows[j-8:j+1].min()
    h9 = highs[j-8:j+1].max()
    if h9 == l9:
        r = 50
    else:
        r = (closes[j] - l9) / (h9 - l9) * 100
    k_prev = 2/3 * k_prev + 1/3 * r
    d_prev = 2/3 * d_prev + 1/3 * k_prev
j_val = 3 * k_prev - 2 * d_prev
print(f"\nKDJ: K={k_prev:.2f}  D={d_prev:.2f}  J={j_val:.2f}")
print(f"  超卖判断: {'极度超卖' if j_val < 0 else '超卖' if j_val < 20 else '中性' if j_val < 80 else '超买'}")

# RSI
deltas = np.diff(closes[i-15:i+1])
gains = np.where(deltas > 0, deltas, 0)
losses = np.where(deltas < 0, -deltas, 0)
avg_gain = gains.mean()
avg_loss = losses.mean()
if avg_loss == 0:
    rsi = 100
else:
    rs = avg_gain / avg_loss
    rsi = 100 - 100/(1+rs)
print(f"\nRSI(14): {rsi:.2f}")
print(f"  超卖判断: {'极度超卖' if rsi < 15 else '超卖' if rsi < 30 else '中性' if rsi < 70 else '超买'}")

# MACD
ema12 = closes[-150:].copy() if n > 150 else closes.copy()
ema26 = closes[-150:].copy() if n > 150 else closes.copy()
for p in [12, 26]:
    ema = closes.copy()
    mult = 2/(p+1)
    e = closes[0]
    for j in range(1, n):
        e = mult * closes[j] + (1-mult) * e
        ema[j] = e
    if p == 12:
        ema12 = ema
    else:
        ema26 = ema

dif = ema12 - ema26
dea = np.zeros(n)
dea[0] = dif[0]
for j in range(1, n):
    dea[j] = 0.2 * dif[j] + 0.8 * dea[j-1]
macd_bar = 2 * (dif - dea)
print(f"\nMACD: DIF={dif[i]:.3f}  DEA={dea[i]:.3f}  柱={macd_bar[i]:.3f}")
print(f"  空头排列: {'是' if dif[i] < dea[i] else '否'}")
print(f"  绿柱放大: {'是' if macd_bar[i] < macd_bar[i-1] else '否'}")

# 量能分析
print(f"\n{'='*60}")
print(f"量价分析")
print(f"{'='*60}")
for j in range(max(0, i-6), i+1):
    print(f"  {dates[j]}  收{closes[j]:.2f}  量{volumes[j]/10000:.0f}万手  额{closes[j]*volumes[j]/100000000:.1f}亿")

v_today = volumes[i]
v_yesterday = volumes[i-1]
v_chg = (v_today/v_yesterday - 1) * 100
print(f"\n7/10 vs 7/9 量能: {v_today/10000:.0f}万手 vs {v_yesterday/10000:.0f}万手 ({v_chg:+.1f}%)")

v_avg20 = volumes[i-19:i+1].mean()
print(f"20日均量: {v_avg20/10000:.0f}万手")
print(f"量比: {v_today/v_avg20:.2f}")

# 换手率估算 (总股本约7.62亿)
total_shares = 7.62e8
turnover = v_today * 100 / total_shares  # volumes单位是手=100股
print(f"换手率(估): {turnover:.2f}%")

# 最高价回撤
peak = highs.max()
peak_idx = highs.argmax()
print(f"\n最高价: {peak:.2f} ({dates[peak_idx]})")
print(f"当前回撤: {(closes[i]/peak-1)*100:.1f}%")

# Fibonacci回撤位
low_ipo = closes[0]
print(f"\nFibonacci回撤位 (从{low_ipo:.2f}到{peak:.2f}):")
for r in [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]:
    level = peak - (peak - low_ipo) * r
    status = "★当前附近" if abs(closes[i] - level) < 2 else ""
    print(f"  {r*100:.1f}% = {level:.2f}  {status}")

# 三振共振检查
print(f"\n{'='*60}")
print(f"【三振共振检查】")
print(f"{'='*60}")

# 均线排列
ma5 = closes[i-4:i+1].mean()
ma10 = closes[i-9:i+1].mean()
ma20 = closes[i-19:i+1].mean()
ma60 = closes[i-59:i+1].mean()
print(f"价格 {closes[i]:.2f}")
print(f"MA5={ma5:.2f}  MA10={ma10:.2f}  MA20={ma20:.2f}  MA60={ma60:.2f}")
all_above = closes[i] < ma5 and ma5 < ma10 and ma10 < ma20 and ma20 < ma60
print(f"均线状态: {'完全空头排列(价格<MA5<MA10<MA20<MA60)' if all_above else '其他'}")

# 与7/9对比
print(f"\n{'='*60}")
print(f"【7/9 vs 7/10 变化】")
print(f"{'='*60}")
i9 = n - 2
print(f"收盘: {closes[i9]:.2f} → {closes[i]:.2f} ({(closes[i]/closes[i9]-1)*100:+.2f}%)")
print(f"成交量: {volumes[i9]/10000:.0f}万手 → {volumes[i]/10000:.0f}万手 ({(volumes[i]/volumes[i9]-1)*100:+.1f}%)")
print(f"成交额: {closes[i9]*volumes[i9]/1e8:.1f}亿 → {closes[i]*volumes[i]/1e8:.1f}亿")
print(f"最低: {lows[i9]:.2f} → {lows[i]:.2f} ({'创新低↓' if lows[i] < lows[i9] else '未创新低↑'})")
print(f"最高: {highs[i9]:.2f} → {highs[i]:.2f}")
