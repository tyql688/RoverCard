# Rover Card 服务

## 功能

- 面板图显示调试

## 本地开发
### 使用 uv

1. 安装依赖：
```bash
uv sync
```

2. 启动服务：
```bash
uv run main.py
```

## Docker 部署
### 构建镜像
```bash
docker build -t card-show-service .
```

### 运行容器
```bash
docker run -p 8108:8108 card-show-service
```

### 访问服务
- 访问 Card Show 服务：[http://localhost:8108](http://localhost:8108)
