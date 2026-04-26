import requests
import json
import time

# ==========================================
# 🚀 基础配置
# ==========================================
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1497842345406632027/E4gnmBOA-9lywCzs481kdGyxnuJ8dwjQF4qFQi9U5ahNuiaUXItT05Jz4RDOZavL-XNv"
WEBSITE_URL = "https://gamerlootdrop.github.io/daily-deals/"

def send_discord_notification(deal):
    """发送 Discord 通知（带强力监控版）"""
    if not DISCORD_WEBHOOK_URL: 
        print("❌ 错误: 未配置 Discord Webhook 链接")
        return
    
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
        resp = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        if resp.status_code == 204:
            print(f"✅ Discord 推送成功: {deal['title']}")
        else:
            print(f"❌ Discord 返回错误: {resp.status_code} - {resp.text}")
        time.sleep(1) # 稍微停顿，防止发太快被屏蔽
    except Exception as e:
        print(f"⚠️ 网络异常，无法连接 Discord: {e}")

def scrape_deals():
    print("🚀 正在从 API 抓取最新游戏数据...")
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
                    "link": game.get("open_giveaway_url"),
                    "image": game.get("thumbnail"),
                    "worth": game.get("worth", "N/A"),
                    "end_date": game.get("end_date", "Limited Time")
                })
            
            # ✅ 核心：保存数据到 deals.json
            with open('deals.json', 'w', encoding='utf-8') as f:
                json.dump(deals, f, ensure_ascii=False, indent=4)
            print(f"✅ 成功抓取 {len(deals)} 个游戏并存入 deals.json")
            
            # 📢 Discord 同步推送（前 3 个）
            print("📢 正在呼叫 Discord 频道...")
            for d in deals[:3]:
                send_discord_notification(d)
                
    except Exception as e:
        print(f"⚠️ 抓取过程中出现严重错误: {e}")

if __name__ == "__main__":
    scrape_deals()
