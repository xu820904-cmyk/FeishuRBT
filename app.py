import os
import logging
from bottle import Bottle, run, default_app
# 确保导入了你定义路由的文件
# 如果你的 setup_routes 在另一个文件，请确保 import 它
# from routes import setup_routes 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = default_app()

# --- 关键：把这里的 # 号全部去掉，让它们干活！ ---
try:
    # init_database()
    # init_static_dir()
    
    # 这一行最重要！它负责接通飞书的 /webhook 路径
    setup_routes() 
    
    logger.info("飞书机器人路由已成功挂载")
except Exception as e:
    logger.error(f"路由挂载失败: {e}")

# --- 加一个首页，防止看到 404 ---
@app.get('/')
def index():
    return "<h1>机器人已上线！</h1><p>请在飞书后台配置回调地址为：/webhook</p>"

# 保持简洁，不要加 app.run
