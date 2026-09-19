#!/usr/bin/env python3
"""301358 7/20 截至10:29 实时分析图 — 主力意图+筹码结构"""
import json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.gridspec import GridSpec

font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
fm.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'WenQuanYi Zen Hei'
plt.rcParams['axes.unicode_minus'] = False

with open('/tmp/301358_tl_0720b.json') as f:
    data = json.load(f)
bars = data['data']
real_vols = []
for i in range(len(bars)):
    if i == 0:
        real_vols.append(int(bars[i]['volume']))
    else:
        real_vols.append(max(int(bars[i]['volume']) - int(bars[i-1]['volume']), 0))
prices = [float(b['price']) for b in bars]
times = [b['time'] for b in bars]
total_vol = sum(real_vols)
vwap = sum(p*v for p,v in zip(prices, real_vols)) / total_vol

with open('/tmp/301358_klines_60d_0720.json') as f:
    k_data = json.load(f)
klines = k_data['data']['sz301358']['qfqday']

fig = plt.figure(figsize=(22, 28))
gs = GridSpec(3, 2, figure=fig, height_ratios=[2.8, 1.4, 2.2], hspace=0.3, wspace=0.2,
              left=0.06, right=0.96, top=0.96, bottom=0.02)

# ============ 1. 分时走势 ============
ax1 = fig.add_subplot(gs[0, :])
x = np.arange(len(bars))
colors_vol = ['#cc0000' if i > 0 and prices[i] >= prices[i-1] else '#00aa00' for i in range(len(bars))]
ax1_v = ax1.twinx()
ax1_v.bar(x, [v/10000 for v in real_vols], color=colors_vol, alpha=0.25, width=0.8)

ax1.plot(x, prices, color='#cc0000', linewidth=2, zorder=5)
ax1.axhline(y=vwap, color='blue', linewidth=1.5, linestyle='--', alpha=0.6, label=f'VWAP {vwap:.2f}')
ax1.axhline(y=59.47, color='#888888', linewidth=1.5, linestyle=':', alpha=0.5, label='7/17 close 59.47')
ax1.axhline(y=60.31, color='#006600', linewidth=1, linestyle='--', alpha=0.3, label='7/16 low 60.31')
ax1.axhline(y=57.54, color='#000099', linewidth=1.5, linestyle='--', alpha=0.3, label='7/13 block 57.54')

# 大单标记
for i in range(len(bars)):
    if real_vols[i] >= 200000:
        color = '#00aa00' if i > 0 and prices[i] >= prices[i-1] else '#cc0000'
        ax1.scatter(i, prices[i], s=80, color=color, zorder=10, edgecolors='black', linewidth=0.8)

tick_idx = [i for i, t in enumerate(times) if t.endswith(':00') or t.endswith(':30') or i == len(bars)-1]
ax1.set_xticks([i for i in tick_idx])
ax1.set_xticklabels([times[i] for i in tick_idx], fontsize=9, rotation=30)
ax1.set_ylabel('Price', fontsize=12)
ax1.set_title('301358 Hunan Yuneng 7/20 (as of 10:29) — REBOUND THEN FADE\n'
              '59.47 → 61.15 high (10:09-11) → 59.82 now | Big Order NET +9537wan | Volume RATIO 1.81',
              fontsize=13, fontweight='bold')
ax1.legend(fontsize=9, loc='upper right')
ax1.grid(True, alpha=0.12)

ax1.annotate('OPEN 60.01\ngap up', xy=(0, 60.01), xytext=(3, 58.2),
             fontsize=9, color='#00aa00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00aa00', lw=1.5))
ax1.annotate('09:31 SUPER BUY\n79.84wan 4806wan\nWHY? peek 60+ first', xy=(1, 60.19), xytext=(3, 62.2),
             fontsize=10, color='#00aa00', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#00aa00', lw=2),
             bbox=dict(boxstyle='round', facecolor='#f0fff0'))
ax1.annotate('09:32 SELL\n43.14wan → 59.68\nSHAKE OUT', xy=(2, 59.68), xytext=(10, 58.0),
             fontsize=9, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
ax1.annotate('10:09-11 PEAK\n61.15 (3笔大单买)', xy=(40, 61.15), xytext=(35, 62.5),
             fontsize=10, color='#cc0000', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#cc0000', lw=2),
             bbox=dict(boxstyle='round', facecolor='#fff0f0'))
ax1.annotate('FADE TO 59.82\nno follow-through\nbig order stopped', xy=(59, 59.82), xytext=(48, 58.0),
             fontsize=10, color='#006600', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#006600', lw=1.5),
             bbox=dict(boxstyle='round', facecolor='#f0fff0'))

# ============ 2a. 大单分段对比 ============
ax2 = fig.add_subplot(gs[1, 0])
seg_labels = ['09:30\n-09:39', '09:40\n-09:49', '09:50\n-09:59', '10:00\n-10:09', '10:10\n-']
seg_buys = [12835, 6399, 3376, 1615, 1766]
seg_sells = [7204, 3546, 3463, 793, 1447]
seg_nets = [b-s for b, s in zip(seg_buys, seg_sells)]

x2 = np.arange(5)
width = 0.35
ax2.bar(x2 - width/2, seg_buys, width, color='#00aa00', alpha=0.7, label='Buy')
ax2.bar(x2 + width/2, seg_sells, width, color='#cc0000', alpha=0.7, label='Sell')
for i, n in enumerate(seg_nets):
    color = '#00aa00' if n > 0 else '#cc0000'
    ax2.text(i, max(seg_buys[i], seg_sells[i]) + 600, f'{n:+.0f}', ha='center', fontsize=10, color=color, fontweight='bold')
ax2.set_xticks(x2)
ax2.set_xticklabels(seg_labels, fontsize=9)
ax2.set_ylabel('Amount (wan)', fontsize=11)
ax2.set_title('Big Order by 10-min Segment\nEarly surge +5630wan → fading to +319wan (buying weakening)',
              fontsize=11, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.15, axis='y')

# ============ 2b. 三天对比 ============
ax3 = fig.add_subplot(gs[1, 1])
days = ['7/16\nFull', '7/17\nFull', '7/20\n10:29']
day_buys = [0, 26623, 25991]
day_sells = [0, 32682, 16453]
day_nets = [-6059, -6059, 9537]

x3 = np.arange(3)
width = 0.35
ax3.bar(x3[:2] - width/2, [0, 26623], width, color='#00aa00', alpha=0.7, label='Buy')
ax3.bar(x3[2:] - width/2, [25991], width, color='#00aa00', alpha=0.7)
ax3.bar(x3[:2] + width/2, [0, 32682], width, color='#cc0000', alpha=0.7, label='Sell')
ax3.bar(x3[2:] + width/2, [16453], width, color='#cc0000', alpha=0.7)

for i, n in enumerate(day_nets):
    color = '#00aa00' if n > 0 else '#cc0000'
    ax3.text(i, max(day_buys[i], day_sells[i]) + 2000, f'{n:+.0f}', ha='center', fontsize=12, color=color, fontweight='bold')
ax3.set_xticks(x3)
ax3.set_xticklabels(days, fontsize=10)
ax3.set_ylabel('Amount (wan)', fontsize=11)
ax3.set_title('3-Day Big Order Net: -6059 → -6059 → +9537\nFLIP from selling to buying!',
              fontsize=11, fontweight='bold')
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.15, axis='y')

