# Middleware API — 卡密中转服务

一个轻量的 Flask 中转服务，接收订单请求并转发到上游 API，返回卡密内容。

## 功能

- **POST /api/transform** — 接收订单参数，转发到上游 API 并返回卡密
- **GET /health** — 健康检查

## 快速部署

```bash
git clone https://github.com/leizi914599611-boop/middleware-api.git
cd middleware-api
docker compose up -d
```

默认监听 `0.0.0.0:5000`，docker-compose 映射到宿主机端口 `19961`。

## API 用法

### 提交订单

```bash
curl -X POST http://localhost:19961/api/transform \
  -H "Content-Type: application/json" \
  -d '{
    "tid": "商品ID",
    "user": "用户名",
    "pass": "密码",
    "input1": "可选参数",
    "num": "数量"
  }'
```

**必填参数：** `tid`、`user`、`pass`

**响应：** 直接返回卡密内容文本

### 健康检查

```bash
curl http://localhost:19961/health
# → {"status":"ok"}
```

## 技术栈

- Python 3.11 + Flask
- Docker / docker-compose
