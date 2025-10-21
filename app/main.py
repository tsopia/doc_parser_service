from fastapi import FastAPI, Request
from app.routers import parse_router
from app.utils.trace import set_trace_id
from app.utils.logger import logger
import uuid

app = FastAPI(title="Doc Parser Service", version="0.4.0")

@app.middleware("http")
async def trace_middleware(request: Request, call_next):
    """添加 trace ID 中间件"""
    # 从请求头获取 trace ID，如果没有则生成一个新的
    trace_id = request.headers.get("x-trace-id") or request.headers.get("trace-id") or str(uuid.uuid4())
    
    # 设置到上下文变量中
    set_trace_id(trace_id)
    
    # 配置 loguru 格式，包含 trace ID
    logger.configure(
        handlers=[
            {
                "sink": lambda msg: print(f"[{trace_id}] {msg}", end=""),
                "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
                "level": "INFO"
            }
        ]
    )
    
    # 记录请求开始
    logger.info(f"Request started: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # 在响应头中添加 trace ID
    response.headers["x-trace-id"] = trace_id
    
    # 记录请求结束
    logger.info(f"Request completed: {response.status_code}")
    
    return response

app.include_router(parse_router.router)
