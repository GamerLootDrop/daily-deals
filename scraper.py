import requests
from bs4 import BeautifulSoup
import json
import os

# 目标：抓取 GamerPower 的免费游戏（这只是个示例，你可以根据需要扩展）
def scrape_deals():
    print("🚀 开始扫描全球免费游戏福利...")
    url = "https://www.gamerpower.com/api/giveaways" # 使用 API 速度最快最稳
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            games = response.json()
            deals = []
            # 只取前 10 个最热门的
            for game in games[:10]:
                deals.append({
                    "title": game.get("title"),
                    "platform": game.get("platforms"),
                    "price": "FREE",
                    "link": game.get("gamerpower_url"),
                    "image": game.get("thumbnail")
                })
            
            # 保存为 JSON 供网页调用
            with open('deals.json', 'w', encoding='utf-8') as f:
                json.dump(deals, f, ensure_ascii=False, indent=4)
            
            # 生成 index.html (简单模板)
            generate_html(deals)
            print("✅ 数据抓取并网页生成成功！")
        else:
            print(f"❌ 抓取失败，错误码：{response.status_code}")
    except Exception as e:
        print(f"⚠️ 运行出错: {e}")

def generate_html(deals):
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>GamerLootDrop - Global Free Games Radar</title>
        <style>
            body { font-family: sans-serif; background: #1a1a1a; color: white; padding: 20px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }
            .card { background: #2a2a2a; border-radius: 8px; overflow: hidden; border: 1px solid #444; }
            .card img { width: 100%; height: 150px; object-fit: cover; }
            .p-4 { padding: 15px; }
            .btn { display: block; text-align: center; background: #27ae60; color: white; text-decoration: none; padding: 10px; border-radius: 4px; margin-top: 10px; }
            .tag { font-size: 12px; background: #444; padding: 2px 6px; border-radius: 4px; }
        </style>
    </head>
    <body>
        <h1>🎮 Global Free Games Radar</h1>
        <p>Auto-updated: Daily (UTC Time)</p>
        <div class="grid">
            {cards}
        </div>
    </body>
    </html>
    """
    
    cards = ""
    for item in deals:
        cards += f"""
        <div class="card">
            <img src="{item['image']}" alt="game">
            <div class="p-4">
                <span class="tag">{item['platform']}</span>
                <h3>{item['title']}</h3>
                <a href="{item['link']}" target="_blank" class="btn">Claim Now</a>
            </div>
        </div>
        """
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_template.replace("{cards}", cards))

if __name__ == "__main__":
    scrape_deals()
