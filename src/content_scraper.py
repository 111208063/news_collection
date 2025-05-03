# -*- coding: utf-8 -*-
"""News content scraper script to extract content from news links"""

from bs4 import BeautifulSoup
import requests
import time
import os
import json
from typing import List, Tuple, Dict, Optional, Any
import logging
from datetime import datetime

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("news_scraper.log"), logging.StreamHandler()]
)
logger = logging.getLogger("content_scraper")

def extract_content(html: str) -> Dict[str, Any]:
    """從 HTML 中提取新聞內容
    
    Args:
        html: 網頁 HTML 內容
        
    Returns:
        Dict: 包含標題、發布日期、內文等的字典
    """
    soup = BeautifulSoup(html, "html.parser")
    result = {
        "title": "",
        "publish_time": "",
        "content": "",
        "author": "",
        "source": ""
    }
    
    try:
        # 提取標題 - 在h1標籤中
        title_tag = soup.select_one("h1")
        if title_tag:
            result["title"] = title_tag.get_text(strip=True)
        
        # 提取作者和來源 - 在class="alr4vq1"的p標籤中
        author_tag = soup.select_one("p.alr4vq1")
        if author_tag:
            author_text = author_tag.get_text(strip=True)
            # 處理文本分離作者和來源
            if "鉅亨網記者" in author_text:
                result["author"] = "鉅亨網記者"
                source_parts = author_text.split("鉅亨網記者")
                if len(source_parts) > 1:
                    result["source"] = source_parts[1].strip()
            
            # 提取時間 - 在同一個p標籤裡，但在span後面
            time_text = ""
            for child in author_tag.contents:
                if isinstance(child, str) and "-" in child and ":" in child:
                    time_text = child.strip()
                    break
            
            if time_text:
                result["publish_time"] = time_text
        
        # 提取內文 - 在id="article-container"的main元素下的所有p標籤
        content_container = soup.select_one("main#article-container")
        if content_container:
            # 獲取所有段落
            paragraphs = []
            for section in content_container.select("section"):
                for p in section.select("p"):
                    # 排除廣告或其他非內容段落
                    if p.parent.get("id") and "ad" in p.parent.get("id", ""):
                        continue
                    if p.get_text(strip=True):
                        paragraphs.append(p.get_text(strip=True))
            
            # 將所有段落合併為單一文字，不使用換行符
            result["content"] = " ".join(paragraphs)
        
    except Exception as e:
        logger.error(f"提取內容時出錯: {e}")
    
    return result

def process_news_links(links: List[str]) -> List[Dict[str, Any]]:
    """處理新聞連結列表，抓取每個連結的內容
    
    Args:
        links: 新聞連結列表
        
    Returns:
        List[Dict]: 新聞內容的列表
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    news_contents = []
    
    try:
        # 創建保存目錄
        content_dir = "news_contents"
        if not os.path.exists(content_dir):
            os.makedirs(content_dir)
        
        # 處理每個連結
        for i, url in enumerate(links, 1):
            try:
                logger.info(f"處理連結 {i}/{len(links)}: {url}")
                
                # 使用requests直接獲取頁面內容
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()  # 確保請求成功
                html = response.text
                
                # 提取內容
                content = extract_content(html)
                content["url"] = url
                news_contents.append(content)
                
                # 保存提取的內容
                content_file = f"news_{i}.json"
                with open(os.path.join(content_dir, content_file), "w", encoding="utf-8") as f:
                    json.dump(content, f, ensure_ascii=False, indent=2)
                
                logger.info(f"內容已保存至: {content_file}")
                
                # 間隔一下，避免請求過快
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"處理連結 {url} 時出錯: {e}")
        
        # 保存所有內容到一個 JSON 文件
        all_content_path = os.path.join(content_dir, "all_news.json")
        with open(all_content_path, "w", encoding="utf-8") as f:
            json.dump(news_contents, f, ensure_ascii=False, indent=2)
        
        logger.info(f"所有新聞內容已保存至: {all_content_path}")
        
    except Exception as e:
        logger.error(f"發生錯誤: {e}")
    
    return news_contents

def load_news_links(filepath: str) -> List[str]:
    """從 JSON 文件中載入新聞連結
    
    Args:
        filepath: JSON 文件路徑
        
    Returns:
        List[str]: 新聞連結列表
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 假設 JSON 是標題和連結的元組列表
        if isinstance(data, list) and len(data) > 0:
            if isinstance(data[0], list) and len(data[0]) > 1:
                return [item[1] for item in data if len(item) > 1 and item[1]]
            # 假設每個元素是dict
            elif isinstance(data[0], dict) and "url" in data[0]:
                return [item["url"] for item in data if "url" in item]
    except Exception as e:
        logger.error(f"載入新聞連結時出錯: {e}")
    
    return []

def main():
    """主函數"""
    # 從 webscraping.py 運行後保存的連結文件中讀取連結
    # 如果沒有保存的文件，則手動提供連結列表
    
    # 方法1: 從文件讀取
    links_file = "news_links.json"
    if os.path.exists(links_file):
        links = load_news_links(links_file)
        logger.info(f"從 {links_file} 載入了 {len(links)} 個連結")
    else:
        # 方法2: 手動提供的測試連結
        links = [
            "https://news.cnyes.com/news/id/5327000",
            "https://news.cnyes.com/news/id/5327001"
        ]
        logger.info("使用測試連結")
    
    if links:
        # 處理連結
        process_news_links(links)
    else:
        logger.error("未找到需要處理的連結")

if __name__ == "__main__":
    main() 