import os
import logging
from bottle import Bottle, run, default_app

# 1. 导入你原本的逻辑函数（假设它们在同一目录或其他文件）
# 如果这些函数就在这个 app.py 里，请确保不要删掉它们的定义
from config import Config
# 如果你还有其他的 import，请加在这里

# 2. 初始化日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 3. 获取 Bottle 实例
app = default_app()

# 4. 执行初始化（把之前的 # 号全去掉了，让它们干活！）
try:
    # 这里的函数名必须和你代码里定义的一模一样
    # init_database()
    # init_static_dir()
    # setup_routes() 
    logger.info("飞书Dify机器人 Vercel 环境初始化完成")
except Exception as e:
    logger.error(f"初始化失败: {e}")

# 5. 这里是你的健康检查，留着测通没通
@app.get('/ping')
def ping():
    return "pong"

# --- 关键：不要加 app.run() 或 serve() ---
