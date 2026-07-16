import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.bilibili.com/"
}

# 从搜索结果提取的BV号
bv_ids = [
    "BV1yS4y1C73i",   # 买命钱 - 606万播放
    "BV1aM4y1D7vz",   # 铜仙鹤 - 582万播放
    "BV1yh4y1B7yp",   # 俄罗斯民间故事 - 501万播放
    "BV17T41197N8",   # 金算盘 - 497万播放
    "BV1j44y127rM",   # 五郎八卦棍 - 485万播放
    "BV1c341117pb",   # 村花生蛇 - 246万播放
    "BV16k2wBsEpY",   # 哺儿鬼妾 - 243万播放
    "BV1Zb4y1s7ev",   # 奇怪的大瓜 - 235万播放
    "BV18q4y1x7Js",   # 不能惹木匠 - 226万播放
    "BV19d4y1A7Ps",   # 驯化杠精 - 226万播放
    "BV1VSxpzBE4P",   # 厨娘烤鱼 - 225万播放
    "BV1EZ4y1o7XF",   # 老虎传说 - 223万播放
]

print("="*80)
print("B站民间故事热门视频详情")
print("="*80)

for bv in bv_ids:
    try:
        r = requests.get(
            f"https://api.bilibili.com/x/web-interface/view?bvid={bv}",
            headers=headers,
            timeout=10
        )
        data = r.json()
        if data.get("data"):
            d = data["data"]
            print(f"\n▶ {d.get('title', '')}")
            print(f"  UP主: {d.get('owner',{}).get('name','')}")
            print(f"  播放: {d.get('stat',{}).get('view','')} | 弹幕: {d.get('stat',{}).get('danmaku','')}")
            print(f"  点赞: {d.get('stat',{}).get('like','')} | 收藏: {d.get('stat',{}).get('favorite','')} | 评论: {d.get('stat',{}).get('coin','')}")
            print(f"  时长: {d.get('duration','')}秒 | 发布日期: {d.get('pubdate','')}")
            print(f"  简介: {d.get('desc','')[:100]}")
            
            # 标签
            tgs = d.get('tags', [])
            if tgs:
                tag_names = [t.get('name','') for t in tgs[:5]]
                print(f"  标签: {tag_names}")
        else:
            print(f"\n❌ {bv}: {data.get('message','unknown')}")
    except Exception as e:
        print(f"❌ {bv} ERROR: {e}")

