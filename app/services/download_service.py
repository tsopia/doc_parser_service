import httpx
import tempfile
import os
from app.utils.logger import logger

class DownloadService:
    @staticmethod
    def download_from_url(url: str, suffix: str = None) -> str:
        """通过 URL 下载文件到本地临时文件"""
        logger.info(f"Downloading file from URL: {url}")
        if not suffix:
            suffix = os.path.splitext(url.split("?")[0])[1] or ".tmp"
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        try:
            with httpx.stream("GET", url) as r:
                r.raise_for_status()
                for chunk in r.iter_bytes():
                    tmp_file.write(chunk)
            tmp_file.close()
            logger.info(f"Downloaded file to: {tmp_file.name}")
            return tmp_file.name
        except Exception as e:
            logger.error(f"Download failed: {e}")
            tmp_file.close()
            os.remove(tmp_file.name)
            raise
