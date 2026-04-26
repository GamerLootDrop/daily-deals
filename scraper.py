#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
折扣资讯爬虫 - GamerPower API 数据抓取
增强版：Discord  webhook 推送 + SEO 自动生成 + 智能引流
"""

import requests
import json
import re
import time
from datetime import datetime

# API 配置
API_URL = "https://www.gamerpower.com/api/giveaways"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

# Discord Webhook 配置
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1497842345406632027/E4gnmBOA-9lywCzs481kdGyxnuJ8dwjQF4qFQi9U5ahNuiaUXItT05Jz4RDOZavL-XNv"

# 我们的网站链接
OUR_WEBSITE_URL = "https://gamerlootdrop.github.io/daily-deals/"

def fetch_deals(limit=10):
    """
    从 GamerPower API 获取最新的折扣/限免信息
    
    Args:
        limit: 返回数据条数，默认 10 条
    
    Returns:
        list: 处理后的折扣信息列表
    """
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        deals = []
        for item in data[:limit]:
            # 安全处理 worth 字段 - 解决 undefined 问题
            worth_raw = item.get("worth", "")
            if worth_raw and worth_raw != "N/A" and worth_raw != "":
                try:
                    # 提取数字，如 "$29.99" -> 29.99
                    worth_num = float(re.sub(r'[^\d.]', '', str(worth_raw)))
                    worth_display = f"${worth_num:.2f}"
                except (ValueError, TypeError):
                    worth_num = 0
                    worth_display = "N/A"
            else:
                worth_num = 0
                worth_display = "N/A"
            
            # 安全处理 end_date 字段
            end_date_raw = item.get("end_date", "")
            if end_date_raw and end_date_raw != "N/A":
                end_date_display = end_date_raw
            else:
                end_date_display = "Limited Time"
            
            deal = {
                "title": item.get("title", "Unknown Game"),
                "description": item.get("description", "No description available")[:200],
                "worth": worth_display,
                "worth_num": worth_num,  # 用于排序的数值
                "open_giveaway": item.get("open_giveaway", ""),
                "image": item.get("image", ""),
                "end_date": end_date_display,
                "type": item.get("type", "Game")
            }
            deals.append(deal)
        
        return deals
    
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return []

def send_discord_notification(top_deals):
    """
    向 Discord 发送高价值游戏通知
    
    Args:
        top_deals: 高价值游戏列表（最多 3 个）
    """
    if not top_deals or not DISCORD_WEBHOOK_URL:
        return
    
    for deal in top_deals:
        # 构建精美格式的 Discord 消息
        embed = {
            "title": f"🔥 High Value Free Game!",
            "description": f"**{deal['title']}**\n\nWorth: **{deal['worth']}**\n\nClaim it now before it's gone!",
            "color": 16753920,  # 橙色 #FF8800
            "url": OUR_WEBSITE_URL,
            "thumbnail": {
                "url": deal['image'] if deal['image'] else None
            },
            "footer": {
                "text": f"Ends: {deal['end_date']} | Via GamerLootDrop",
                "icon_url": "https://gamerlootdrop.github.io/daily-deals/favicon.ico" if deal['image'] else None
            }
        }
        
        payload = {
            "embeds": [embed],
            "username": "GamerLootDrop Bot",
            "avatar_url": "https://gamerlootdrop.github.io/daily-deals/favicon.ico"
        }
        
        try:
            response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
            if response.status_code == 204:
                print(f"✅ Discord 推送成功：{deal['title']}")
            else:
                print(f"⚠️ Discord 推送状态码：{response.status_code}")
            time.sleep(1)  # 避免频率限制
        except requests.exceptions.RequestException as e:
            print(f"❌ Discord 推送失败：{e}")

def get_top_worth_deals(deals, top_n=3):
    """
    筛选出 Worth 最高的 N 款游戏
    
    Args:
        deals: 所有游戏列表
        top_n: 返回前 N 个，默认 3 个
    
    Returns:
        list: 高价值游戏列表
    """
    # 按 worth_num 降序排序
    sorted_deals = sorted(deals, key=lambda x: x.get('worth_num', 0), reverse=True)
    # 只返回 worth_num > 0 的游戏（真正有价值的）
    paid_deals = [d for d in sorted_deals if d.get('worth_num', 0) > 0]
    return paid_deals[:top_n]

def generate_sitemap(deals, base_url="https://gamerlootdrop.github.io/daily-deals/"):
    """
    自动生成 sitemap.xml 用于 SEO
    
    Args:
        deals: 游戏列表
        base_url: 网站基础 URL
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{base_url}</loc>
        <lastmod>{today}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
