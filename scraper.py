import requests
import json
import time

# ==========================================
# 🚀 这里的配置一定要对！
# ==========================================
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1497842345406632027/E4gnmBOA-9lywCzs481kdGyxnuJ8dwjQF4qFQi9U5ahNuiaUXItT05Jz4RDOZavL-XNv"
WEBSITE_URL = "https://gamerlootdrop.github.io/daily-deals/"

def send_discord_notification(deal):
    """发送通知到 Discord"""
    if not DISCORD_WEBHOOK_URL: return
    payload = {
        "embeds": [{
            "title": f"🎁 New Loot: {deal['title']}",
            "description": f"Platform: **{deal['platform']}**\nGrab it on GamerLootDrop!",
            "url": WEBSITE_URL,
            "color": 15548997, # 红色边框，匹配你的地平线卡片
            "image": {"url": deal['image']},
            "footer": {"text": "GamerLootDrop - Daily Deals"}
        }]
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        time.sleep(1)
    except: pass

def scrape_deals():
    print("🚀 正在扩容货架，并加载你的专属《地平线 6》广告...")
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
                    "image": game.get("thumbnail")
                })
            
            generate_html(deals)
            
            # 📢 这一步就是让 Discord 响起来的关键！
            print("📢 正在呼叫 Discord Bot...")
            for d in deals[:3]: # 只推送最火的3个
                send_discord_notification(d)
    except Exception as e:
        print(f"⚠️ 出错: {e}")

def generate_html(deals):
    # 💰 这里换回你最爱的《地平线 6》广告位！
    sponsored_card = '''
        <div class="card" style="border-color: #ff4d4d; box-shadow: 0 0 15px rgba(255, 77, 77, 0.3);">
            <img class="card-img" src="https://gamerlootdrop.github.io/daily-deals/assets/fh6.jpg" alt="Forza Horizon 6" onerror="this.src='https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1551360/header.jpg'">
            <div class="card-content">
                <span class="tag" style="background: #ff4d4d; color: #fff;">🔥 TOP PRE-ORDER</span>
                <h3 class="title">Forza Horizon 6 - Epic Pre-order Deal!</h3>
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
            .header {{ text-align: center; padding: 60px 0; }}
            .header h1 {{ font-size: 3rem; color: var(--primary); text-shadow: 0 0 20px rgba(0,255,136,0.5); }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 25px; max-width: 1400px; margin: 0 auto; }}
            .card {{ background: var(--card); border-radius: 15px; overflow: hidden; transition: 0.3s; border: 1px solid #222; display: flex; flex-direction: column; height: 100%; }}
            .card:hover {{ transform: translateY(-10px); border-color: var(--primary); box-shadow: 0 10px 30px rgba(0,255,136,0.2); }}
            .card-img {{ width: 100%; height: 160px; object-fit: cover; }}
            .card-content {{ padding: 20px; display: flex; flex-direction: column; flex-grow: 1; }}
            .tag {{ align-self: flex-start; font-size: 0.75rem; background: #333; padding: 5px 12px; border-radius: 6px; color: #00ff88; margin-bottom: 15px; font-weight: bold; letter-spacing: 1px; }}
            .title {{ font-size: 1.1rem; margin: 0 0 20px 0; line-height: 1.4; height: 2.8em; overflow: hidden; }}
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
        <div class="grid">{cards}</div>
        <footer><p>&copy; 2026 GamerLootDrop. All rights reserved.</p></footer>
    </body>
    </html>'''
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    scrape_deals()
