# 新聞爬蟲工具

這是一個用於抓取[鉅亨網](https://news.cnyes.com/)新聞的爬蟲工具。該工具分為兩個主要模組：一個用於抓取新聞列表，另一個用於提取各個新聞內容。

## 功能特點

- 抓取鉅亨網股票相關新聞列表和連結
- 提取新聞內容，包括標題、發布時間、作者、來源和正文
- 將結果以JSON格式保存，便於後續分析和處理

## 環境需求

- Python 3.8+
- Chrome瀏覽器（用於webscraping.py）
- 相關依賴包（詳見 `requirements.txt`）

## 安裝步驟

1. 克隆此代碼庫：

```bash
git clone https://github.com/你的用戶名/news_collection.git
cd news_collection
```

2. 創建並激活虛擬環境（推薦）：

```bash
# 使用venv
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate
```

3. 安裝所需依賴：

```bash
pip install -r requirements.txt
```

4. 確保已安裝Chrome瀏覽器（webscraping.py需要使用）

## 使用說明

此爬蟲工具分兩步執行：

### 1. 抓取新聞列表

首先運行 `webscraping.py` 來抓取新聞列表和連結：

```bash
python src/webscraping.py
```

這將生成 `news_links.json` 文件，其中包含所有抓取到的新聞標題和連結。

**注意**：這一步驟需要Chrome瀏覽器，過程中會自動下載對應版本的ChromeDriver。如果遇到問題，可嘗試修改程式碼中的`setup_chrome_options`函數來調整瀏覽器設定。

### 2. 提取新聞內容

然後運行 `content_scraper.py` 來處理連結並提取新聞內容：

```bash
python src/content_scraper.py
```

這將生成 `news_contents` 目錄，其中包含每篇新聞的JSON文件和一個匯總所有新聞的 `all_news.json` 文件。

## 項目結構

```
news_collection/
├── src/
│   ├── webscraping.py    - 抓取新聞列表和連結
│   └── content_scraper.py - 提取新聞內容
├── screenshots/          - 網頁截圖保存目錄
├── news_contents/        - 提取的新聞內容保存目錄
├── requirements.txt      - 依賴包列表
├── .gitignore           - Git忽略文件
└── README.md             - 項目說明
```

## 配置Git和上傳到GitHub

如果你想將此項目上傳到自己的GitHub：

1. 初始化Git倉庫（如果還未初始化）：
```bash
git init
```

2. 添加文件到Git：
```bash
git add .
```

3. 提交變更：
```bash
git commit -m "初始提交：新聞爬蟲工具"
```

4. 添加你的GitHub倉庫作為遠程倉庫：
```bash
git remote add origin https://github.com/你的用戶名/news_collection.git
```

5. 推送到GitHub：
```bash
git push -u origin master  # 或 git push -u origin main
```

## 注意事項

- 此爬蟲僅供學習和研究使用，請勿用於商業目的
- 請合理控制爬取頻率，避免對目標網站造成過大負擔
- 網站結構可能會改變，若爬蟲失效，可能需要更新選擇器
- 初次運行時，`webdriver-manager`會自動下載Chrome驅動，確保您的網絡連接正常

## 常見問題解決

1. **ChromeDriver相關問題**：
   - 如果自動下載失敗，可以手動下載適合您Chrome版本的[ChromeDriver](https://chromedriver.chromium.org/downloads)
   - 下載後修改程式碼指定ChromeDriver路徑

2. **網絡訪問問題**：
   - 確保您的網絡可以正常訪問目標網站
   - 如果需要使用代理，可在`requests.get`方法中添加代理設定

## 依賴說明

主要依賴包括：

- `selenium` - 用於自動化瀏覽器操作（僅在 webscraping.py 中使用）
- `beautifulsoup4` - 用於解析HTML
- `requests` - 用於發送HTTP請求
- `webdriver-manager` - 用於管理瀏覽器驅動
- `Pillow` - 用於處理截圖 