# -*- coding: utf-8 -*-
"""000636 风华高科 四周期形态识别 + 支撑/压力位计算"""
import json, re
from collections import defaultdict

BASE = '/data/hermes/workspace/MyDocuments/stocks/000636/data'

# ---------- 1. 实时行情 ----------
q = json.load(open(f'{BASE}/quote.json'))
d = q[0] if isinstance(q, list) else q
print('=== 实时行情 ===')
print('名称:', d.get('name'), '| 现价:', d.get('price'), '| 涨跌幅:', d.get('changePercent'),
      '| 量比:', d.get('volumeRatio'), '| 换手:', d.get('turnoverRate'),
      '| 今开:', d.get('open'), '| 昨收:', d.get('prevClose'),
      '| high:', d.get('high'), '| low:', d.get('low'))
print('成交额(元):', d.get('amount'), '| 市值:', d.get('marketCapital', 'N/A'))

# ---------- 2. 大盘对比 ----------
raw = open(f'{BASE}/market.txt', encoding='latin-1').read()
for line in raw.split(';'):
    m = re.search(r'v_(.+?)="(.+?)"', line.strip())
    if m:
        f = m.group(2).split('~')
        if len(f) > 40:
            print(f"指数/对比 {m.group(1)} {f[1]}: 价={f[3]} 涨跌幅={f[32]}%")

# ---------- 3. K线解析 (腾讯字段顺序: date,open,close,high,low,vol) ----------
def load_kline(fname, code='sz000636'):
    data = json.load(open(f'{BASE}/{fname}'))
    node = data['data'][code]
    for key in ('qfqday', 'qfqweek', 'qfqmonth', 'day', 'week', 'month'):
        if key in node and isinstance(node[key], list):
            return [row[:6] for row in node[key] if len(row) >= 6]
    return None

daily = load_kline('kline_day.json')
weekly = load_kline('kline_week.json')
monthly = load_kline('kline_month.json')
print('\n=== 数据校验 ===')
print('日K根数:', len(daily), '首:', daily[0][:2], '末:', daily[-1][:6])
print('周K根数:', len(weekly), '末:', weekly[-1][:6])
print('月K根数:', len(monthly), '末:', monthly[-1][:6])

# 用新浪交叉验证字段顺序(抽最近3天)
# ---------- 4. 60分钟K线 ----------
mk = json.load(open(f'{BASE}/kline_60min.json'))
mnode = mk['data']['sz000636']
mkey = [k for k in mnode if k.startswith('m60')][0]
min60 = [row[:6] for row in mnode[mkey] if len(row) >= 6]
print('60min根数:', len(min60), '末:', min60[-1][:6])

# ---------- 5. 技术指标计算 ----------
def to_df(rows):
    out = []
    for r in rows:
        out.append({'date': r[0], 'open': float(r[1]), 'close': float(r[2]),
                    'high': float(r[3]), 'low': float(r[4]), 'vol': float(r[5])})
    return out

ddf = to_df(daily)
wdf = to_df(weekly)
mdf = to_df(monthly)
hdf = to_df(min60)

def ma(closes, n, i):
    if i + 1 < n: return None
    return sum(closes[i-n+1:i+1]) / n

closes = [x['close'] for x in ddf]
highs = [x['high'] for x in ddf]
lows = [x['low'] for x in ddf]
vols = [x['vol'] for x in ddf]
n = len(ddf)

print('\n=== 日线关键指标 ===')
for p in (5, 10, 20, 60, 120):
    v = ma(closes, p, n-1)
    print(f'MA{p}: {v:.3f}' if v else f'MA{p}: N/A')
