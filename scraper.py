import requests
import json

def scrape_deals():
    print("🚀 正在扩容货架，抓取最新 30 个福利...")
    url = "https://www.gamerpower.com/api/giveaways"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            games = response.json()
            deals = []
            # 这里改成 30，让页面更丰富
            for game in games[:30]:
                deals.append({
                    "title": game.get("title"),
                    "platform": game.get("platforms"),
                    "link": game.get("gamerpower_url"),
                    "image": game.get("thumbnail")
                })
            with open('deals.json', 'w', encoding='utf-8') as f:
                json.dump(deals, f, ensure_ascii=False, indent=4)
            generate_html(deals)
            print("✅ 30个福利已上架！")
    except Exception as e:
        print(f"⚠️ 出错: {e}")

def generate_html(deals):
    cards = ""
    for item in deals:
        cards += f'''
        <div class="card">
            <img class="card-img" src="{item['image']}" alt="Game Cover">
            <div class="card-content">
                <span class="tag">{item['platform']}</span>
                <h3 class="title">{item['title']}</h3>
                <a href="{item['link']}" target="_blank" class="btn">Claim Now</a>
            </div>
        </div>'''

    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GamerLootDrop - Daily Free Games & Giveaways</title>
        <style>
            :root {{ --bg: #121212; --card: #1e1e1e; --primary: #27ae60; --text: #ffffff; }}
            body {{ font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; }}
            .header {{ text-align: center; padding: 40px 0; }}
            .header h1 {{ font-size: 2.5rem; color: var(--primary); }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; }}
            .card {{ background: var(--card); border-radius: 12px; overflow: hidden; transition: 0.3s; border: 1px solid #333; }}
            .card:hover {{ transform: translateY(-5px); border-color: var(--primary); }}
            .card-img {{ width: 100%; height: 160px; object-fit: cover; }}
            .card-content {{ padding: 15px; }}
            .tag {{ font-size: 0.7rem; background: #333; padding: 4px 8px; border-radius: 4px; color: #aaa; }}
            .title {{ font-size: 1rem; margin: 10px 0; height: 2.8em; overflow: hidden; }}
            .btn {{ display: block; text-align: center; background: var(--primary); color: white; text-decoration: none; padding: 10px; border-radius: 6px; font-weight: bold; transition: 0.2s; }}
            .btn:hover {{ background: #2ecc71; transform: scale(1.02); }}
            footer {{ text-align: center; margin-top: 50px; padding: 20px; color: #666; font-size: 0.9rem; border-top: 1px solid #333; }}
            footer a {{ color: #888; text-decoration: none; margin: 0 10px; }}
            footer a:hover {{ color: var(--primary); }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎮 GamerLootDrop</h1>
            <p>Your Daily Source for Global Free Games</p>
        </div>
        <div class="grid">{cards}</div>
        <footer>
            <p>&copy; 2024 GamerLootDrop. All rights reserved.</p>
            <a href="about.html">About Us</a> | 
            <a href="privacy.html">Privacy Policy</a> | 
            <a href="terms.html">Terms of Service</a>
        </footer>
    </body>
    </html>'''
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    scrape_deals()
