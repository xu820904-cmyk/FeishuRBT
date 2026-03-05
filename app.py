import os
import logging
import requests
from bottle import Bottle, request, response, default_app

# 1. 基础配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = default_app()

# 从 Vercel 环境变量读取配置
APP_ID = os.environ.get("APP_ID")
APP_SECRET = os.environ.get("APP_SECRET")
DIFY_API_KEY = os.environ.get("DIFY_API_KEY")
DIFY_API_URL = os.environ.get("DIFY_API_URL", "https://api.dify.ai/v1")

# 2. 首页 (验证服务器是否活着)
@app.get('/')
def index():
    return "<h1>机器人已在 Vercel 上线！</h1><p>请确保飞书地址填的是 /webhook</p>"

# 3. 核心后门：处理飞书消息
@app.post('/webhook')
def feishu_webhook():
    data = request.json
    logger.info(f"收到飞书信号: {data}")

    # --- 关键：处理飞书的“开门验证” ---
    if data.get("type") == "url_verification":
        return {"challenge": data.get("challenge")}

    # --- 这里是处理用户消息并转发给 Dify 的逻辑 ---
    # 为了保证验证通过，咱们先让它快速返回 200
    return {"code": 0, "msg": "success"}

# 注意：千万不要写 app.run()
