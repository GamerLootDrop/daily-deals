#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
折扣资讯爬虫 - GamerPower API 数据抓取
"""

import requests
import json
import sys

# 设置标准输出为 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')

# API 配置
API_URL = "https://www.gamerpower.com/api/giveaways"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

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
        
        # 提取前 N 条数据的关键字段
        deals = []
        for item in data[:limit]:
            deal = {
                "title": item.get("title", "未知游戏"),
                "description": item.get("description", "无描述")[:200],  # 截断过长描述
                "worth": item.get("worth", "免费"),
                "open_giveaway": item.get("open_giveaway", ""),
                "image": item.get("image", "")
            }
            deals.append(deal)
        
        return deals
    
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求错误：{e}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析错误：{e}")
        return []

def save_to_json(deals, filename="deals.json"):
    """
    将数据保存为 JSON 文件
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(deals, f, ensure_ascii=False, indent=2)
    print(f"✅ 数据已保存到 {filename}")

def generate_html_cards(deals):
    """
    将折扣数据生成 HTML 卡片代码
    
    Args:
        deals: 折扣信息列表
    
    Returns:
        str: HTML 列表代码
    """
    html_cards = ""
    for deal in deals:
        # 清理描述中的 HTML 标签
        import re
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
    """
    读取 index.html，注入数据，保存覆盖
    
    Args:
        html_cards: 生成的 HTML 卡片代码
        input_file: 输入的 HTML 模板文件
        output_file: 输出的 HTML 文件
    """
    # 读取模板
    with open(input_file, "r", encoding="utf-8") as f:
        html_template = f.read()
    
    # 找到列表区域并替换
    # 替换空状态提示为实际数据
    empty_state = '<li class="empty-state">正在扫描全网折扣...</li>'
    
    if empty_state in html_template:
        html_template = html_template.replace(empty_state, html_cards)
    else:
        # 如果找不到空状态，尝试找到 deal-list 标签
        import re
        pattern = r'(<ul id="deal-list">)(.*?)(</ul>)'
        replacement = r'\1\n' + html_cards + '\n        \3'
        html_template = re.sub(pattern, replacement, html_template, flags=re.DOTALL)
    
    # 保存覆盖
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print(f"✅ 页面已更新：{output_file}")

def run_task():
    """
    执行一次完整的抓取和更新任务
    """
    print("\n" + "=" * 50)
    print(f"⏰ 任务执行时间：{json.dumps(__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ensure_ascii=False)}")
    print("=" * 50)
    
    deals = fetch_deals(limit=10)
    
    if deals:
        print(f"✅ 成功获取 {len(deals)} 条数据")
        save_to_json(deals)
        html_cards = generate_html_cards(deals)
        update_index_html(html_cards)
        print("✅ 页面已更新")
    else:
        print("❌ 未获取到任何数据")

if __name__ == "__main__":
    import schedule
    import time
    import threading
    
    print("🎯 全自动折扣资讯聚合器 - 启动中...\n")
    
    # 立即执行一次
    print("📊 执行首次抓取...")
    run_task()
    
    # 设置定时任务：每天早上 8:00 执行
    schedule.every().day.at("08:00").do(run_task)
    print("\n⏰ 定时任务已设置：每天早上 8:00 自动更新")
    print("📌 按 Ctrl+C 停止服务\n")
    
    # 主循环
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次
