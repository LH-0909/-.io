# main.py
"""渔瞳 · AquaVision 应用入口"""

import logging
from utils import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

from app import create_app
from app.websocket import socketio, start_background_tasks
from config import AppConfig
from core.wqi.predictor import HAS_SKLEARN

app = create_app()

if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("渔瞳 · AquaVision 启动中...")
    logger.info(f"  - sklearn 可用: {HAS_SKLEARN}")
    logger.info(f"  - 数据库: {AppConfig.DATABASE}")
    logger.info(f"  - WebSocket: 已启用")
    logger.info(f"  - 访问地址: http://0.0.0.0:5000")
    logger.info("=" * 50)
    start_background_tasks(app)
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
