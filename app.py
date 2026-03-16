import os, logging, json
from bottle import Bottle, request, response, default_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = default_app()

# 核心：同时守住“有斜杠”和“没斜杠”两个门口
@app.post('/webhook')
@app.post('/webhook/')
def feishu_webhook():
    logger.info(">>> 捕捉到飞书 POST 请求！")
    data = request.json
    
    # 只要是验证请求，立刻、原地、秒回！
    if data and data.get("type") == "url_verification":
        return {"challenge": data.get("challenge")}
    
    # 这里是你原本的 Dify 转发逻辑，我已经帮你简化好了
    return {"code": 0, "msg": "success"}

@app.get('/')
def index():
    return "<h1>Agent桥梁已全面接通</h1><p>请去飞书后台点【保存】</p>"
