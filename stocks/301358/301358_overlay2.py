#!/usr/bin/env python3
"""301358 归一化走势叠加图"""
import json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

with open('/data/hermes/workspace/301358_klines.json') as f:
    all_klines = json.load(f)

closes = np.array([k['close'] for k in all_klines])
volumes = np.array([k['volume'] for k in all_klines])
highs = np.array([k['high'] for k in all_klines])
lows = np.array([k['low'] for k in all_klines])
opens = np.array([k['open'] for k in all_klines])
dates = [k['date'] for k in all_klines]
n = len(closes)

# 设置中文字体 - 用系统可用的
import matplotlib.font_manager as fm
font_paths = [
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
]
for fp in font_paths:
    try:
        fm.fontManager.addfont(fp)
        plt.rcParams['font.family'] = fm.FontProperties(fname=fp).get_name()
        print(f"✓ 字体加载: {fp}")
        break
    except:
        pass

seg_defs = [
    {"name": "A", "label": "A 首轮回调(-10%, +27%)", "peak": "2025-07-25", "trough": "2025-10-23"},
    {"name": "B", "label": "B ①浪顶→②浪(-33%, +5%)", "peak": "2025-11-13", "trough": "2025-12-16"},
    {"name": "C", "label": "C 解禁前杀跌(-20%, +24%) ★最像", "peak": "2025-12-26", "trough": "2026-02-06"},
    {"name": "D", "label": "D 缩量回调(-19%, +34%)", "peak": "2026-03-16", "trough": "2026-04-03"},
    {"name": "E", "label": "E C浪下跌(-28%, ongoing)", "peak": "2026-06-23", "trough": None},
]

colors = {'A': '#4caf50', 'B': '#2196f3', 'C': '#e91e63', 'D': '#9c27b0', 'E': '#ff6f00'}

fig, axes = plt.subplots(2, 1, figsize=(22, 16), gridspec_kw={'height_ratios': [1, 1]})
fig.subplots_adjust(hspace=0.25, top=0.93, bottom=0.06, left=0.08, right=0.95)
fig.suptitle('301358 湖南裕能 · 历史下跌段叠加对比 & 段C后续走势', fontsize=20, fontweight='bold')

# ===== 上图：归一化走势叠加 =====
ax1 = axes[0]
ax1.set_title('各下跌段归一化走势叠加（起点=0%，横轴=交易日天数）', fontsize=14, fontweight='bold')
ax1.axhline(y=0, color='#333', linewidth=0.5)
ax1.axhline(y=-30, color='#ccc', linewidth=0.4, linestyle=':')
ax1.axhline(y=-20, color='#ccc', linewidth=0.4, linestyle=':')

segments = {}
for s in seg_defs:
    pi = dates.index(s["peak"])
    ti = dates.index(s["trough"]) if s["trough"] else n-1
    seg_c = closes[pi:ti+1]
    norm = (seg_c / seg_c[0] - 1) * 100
    name = s["name"]
    segments[name] = {"norm": norm, "seg_c": seg_c, "pi": pi, "ti": ti, "def": s}
    ax1.plot(range(len(norm)), norm, color=colors[name], linewidth=2.5 if name in 'CE' else 1.8,
             label=s["label"], alpha=1.0 if name == 'E' else 0.8)
    ax1.annotate(f'{name}({norm[-1]:.1f}%)', xy=(len(norm)-1, norm[-1]),
                fontsize=9, color=colors[name], fontweight='bold',
                xytext=(5, 0), textcoords='offset points')

ax1.set_xlabel('交易日（从高点起算）', fontsize=11)
ax1.set_ylabel('累计涨跌幅(%)', fontsize=11)
ax1.legend(loc='lower left', fontsize=10, framealpha=0.9)
ax1.grid(True, alpha=0.15)

# ===== 下图：段C完整走势（含见底后反弹30日）=====
ax2 = axes[1]
seg_c_data = segments["C"]
pi = seg_c_data["pi"]
ti = seg_c_data["ti"]

