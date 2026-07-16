#!/usr/bin/env python3
"""301358 湖南裕能 历史走势对比分析"""
import json, numpy as np, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 加载数据
with open('/data/hermes/workspace/301358_klines.json') as f:
    all_klines = json.load(f)

closes = np.array([k['close'] for k in all_klines])
volumes = np.array([k['volume'] for k in all_klines])
highs = np.array([k['high'] for k in all_klines])
lows = np.array([k['low'] for k in all_klines])
opens = np.array([k['open'] for k in all_klines])
dates = [k['date'] for k in all_klines]
n = len(closes)

# 5个下跌段定义
seg_defs = [
    {"name": "A", "label": "上市后首轮回调", "peak_date": "2025-07-25", "trough_date": "2025-10-23",
     "events": [("2025-08-20", "磷酸铁锂行业\n产能过剩担忧"), ("2025-09-14", "大盘回调\n创业板-3%")]},
    {"name": "B", "label": "①浪顶→②浪回调", "peak_date": "2025-11-13", "trough_date": "2025-12-16",
     "events": [("2025-11-20", "获利盘回吐"), ("2025-12-08", "磷酸铁锂\n开始涨价")]},
    {"name": "C", "label": "反弹高点→解禁前杀跌", "peak_date": "2025-12-26", "trough_date": "2026-02-06",
     "events": [("2026-01-15", "解禁前夕\n机构提前减仓"), ("2026-02-06", "2/9解禁3.74亿股\n(49.13%)即将到来")]},
    {"name": "D", "label": "反弹高点→缩量回调", "peak_date": "2026-03-16", "trough_date": "2026-04-03",
     "events": [("2026-03-25", "Q1业绩超预期\n但机构继续减仓")]},
    {"name": "E", "label": "B浪反弹顶→C浪下跌(当前)", "peak_date": "2026-06-23", "trough_date": None,
     "events": [("2026-06-03", "宁德时代+津晟\n公告减持38亿"), ("2026-06-26", "放量暴跌\n8800万→14.7亿"), ("2026-07-09", "逆市暴跌\n创业板+4.49%"), ("2026-07-10", "缩量46%\nRSI=10")]},
]

results = []
for s in seg_defs:
    pi = dates.index(s["peak_date"])
    ti = dates.index(s["trough_date"]) if s["trough_date"] else n-1
    seg_c = closes[pi:ti+1]
    seg_v = volumes[pi:ti+1]
    seg_h = highs[pi:ti+1]
    seg_l = lows[pi:ti+1]
    seg_o = opens[pi:ti+1]
    peak_p = highs[pi]
    trough_p = seg_l.min()
    decline = (trough_p / peak_p - 1) * 100
    dur = ti - pi
    avg_vol = seg_v.mean()

    if len(seg_c) > 1:
        rets = np.diff(seg_c) / seg_c[:-1]
        max_drop = rets.min() * 100
    else:
        max_drop = 0

    corr = np.corrcoef(seg_c, seg_v)[0, 1] if len(seg_c) > 2 else 0

    rebound = 0
    if s["trough_date"]:
        r_end = min(ti+31, n)
        rc = closes[ti:r_end]
        if len(rc) > 1:
            rebound = (rc[-1] / rc[0] - 1) * 100

    norm = (seg_c / seg_c[0] - 1) * 100

    results.append({
        "name": s["name"], "label": s["label"], "events": s["events"],
        "peak_date": s["peak_date"], "trough_date": s["trough_date"] or "ongoing",
        "peak_idx": pi, "trough_idx": ti,
        "peak_price": peak_p, "trough_price": trough_p,
        "decline_pct": decline, "duration": dur,
        "avg_vol": avg_vol, "max_drop": max_drop,
        "corr": corr, "rebound": rebound,
        "norm": norm, "seg_c": seg_c, "seg_v": seg_v,
        "seg_h": seg_h, "seg_l": seg_l, "seg_o": seg_o,
        "seg_dates": dates[pi:ti+1]
    })

# 打印分析结果
print("=" * 60)
print("301358 湖南裕能 · 历史下跌段对比分析")
print("=" * 60)
for r in results:
    print(f"\n【段{r['name']}】{r['label']}")
    print(f"  时间: {r['peak_date']} → {r['trough_date']}")
    print(f"  高点: {r['peak_price']:.2f} → 低点: {r['trough_price']:.2f} ({r['decline_pct']:.1f}%)")
    print(f"  持续: {r['duration']}个交易日")
    print(f"  均量: {r['avg_vol']/10000:.0f}万手")
    print(f"  最大单日跌: {r['max_drop']:.2f}%")
    print(f"  价量相关: {r['corr']:.3f}")
    print(f"  后续30日反弹: {r['rebound']:+.1f}%")

# 相似度
print("\n" + "=" * 60)
print("与当前段E的走势形态相似度")
print("=" * 60)
curr_norm = results[-1]["norm"]
curr_len = len(curr_norm)
for r in results[:-1]:
    h_norm = r["norm"]
    min_l = min(curr_len, len(h_norm))
    if min_l < 5:
        continue
    sim = np.corrcoef(curr_norm[:min_l], h_norm[:min_l])[0, 1]
    dist = np.sqrt(np.sum((curr_norm[:min_l] - h_norm[:min_l])**2))
    print(f"  段{r['name']}({r['label']}): 相似度={sim:.3f}  距离={dist:.1f}  {'★最像' if sim > 0.7 else ''}")

