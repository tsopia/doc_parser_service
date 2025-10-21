from fastapi import APIRouter, UploadFile, File, Form, Body
from app.services.parser_service import DocumentParser
from app.services.download_service import DownloadService
from app.models.schema import ParseUrlRequest, ParseResponse
from app.utils.logger import logger
import os
from typing import Optional

router = APIRouter(prefix="/parse", tags=["Parser"])
parser = DocumentParser()


def build_response(data=None, code=0, message="ok"):
    """统一响应结构"""
    return {"code": code, "message": message, "data": data}


@router.post("/upload", response_model=ParseResponse)
async def parse_upload(
    file: UploadFile = File(...),
    docintel_endpoint: Optional[str] = Form(None, description="Azure Document Intelligence 端点 URL")
):
    """上传文档文件并解析
    
    Args:
        file: 要解析的文档文件
        docintel_endpoint: 可选的 Azure Document Intelligence 端点 URL
    """
    try:
        logger.info(f"Starting to parse uploaded file: {file.filename}")
        
        result = parser.parse_bytes(
            await file.read(), 
            suffix="." + file.filename.split(".")[-1],
            docintel_endpoint=docintel_endpoint
        )
        logger.info(f"Successfully parsed uploaded file: {file.filename}")
        return build_response(data=result)
    except Exception as e:
        logger.error(f"Error parsing uploaded file {file.filename}: {e}")
        return build_response(code=500, message=str(e), data=None)


@router.post("/url", response_model=ParseResponse)
async def parse_url(request: ParseUrlRequest = Body(...)):
    """通过 URL 下载文件并解析
    
    Args:
        request: 包含文件 URL 和可选的 Azure Document Intelligence 端点
    """
    tmp_path = None
    try:
        logger.info(f"Starting to parse file from URL: {request.file_url}")
        
        suffix = os.path.splitext(request.file_url.split("?")[0])[1] or ".tmp"
        tmp_path = DownloadService.download_from_url(request.file_url, suffix)
        result = parser.parse_file(tmp_path, docintel_endpoint=request.docintel_endpoint)
        logger.info(f"Successfully parsed file from URL: {request.file_url}")
        return build_response(data=result)
    except Exception as e:
        logger.error(f"Error parsing file from URL {request.file_url}: {e}")
        return build_response(code=500, message=str(e), data=None)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
