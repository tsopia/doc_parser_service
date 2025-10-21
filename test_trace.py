#!/usr/bin/env python3
"""
测试 trace ID 功能的示例脚本
"""
import httpx
import uuid

def test_trace_id():
    """测试 trace ID 功能"""
    base_url = "http://localhost:8000"
    
    # 生成一个测试用的 trace ID
    test_trace_id = str(uuid.uuid4())
    
    print(f"Testing with trace ID: {test_trace_id}")
    
    # 测试上传接口（需要准备一个测试文件）
    headers = {"x-trace-id": test_trace_id}
    
    # 测试 URL 解析接口
    test_data = {
        "file_url": "https://example.com/test.pdf"
    }
    
    try:
        response = httpx.post(
            f"{base_url}/parse/url",
            json=test_data,
            headers=headers
        )
        print(f"Response status: {response.status_code}")
        print(f"Response trace ID: {response.headers.get('x-trace-id')}")
        print(f"Response body: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_trace_id()