# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from pathlib import Path
import time

import requests
from PIL import Image
from loguru import logger


def download_uri(uri, dir="./", max_retries=3):
    """Downloads file from URI, performing checks and renaming; supports timeout and image format suffix addition.
    
    Args:
        uri (str): 要下載的檔案 URL
        dir (str or Path): 下載目錄
        max_retries (int): 最大重試次數，預設為 3 次
        
    Returns:
        Path: 下載完成的檔案路徑，如果失敗或檔案已存在則返回 None
    """
    for attempt in range(max_retries + 1):  # +1 是因為第一次不算重試
        try:
            # Download
            dir = Path(dir)
            f = dir / Path(uri).name  # filename
            
            # 檢查檔案是否已存在
            if f.exists():
                logger.info(f"檔案已存在，跳過下載: {f.name}")
                return f  # 返回已存在的檔案路徑
            
            # 下載檔案
            if attempt == 0:
                logger.debug(f"開始下載: {uri}")
            else:
                logger.info(f"重試下載 (第 {attempt} 次): {uri}")
                
            response = requests.get(uri, timeout=10)
            response.raise_for_status()  # 檢查 HTTP 狀態碼
            
            with open(f, "wb") as file:
                file.write(response.content)

            # Rename (remove wildcard characters)
            src = f  # original name
            f = Path(
                str(f)
                .replace("%20", "_")
                .replace("%", "_")
                .replace("*", "_")
                .replace("~", "_")
                .replace("(", "_")
                .replace(")", "_")
            )

            if "?" in str(f):
                f = Path(str(f)[: str(f).index("?")])

            if src != f:
                src.rename(f)  # rename

            # Add suffix (if missing)
            if not f.suffix:
                try:
                    src = f  # original name
                    f = f.with_suffix(f".{Image.open(f).format.lower()}")
                    src.rename(f)  # rename
                except Exception as e:
                    logger.warning(f"無法識別圖片格式，使用預設 .jpg 副檔名: {e}")
                    f = f.with_suffix(".jpg")
            
            if attempt == 0:
                logger.debug(f"下載完成: {f.name}")
            else:
                logger.info(f"重試成功，下載完成: {f.name}")
            return f  # 返回最終檔案路徑
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Too Many Requests
                if attempt < max_retries:
                    logger.warning(f"遇到 429 錯誤 (Too Many Requests)，等待 3 秒後重試... (第 {attempt + 1} 次嘗試)")
                    time.sleep(3)  # 等待 3 秒
                    continue  # 繼續重試
                else:
                    logger.error(f"下載失敗: {uri} - 429 錯誤，已重試 {max_retries} 次，放棄下載")
                    return None
            else:
                logger.error(f"下載失敗: {uri} - HTTP {e.response.status_code}: {e}")
                return None
        except requests.exceptions.RequestException as e:
            # 檢查錯誤訊息中是否包含 429 錯誤
            error_msg = str(e).lower()
            if "429" in error_msg or "too many requests" in error_msg:
                if attempt < max_retries:
                    logger.warning(f"遇到 429 錯誤 (Too Many Requests)，等待 3 秒後重試... (第 {attempt + 1} 次嘗試)")
                    time.sleep(3)  # 等待 3 秒
                    continue  # 繼續重試
                else:
                    logger.error(f"下載失敗: {uri} - 429 錯誤，已重試 {max_retries} 次，放棄下載")
                    return None
            else:
                logger.error(f"下載失敗: {uri} - {e}")
                return None
        except Exception as e:
            logger.error(f"處理檔案失敗: {uri} - {e}")
            return None屋
    
    # 如果所有重試都失敗了
    logger.error(f"下載失敗: {uri} - 已重試 {max_retries} 次，最終失敗")
    return None
