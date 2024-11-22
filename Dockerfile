# 使用官方 Python 镜像作为基础镜像
FROM python:3.10-alpine as builder

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到容器的 /app 目录
COPY . /app

# 安装 Python 依赖
RUN python -m venv .venv && \
    chmod a+x .venv/bin/activate && \
    .venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

FROM python:3.10-alpine
# 声明容器会使用的端口
COPY --from=builder /app /app

WORKDIR /app

CMD .venv/bin/activate

# 设置容器启动时执行的命令
ENTRYPOINT ["python", "main.py"]
