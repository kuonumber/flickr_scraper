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

### 5) Custom Output Directory / 自定義輸出目錄
- Use `--output-dir` to specify custom download path
- Default: "images" directory
- Example:
```bash
python3 flickr_scraper.py --search "sunset" --n 5 --download --output-dir "my_photos"
```

### 6) Creator Lock / 創作者鎖定
- Use `--user-id` to lock specific Flickr user ID
- Use `--owner-name` to lock specific Flickr username
- Example:
```bash
# Lock by user ID
python3 flickr_scraper.py --search "nature" --download --user-id "98765432@N00"

# Lock by username
python3 flickr_scraper.py --search "space" --download --owner-name "example_user123"
```

### 7) All Albums Search / 所有相簿搜尋
- Use `--all-albums` with creator lock to search across all user albums
- When enabled, searches user's entire photo collection (not limited by keywords)
- Example:
```bash
# Search all albums of a specific user
python3 flickr_scraper.py --search "" --download --owner-name "example_user123" --all-albums

# Search specific keyword across all user albums
python3 flickr_scraper.py --search "nature" --download --owner-name "example_user123" --all-albums
```

### 8) Album Management / 相簿管理
- `--list-albums`: List all albums of a specific user
- `--album-id`: Download photos from a specific album
- `--download-all-albums`: Download all albums of a user
- Example:
```bash
# List user albums
python3 flickr_scraper.py --list-albums --owner-name "example_user123"

# Download from specific album
python3 flickr_scraper.py --album-id "99999999999999999" --download --size large

# Download all albums of a user
python3 flickr_scraper.py --download-all-albums --owner-name "example_user123" --download --size medium
```

### 9) Skip Existing Files / 檔案已存在自動跳過
- If destination filename exists, skip download to avoid duplicates.
- 日誌輸出: "檔案已存在，跳過下載: <filename>"

### 10) 429 Retry Handling / 429 重試機制
- On HTTP 429: sleep 3s, retry up to 3 times (configurable via code)
- 日誌會記錄每次重試與最終結果

### 11) Empty-file Guard / 空檔守衛
- Files < 1KB are treated as invalid and removed
- Stop after 3 consecutive empties

### 12) Usage Examples / 使用範例
```bash
# Single keyword
python3 flickr_scraper.py --search "forest" --n 10 --download

# Multiple keywords (multithread)
python3 flickr_scraper.py --search "forest" "mountain" --n 10 --download --max-workers 4

# Specify size
python3 flickr_scraper.py --search "beach" --n 5 --download --size medium

# Custom output directory
python3 flickr_scraper.py --search "forest" --n 10 --download --output-dir "nature_photos"

# Multiple keywords with custom output
python3 flickr_scraper.py --search "sunset" "mountain" --n 5 --download --output-dir "landscape" --max-workers 2

# Creator lock examples
python3 flickr_scraper.py --search "nature" --download --owner-name "example_user123"
python3 flickr_scraper.py --search "portrait" --download --user-id "98765432@N00"
python3 flickr_scraper.py --search "landscape" "city" --download --owner-name "sample_photographer" --max-workers 2

# All albums search examples
python3 flickr_scraper.py --search "" --download --owner-name "example_user123" --all-albums
python3 flickr_scraper.py --search "space" --download --owner-name "example_user123" --all-albums
python3 flickr_scraper.py --search "earth" "moon" --download --owner-name "example_user123" --all-albums --max-workers 2

# Album management examples
python3 flickr_scraper.py --list-albums --owner-name "example_user123"
python3 flickr_scraper.py --album-id "99999999999999999" --download --size large
python3 flickr_scraper.py --download-all-albums --owner-name "example_user123" --download --size medium --max-workers 4
```

### Notes / 注意事項
- Ensure dependencies installed: flickrapi, python-dotenv, loguru, pillow, requests
- Do not commit `.env` or logs to Git
