from fastapi import APIRouter, UploadFile, File, Query
from app.services.parser_service import DocumentParser
from app.services.download_service import DownloadService
from loguru import logger
import os

router = APIRouter(prefix="/parse", tags=["Parser"])
parser = DocumentParser()


def build_response(data=None, code=0, message="ok"):
    """统一响应结构"""
    return {"code": code, "message": message, "data": data}


@router.post("/upload")
async def parse_upload(file: UploadFile = File(...)):
    """上传文档文件并解析"""
    try:
        result = parser.parse_bytes(await file.read(), suffix="." + file.filename.split(".")[-1])
        logger.info(f"Parsed uploaded file: {file.filename}")
        return build_response(data=result)
    except Exception as e:
        logger.error(f"Error parsing uploaded file: {e}")
        return build_response(code=500, message=str(e), data=None)


@router.post("/url")
async def parse_url(file_url: str = Query(..., description="签名对象存储 URL")):
    """通过 URL 下载文件并解析"""
    tmp_path = None
    try:
        suffix = os.path.splitext(file_url.split("?")[0])[1] or ".tmp"
        tmp_path = DownloadService.download_from_url(file_url, suffix)
        result = parser.parse_file(tmp_path)
        logger.info(f"Parsed file from URL: {file_url}")
        return build_response(data=result)
    except Exception as e:
        logger.error(f"Error parsing file from URL: {e}")
        return build_response(code=500, message=str(e), data=None)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
