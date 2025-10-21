"""
带 trace ID 的日志工具
"""
from loguru import logger as _logger
from app.utils.trace import get_trace_id
from typing import Any


class TraceLogger:
    """自动包含 trace ID 的日志器"""
    
    def _format_message(self, message: str) -> str:
        """格式化消息，自动添加 trace ID"""
        trace_id = get_trace_id()
        if trace_id:
            return f"[{trace_id}] {message}"
        return message
    
    def info(self, message: str, *args, **kwargs) -> None:
        """记录 INFO 级别日志"""
        _logger.info(self._format_message(message), *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs) -> None:
        """记录 ERROR 级别日志"""
        _logger.error(self._format_message(message), *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs) -> None:
        """记录 WARNING 级别日志"""
        _logger.warning(self._format_message(message), *args, **kwargs)
    
    def debug(self, message: str, *args, **kwargs) -> None:
        """记录 DEBUG 级别日志"""
        _logger.debug(self._format_message(message), *args, **kwargs)
    
    def success(self, message: str, *args, **kwargs) -> None:
        """记录 SUCCESS 级别日志"""
        _logger.success(self._format_message(message), *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs) -> None:
        """记录 CRITICAL 级别日志"""
        _logger.critical(self._format_message(message), *args, **kwargs)


# 创建全局日志实例
logger = TraceLogger()