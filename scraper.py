import requests
import json
import os

def scrape_deals():
    print("🚀 正在从全球采集最新免费游戏数据...")
    # 使用带排序的 API 确保拿到的是最新发布的
    url = "https://www.gamerpower.com/api/giveaways?sort-by=date"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            games = response.json()
            deals = []
            
            # 抓取前 30 个，并提取更丰富的信息
            for game in games[:30]:
                deals.append({
                    "title": game.get("title"),
                    "platform": game.get("platforms"),
                    "link": game.get("open_giveaway_url"), # 使用直接跳转链接
                    "image": game.get("thumbnail"),
                    "worth": game.get("worth", "N/A"),    # 抓取原价
                    "end_date": game.get("end_date", "Limited Time") # 抓取截止日期
                })
            
            # 核心：只更新数据文件 deals.json
            with open('deals.json', 'w', encoding='utf-8') as f:
                json.dump(deals, f, ensure_ascii=False, indent=4)
            
            print(f"✅ 成功进货 {len(deals)} 款游戏！数据已存入 deals.json")
        else:
            print(f"❌ 接口请求失败，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ 出错: {e}")

if __name__ == "__main__":
    scrape_deals()
