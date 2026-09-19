#!/usr/bin/env python3
"""301358 30min K线完整分析"""
import json, numpy as np
from collections import defaultdict

with open('/tmp/301358_30m_latest.json') as f:
    data = json.load(f)

bars = data['data']['sz301358']['m30']

parsed = []
for b in bars:
    t = b[0]
    day = t[:8]
    o = float(b[1])
    c = float(b[2])
    h = float(b[3])
    l = float(b[4])
    v = float(b[5])
    parsed.append({'t': t, 'day': day, 'o': o, 'c': c, 'h': h, 'l': l, 'v': v})

daily = defaultdict(list)
for p in parsed:
    daily[p['day']].append(p)

sorted_days = sorted(daily.keys())

print('=' * 70)
print('301358 30min K线 -- 最近6个交易日概览')
print('=' * 70)
for d in sorted_days[-6:]:
    g = daily[d]
    total_v = sum(b['v'] for b in g) / 10000
    net = g[-1]['c'] - g[0]['o']
    net_pct = net / g[0]['o'] * 100
    hi = max(b['h'] for b in g)
    lo = min(b['l'] for b in g)
    print('  %s: %2d根 开%6.2f 高%6.2f 低%6.2f 收%6.2f 量%5.0fw %+.2f(%+.2f%%)' % (
        d, len(g), g[0]['o'], hi, lo, g[-1]['c'], total_v, net, net_pct))

# 7/22 完整8根
print('\n' + '=' * 70)
print('7/22 全部30min K线逐根拆解')
print('=' * 70)

last_day = sorted_days[-1]
today = daily[last_day]
total_vol = sum(b['v'] for b in today)

for i, b in enumerate(today):
    hm = b['t'][10:14]
    pct = (b['c']-b['o'])/b['o']*100
    amp = (b['h']-b['l'])/b['o']*100
    vol_pct = b['v']/total_vol*100
    direction = '阳' if b['c'] >= b['o'] else '阴'
    marker = ''
    if i == 0: marker = ' <-开盘'
    if b['h'] == max(bb['h'] for bb in today): marker = ' <-日内高'
    if b['l'] == min(bb['l'] for bb in today): marker = ' <-日内低'
    if i == len(today)-1: marker = ' <-收盘'
    print('  [%d] %s %s O%6.2f H%6.2f L%6.2f C%6.2f vol=%5.1fw(%2d%%) %+.2f%% amp=%.1f%%%s' % (
        i, hm, direction, b['o'], b['h'], b['l'], b['c'], b['v']/10000, int(vol_pct), pct, amp, marker))

# 上午下午量分布
morn = sum(b['v'] for b in today if int(b['t'][10:12]) < 12)
aft = total_vol - morn
print('\n  上午: %.1fw (%d%%)  下午: %.1fw (%d%%)' % (
    morn/10000, morn/total_vol*100, aft/10000, aft/total_vol*100))

# === MACD ===
prices_c = [p['c'] for p in parsed]

def ema(data, period):
    result = [data[0]]
    alpha = 2.0 / (period + 1)
    for i in range(1, len(data)):
        result.append(data[i] * alpha + result[-1] * (1 - alpha))
    return result

ema12 = ema(prices_c, 12)
ema26 = ema(prices_c, 26)
dif = [a - b for a, b in zip(ema12, ema26)]
dea = ema(dif, 9)
macd = [2 * (d - e) for d, e in zip(dif, dea)]

print('\n=== MACD(全320根, 趋势) ===')
print('  最新 DIF=%.4f DEA=%.4f MACD=%.4f' % (dif[-1], dea[-1], macd[-1]))

# 近期交叉
crossings = []
for i in range(1, len(macd)):
    if macd[i-1] <= 0 and macd[i] > 0:
        crossings.append(('金叉', i, parsed[i]['t'], parsed[i]['c']))
    elif macd[i-1] >= 0 and macd[i] < 0:
        crossings.append(('死叉', i, parsed[i]['t'], parsed[i]['c']))

print('\n=== 近期MACD交叉点 ===')
for ctype, idx, timestr, price in crossings[-8:]:
    print('  %s @ %s 价格=%.2f' % (ctype, timestr[:12], price))

# 只取最近5天做MA
recent_bars = [p for d in sorted_days[-5:] for p in daily[d]]
rc = [p['c'] for p in recent_bars]

print('\n=== MA均线(最近5天, MA2/5/10/20) ===')
ma_dict = {}
for p in [2, 5, 10, 20]:
    vals = []
    for i in range(len(rc)):
        start = max(0, i - p + 1)
        vals.append(np.mean(rc[start:i+1]))
    ma_dict[p] = vals
    last = vals[-1]
    prev = vals[-2] if len(vals) > 1 else last
    trend = 'up' if last > prev else 'down'
    gap = (last - rc[-1]) / rc[-1] * 100
    print('  MA%d: %.2f (%s, 距现价%+.2f%%)' % (p, last, trend, gap))