# ===== 画图 =====
try:
    fm.fontManager.addfont('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')
    plt.rcParams['font.family'] = 'WenQuanYi Zen Hei'
except:
    pass
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(5, 1, figsize=(22, 28))
fig.subplots_adjust(hspace=0.35, top=0.96, bottom=0.04, left=0.07, right=0.93)
fig.suptitle('301358 湖南裕能 · 历史下跌走势对比分析（截至2026-07-10）', fontsize=20, fontweight='bold')

curr_color = '#ff6f00'

for idx, r in enumerate(results):
    ax = axes[idx]
    seg_c = r["seg_c"]
    seg_v = r["seg_v"]
    seg_h = r["seg_h"]
    seg_l = r["seg_l"]
    seg_o = r["seg_o"]
    seg_dates = r["seg_dates"]
    seg_n = len(seg_c)

    x = np.arange(seg_n)

    # 标题
    is_current = (r["name"] == "E")
    title_color = '#d32f2f' if is_current else '#1565c0'
    ax.set_title(f"段{r['name']}：{r['label']}  ({r['peak_date']}→{r['trough_date']})  "
                 f"{r['peak_price']:.2f}→{r['trough_price']:.2f} ({r['decline_pct']:.1f}%)  "
                 f"持续{r['duration']}日 | 后续反弹{r['rebound']:+.1f}%",
                 fontsize=13, fontweight='bold', color=title_color)

    # 画K线
    from matplotlib.patches import FancyBboxPatch
    for i in range(seg_n):
        color = '#d32f2f' if seg_c[i] >= seg_o[i] else '#2e7d32'
        ax.plot([i, i], [seg_l[i], seg_h[i]], color=color, linewidth=0.8)
        bottom = min(seg_o[i], seg_c[i])
        height = abs(seg_c[i] - seg_o[i])
        if height < 0.01:
            height = 0.01
        rect = FancyBboxPatch((i-0.35, bottom), 0.7, height, boxstyle="round,pad=0",
                              facecolor=color, edgecolor=color, linewidth=0.5)
        ax.add_patch(rect)

    # 叠加当前段E的归一化走势（如果是非E段）
    if not is_current:
        curr_c = results[-1]["seg_c"]
        curr_n_len = len(curr_c)
        # 对齐长度
        min_l = min(seg_n, curr_n_len)
        # 缩放当前段到历史段的价格范围
        scale = r["peak_price"] / results[-1]["seg_c"][0]
        curr_scaled = curr_c[:min_l] * scale
        ax.plot(x[:min_l], curr_scaled, color=curr_color, linewidth=2, linestyle='--',
                alpha=0.7, label='当前段E(缩放叠加)')

    # 标注事件
    for event_date, event_text in r["events"]:
        # 在seg_dates中找到最近日期
        best_idx = -1
        best_diff = 999
        for di, d in enumerate(seg_dates):
            diff = abs(int(d.replace('-','')) - int(event_date.replace('-','')))
            if diff < best_diff:
                best_diff = diff
                best_idx = di
        if best_idx >= 0:
            y_pos = seg_h[best_idx] + (r["peak_price"] - r["trough_price"]) * 0.08
            ax.annotate(event_text, xy=(best_idx, y_pos), fontsize=7.5,
                       color='#333', ha='center', fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff9c4', alpha=0.8),
                       arrowprops=dict(arrowstyle='->', color='#666', lw=1))

    # 高点/低点标注
    ax.axhline(y=r["peak_price"], color='#e91e63', linewidth=0.5, linestyle=':', alpha=0.5)
    ax.axhline(y=r["trough_price"], color='#1565c0', linewidth=0.5, linestyle=':', alpha=0.5)
    ax.text(seg_n-1, r["peak_price"], f' 高{r["peak_price"]:.2f}', fontsize=8, color='#e91e63', va='bottom')
    ax.text(seg_n-1, r["trough_price"], f' 低{r["trough_price"]:.2f}', fontsize=8, color='#1565c0', va='top')

    # 成交量子轴
    ax2 = ax.twinx()
    vol_colors = ['#d32f2f' if seg_c[i] >= seg_o[i] else '#2e7d32' for i in range(seg_n)]
    ax2.bar(x, seg_v/10000, color=vol_colors, width=0.6, alpha=0.2)
    ax2.set_ylabel('成交量(万手)', fontsize=9, color='#888')
    ax2.set_ylim(0, max(seg_v/10000)*3)

    # X轴日期
    step = max(1, seg_n // 8)
    ax.set_xticks(x[::step])
    ax.set_xticklabels([seg_dates[i] for i in range(0, seg_n, step)], rotation=30, fontsize=8)

    ax.set_ylabel('价格(元)', fontsize=10)
    ax.grid(True, alpha=0.1)
    ax.legend(loc='upper right', fontsize=9)

plt.savefig('/data/hermes/workspace/301358_pattern_comparison.png', dpi=150, bbox_inches='tight')
print("\n✓ 图表已保存：/data/hermes/workspace/301358_pattern_comparison.png")
