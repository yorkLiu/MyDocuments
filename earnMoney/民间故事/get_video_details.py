import requests
import json
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.bilibili.com/"
}

# 从搜索结果中筛选出的纯民间故事类UP主及其BV号
# 按播放量排序，选20个
targets = [
    ("BV1Y2rXY2Ec1", "-小喵meme"),
    ("BV1yS4y1C73i", "进击的小瓜o"),
    ("BV1aM4y1D7vz", "晴空电影"),
    ("BV1yh4y1B7yp", "小郑说故事呀"),
    ("BV17T41197N8", "晴空电影"),
    ("BV1j44y127rM", "朱仙的武侠梦"),
    ("BV1c341117pb", "沙雕101sd"),
    ("BV16k2wBsEpY", "芳芳bu慌慌"),
    ("BV1Zb4y1s7ev", "进击的小瓜o"),
    ("BV18q4y1x7Js", "进击的小瓜o"),
    ("BV1VSxpzBE4P", "白鸦v"),
    ("BV1EZ4y1o7XF", "阿良漫话"),
    ("BV1h8411W7cD", "待查"),
    ("BV1pK411o7gQ", "待查"),
    ("BV1GJ411x7h7", "待查"),
    ("BV1sJ411V71d", "待查"),
    ("BV1xJ411V71d", "待查"),
    ("BV1Ys411Q7hK", "待查"),
    ("BV1oJ411V71d", "待查"),
    ("BV1TK411m7qk", "待查"),
]

print("="*100)
print(f"{'排名':>3} | {'标题':<50} | {'UP主':<15} | {'播放':>8} | {'赞':>6} | {'藏':>6} | {'弹幕':>6} | {'时长'}")
print("-"*100)

results = []
for i, (bv, fallback_owner) in enumerate(targets[:25]):
    try:
        r = requests.get(
            f"https://api.bilibili.com/x/web-interface/view?bvid={bv}",
            headers=headers,
            timeout=10
        )
        d = r.json().get("data", {})
        if d:
            owner = d.get("owner", {}).get("name", fallback_owner)
            stat = d.get("stat", {})
            title = d.get("title", "")[:50]
            view = stat.get("view", 0)
            like = stat.get("like", 0)
            fav = stat.get("favorite", 0)
            danmaku = stat.get("danmaku", 0)
            duration = d.get("duration", 0)
            min_sec = duration // 60
            sec = duration % 60
            dur_str = f"{min_sec}:{sec:02d}"
            
            results.append({
                "index": i+1,
                "bv": bv,
                "title": title,
                "owner": owner,
                "view": view,
                "like": like,
                "fav": fav,
                "danmaku": danmaku,
                "duration": dur_str,
                "desc": d.get("desc", ""),
                "cid": d.get("cid", 0),
                "mid": d.get("owner", {}).get("mid", 0),
                "pubdate": d.get("pubdate", 0),
                "tags": d.get("tags", []),
            })
            
            print(f"{i+1:>3} | {title:<50} | {owner:<15} | {view:>8,} | {like:>6,} | {fav:>6,} | {danmaku:>6,} | {dur_str}")
        time.sleep(0.3)
    except Exception as e:
        print(f"{i+1:>3} | {bv} ERROR: {e}")
        time.sleep(0.3)

# 按播放量排序
results.sort(key=lambda x: x["view"], reverse=True)

# 保存结果供后续分析
with open("/tmp/bili_results.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n共获取 {len(results)} 个视频数据，已保存到 /tmp/bili_results.json")

# 统计UP主分布
from collections import Counter
owner_counts = Counter(r["owner"] for r in results)
print("\nUP主出现次数（热度指标）:")
for owner, count in owner_counts.most_common(15):
    print(f"  {owner}: {count}个视频上榜")