# === 5天日间结构对比 ===
print('\n' + '=' * 70)
print('近5日 30min走势节奏对比')
print('=' * 70)

for d in sorted_days[-5:]:
    g = daily[d]
    net = g[-1]['c'] - g[0]['o']
    net_pct = net / g[0]['o'] * 100
    total_v = sum(b['v'] for b in g) / 10000
    hi = max(b['h'] for b in g)
    lo = min(b['l'] for b in g)
    
    # 分段
    first3 = g[:3]  # 9:30-10:30
    mid2 = g[3:5]   # 11:00-11:30
    last3 = g[5:]    # 13:30-15:00
    
    f3_net = first3[-1]['c'] - first3[0]['o'] if len(first3) >= 2 else 0
    f3_v = sum(b['v'] for b in first3) / 10000
    l3_net = last3[-1]['c'] - last3[0]['o'] if len(last3) >= 2 else 0
    l3_v = sum(b['v'] for b in last3) / 10000
    
    direction = '涨' if net > 0 else '跌' if net < 0 else '平'
    print('\n  %s [%s] 开%.2f->收%.2f (%+.2f, %+.2f%%) 量%.0fw 振幅%.2f-%.2f=%.2f' % (
        d, direction, g[0]['o'], g[-1]['c'], net, net_pct, total_v, hi, lo, hi-lo))
    print('    早盘(9:30-10:30): %+.2f 量%.0fw | 尾盘(13:30-15:00): %+.2f 量%.0fw' % (
        f3_net, f3_v, l3_net, l3_v))

# === 7/22 vs 7/21 对比 ===
print('\n' + '=' * 70)
print('7/21 vs 7/22 30min结构对比')
print('=' * 70)

d21 = daily.get('20260721', [])
d22 = daily.get('20260722', [])

if d21 and d22:
    print('  7/21: 开%.2f 高%.2f 低%.2f 收%.2f 量%.0fw' % (
        d21[0]['o'], max(b['h'] for b in d21), min(b['l'] for b in d21), d21[-1]['c'], sum(b['v'] for b in d21)/10000))
    print('  7/22: 开%.2f 高%.2f 低%.2f 收%.2f 量%.0fw' % (
        d22[0]['o'], max(b['h'] for b in d22), min(b['l'] for b in d22), d22[-1]['c'], sum(b['v'] for b in d22)/10000))
    
    # 逐30min对比
    print('\n  逐30min时段对比:')
    for i in range(min(len(d21), len(d22))):
        b21 = d21[i]
        b22 = d22[i]
        hm = b21['t'][10:14]
        c21 = b21['c']
        c22 = b22['c']
        v21 = b21['v']/10000
        v22 = b22['v']/10000
        print('    %s: 7/21 C%.2f V%.1fw | 7/22 C%.2f V%.1fw | 价差%+.2f 量比%.2f' % (
            hm, c21, v21, c22, v22, c22-c21, v22/v21 if v21 else 0))

# === 引用近10根MACD柱趋势 ===
print('\n=== 最近10根MACD柱趋势 ===')
for i in range(-10, 0):
    idx = len(macd) + i
    t_str = parsed[idx]['t']
    sign = '+' if macd[idx] > 0 else '-'
    bar_len = int(abs(macd[idx]) * 50)
    bar_str = sign * min(bar_len, 30)
    print('  %s DIF=%.4f DEA=%.4f MACD=%+.4f %s' % (t_str[:12], dif[idx], dea[idx], macd[idx], bar_str))

# === 30min级别支撑/阻力 ===
print('\n' + '=' * 70)
print('30min级别支撑/阻力位')
print('=' * 70)

# 近5天所有30min K线的高低点
recent_5d = [p for d in sorted_days[-5:] for p in daily[d]]
all_h = [p['h'] for p in recent_5d]
all_l = [p['l'] for p in recent_5d]
all_c = [p['c'] for p in recent_5d]

# 密集成交区
price_levels = sorted(set([round(p, 1) for p in all_h + all_l + all_c]))
print('\n近5日30min价格频次:')
from collections import Counter
all_prices = [round(p, 1) for p in all_h + all_l + all_c]
freq = Counter(all_prices)
for price, count in freq.most_common(15):
    bar = '#' * count
    print('  %6.1f: %2d次 %s' % (price, count, bar))

# 当前价
print('\n当前收盘: %.2f' % parsed[-1]['c'])
print('\n阻力位 (由近到远):')
resistances = [60.60, 61.04, 61.79, 62.26, 62.60, 63.10]
for r in resistances:
    if r > parsed[-1]['c']:
        gap = (r - parsed[-1]['c']) / parsed[-1]['c'] * 100
        print('  %6.2f (+%.2f%%)' % (r, gap))

print('\n支撑位 (由近到远):')
supports = [60.35, 60.00, 59.90, 59.50, 58.68, 58.08, 57.54]
for s in supports:
    if s < parsed[-1]['c']:
        gap = (s - parsed[-1]['c']) / parsed[-1]['c'] * 100
        print('  %6.2f (%.2f%%)' % (s, gap))
