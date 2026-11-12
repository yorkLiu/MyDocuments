# -*- coding: utf-8 -*-
"""600460 士兰微 多周期K线图：日线(主图+成交量) / 周线 / 月线
红涨绿跌，白底，支撑压力线+形态连线+事件标注。"""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Rectangle

font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
prop = fm.FontProperties(fname=font_path)
fp_title = fm.FontProperties(fname=font_path, size=15, weight='bold')
fp_mid = fm.FontProperties(fname=font_path, size=10)
fp_sm = fm.FontProperties(fname=font_path, size=8.5)
plt.rcParams['axes.unicode_minus'] = False

RED, GREEN = '#ff1744', '#00e676'   # 红涨绿跌
GRAY = '#555555'

k = json.load(open('/tmp/600460_klines2.json'))
daily, weekly, monthly = k['daily'], k['weekly'], k['monthly']

def arrays(rows):
    return (np.array([r['date'] for r in rows]),
            np.array([float(r['open']) for r in rows]),
            np.array([float(r['close']) for r in rows]),
            np.array([float(r['high']) for r in rows]),
            np.array([float(r['low']) for r in rows]),
            np.array([float(r['vol']) for r in rows]))

dd, do, dc, dh, dl, dv = arrays(daily)
wd, wo, wc, wh, wl, wv = arrays(weekly)
md, mo, mc, mh, ml, mv = arrays(monthly)

def ma(arr, n):
    out = np.full(len(arr), np.nan)
    for i in range(n - 1, len(arr)):
        out[i] = arr[i - n + 1:i + 1].mean()
    return out

N = len(daily)
ma5, ma10, ma20, ma60 = ma(dc, 5), ma(dc, 10), ma(dc, 20), ma(dc, 60)
wmw10, wmw20 = ma(wc, 10), ma(wc, 20)

# ---- 显示窗口：日线最后55根 ----
WS = 55
i0 = N - WS
idx = np.arange(i0, N)

fig = plt.figure(figsize=(17, 11), facecolor='white')
gs = fig.add_gridspec(2, 3, width_ratios=[3, 1, 1], height_ratios=[3, 1.1],
                      hspace=0.18, wspace=0.12,
                      left=0.055, right=0.985, top=0.90, bottom=0.05)
ax = fig.add_subplot(gs[0, 0])       # 主图 日线
axv = fig.add_subplot(gs[1, 0], sharex=ax)  # 日线成交量
axw = fig.add_subplot(gs[0, 1])      # 周线
axm = fig.add_subplot(gs[1, 1])      # 月线
axf = fig.add_subplot(gs[0, 2])      # 9·22 盘中分时(价格)
axfv = fig.add_subplot(gs[1, 2], sharex=axf)  # 9·22 盘中分钟量能

