# -*- coding: utf-8 -*-
"""Web scraping script for news collection"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from PIL import Image
import io
import requests
import os
import json
from typing import List, Tuple, Dict, Any

def setup_chrome_options():
    """Set up Chrome options for web scraping"""
    chrome_options = Options()
    
    # Headless mode (optional, uncomment to run in headless mode)
    # chrome_options.add_argument("--headless=new")
    
    # Window size
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Disable features for stability
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    
    # User agent
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    return chrome_options

def save_screenshot(driver, filename):
    """Save screenshot to file"""
    screenshot = driver.get_screenshot_as_png()
    image = Image.open(io.BytesIO(screenshot))
    image.save(filename)

def save_news_links(news_list: List[Tuple[str, str]], filename: str = "news_links.json") -> None:
    """保存新聞連結到檔案
    
    Args:
        news_list: 包含標題和連結的列表
        filename: 輸出文件名
    """
    # 提取連結
    links = [link for _, link in news_list if link]
    
    # 保存為JSON格式
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)
    
    print(f"已保存 {len(links)} 個新聞連結到 {filename}")

def main():
    # Create screenshots directory if it doesn't exist
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
    
    # Set up Chrome options
    chrome_options = setup_chrome_options()
    
    try:
        # Initialize WebDriver with ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("WebDriver initialized successfully!")
        
        # Navigate to the news page
        url = "https://news.cnyes.com/news/cat/wd_stock"
        driver.get(url)
        
        # Take initial screenshot
        save_screenshot(driver, 'screenshots/initial_page.png')
        
        # Scroll to bottom to load more news
        scroll_pause_time = 2
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break
            last_height = new_height
        
        # Take final screenshot
        save_screenshot(driver, 'screenshots/final_page.png')
        
        # Get the complete HTML
        html = driver.page_source
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        
        # Extract news titles and links
        news_list = []
        for news in soup.select("a.t2rnaph"):
            # 從連結取得相對路徑
            link = news["href"] if news.has_attr("href") else None
            # 取得完整URL
            if link and not link.startswith('http'):
                link = f"https://news.cnyes.com{link}"
            
            # 從p標籤取得標題
            title_tag = news.select_one("p.news-title")
            title = title_tag.get_text(strip=True) if title_tag else news.get_text(strip=True)
            
            news_list.append((title, link))
        
        # Print results
        print("\nNews List:")
        for i, (title, link) in enumerate(news_list, start=1):
            print(f"{i}. {title} - {link}")
        
        # 保存新聞連結到文件
        save_news_links(news_list)
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()