ext_dates = dates[pi:n]
ext_closes = closes[pi:n]
ext_vols = volumes[pi:n]
ext_highs = highs[pi:n]
ext_lows = lows[pi:n]
ext_opens = opens[pi:n]

ext_len = min(ti - pi + 31, n - pi)
ext_dates = ext_dates[:ext_len]
ext_closes = ext_closes[:ext_len]
ext_vols = ext_vols[:ext_len]
ext_highs = ext_highs[:ext_len]
ext_lows = ext_lows[:ext_len]
ext_opens = ext_opens[:ext_len]

x = np.arange(ext_len)
trough_x = ti - pi

from matplotlib.patches import FancyBboxPatch
for i in range(ext_len):
    color = '#2e7d32' if i >= trough_x else ('#d32f2f' if ext_closes[i] >= ext_opens[i] else '#2e7d32')
    ax2.plot([i, i], [ext_lows[i], ext_highs[i]], color=color, linewidth=0.6)
    bottom = min(ext_opens[i], ext_closes[i])
    height = abs(ext_closes[i] - ext_opens[i])
    if height < 0.01: height = 0.01
    rect = FancyBboxPatch((i-0.3, bottom), 0.6, height, boxstyle="round,pad=0",
                          facecolor=color, edgecolor=color, linewidth=0.4, alpha=0.8)
    ax2.add_patch(rect)

# 事件标注
event_annotations = [
    (0, "12/26 反弹高点\n73.61元", '#e91e63'),
    (10, "1/14 首探59.04", '#1565c0'),
    (trough_x, "2/06 谷底59.04\n解禁前最后杀跌", '#d32f2f'),
    (trough_x+3, "2/09 解禁3.74亿\n(49.13%)", '#ff9800'),
]
for ex, et, ec in event_annotations:
    if ex < ext_len:
        y_pos = ext_highs[ex] + 3
        ax2.annotate(et, xy=(ex, y_pos), fontsize=8, color=ec, ha='center', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff9c4', alpha=0.8),
                    arrowprops=dict(arrowstyle='->', color=ec, lw=1))

# 反弹区间
ax2.axvspan(trough_x, ext_len-1, alpha=0.08, color='#4caf50')
ax2.annotate('后续30日\n反弹+24.4%', xy=(trough_x+5, ext_closes[trough_x+5]),
            fontsize=11, color='#2e7d32', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#c8e6c9', alpha=0.8))

ax2v = ax2.twinx()
ax2v.bar(x, ext_vols/10000, color='#888', width=0.5, alpha=0.15)
ax2v.set_ylabel('成交量(万手)', fontsize=9, color='#888')
ax2v.tick_params(axis='y', labelcolor='#888')

step = max(1, ext_len // 12)
ax2.set_xticks(x[::step])
ax2.set_xticklabels([ext_dates[i] for i in range(0, ext_len, step)], rotation=30, fontsize=8)
ax2.set_ylabel('价格(元)', fontsize=11)
ax2.set_xlabel('交易日', fontsize=11)
ax2.grid(True, alpha=0.1)

# 对比文字框
textstr = (
    '段C vs 段E(当前) 对比\n'
    '────────────────────\n'
    f'相似度: 0.862 ★最高\n'
    f'段C跌幅: -19.8%  持续28日\n'
    f'段E跌幅: -28.4%  持续13日(进行中)\n'
    f'段C背景: 解禁前机构减仓\n'
    f'段E背景: 解禁后股东减持\n'
    f'段C见底后30日: +24.4%\n'
    f'段D见底后30日: +33.5%'
)
props = dict(boxstyle='round', facecolor='#fff9c4', alpha=0.9)
ax2.text(0.98, 0.95, textstr, transform=ax2.transAxes, fontsize=9,
        verticalalignment='top', horizontalalignment='right', bbox=props, family='monospace')

plt.savefig('/data/hermes/workspace/301358_overlay_comparison.png', dpi=150, bbox_inches='tight')
print("✓ 叠加对比图已保存")
