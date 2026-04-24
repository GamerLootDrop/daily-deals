import requests
import json

def scrape_deals():
    print("🚀 正在扩容货架，并加载专属广告位...")
    url = "https://www.gamerpower.com/api/giveaways"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            games = response.json()
            deals = []
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
            print("✅ 网页更新成功！广告位已置顶，强迫症对齐已修复！")
    except Exception as e:
        print(f"⚠️ 出错: {e}")

def generate_html(deals):
    # ==========================================
    # 💰 这里就是你的“专属赚钱广告位”
    # ==========================================
    sponsored_card = '''
        <div class="card" style="border-color: #f1c40f; box-shadow: 0 0 15px rgba(241, 196, 15, 0.3);">
            <img class="card-img" src="https://images.unsplash.com/photo-1605901309584-818e25960b8f?q=80&w=600&auto=format&fit=crop" alt="Sponsored Game">
            <div class="card-content">
                <span class="tag" style="background: #f1c40f; color: #000;">🔥 SPONSORED DEAL</span>
                <h3 class="title">Mystery AAA Game - Up to 90% OFF!</h3>
                <a href="#" target="_blank" class="btn" style="background: #f1c40f; color: #000;">Get it now</a>
            </div>
        </div>
    '''

    cards = sponsored_card 
    
    for item in deals:
        cards += f'''
        <div class="card">
            <img class="card-img" src="{item['image']}" alt="Game Cover">
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
            :root {{ --bg: #121212; --card: #1e1e1e; --primary: #27ae60; --text: #ffffff; }}
            body {{ font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; }}
            .header {{ text-align: center; padding: 40px 0; }}
            .header h1 {{ font-size: 2.5rem; color: var(--primary); }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; }}
            
            /* 这里做了强迫症对齐优化 */
            .card {{ background: var(--card); border-radius: 12px; overflow: hidden; transition: 0.3s; border: 1px solid #333; display: flex; flex-direction: column; height: 100%; }}
            .card:hover {{ transform: translateY(-5px); border-color: var(--primary); }}
            .card-img {{ width: 100%; height: 160px; object-fit: cover; }}
            .card-content {{ padding: 15px; display: flex; flex-direction: column; flex-grow: 1; }}
            .tag {{ align-self: flex-start; font-size: 0.7rem; background: #333; padding: 4px 8px; border-radius: 4px; color: #aaa; margin-bottom: 10px; font-weight: bold; }}
            
            /* 强制标题只显示2行，固定高度 */
            .title {{ font-size: 1rem; margin: 0 0 15px 0; line-height: 1.4; height: 2.8em; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; text-overflow: ellipsis; }}
            
            /* 强制按钮沉底对齐 */
            .btn {{ margin-top: auto; display: block; text-align: center; background: var(--primary); color: white; text-decoration: none; padding: 10px; border-radius: 6px; font-weight: bold; transition: 0.2s; }}
            .btn:hover {{ filter: brightness(1.1); transform: scale(1.02); }}
            
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