# ============ 3. 筹码结构分析 ============
ax4 = fig.add_subplot(gs[2, :])

# 近期K线（10天）
recent_ks = klines[-10:]
k_labels = [k[0][-5:] for k in recent_ks]
opens_k = [float(k[1]) for k in recent_ks]
closes_k = [float(k[2]) for k in recent_ks]
highs_k = [float(k[3]) for k in recent_ks]
lows_k = [float(k[4]) for k in recent_ks]
vols_k = [float(k[5]) for k in recent_ks]

x4 = np.arange(len(recent_ks))
# K线
for i in range(len(recent_ks)):
    up = closes_k[i] >= opens_k[i]
    color = '#cc0000' if up else '#00aa00'
    ax4.plot([i, i], [lows_k[i], highs_k[i]], color=color, linewidth=1, zorder=1)
    body_bottom = min(opens_k[i], closes_k[i])
    body_height = abs(closes_k[i] - opens_k[i])
    rect = plt.Rectangle((i-0.25, body_bottom), 0.5, max(body_height, 0.1),
                         facecolor=color if up else 'white', edgecolor=color, linewidth=1.5, zorder=2)
    ax4.add_patch(rect)
    chg = (closes_k[i] - opens_k[i]) / opens_k[i] * 100
    ax4.text(i, lows_k[i]-0.8, f'{closes_k[i]:.1f}', ha='center', fontsize=8, color=color)
    ax4.text(i, highs_k[i]+0.3, f'{chg:+.1f}%', ha='center', fontsize=8, color=color)

# 成交量
ax4_v = ax4.twinx()
vol_colors = ['#cc0000' if c >= o else '#00aa00' for c, o in zip(closes_k, opens_k)]
ax4_v.bar(x4, [v/10000 for v in vols_k], color=vol_colors, alpha=0.2, width=0.5)
ax4_v.set_ylabel('Volume (wan lots)', fontsize=11, color='#666666')
ax4_v.set_ylim(0, max(vols_k)/10000*2)

# 筹码区间标注
ax4.axhspan(57.5, 58.5, color='#000099', alpha=0.08, zorder=0)
ax4.axhspan(59, 61, color='#00aa00', alpha=0.08, zorder=0)
ax4.axhspan(62, 64, color='#ff6600', alpha=0.06, zorder=0)
ax4.axhspan(65, 76, color='#cc0000', alpha=0.06, zorder=0)

ax4.text(0.5, 58, '57.5-58.5\n大宗底', fontsize=8, color='#000099', ha='center', fontweight='bold')
ax4.text(3.5, 60, '59-61\n新主力区', fontsize=8, color='#006600', ha='center', fontweight='bold')
ax4.text(6, 63, '62-64\n7/16出货区', fontsize=8, color='#ff6600', ha='center', fontweight='bold')
ax4.text(8, 70, '65-76\n60日套牢盘(94.6%)', fontsize=8, color='#cc0000', ha='center', fontweight='bold')

# 7/20实时
i_today = len(recent_ks)-1
ax4.scatter(i_today, 60.72, s=150, color='#cc0000', zorder=15, marker='*', label='Now 60.72')
ax4.scatter(i_today, 59.16, s=50, color='#00aa00', zorder=15, marker='v')

ax4.set_xticks(x4)
ax4.set_xticklabels(k_labels, fontsize=9, rotation=15)
ax4.set_ylabel('Price', fontsize=12)
ax4.set_title('10-Day K-Line + Chip Structure Zones\n'
              '57.5 floor | 59-61 NEW floor | 62-64 distribution zone | 65-76 60day trapped (94.6%)',
              fontsize=12, fontweight='bold')
ax4.legend(fontsize=10, loc='upper right')
ax4.grid(True, alpha=0.12, axis='y')

plt.savefig('/data/hermes/workspace/301358_0720_intent_chips.png', dpi=150, bbox_inches='tight')
print('Saved: 301358_0720_intent_chips.png')
