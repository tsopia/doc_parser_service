from pydantic import BaseModel
from typing import Optional


class ParseUrlRequest(BaseModel):
    file_url: str
    docintel_endpoint: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "file_url": "https://example.com/document.pdf",
                "docintel_endpoint": "https://your-resource.cognitiveservices.azure.com/"
            }
        }


class ParseResponse(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None