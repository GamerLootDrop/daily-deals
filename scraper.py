import requests
import json

# 配置
URL = "https://discord.com/api/webhooks/1497842345406632027/E4gnmBOA-9lywCzs481kdGyxnuJ8dwjQF4qFQi9U5ahNuiaUXItT05Jz4RDOZavL-XNv"

def scrape():
    print("开始执行...")
    try:
        # 1. 抓取数据
        res = requests.get("https://www.gamerpower.com/api/giveaways")
        games = res.json()[:30]
        
        # 2. 保存文件
        with open('deals.json', 'w', encoding='utf-8') as f:
            json.dump(games, f, ensure_ascii=False, indent=4)
        print("数据已保存到 deals.json")

        # 3. 发送 Discord (前3个)
        for g in games[:3]:
            payload = {
                "embeds": [{
                    "title": f"🎁 限时免费: {g['title']}",
                    "description": f"价值: {g['worth']}\n平台: {g['platforms']}",
                    "url": "https://gamerlootdrop.github.io/daily-deals/",
                    "color": 39423,
                    "image": {"url": g['thumbnail']}
                }]
            }
            r = requests.post(URL, json=payload)
            print(f"推送状态: {r.status_code}")
            
    except Exception as e:
        print(f"出错了: {e}")

if __name__ == "__main__":
    scrape()
