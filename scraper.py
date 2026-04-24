import requests
import json

def scrape_deals():
    print("🚀 正在为全球玩家扫描免费游戏...")
    # 使用 API 获取数据，这是最稳、最快的方式
    url = "https://www.gamerpower.com/api/giveaways"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            games = response.json()
            deals = []
            # 抓取前 12 个最新的福利
            for game in games[:12]:
                deals.append({
                    "title": game.get("title"),
                    "platform": game.get("platforms"),
                    "link": game.get("gamerpower_url"),
                    "image": game.get("thumbnail")
                })
            
            # 保存数据
            with open('deals.json', 'w', encoding='utf-8') as f:
                json.dump(deals, f, ensure_ascii=False, indent=4)
            
            # 自动生成网页
            generate_html(deals)
            print("✅ 网页更新成功！")
        else:
            print(f"❌ 接口请求失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"⚠️ 出错了: {e}")

def generate_html(deals):
    cards = ""
    for item in deals:
        cards += f'''
        <div style="background:#2a2a2a; border-radius:8px; overflow:hidden; border:1px solid #444;">
            <img src="{item['image']}" style="width:100%; height:150px; object-fit:cover;">
            <div style="padding:15px;">
                <span style="font-size:12px; background:#444; padding:2px 6px; border-radius:4px;">{item['platform']}</span>
                <h3 style="margin:10px 0; font-size:16px;">{item['title']}</h3>
                <a href="{item['link']}" target="_blank" style="display:block; text-align:center; background:#27ae60; color:white; text-decoration:none; padding:10px; border-radius:4px;">Claim Now</a>
            </div>
        </div>'''

    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GamerLootDrop - Global Free Games</title>
    </head>
    <body style="font-family:sans-serif; background:#1a1a1a; color:white; padding:20px;">
        <h1 style="text-align:center;">🎮 Global Free Games Radar</h1>
        <p style="text-align:center; color:#888;">Auto-updated Daily for Gamers Worldwide</p>
        <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(250px, 1fr)); gap:20px; max-width:1200px; margin:0 auto;">
            {cards}
        </div>
    </body>
    </html>'''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    scrape_deals()