def draw_kline(ax, dates, o, c, h, l, v, x0, n_show, ma_list=None):
    """x0: 全序列中起始索引, n_show: 显示根数; ma_list: [(name, 全序列数组, color)]"""
    sl = slice(x0, x0 + n_show)
    xs = np.arange(n_show)
    for i in range(n_show):
        gi = x0 + i
        up = c[gi] >= o[gi]
        col = RED if up else GREEN
        ax.plot([i, i], [l[gi], h[gi]], color=col, linewidth=0.8, zorder=2)
        body_lo, body_h = min(o[gi], c[gi]), max(o[gi], c[gi])
        bh = max(body_h - body_lo, 0.06)
        ax.add_patch(Rectangle((i - 0.38, body_lo), 0.76, bh,
                               facecolor=col if not up else 'white',
                               edgecolor=col, linewidth=0.9, zorder=3))
    for name, m, color in (ma_list or []):
        seg = m[sl]
        if np.any(~np.isnan(seg)):
            ax.plot(xs, seg, color=color, linewidth=0.9, alpha=0.9, label=name)
    step = max(n_show // 12, 1)
    tickpos = [i for i in range(n_show) if i % step == 0]
    ax.set_xticks([xs[i] for i in tickpos])
    ax.set_xticklabels([dates[x0 + i][5:] for i in tickpos], rotation=0, fontsize=8)
    ax.set_xlim(-1.2, n_show - 1 + 1.2)
    return xs

# ============ 主图 ============
xs = draw_kline(ax, dd, do, dc, dh, dl, dv, i0, WS,
                [('MA5', ma5, '#f0883e'), ('MA10', ma10, '#2196F3'),
                 ('MA20', ma20, '#9C27B0'), ('MA60', ma60, '#da3633')])
def gi(date_str):
    return list(dd).index(date_str)

# 支撑压力水平线
def hline(y, txt, color, lw=1.0, ls='--', fs=9, alpha=0.85):
    ax.axhline(y, color=color, linewidth=lw, linestyle=ls, alpha=alpha)
    ax.text(WS + 0.6, y, txt, fontproperties=fm.FontProperties(fname=font_path, size=fs),
            color=color, va='center')
hline(27.39, '铁底 27.39 (60日低/8·3)', '#da3633')
hline(29.00, '否决线 29.00 (9·11低)', '#00897B')
hline(30.88, '压力 MA20 30.88 (今收26.99已破)', '#1565C0')
hline(32.04, '压力 MA60 32.04 (9·22高34.47未破)', '#6A1B9A')
hline(37.43, '前高 37.43 (8·24/套牢区下沿)', '#e65100')
hline(34.05, '9·1 上沿 34.05 = 突破位', '#e65100', ls='-', lw=0.8, alpha=0.55, fs=8.5)
ax.text(1.5, 38.5, '上方 37~57.02 为 6-7 月放量套牢区（7·1 顶 57.02，图外）',
        fontproperties=fp_sm, color=GRAY)
ax.set_ylim(26.4, 39.3)

# 收敛三角形：两条边画到交点(顶点)为止，内部楔形浅色填充，边加粗
def pos(date_str):
    j = gi(date_str)
    return j - i0 if j >= i0 else None
p_824, p_901 = pos('2026-08-24'), pos('2026-09-01')
p_803, p_911 = pos('2026-08-03'), pos('2026-09-11')
s1 = (34.05 - 37.43) / (p_901 - p_824)          # 上边斜率(负)
s2 = (29.00 - 27.39) / (p_911 - p_803)           # 下边斜率(正)
top_y = lambda x: 37.43 + s1 * (x - p_824)
bot_y = lambda x: 27.39 + s2 * (x - p_803)
xv = (27.39 - s2 * p_803 - 37.43 + s1 * p_824) / (s1 - s2)   # 交点x
yv = top_y(xv)
from matplotlib.patches import Polygon
poly = Polygon([(p_824, 37.43), (p_901, 34.05), (xv, yv),
                (p_911, 29.00), (p_803, 27.39)],
               closed=True, facecolor='#FF9800', alpha=0.10, edgecolor='none', zorder=1)
ax.add_patch(poly)
ax.plot([p_824, xv], [37.43, yv], color='#e65100', linewidth=2.3, zorder=4, label='上边(降)')
ax.plot([p_803, xv], [27.39, yv], color='#00897B', linewidth=2.3, zorder=4, label='下边(升)')
ax.plot([xv], [yv], marker='v', color='#333333', markersize=8, zorder=5)
ax.text(p_824 + 0.5, 37.9, '上边 37.43→34.05 (降)', fontproperties=fp_sm, color='#e65100')
ax.text(p_803 + 0.5, 26.85, '下边 27.39→29.00 (升)', fontproperties=fp_sm, color='#00897B')
ax.text(xv - 6.5, yv + 1.7, '顶点≈%.1f 收口' % yv, fontproperties=fp_sm, color='#333333')
# 收口后放量点火(真实突破发生在顶点收口处)
p_916 = pos('2026-09-16')
if p_916 is not None:
    j916 = i0 + p_916
    ax.annotate('9·16 放量点火\n89.8万手(+4.3%)', xy=(p_916, dl[j916]),
                xytext=(p_916 - 14, 26.9),
                fontproperties=fp_sm, color='#c62828',
                arrowprops=dict(arrowstyle='->', color='#c62828', lw=1.0,
                                connectionstyle='arc3,rad=0.25'), zorder=6)

# ============ 9·14 收口后的上攻结构 ============
up_dates = ['2026-09-14', '2026-09-15', '2026-09-16', '2026-09-17', '2026-09-18', '2026-09-21', '2026-09-22', '2026-09-23', '2026-09-24', '2026-09-28', '2026-09-29', '2026-09-30', '2026-10-08', '2026-10-09', '2026-10-12', '2026-10-13', '2026-10-14']
up_lows = [29.31, 29.51, 29.82, 31.0, 31.77, 32.91, 33.21, 32.90, 32.70, 31.27, 31.06, 30.69, 29.39, 27.80, 27.80, 26.54, 27.50]
up_hs = [30.2, 30.46, 31.46, 32.68, 33.30, 34.00, 34.47, 33.87, 33.58, 32.69, 32.44, 32.30, 31.70, 29.52, 28.84, 27.39, 27.69]
pxs = [pos(d) for d in up_dates]
p_good = [(a, b, c) for a, b, c in zip(pxs, up_lows, up_hs) if a is not None]
# 低点抬升台阶线（蓝虚线）
ax.plot([a for a, _, _ in p_good], [b for _, b, _ in p_good],
        color='#1565C0', linewidth=1.8, linestyle='--', marker='o', markersize=4,
        zorder=5, label='低点抬升(台阶)')
# 高点抬升台阶线（品红点线，不画9·14的高，因为它收口后起点）
ax.plot([a for a, _, c in p_good[1:]], [c for _, _, c in p_good[1:]],
        color='#C2185B', linewidth=1.4, linestyle=':', marker='o', markersize=4,
        zorder=5, label='高点抬升(台阶)')
ax.text(pxs[1] + 0.4, up_lows[1] - 1.5,
        '收口后台阶: 低点 29.31→32.91 抬高\n高点 31.46→34.00 上移',
        fontproperties=fp_sm, color='#1565C0')
# 9·21 高 34.00 测 34.05 上沿
p_921 = pxs[5]
ax.annotate('9·21 高 34.00\n测上沿 34.05', xy=(p_921, up_hs[5]),
            xytext=(p_921 - 9, 35.2),
            fontproperties=fp_sm, color='#C2185B',
            arrowprops=dict(arrowstyle='->', color='#C2185B', lw=1.1,
                            connectionstyle='arc3,rad=0.2'), zorder=7)

# 事件标注（标签放空白区，箭头指向K线端点）
def ev(date_str, txt, above=True):
    p = pos(date_str)
    if p is None:
        return
    j = i0 + p
    y = dl[j] if not above else dh[j]
    off = -1.6 if not above else 1.6
    ax.annotate(txt, xy=(p, y), xytext=(p - 6, y + off),
                fontproperties=fp_sm, color='#333',
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#ECEFF1', edgecolor=GRAY, alpha=0.9),
                arrowprops=dict(arrowstyle='->', color=GRAY, lw=0.9,
                                connectionstyle='arc3,rad=0.15'), zorder=6)
ev('2026-08-03', '8·3 铁底 27.39', above=False)
ev('2026-09-11', '9·11 低 29.00', above=False)
ev('2026-09-14', '9·14 地量(35%均量)', above=False)
ev('2026-09-16', '9·16 放量+4.3%点火', above=True)
ev('2026-09-22', '9·22 盘中高34.47 破34.05 回落', above=True)
ev('2026-09-23', '9·23 低32.90 守台阶 V型反抽', above=False)
ev('2026-09-24', '9·24 低32.70 跌破台阶 破位', above=False)
ev('2026-09-28', '9·28 低31.27 缩量回踩 MA5/MA20', above=False)
ev('2026-10-12', '10·12 低27.80 缩量磨底', above=False)
ev('2026-10-13', '10·13 低26.54 自由落体', above=False)
ev('2026-10-14', '10·14 高开 缩量企稳 27.5', above=True)

ax.set_ylabel('价格（元）', fontproperties=fp_mid)
ax.legend(prop=fp_sm, loc='upper left')
ax.set_title('士兰微 600460 · 日线 · 收敛三角形 10·14 缩量企稳 27.5 关口（红涨绿跌）· 2026-10-14',
             fontproperties=fp_title, pad=12)

# ============ 成交量 ============
for i in range(WS):
    gi2 = i0 + i
    col = RED if dc[gi2] >= do[gi2] else GREEN
    axv.bar(i, dv[gi2] / 1e4, width=0.76, color=col, alpha=0.85)
vma5 = ma(dv, 5)
axv.plot(np.arange(WS), vma5[i0:i0 + WS] / 1e4, color='#2196F3', linewidth=1.0, label='5日均量')
axv.axhline(vma5[i0 + (gi('2026-09-14') - i0)] / 1e4, color='#9C27B0', linestyle=':', linewidth=1)
axv.text(2, vma5[i0 + (gi('2026-09-14') - i0)] / 1e4 * 1.04, '地量基准 37万手', fontproperties=fp_sm, color='#9C27B0')
axv.set_ylabel('成交量(万手)', fontproperties=fp_sm)
axv.legend(prop=fp_sm, loc='upper left')
axv.set_xlim(-1.2, WS - 1 + 1.2)

# ============ 周线 ============
WWS = 13
wx = draw_kline(axw, wd, wo, wc, wh, wl, wv, len(weekly) - WWS, WWS,
                [('MA10w', wmw10, '#2196F3'), ('MA20w', wmw20, '#da3633')])
axw.axhline(29.00, color='#00897B', linestyle=':', linewidth=1.0)
axw.text(0.2, 29.15, '否决线 29.00', fontproperties=fp_sm, color='#00897B')
axw.set_title('周线（13周）：两连阳，节奏刚起', fontproperties=fp_mid, pad=6)
axw.set_ylabel('价格（元）', fontproperties=fp_sm)

# ============ 月线 ============
MWS = 8
mx = draw_kline(axm, md, mo, mc, mh, ml, mv, len(monthly) - MWS, MWS)
axm.text(0.2, 55.5, '6月大阳冲54.58→7月崩至27.42', fontproperties=fp_sm, color='#c62828')
axm.text(4.2, 38.5, '8月反弹+21%', fontproperties=fp_sm, color='#2e7d32')
axm.set_title('月线（8月）：方向未反转，7月巨阴待修复', fontproperties=fp_mid, pad=6)
axm.set_ylabel('价格（元）', fontproperties=fp_sm)

# ============ 9·22 盘中分时 ============
import json as _json
_m2 = _json.load(open('/tmp/600460_min2.json'))
mT, mP = _m2['T'], _m2['P']
_mCV = _m2['CV']
nM = len(mT)
_prev = 27.75  # 10·13 收盘
# per-minute volume
_mdiff = np.array([0.0] + [_mCV[i] - _mCV[i - 1] for i in range(1, nM)])
_vwap = _mCV[-1] and 2049537264.0 / (_mCV[-1] * 100)  # total amount / total shares
# cumulative VWAP approx using CA
_mCA = _m2['CA']
_vwap = _mCA[-1] / (_mCV[-1] * 100)
# x: minutes; show every ~10th label
axf.plot(range(nM), mP, color='#e65100', linewidth=1.6, zorder=4)
# VWAP line
vwap_cum = np.array([_mCA[i] / (_mCV[i] * 100) for i in range(1, nM)])
axf.plot(range(1, nM), vwap_cum, color='#1565C0', linewidth=1.3, linestyle='--',
        zorder=5, label='均价线(VWAP)')
axf.axhline(34.05, color='#C2185B', linewidth=1.1, ls=':', alpha=0.9)
axf.text(0.3, 34.18, '突破位 34.05', fontproperties=fp_sm, color='#C2185B')
axf.axhline(_prev, color=GRAY, linewidth=1.0, ls='-', alpha=0.7)
axf.text(0.3, _prev + 0.05, '昨收 27.75', fontproperties=fp_sm, color=GRAY)
axf.axhline(_vwap, color='#1565C0', linewidth=0.8, alpha=0.35)
axf.text(nM - 12, _vwap - 0.03, '均价 %.2f' % _vwap, fontproperties=fp_sm, color='#1565C0')
_hi_i = mP.index(max(mP)); _lo_i = mP.index(min(mP))
axf.annotate('高 %.2f (%+.1f%%)' % (mP[_hi_i], (mP[_hi_i] / _prev - 1) * 100),
             xy=(_hi_i, mP[_hi_i]), xytext=(_hi_i - 6, mP[_hi_i] + 0.25),
             fontproperties=fp_sm, color='#c62828',
             arrowprops=dict(arrowstyle='->', color='#c62828', lw=1.0,
                             connectionstyle='arc3,rad=-0.2'), zorder=7)
axf.annotate('低 %.2f' % mP[_lo_i], xy=(_lo_i, mP[_lo_i]),
             xytext=(_lo_i + 2, mP[_lo_i] - 0.55),
             fontproperties=fp_sm, color='#2e7d32',
             arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=1.0,
                             connectionstyle='arc3,rad=0.2'), zorder=7)
