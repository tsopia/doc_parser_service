import tempfile
import os
import re
from markitdown import MarkItDown
from loguru import logger
from typing import Optional

class DocumentParser:
    def __init__(self):
        self.md = MarkItDown()
    
    def _get_markitdown_instance(self, docintel_endpoint: Optional[str] = None) -> MarkItDown:
        """根据是否提供 docintel_endpoint 创建 MarkItDown 实例"""
        if docintel_endpoint:
            return MarkItDown(docintel_endpoint=docintel_endpoint)
        return self.md

    def parse_file(self, file_path: str, docintel_endpoint: Optional[str] = None) -> dict:
        """解析本地文件并返回结构化结果"""
        logger.info(f"Parsing local file: {file_path}")
        md_instance = self._get_markitdown_instance(docintel_endpoint)
        result = md_instance.convert(file_path)
        markdown_text = result.text_content

        structured = {"titles": [], "paragraphs": [], "tables": []}
        lines = markdown_text.splitlines()
        paragraph_buffer = []
        table_buffer = []
        in_table = False

        for line in lines:
            if line.startswith("#"):
                if paragraph_buffer:
                    structured["paragraphs"].append(" ".join(paragraph_buffer).strip())
                    paragraph_buffer = []
                structured["titles"].append(line.strip("# ").strip())
            elif re.match(r"^\|.*\|$", line):
                in_table = True
                table_buffer.append(line)
            elif in_table and not line.strip():
                in_table = False
                if table_buffer:
                    structured["tables"].append("\n".join(table_buffer))
                    table_buffer = []
            else:
                if line.strip():
                    paragraph_buffer.append(line.strip())

        if paragraph_buffer:
            structured["paragraphs"].append(" ".join(paragraph_buffer).strip())
        if table_buffer:
            structured["tables"].append("\n".join(table_buffer))

        return {
            "markdown": markdown_text,
            "structured": structured,
            "plain_text": markdown_text.strip()
        }

    def parse_bytes(self, data: bytes, suffix: str, docintel_endpoint: Optional[str] = None) -> dict:
        """支持从内存解析文件内容"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        try:
            return self.parse_file(tmp_path, docintel_endpoint)
        finally:
            os.remove(tmp_path)
