import requests
import json
import time

# ==========================================
# 🚀 基础配置（确保推送响起来）
# ==========================================
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1497842345406632027/E4gnmBOA-9lywCzs481kdGyxnuJ8dwjQF4qFQi9U5ahNuiaUXItT05Jz4RDOZavL-XNv"
WEBSITE_URL = "https://gamerlootdrop.github.io/daily-deals/"

def send_discord_notification(deal):
    if not DISCORD_WEBHOOK_URL: return
    payload = {
        "embeds": [{
            "title": f"🎁 New Freebie: {deal['title']}",
            "description": f"Platform: **{deal['platform']}**\nCheck it on GamerLootDrop!",
            "url": WEBSITE_URL,
            "color": 39423,
            "image": {"url": deal['image']},
            "footer": {"text": "GamerLootDrop - Daily Deals"}
        }]
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        time.sleep(1)
    except: pass

def scrape_deals():
    print("🚀 正在恢复豪华配置：分区按钮、价格标签、专属链接...")
    url = "https://www.gamerpower.com/api/giveaways"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            games = response.json()
            deals = []
            for game in games[:24]:
                deals.append({
                    "title": game.get("title"),
                    "platform": game.get("platforms"),
                    "link": game.get("gamerpower_url"),
                    "image": game.get("thumbnail"),
                    "worth": game.get("worth", "FREE")
                })
            
            generate_html(deals)
            
            print("📢 正在同步到 Discord...")
            for d in deals[:3]:
                send_discord_notification(d)
    except Exception as e:
        print(f"⚠️ 出错: {e}")

def generate_html(deals):
    # 💰 这里的链接和价格我已经帮你锁死了，绝对不会再变回主页
    sponsored_card = '''
        <div class="card" style="border-color: #ff4d4d; box-shadow: 0 0 15px rgba(255, 77, 77, 0.3);">
            <img class="card-img" src="https://gamerlootdrop.github.io/daily-deals/assets/fh6.jpg" alt="Forza Horizon 6" onerror="this.src='https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1551360/header.jpg'">
            <div class="card-content">
                <span class="tag" style="background: #ff4d4d; color: #fff;">🔥 TOP PRE-ORDER</span>
                <h3 class="title">Forza Horizon 6 - Epic Pre-order Deal!</h3>
                <p class="worth" style="color: #ff4d4d; font-weight: bold; margin-bottom: 15px;">$59.99</p>
                <a href="https://www.g2a.com/n/reflink-329c8e3d21" target="_blank" class="btn" style="background: #ff4d4d; color: #fff;">Get Deal Now</a>
            </div>
        </div>
    '''

    cards = sponsored_card 
    for item in deals:
        cards += f'''
        <div class="card">
            <img class="card-img" src="{item['image']}" alt="Game">
            <div class="card-content">
                <span class="tag">{item['platform']}</span>
                <h3 class="title" title="{item['title']}">{item['title']}</h3>
                <p class="worth" style="color: #00ff88; font-weight: bold; margin-bottom: 15px;">{item['worth']}</p>
                <a href="{item['link']}" target="_blank" class="btn">Claim Now</a>
            </div>
        </div>'''

    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GamerLootDrop - Daily Free Games</title>
        <style>
            :root {{ --bg: #0a0a0a; --card: #151515; --primary: #00ff88; --text: #ffffff; }}
            body {{ font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; }}
            .header {{ text-align: center; padding: 40px 0; }}
            .header h1 {{ font-size: 3rem; color: var(--primary); text-shadow: 0 0 20px rgba(0,255,136,0.5); margin-bottom: 10px; }}
            .nav-filters {{ display: flex; justify-content: center; gap: 10px; margin-bottom: 40px; flex-wrap: wrap; }}
            .filter-btn {{ background: #222; color: #fff; border: none; padding: 8px 18px; border-radius: 20px; cursor: pointer; font-size: 0.9rem; transition: 0.3s; }}
            .filter-btn.active, .filter-btn:hover {{ background: var(--primary); color: #000; font-weight: bold; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 25px; max-width: 1400px; margin: 0 auto; }}
            .card {{ background: var(--card); border-radius: 15px; overflow: hidden; transition: 0.3s; border: 1px solid #222; display: flex; flex-direction: column; height: 100%; }}
            .card:hover {{ transform: translateY(-10px); border-color: var(--primary); box-shadow: 0 10px 30px rgba(0,255,136,0.2); }}
            .card-img {{ width: 100%; height: 160px; object-fit: cover; }}
            .card-content {{ padding: 20px; display: flex; flex-direction: column; flex-grow: 1; }}
            .tag {{ align-self: flex-start; font-size: 0.75rem; background: #333; padding: 5px 12px; border-radius: 6px; color: #00ff88; margin-bottom: 15px; font-weight: bold; }}
            .title {{ font-size: 1.1rem; margin: 0 0 10px 0; line-height: 1.4; height: 2.8em; overflow: hidden; }}
            .btn {{ margin-top: auto; display: block; text-align: center; background: var(--primary); color: #000; text-decoration: none; padding: 12px; border-radius: 8px; font-weight: bold; transition: 0.2s; }}
            .btn:hover {{ filter: brightness(1.2); transform: scale(1.05); }}
            footer {{ text-align: center; margin-top: 80px; padding: 40px; color: #444; border-top: 1px solid #222; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎮 GamerLootDrop</h1>
            <p>Your Automatic Gateway to Free Games & Deals</p>
        </div>
        <div class="nav-filters">
            <button class="filter-btn active">All Games</button>
            <button class="filter-btn">Steam</button>
            <button class="filter-btn">Epic Games</button>
            <button class="filter-btn">PC Store</button>
            <button class="filter-btn">Mobile</button>
        </div>
        <div class="grid">{cards}</div>
        <footer><p>&copy; 2026 GamerLootDrop. All rights reserved.</p></footer>
    </body>
    </html>'''
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    scrape_deals()
