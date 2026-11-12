# -*- coding: utf-8 -*-
"""600460 士兰微 全新 K 线图：10-19 重新分析支撑压力位
红涨绿跌，白底，支撑/压力线+形态标注+事件标注。"""
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

k = json.load(open('/tmp/600460_klines_new2.json'))
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

# ---- 显示窗口：日线最后 55 根 ----
WS = 55
i0 = N - WS

# ============ 布局：2×2 ============
fig = plt.figure(figsize=(17, 11), facecolor='white')
gs = fig.add_gridspec(2, 2, width_ratios=[3, 1], height_ratios=[3, 1.1],
                      hspace=0.18, wspace=0.12,
                      left=0.055, right=0.985, top=0.90, bottom=0.05)
ax = fig.add_subplot(gs[0, 0])       # 主图 日线
axv = fig.add_subplot(gs[1, 0], sharex=ax)  # 成交量
axw = fig.add_subplot(gs[0, 1])      # 周线
axm = fig.add_subplot(gs[1, 1])      # 月线

def draw_kline(ax, dates, o, c, h, l, v, x0, n_show, ma_list=None):
    """x0: 全序列起始索引, n_show: 显示根数; ma_list: [(name, 全序列数组, color)]"""
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

def pos(date_str):
    j = gi(date_str)
    return j - i0 if j >= i0 else None

# 支撑压力水平线
def hline(y, txt, color, lw=1.0, ls='--', fs=9, alpha=0.85):
    ax.axhline(y, color=color, linewidth=lw, linestyle=ls, alpha=alpha)
    ax.text(WS + 0.6, y, txt, fontproperties=fm.FontProperties(fname=font_path, size=fs),
            color=color, va='center')

# ========== 关键支撑位（从下到上，基于最新数据重新梳理）==========
hline(24.62, '支撑 24.62 (4月低/月线方向底/当前距0.3)', '#da3633', lw=1.5)
hline(24.88, '支撑 24.88 (10·19低/今日最低)', '#e65100')
hline(26.54, '支撑 26.54 (10·13低/超跌反弹低点)', '#c62828')
hline(27.39, '铁底 27.39 (8·3/60日低/月线关键支撑)', '#c62828', lw=1.2)
hline(27.80, '支撑 27.80 (10·9/10·12双底)', '#d84315')
hline(29.00, '否决线 29.00 (9·11低/五步法①②铁底/已破)', '#00897B', lw=1.5, ls='-')

# ========== 关键压力位（从下到上）==========
hline(26.22, '压力 MA5 26.22 (短线反弹首阻/当前距1.3)', '#f0883e')
hline(27.39, '压力 27.39 (铁底/月线关键/失守即反压)', '#c62828', ls='-', lw=0.8)
hline(28.03, '压力 MA10 28.03 (中期均线)', '#2196F3')
hline(29.00, '压力 29.00 (否决线/前低位反压/已破)', '#00897B', ls='-', lw=0.8)
hline(30.04, '压力 MA20 30.04 (中枢均线)', '#9C27B0')
hline(31.28, '压力 MA60 31.28 (长期均线/空头排列确认)', '#da3633')
hline(32.89, '压力 32.89 (9·29高/缺口上沿)', '#e65100')
hline(34.05, '压力 34.05 (9·1高/三角形上沿/突破位)', '#e65100', ls='-', lw=1.0)
hline(37.43, '压力 37.43 (8·24高/套牢区下沿)', '#e65100')
ax.text(1.5, 38.5, '上方 37~57 为 6-7 月巨量套牢区（7·1 顶 57.02）',
        fontproperties=fp_sm, color=GRAY)

# 设置 Y 轴范围（根据最新价格调整）
ax.set_ylim(23.5, 39.5)

# ============ 下行通道（10·9以来）==========
p_1009 = pos('2026-10-09')
p_1019 = pos('2026-10-19')
if p_1009 is not None and p_1019 is not None:
    # 上轨：10·9高 29.52 -> 10·19高 25.55
    s_up = (25.55 - 29.52) / (p_1019 - p_1009)
    ax.plot([p_1009, p_1019], [29.52, 25.55], color='#c62828', linewidth=1.8, linestyle='--', zorder=4, label='下行通道上轨')
    # 下轨：10·9低 27.80 -> 10·19低 24.88
    s_dn = (24.88 - 27.80) / (p_1019 - p_1009)
    ax.plot([p_1009, p_1019], [27.80, 24.88], color='#2e7d32', linewidth=1.8, linestyle='--', zorder=4, label='下行通道下轨')
    # 延伸
    p_now = WS - 1
    ax.plot([p_1009, p_now], [29.52, 29.52 + s_up * (p_now - p_1009)], color='#c62828', linewidth=1.0, linestyle=':', alpha=0.6, zorder=3)
    ax.plot([p_1009, p_now], [27.80, 27.80 + s_dn * (p_now - p_1009)], color='#2e7d32', linewidth=1.0, linestyle=':', alpha=0.6, zorder=3)

# 事件标注
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

ev('2026-10-09', '10·9 破29.0否决线', above=False)
ev('2026-10-13', '10·13 低26.54 超跌', above=False)
ev('2026-10-19', '10·19 破24.62月线方向底', above=False)

ax.set_ylabel('价格（元）', fontproperties=fp_mid)
ax.legend(prop=fp_sm, loc='upper left')
ax.set_title('士兰微 600460 · 日线 · 10-19 破月线方向底 24.62（红涨绿跌）· 2026-10-19',
             fontproperties=fp_title, pad=12)

# ============ 成交量 ============
for i in range(WS):
    gi2 = i0 + i
    col = RED if dc[gi2] >= do[gi2] else GREEN
    axv.bar(i, dv[gi2] / 1e4, width=0.76, color=col, alpha=0.85)
vma5 = ma(dv, 5)
axv.plot(np.arange(WS), vma5[i0:i0 + WS] / 1e4, color='#2196F3', linewidth=1.0, label='5日均量')
axv.set_ylabel('成交量(万手)', fontproperties=fp_sm)
axv.legend(prop=fp_sm, loc='upper left')
axv.set_xlim(-1.2, WS - 1 + 1.2)

# ============ 周线 ============
WWS = 13
wx = draw_kline(axw, wd, wo, wc, wh, wl, wv, len(weekly) - WWS, WWS,
                [('MA10w', wmw10, '#2196F3'), ('MA20w', wmw20, '#da3633')])
axw.axhline(29.00, color='#00897B', linestyle=':', linewidth=1.0)
axw.text(0.2, 29.15, '否决线 29.00', fontproperties=fp_sm, color='#00897B')
axw.set_title('周线（13周）：破位下行，空头排列', fontproperties=fp_mid, pad=6)
axw.set_ylabel('价格（元）', fontproperties=fp_sm)

# ============ 月线 ============
MWS = 8
mx = draw_kline(axm, md, mo, mc, mh, ml, mv, len(monthly) - MWS, MWS)
axm.text(0.2, 55.5, '月线方向已反转：低点 24.62->27.39->29.00->26.54->24.88',
         fontproperties=fp_sm, color='#c62828')
axm.text(4.2, 38.5, '关键：24.62(4月低)已破，方向彻底反转',
         fontproperties=fp_sm, color='#2e7d32')
axm.set_title('月线（8月）：方向彻底反转，寻找新底', fontproperties=fp_mid, pad=6)
axm.set_ylabel('价格（元）', fontproperties=fp_sm)

out = '/data/hermes/workspace/MyDocuments/stocks/600460/600460_kline_new_20261019.png'
fig.savefig(out, dpi=140, facecolor='white', bbox_inches='tight')
print('saved:', out)