## Flickr Scraper - Custom Features (EN/中文)

### 1) Loguru Logging / Loguru 日誌
- Console: colored INFO logs.
- Files: logs/flickr_scraper_YYYY-MM-DD.log (DEBUG), logs/errors_YYYY-MM-DD.log (ERROR)
- Rotation + compression; logs are git-ignored.

### 2) Environment Setup / 環境變數設定
- Use python-dotenv to load `.env`.
- `.env` keys: FLICKR_API_KEY, FLICKR_API_SECRET
- Example:
```bash
export FLICKR_API_KEY=your_key
export FLICKR_API_SECRET=your_secret
# or create .env with the same keys
```

### 3) Photo Size Selection / 照片尺寸選擇
- Use `--size`: square, large_square, thumbnail, small, small_320, medium, medium_640, medium_800, large, large_1600, large_2048, original
- Example:
```bash
python3 flickr_scraper.py --search "honeybees on flowers" --n 10 --download --size large
```

### 4) Multi-Thread Mode / 多線程模式
- Multiple keywords => ThreadPoolExecutor
- `--max-workers` to control concurrency
- Example:
```bash
python3 flickr_scraper.py --search "sunset" "beach" --n 5 --download --max-workers 4
```

### 5) Skip Existing Files / 檔案已存在自動跳過
- If destination filename exists, skip download to avoid duplicates.
- 日誌輸出: "檔案已存在，跳過下載: <filename>"

### 6) 429 Retry Handling / 429 重試機制
- On HTTP 429: sleep 3s, retry up to 3 times (configurable via code)
- 日誌會記錄每次重試與最終結果

### 7) Empty-file Guard / 空檔守衛
- Files < 1KB are treated as invalid and removed
- Stop after 3 consecutive empties

### 8) Usage Examples / 使用範例
```bash
# Single keyword
python3 flickr_scraper.py --search "forest" --n 10 --download

# Multiple keywords (multithread)
python3 flickr_scraper.py --search "forest" "mountain" --n 10 --download --max-workers 4

# Specify size
python3 flickr_scraper.py --search "beach" --n 5 --download --size medium
```

### Notes / 注意事項
- Ensure dependencies installed: flickrapi, python-dotenv, loguru, pillow, requests
- Do not commit `.env` or logs to Git
