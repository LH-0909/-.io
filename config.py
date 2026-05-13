# config.py
"""
全局配置常量，避免硬编码
"""
import os

class AppConfig:
    # ---------- 主题配色 ----------
    BG_COLOR = '#0f172a'
    TEXT_COLOR = 'white'
    SPINE_COLOR = '#334155'
    TICK_COLOR = 'white'
    HIGHLIGHT_COLOR = '#22d3ee'
    WARNING_COLOR = '#ef4444'

    # ---------- 仪表盘 ----------
    GAUGE_WIDTH = 280
    GAUGE_HEIGHT = 320

    # ---------- 路径 ----------
    MODEL_DIR = 'models'
    CONFIG_FILE = 'config.json'
    DATABASE = 'monitor_data.db'

    # ---------- 预测模型 ----------
    LOOKBACK = 12               # LSTM 滑动窗口长度
    DEFAULT_SPECIES = '大黄鱼'

    # ---------- AI 助手 ----------
    DEEPSEEK_API_KEY_ENV = 'DEEPSEEK_API_KEY'
    DEEPSEEK_BASE_URL = 'https://api.deepseek.com/v1'

    # ---------- 数据阈值默认值（仅限 UI 初始值，真实阈值从 config.json 加载）----------
    DEFAULT_THRESHOLDS = {
        'ph_min': 6.0, 'ph_max': 9.0,
        'temp_min': 20.0, 'temp_max': 25.0,
        'sal_min': 25.0, 'sal_max': 45.0,
        'do_min': 5.0, 'do_max': 12.0,
        'chl_max': 20.0,
        'turb_max': 15.0
    }