FROM python:3.11-slim

WORKDIR /app
COPY . .

# 安装系统依赖（如果需要 ffmpeg）
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# 安装 uv 和项目依赖
RUN python -m pip install --upgrade pip
RUN pip install uv
RUN uv pip install --system .
RUN #uv pip install python-multipart

EXPOSE 80

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
