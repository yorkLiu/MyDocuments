import requests
import json
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.bilibili.com/"
}

# 用正确的BV号重新搜索
# 搜索民间故事关键词，获取高质量结果
keywords = ["民间故事", "民间传说", "中国妖怪", "民间奇闻", "志怪故事", "鬼故事民间"]

all_videos = []
seen_bvs = set()

for kw in keywords:
    try:
        r = requests.get(
            f"https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={kw}&order=click&page=1&page_type=0",
            headers=headers,
            timeout=15
        )
        data = r.json()
        results = data.get("data", {}).get("result", [])
        print(f"'{kw}': {len(results)} results")
        for item in results[:15]:
            bv = item.get("bvid", "")
            if bv and bv not in seen_bvs:
                seen_bvs.add(bv)
                all_videos.append((bv, item.get("title", ""), item.get("author", "")))
        time.sleep(0.5)
    except Exception as e:
        print(f"'{kw}' ERROR: {e}")
        time.sleep(0.5)

print(f"\n总计 {len(all_videos)} 个唯一视频")

# 获取详情
print("\n" + "="*120)
print(f"{'排名':>3} | {'标题':<45} | {'UP主':<15} | {'播放':>8} | {'赞':>6} | {'藏':>6} | {'弹幕':>6} | {'时长':>5}")
print("-"*120)

results = []
for i, (bv, title_fallback, owner_fallback) in enumerate(all_videos[:30]):
    try:
        r = requests.get(
            f"https://api.bilibili.com/x/web-interface/view?bvid={bv}",
            headers=headers,
            timeout=10
        )
        d = r.json().get("data", {})
        if d and d.get("title"):
            owner = d.get("owner", {}).get("name", owner_fallback)
            stat = d.get("stat", {})
            title = d.get("title", "")[:45]
            view = stat.get("view", 0)
            like = stat.get("like", 0)
            fav = stat.get("favorite", 0)
            danmaku = stat.get("danmaku", 0)
            duration = d.get("duration", 0)
            min_sec = duration // 60
            sec = duration % 60
            dur_str = f"{min_sec}:{sec:02d}"
            
            results.append({
                "title": title,
                "owner": owner,
                "mid": d.get("owner", {}).get("mid", 0),
                "view": view,
                "like": like,
                "fav": fav,
                "danmaku": danmaku,
                "duration": dur_str,
                "duration_sec": duration,
                "desc": d.get("desc", ""),
                "tags": [t.get("name","") for t in d.get("tags", [])[:5]],
                "pubdate": d.get("pubdate", 0),
                "bv": bv,
            })
            
            print(f"{i+1:>3} | {title:<45} | {owner:<15} | {view:>8,} | {like:>6,} | {fav:>6,} | {danmaku:>6,} | {dur_str:>5}")
        time.sleep(0.3)
    except Exception as e:
        time.sleep(0.3)

# 按播放量排序
results.sort(key=lambda x: x["view"], reverse=True)

# 保存
with open("/tmp/bili_final.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# 统计UP主
from collections import Counter
owner_views = Counter()
owner_videos = Counter()
for r in results:
    owner_views[r["owner"]] += r["view"]
    owner_videos[r["owner"]] += 1

print("\n" + "="*80)
print("UP主综合热度排名（按总播放量）:")
print("-"*80)
for owner, total_views in owner_views.most_common(20):
    print(f"  {owner:<20} | 总播放: {total_views:>12,} | 上榜视频: {owner_videos[owner]}")