print('60日最高:', max(highs[-60:]), '60日最低:', min(lows[-60:]))
print('120日最高:', max(highs[-120:]), '120日最低:', min(lows[-120:]))
print('最近10日:')
for x in ddf[-10:]:
    pct = (x['close'] - ddf[ddf.index(x)-1]['close']) / ddf[ddf.index(x)-1]['close'] * 100 if ddf.index(x) > 0 else 0
    print(f"  {x['date']} O:{x['open']:.2f} H:{x['high']:.2f} L:{x['low']:.2f} C:{x['close']:.2f} vol:{x['vol']:.0f}")

# BOLL(20,2)
m20 = ma(closes, 20, n-1)
std20 = (sum((c - ma(closes,20,i))**2 for i, c in enumerate(closes[-20:], start=n-20)) / 20) ** 0.5
print(f'BOLL: 上轨 {m20+2*std20:.3f} 中轨 {m20:.3f} 下轨 {m20-2*std20:.3f}')

# ---------- 6. 摆动点识别(日线, fractal) ----------
def swings(df, k=3):
    """k根左右的fractal摆动点"""
    sw_hi, sw_lo = [], []
    for i in range(k, len(df)-k):
        window = df[i-k:i+k+1]
        if df[i]['high'] == max(w['high'] for w in window):
            sw_hi.append((i, df[i]['date'], df[i]['high']))
        if df[i]['low'] == min(w['low'] for w in window):
            sw_lo.append((i, df[i]['date'], df[i]['low']))
    return sw_hi, sw_lo

sw_hi, sw_lo = swings(ddf, 3)
print('\n=== 近90日摆动高点(压力候选) ===')
n90 = max(0, n-90)
for i, dt, h in sw_hi:
    if i >= n90:
        print(f'  {dt} 高点 {h}')
print('=== 近90日摆动低点(支撑候选) ===')
for i, dt, l in sw_lo:
    if i >= n90:
        print(f'  {dt} 低点 {l}')

# ---------- 7. 筹码分布(均匀分配法, 近120日) ----------
bins = defaultdict(float)
n120 = max(0, n-120)
for x in ddf[n120:]:
    lo, hi, vol = x['low'], x['high'], x['vol']
    steps = max(int(round((hi - lo) / 0.05)), 1)
    for j in range(steps):
        p = round((lo + (hi-lo)*j/steps) / 0.05) * 0.05
        bins[p] += vol / steps
total = sum(bins.values())
peaks = sorted(bins.items(), key=lambda kv: -kv[1])[:15]
print('\n=== 近120日筹码分布峰(0.05元粒度, 前15) ===')
for p, v in sorted(peaks):
    print(f'  {p:.2f}元: {v/total*100:.2f}%')

# ---------- 8. 形态识别数据点 ----------
print('\n=== 近40日高低点序列(形态判定用) ===')
for x in ddf[-40:]:
    print(f"  {x['date']} H:{x['high']:.2f} L:{x['low']:.2f} C:{x['close']:.2f}")

print('\n=== 近26周高低点(周线形态) ===')
for x in wdf[-26:]:
    print(f"  {x['date']} H:{x['high']:.2f} L:{x['low']:.2f} C:{x['close']:.2f}")

print('\n=== 近12月高低点(月线形态) ===')
for x in mdf[-12:]:
    print(f"  {x['date']} H:{x['high']:.2f} L:{x['low']:.2f} C:{x['close']:.2f}")

print('\n=== 近32根60分钟K线 ===')
for x in hdf[-32:]:
    print(f"  {x['date']} O:{x['open']:.2f} H:{x['high']:.2f} L:{x['low']:.2f} C:{x['close']:.2f}")

# 均线多周期
wc = [x['close'] for x in wdf]
print('\n周线MA: MA5=%.3f MA10=%.3f MA20=%.3f' % (sum(wc[-5:])/5, sum(wc[-10:])/10, sum(wc[-20:])/20) if len(wc)>=20 else '')
mc = [x['close'] for x in mdf]
print('月线MA: MA5=%.3f MA10=%.3f' % (sum(mc[-5:])/5, sum(mc[-10:])/10))
