# Trace ID 功能说明

## 概述

本服务已经集成了 trace ID 功能，支持在 HTTP 请求中获取 trace ID 并在日志中输出，便于追踪调用链路。使用了封装的日志工具，开发者无需手动处理 trace ID。

## 功能特性

### 1. Trace ID 获取
- 自动从 HTTP 请求头中获取 trace ID
- 支持的请求头字段：`x-trace-id` 或 `trace-id`
- 如果请求头中没有 trace ID，系统会自动生成一个 UUID

### 2. 日志追踪
- 所有日志都包含 trace ID 前缀：`[trace-id] 日志内容`
- 支持跨服务调用的 trace ID 传递
- 统一的日志格式便于日志聚合和分析
- **无感使用**：开发者只需导入 `app.utils.logger` 中的 `logger`，无需手动获取 trace ID

### 3. 响应头
- 在 HTTP 响应头中返回 trace ID：`x-trace-id`
- 客户端可以获取 trace ID 用于后续调用

## 使用方法

### 客户端发送请求
```bash
# 使用 curl 发送带 trace ID 的请求
curl -X POST "http://localhost:8000/parse/url" \
  -H "Content-Type: application/json" \
  -H "x-trace-id: your-trace-id-here" \
  -d '{"file_url": "https://example.com/document.pdf"}'
```

### Python 客户端示例
```python
import httpx
import uuid

# 生成或使用现有的 trace ID
trace_id = str(uuid.uuid4())

headers = {"x-trace-id": trace_id}
data = {"file_url": "https://example.com/document.pdf"}

response = httpx.post(
    "http://localhost:8000/parse/url",
    json=data,
    headers=headers
)

# 获取响应中的 trace ID
response_trace_id = response.headers.get("x-trace-id")
print(f"Request trace ID: {trace_id}")
print(f"Response trace ID: {response_trace_id}")
```

## 日志格式

### 标准日志格式
```
2024-10-21 10:30:45 | INFO | app.routers.parse_router:parse_url:45 | [abc123-def456-ghi789] Starting to parse file from URL: https://example.com/document.pdf
2024-10-21 10:30:45 | INFO | app.services.download_service:download_from_url:15 | [abc123-def456-ghi789] Downloading file from URL: https://example.com/document.pdf
2024-10-21 10:30:46 | INFO | app.services.parser_service:parse_file:20 | [abc123-def456-ghi789] Parsing local file: /tmp/tmpxyz.pdf
```

### 日志字段说明
- 时间戳：`2024-10-21 10:30:45`
- 日志级别：`INFO`、`ERROR`、`WARNING` 等
- 模块信息：`app.routers.parse_router:parse_url:45`
- Trace ID：`[abc123-def456-ghi789]`
- 日志内容：具体的操作描述

## 调用链路追踪

通过 trace ID，你可以：

1. **跟踪单个请求**：使用相同的 trace ID 过滤日志
2. **性能分析**：分析请求的完整处理时间
3. **错误排查**：快速定位特定请求的错误信息
4. **服务调用链**：在微服务架构中传递 trace ID

### 日志查询示例
```bash
# 查询特定 trace ID 的所有日志
grep "abc123-def456-ghi789" application.log

# 使用 jq 处理 JSON 格式日志（如果使用结构化日志）
cat application.log | jq 'select(.trace_id == "abc123-def456-ghi789")'
```

## 最佳实践

1. **客户端生成 trace ID**：建议在客户端生成 trace ID 并在所有相关请求中使用
2. **传递 trace ID**：在微服务调用中传递 trace ID
3. **日志聚合**：使用 ELK、Fluentd 等工具聚合日志并按 trace ID 索引
4. **监控告警**：基于 trace ID 设置错误监控和告警

## 配置说明

Trace ID 功能通过 FastAPI 中间件实现，无需额外配置。如需自定义：

- 修改 `app/main.py` 中的中间件配置
- 调整 `app/utils/trace.py` 中的工具函数
- 自定义日志格式和输出方式
## 开发者使用指
南

### 简化的日志使用方式

现在开发者可以直接使用封装好的日志工具，无需手动处理 trace ID：

```python
# 旧方式（不推荐）
from loguru import logger
from app.utils.trace import get_trace_id

trace_id = get_trace_id()
logger.info(f"[{trace_id}] 处理请求")

# 新方式（推荐）
from app.utils.logger import logger

logger.info("处理请求")  # trace ID 会自动添加
```

### 支持的日志级别

```python
from app.utils.logger import logger

logger.info("信息日志")
logger.error("错误日志")
logger.warning("警告日志")
logger.debug("调试日志")
logger.success("成功日志")
logger.critical("严重错误日志")
```

### 在新服务中使用

如果你要添加新的服务或模块，只需：

1. 导入封装的日志工具：
```python
from app.utils.logger import logger
```

2. 直接使用，无需关心 trace ID：
```python
def your_function():
    logger.info("开始处理")
    try:
        # 你的业务逻辑
        result = do_something()
        logger.info("处理成功")
        return result
    except Exception as e:
        logger.error(f"处理失败: {e}")
        raise
```

这样所有日志都会自动包含当前请求的 trace ID，便于追踪调用链路。