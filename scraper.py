import requests
import json
import time

# ==========================================
# 🚀 基础配置
# ==========================================
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1497872616726200451/DAoEbhs-NBIBQEt6m5vwwguKYm33DN86BoB0YxN6R02NOSlwUDDp3ByMFqbAHENPU7Up"
WEBSITE_URL = "https://gamerlootdrop.github.io/daily-deals/"

def run():
    print("🚦 机器人启动，开始执行任务...")
    try:
        # 1. 抓取 API 数据
        print("🌐 正在从 GamerPower 抓取最新游戏...")
        r = requests.get("https://www.gamerpower.com/api/giveaways", timeout=15)
        if r.status_code != 200:
            print(f"❌ API 抓取失败，状态码: {r.status_code}")
            return
            
        data = r.json()[:30]
        
        # 2. 保存到 deals.json（供网页读取）
        with open("deals.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("💾 deals.json 文件已更新，网页数据已就绪")

        # 3. 推送 Discord 消息
        print(f"📢 正在向 Discord 频道发送前 3 个最火爆的推送...")
        for item in data[:3]:
            payload = {
                "embeds": [{
                    "title": f"🎁 New Freebie: {item['title']}",
                    "description": f"价值: **{item.get('worth', 'FREE')}**\n平台: **{item['platforms']}**\n\n[点击这里查看更多免费游戏]({WEBSITE_URL})",
                    "url": WEBSITE_URL,
                    "color": 39423, # 霓虹绿
                    "image": {"url": item['thumbnail']},
                    "footer": {"text": "GamerLootDrop - Daily Deals"}
                }]
            }
            res = requests.post(DISCORD_WEBHOOK_URL, json=payload)
            if res.status_code == 204:
                print(f"✅ Discord 成功送达: {item['title']}")
            else:
                print(f"❌ Discord 推送失败: {res.status_code}")
            
            # 停顿 1 秒，防止发送频率过快
            time.sleep(1)

    except Exception as e:
        print(f"❌ 运行过程中出现崩溃: {e}")

if __name__ == "__main__":
    run()
