import os, logging, requests, json
from bottle import Bottle, request, response, default_app

logging.basicConfig(level=logging.INFO)
app = default_app()

@app.post('/webhook/')
def feishu_webhook():
    data = request.json
    # 1. 核心：秒回飞书的“开门挑战”，解决验证失败问题
    if data.get("type") == "url_verification":
        return {"challenge": data.get("challenge")}
    
    # 2. 核心：识别到用户消息，转手交给 Dify 的大脑
    try:
        if "header" in data and data["header"]["event_type"] == "im.message.receive_v1":
            content = json.loads(data["event"]["message"]["content"])
            user_query = content.get("text", "")
            user_id = data["event"]["sender"]["sender_id"]["open_id"]
            
            # 这一步就是把球传给 Dify
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
        logging.error(f"消息转发失败: {e}")

    return {"code": 0, "msg": "success"}

@app.get('/')
def index():
    return "<h1>Agent桥梁已接通！</h1><p>请在飞书后台配置地址：/webhook</p>"
