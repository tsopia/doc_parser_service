import contextvars
from typing import Optional

# 导入 trace_id 上下文变量
trace_id_var: contextvars.ContextVar[str] = contextvars.ContextVar('trace_id')

def get_trace_id() -> Optional[str]:
    """获取当前请求的 trace ID"""
    try:
        return trace_id_var.get()
    except LookupError:
        return None

def set_trace_id(trace_id: str) -> None:
    """设置当前请求的 trace ID"""
    trace_id_var.set(trace_id)