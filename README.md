
# Doc Parser Service

## 📌 项目简介

`Doc Parser Service` 是一个基于 **FastAPI** 的文档解析服务，提供以下能力：

* **文件上传解析**：上传 `.docx`、`.pdf`、`.txt` 等文档，返回结构化信息、Markdown 内容和纯文本。
* **URL 下载解析**：提供签名对象存储 URL，服务自动下载并解析文件。
* **统一响应格式**：所有接口返回统一 JSON 包装 `{ code, message, data }`。
* **日志记录**：使用 `loguru` 记录解析过程和异常信息。

该服务适合与其他后端系统对接，实现文档解析自动化。

---

## 🛠️ 项目依赖

* Python 3.11+
* FastAPI
* uv / uvicorn
* python-multipart
* MarkItDown
* loguru
* httpx
* ffmpeg（可选，用于音频解析）

---

## 📦 项目结构

```
doc-parser-service/
├── app/
│   ├── main.py                  # FastAPI 启动入口
│   ├── routers/parse_router.py  # 路由定义
│   ├── services/parser_service.py   # 文档解析逻辑
│   ├── services/download_service.py # URL 下载服务
│   └── services/storage_service.py  # 可选对象存储服务
├── pyproject.toml
├── Dockerfile
├── README.md
└── uv.lock
```

---

## 🚀 本地运行

1. 安装依赖：

```bash
uv pip install --system
uv pip install python-multipart
```

2. 启动服务：

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

3. 接口访问：

* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

---

## 🐳 Docker 运行

1. 构建镜像：

```bash
docker build -t doc-parser-service .
```

2. 运行容器（监听宿主机 80 端口）：

```bash
docker run -p 80:80 doc-parser-service
```

---

## 📄 接口文档

### 1️⃣ 上传文件解析

```
POST /parse/upload
Content-Type: multipart/form-data
Form Field: file (上传文件)
```

**成功响应示例：**

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "markdown": "# 产品需求\n这是需求文档内容。",
    "structured": {
      "titles": ["产品需求"],
      "paragraphs": ["这是需求文档内容。"],
      "tables": []
    },
    "plain_text": "# 产品需求\n这是需求文档内容。"
  }
}
```

---

### 2️⃣ URL 下载解析

```
POST /parse/url?file_url=<签名对象存储 URL>
```

**参数说明：**

* `file_url`：其他服务签名的对象存储文件地址

**成功响应示例：**

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "markdown": "# 产品需求\n这是需求文档内容。",
    "structured": {
      "titles": ["产品需求"],
      "paragraphs": ["这是需求文档内容。"],
      "tables": []
    },
    "plain_text": "# 产品需求\n这是需求文档内容。"
  }
}
```

**错误响应示例：**

```json
{
  "code": 500,
  "message": "下载失败：403 Forbidden",
  "data": null
}
```

---

## ⚡ 日志

* 默认输出到控制台
* 记录文件上传解析、URL 下载解析及异常信息
* 使用 `loguru`，可扩展到文件或对象存储日志


