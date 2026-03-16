import os, logging, requests, json
from bottle import Bottle, request, response, default_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = default_app()

# 核心修正：同时兼容有斜杠和没斜杠的情况
@app.post('/webhook')
@app.post('/webhook/')
def feishu_webhook():
    # 增加这行日志，只要飞书来过，Logs里一定会蹦出这句话
    logger.info(">>> 收到飞书 POST 请求！")
    
    data = request.json
    # 1. 核心：秒回飞书的“开门挑战”
    if data.get("type") == "url_verification":
        logger.info("正在处理飞书 URL 验证...")
        return {"challenge": data.get("challenge")}
    
    # 2. 核心：识别用户消息并传给 Dify
    try:
        if "header" in data and data["header"]["event_type"] == "im.message.receive_v1":
            content = json.loads(data["event"]["message"]["content"])
            user_query = content.get("text", "")
            user_id = data["event"]["sender"]["sender_id"]["open_id"]
            
            logger.info(f"收到消息: {user_query}，准备发给 Dify")
            
            requests.post(
                f"{os.environ.get('DIFY_API_URL')}/chat-messages",
                headers={"Authorization": f"Bearer {os.environ.get('DIFY_API_KEY')}"},
                json={
                    "inputs": {},
                    "query": user_query,
                    "response_mode": "blocking",
                    "user": user_id
                }
            )
    except Exception as e:
        logger.error(f"处理失败: {e}")

    return {"code": 0, "msg": "success"}

@app.get('/')
def index():
    return "<h1>Agent桥梁已接通！</h1><p>请在飞书后台配置地址：/webhook</p>"
