import requests
import json

def scrape_deals():
    print("🚀 正在为全球玩家扫描免费游戏...")
    url = "https://www.gamerpower.com/api/giveaways"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            games = response.json()
            deals = []
            for game in games[:12]:
                deals.append({
                    "title": game.get("title"),
                    "platform": game.get("platforms"),
                    "link": game.get("gamerpower_url"),
                    "image": game.get("thumbnail")
                })
            
            with open('deals.json', 'w', encoding='utf-8') as f:
                json.dump(deals, f, ensure_ascii=False, indent=4)
            
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
        <title>GamerLootDrop - Global Free Games</title>
        <style>
            :root {{
                --bg-color: #121212;
                --card-bg: #1e1e1e;
                --primary: #27ae60;
                --text: #ffffff;
                --text-muted: #aaaaaa;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: var(--bg-color);
                color: var(--text);
                padding: 30px 20px;
                margin: 0;
            }}
            .header {{ text-align: center; margin-bottom: 50px; }}
            .header h1 {{ font-size: 2.8rem; margin-bottom: 10px; color: var(--text); letter-spacing: 1px; }}
            .header h1 span {{ color: var(--primary); }}
            .header p {{ color: var(--text-muted); font-size: 1.1rem; }}
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                gap: 25px;
                max-width: 1250px;
                margin: 0 auto;
            }}
            .card {{
                background: var(--card-bg);
                border-radius: 12px;
                overflow: hidden;
                border: 1px solid #333;
                display: flex;
                flex-direction: column;
                transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
            }}
            .card:hover {{
                transform: translateY(-8px);
                box-shadow: 0 15px 30px rgba(0,0,0,0.5);
                border-color: var(--primary);
            }}
            .card-img {{
                width: 100%;
                height: 160px;
                object-fit: cover;
                border-bottom: 1px solid #333;
            }}
            .card-content {{
                padding: 20px;
                display: flex;
                flex-direction: column;
                flex-grow: 1;
            }}
            .tag {{
                align-self: flex-start;
                font-size: 0.75rem;
                font-weight: bold;
                background: #333;
                padding: 5px 10px;
                border-radius: 6px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 15px;
                color: #ddd;
            }}
            .title {{
                font-size: 1.1rem;
                margin: 0 0 20px 0;
                line-height: 1.4;
                flex-grow: 1;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
            }}
            /* 重点修复：增强按钮动画 */
            .btn {{
                display: block;
                text-align: center;
                background: var(--primary);
                color: white;
                text-decoration: none;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                transition: all 0.2s ease; /* 开启所有属性的平滑动画 */
            }}
            .btn:hover {{ 
                background: #2ecc71; 
                transform: scale(1.05); /* 鼠标放上去时：按钮微微放大 5% */
                box-shadow: 0 4px 12px rgba(46, 204, 113, 0.5); /* 鼠标放上去时：底部出现绿色发光阴影 */
            }}
            .btn:active {{ 
                transform: scale(0.95); /* 鼠标点击时：按钮往下陷 */
                box-shadow: none;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎮 Gamer<span>Loot</span>Drop</h1>
            <p>Global Free Games Radar • Auto-updated Daily</p>
        </div>
        <div class="grid">
            {cards}
        </div>
    </body>
    </html>'''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    scrape_deals()
