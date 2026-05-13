#!/bin/bash
# AutoDL 一键启动脚本
# 用法: bash setup_autodl.sh

echo "=== FishEye · AquaVision 环境安装 ==="

# 1. 安装依赖
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 2. 初始化数据库
python -c "
from app import create_app
app = create_app()
with app.app_context():
    from data.database import init_db
    init_db()
    print('Database initialized.')
"

# 3. 启动服务
echo "Starting FishEye on port 5000..."
python main.py
