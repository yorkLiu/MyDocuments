import requests
import json
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.bilibili.com/"
}

# 搜索多页
all_bvs = []
for page in range(1, 4):
    try:
        r = requests.get(
            f"https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword=%E6%B0%91%E9%97%B4%E6%95%85%E4%BA%8B&order=click&page={page}&page_type=0",
            headers=headers,
            timeout=15
        )
        data = r.json()
        results = data.get("data", {}).get("result", [])
        print(f"Page {page}: {len(results)} results")
        for item in results:
            bv = item.get("bvid", "")
            if bv and bv not in all_bvs:
                all_bvs.append(bv)
        time.sleep(0.5)
    except Exception as e:
        print(f"Page {page} ERROR: {e}")

print(f"\nTotal unique BVs: {len(all_bvs)}")

# 获取详情 - 取前25个
for i, bv in enumerate(all_bvs[:25]):
    try:
        r = requests.get(
            f"https://api.bilibili.com/x/web-interface/view?bvid={bv}",
            headers=headers,
            timeout=10
        )
        d = r.json().get("data", {})
        if d:
            owner = d.get("owner", {}).get("name", "?")
            stat = d.get("stat", {})
            mid = d.get("owner", {}).get("mid", "?")
            desc = d.get("desc", "")[:80]
            print(f"{i+1}. ▶ {d.get('title','')[:45]}")
            print(f"   UP:{owner}(mid:{mid}) | 播放:{stat.get('view','?')} 赞:{stat.get('like','?')} 藏:{stat.get('favorite','?')} 评:{stat.get('reply','?')}")
            print(f"   简介:{desc}")
            print()
        time.sleep(0.3)
    except Exception as e:
        print(f"{i+1}. {bv} ERROR: {e}")
        time.sleep(0.3)

