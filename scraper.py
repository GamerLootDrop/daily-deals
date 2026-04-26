import requests
import json
import time

# ==========================================
# 🚀 基础配置
# ==========================================
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1497842345406632027/E4gnmBOA-9lywCzs481kdGyxnuJ8dwjQF4qFQi9U5ahNuiaUXItT05Jz4RDOZavL-XNv"
WEBSITE_URL = "https://gamerlootdrop.github.io/daily-deals/"

def send_discord_notification(deal):
    """发送 Discord 通知"""
    if not DISCORD_WEBHOOK_URL: return
    payload = {
        "embeds": [{
            "title": f"🎁 New Freebie: {deal['title']}",
            "description": f"Worth: **{deal['worth']}**\nPlatform: **{deal['platform']}**\nClaim it on GamerLootDrop!",
            "url": WEBSITE_URL,
            "color": 39423, # 霓虹绿
            "image": {"url": deal['image']},
            "footer": {"text": "GamerLootDrop - Daily Deals"}
        }]
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        time.sleep(1)
    except: pass

def scrape_deals():
    print("🚀 正在抓取最新游戏，准备喂给“白月光”网页...")
    url = "https://www.gamerpower.com/api/giveaways"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            games = response.json()
            deals = []
            # 抓取前 30 个游戏
            for game in games[:30]:
                deals.append({
                    "title": game.get("title"),
                    "platform": game.get("platforms"),
                    "link": game.get("open_giveaway_url"), # 直达链接
                    "image": game.get("thumbnail"),
                    "worth": game.get("worth", "N/A"),
                    "end_date": game.get("end_date", "Limited Time")
                })
            
            # ✅ 关键：只更新数据文件，不碰 HTML 页面！
            with open('deals.json', 'w', encoding='utf-8') as f:
                json.dump(deals, f, ensure_ascii=False, indent=4)
            
            print("✅ 数据已入库 (deals.json)。")
            
            # 📢 Discord 同步
            print("📢 正在呼叫 Discord...")
            for d in deals[:3]:
                send_discord_notification(d)
                
    except Exception as e:
        print(f"⚠️ 抓取失败: {e}")

if __name__ == "__main__":
    scrape_deals()
