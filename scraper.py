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
    # 构造推送内容
    payload = {
        "embeds": [{
            "title": f"🎁 New Freebie: {deal['title']}",
            "description": f"Worth: **{deal['worth']}**\nPlatform: **{deal['platform']}**\nClaim it on GamerLootDrop!",
            "url": WEBSITE_URL,
            "color": 39423, # 霓虹绿
            "image": {"url": deal.get('image', '')},
            "footer": {"text": "GamerLootDrop - Daily Deals"}
        }]
    }
    
    try:
        # 强行发送并打印结果
        resp = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        if resp.status_code == 204:
            print(f"✅ Discord 成功推送: {deal['title']}")
        else:
            print(f"❌ Discord 报错码: {resp.status_code}, 内容: {resp.text}")
    except Exception as e:
        print(f"⚠️ 网络请求炸了: {e}")

def scrape_deals():
    print("🚀 正在从 API 抓取最新游戏...")
    url = "https://www.gamerpower.com/api/giveaways"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            games = response.json()
            deals = []
            
            # 抓取前 30 个
            for game in games[:30]:
                deals.append({
                    "title": game.get("title"),
                    "platform": game.get("platforms"),
                    "link": game.get("open_giveaway_url"),
                    "image": game.get("thumbnail"),
                    "worth": game.get("worth", "N/A"),
                    "end_date": game.get("end_date", "Limited Time")
                })
            
            # 保存到文件
            with open('deals.json', 'w', encoding='utf-8') as f:
                json.dump(deals, f, ensure_ascii=False, indent=4)
            print("✅ deals.json 已更新")
            
            # 📢 强制推送前 3 个
            print("📢 正在尝试呼叫 Discord...")
            for d in deals[:3]:
                send_discord_notification(d)
                time.sleep(1) # 停 1 秒，防刷屏保护
                
    except Exception as e:
        print(f"⚠️ 抓取失败: {e}")

if __name__ == "__main__":
    scrape_deals()