'''
    
    # 为每个游戏生成独立页面（如果有）
    for deal in deals[:20]:
        safe_title = re.sub(r'[^a-zA-Z0-9]', '-', deal['title'].lower())[:50]
        game_url = f"{base_url}games/{safe_title}.html"
        sitemap += f'''    <url>
        <loc>{game_url}</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
'''
    
    sitemap += '''</urlset>
'''
    
    try:
        with open("sitemap.xml", "w", encoding="utf-8") as f:
            f.write(sitemap)
        print(f"✅ 生成 sitemap.xml")
    except Exception as e:
        print(f"⚠️ sitemap.xml 生成失败：{e}")

def save_to_json(deals, filename="deals.json"):
    """将数据保存为 JSON 文件"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(deals, f, ensure_ascii=False, indent=2)
    print(f"Saved: {filename}")

def generate_html_cards(deals):
    """将折扣数据生成 HTML 卡片代码"""
    html_cards = ""
    for deal in deals:
        clean_desc = re.sub(r'<[^>]+>', '', deal['description'])
        
        html_cards += f'''
            <li class="deal-card">
                <div class="deal-image">
                    <img src="{deal['image']}" alt="{deal['title']}" onerror="this.style.display='none'">
                </div>
                <div class="deal-content">
                    <h3 class="deal-title">{deal['title']}</h3>
                    <p class="deal-desc">{clean_desc[:150]}...</p>
                    <div class="deal-price-row">
                        <span class="deal-price">{deal['worth']}</span>
                    </div>
                    <a href="{deal['open_giveaway']}" class="deal-btn" target="_blank" rel="noopener">Get it Now →</a>
                </div>
            </li>'''
    
    return html_cards

def update_index_html(html_cards, input_file="index.html", output_file="index.html"):
    """读取 index.html，注入数据，保存覆盖"""
    with open(input_file, "r", encoding="utf-8") as f:
        html_template = f.read()
    
    empty_state = '<li class="empty-state">Scanning for latest deals...</li>'
    
    if empty_state in html_template:
        html_template = html_template.replace(empty_state, html_cards)
    else:
        pattern = r'(<ul id="deal-list">)(.*?)(</ul>)'
        replacement = r'\1\n' + html_cards + '\n        \3'
        html_template = re.sub(pattern, replacement, html_template, flags=re.DOTALL)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print(f"Updated: {output_file}")

def run_task():
    """执行一次完整的抓取和更新任务"""
    print("\n" + "=" * 50)
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 1. 抓取数据
    deals = fetch_deals(limit=10)
    
    if deals:
        print(f"Fetched {len(deals)} deals")
        
        # 2. 保存 JSON
        save_to_json(deals)
        
        # 3. 生成 HTML 卡片并更新页面
        html_cards = generate_html_cards(deals)
        update_index_html(html_cards)
        
        # 4. 生成 sitemap.xml（SEO 自动化）
        generate_sitemap(deals)
        
        # 5. 筛选高价值游戏并推送 Discord
        top_deals = get_top_worth_deals(deals, top_n=3)
        if top_deals:
            print(f"\n🔥 发现 {len(top_deals)} 款高价值游戏，准备推送 Discord...")
            send_discord_notification(top_deals)
        else:
            print("\n⚠️ 未发现高价值付费游戏（可能都是免费限免）")
        
        print("\n✅ Page updated successfully")
    else:
        print("No deals fetched")
        return 1
    
    return 0

if __name__ == "__main__":
    print("🎯 Daily Free Games & Deals Radar - Scraper")
    print("🚀 Enhanced: Discord Webhook + SEO Auto-Generation")
    print("=" * 50)
    exit_code = run_task()
    exit(exit_code)
