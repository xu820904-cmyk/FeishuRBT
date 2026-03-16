import os, logging, json
from bottle import Bottle, request, response, default_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = default_app()

# 这个路径必须和你在飞书后台填的一模一样
@app.post('/webhook')
def feishu_webhook():
    logger.info(">>> 捕捉到飞书 POST 请求！")
    data = request.json
    logger.info(f"收到的数据: {data}")

    # 专门处理飞书的开门验证，这是最优先的！
    if data and data.get("type") == "url_verification":
        challenge = data.get("challenge")
        logger.info(f"正在返回 challenge: {challenge}")
        return {"challenge": challenge}
    
    return {"code": 0, "msg": "success"}

@app.get('/')
def index():
    return "<h1>DEBUG 模式已开启</h1><p>路径：/webhook</p>"