axf.annotate('现 %.2f (%+.1f%%)' % (mP[-1], (mP[-1] / _prev - 1) * 100),
             xy=(nM - 1, mP[-1]), xytext=(nM - 14, mP[-1] + 0.35),
             fontproperties=fp_sm, color='#333',
             arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.0,
                             connectionstyle='arc3,rad=0.1'), zorder=7)
# x ticks (HH:MM)
tick = list(range(0, nM, 10))
axf.set_xticks(tick)
axf.set_xticklabels(['%s:%s' % (mT[i][0:2], mT[i][2:]) for i in tick], fontsize=7)
axf.set_xlim(-1, nM)
axf.set_ylim(min(mP) - 0.35, max(mP) + 0.6)
axf.set_title('10·14 盘中分时（价格/均价线）· 缩量企稳', fontproperties=fp_mid, pad=6)
axf.set_ylabel('价格（元）', fontproperties=fp_sm)
axf.legend(prop=fp_sm, loc='upper left')
# minute volume bars
colv = []
for i in range(1, nM):
    colv.append('#ff1744' if mP[i] >= _prev else '#00e676')
axfv.bar(range(1, nM), _mdiff[1:] / 1e4, width=0.85, color=colv, alpha=0.85)
axfv.set_ylabel('分钟量(万手)', fontproperties=fp_sm)
axfv.set_xlim(-1, nM)

out = '/data/hermes/workspace/MyDocuments/stocks/600460/600460_kline_20261014.png'
fig.savefig(out, dpi=140, facecolor='white', bbox_inches='tight')
print('saved:', out)
