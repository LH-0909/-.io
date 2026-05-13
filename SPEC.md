# 渔瞳 · AquaVision 技术规范 v2.0

## 1. 目标与用户
- **学术场景**：水质预测模型实验、WQI评估对比、特征重要性分析、模型可解释性
- **生产场景**：养殖户实时监控、告警推送、AI诊断辅助决策
- **核心指标**：溶解氧预测 MAE < 0.5 mg/L (当前目标)，R² > 0.85

## 2. 项目结构 (重构后)
```
FishEye/
├── main.py                  # Flask 应用入口 + 蓝图注册
├── config.py                # 统一配置 (数据类)
├── requirements.txt
├── SPEC.md                  # 本文件
│
├── app/                     # Flask 应用层
│   ├── __init__.py          # create_app() 工厂
│   ├── routes/              # 按领域拆分路由
│   │   ├── dashboard.py     # /api/current, /api/history
│   │   ├── prediction.py    # /api/train, /api/forecast
│   │   ├── wqi.py           # /api/wqi/*
│   │   ├── alert.py         # /api/alert/*
│   │   ├── ai.py            # /api/ai
│   │   └── export.py        # /api/export, /api/import
│   └── middleware.py         # 错误处理、请求验证装饰器
│
├── core/                    # 核心算法 (无框架依赖)
│   ├── __init__.py
│   ├── xlstm.py             # xLSTM 网络定义 (原 model.py)
│   ├── forecasting/         # 预测模块
│   │   ├── hybrid_forecaster.py   # xLSTM+XGBoost 混合
│   │   ├── revin.py               # RevIN 归一化
│   │   └── feature_engineering.py # 特征工程 (时间特征、滞后特征、滚动统计)
│   ├── wqi/                 # WQI 模块
│   │   ├── calculator.py    # 公式计算
│   │   └── predictor.py     # Random Forest ML 预测
│   ├── anomaly/             # 异常检测
│   │   ├── bayesian_tracer.py    # 因果规则引擎
│   │   └── statistical.py        # 统计异常检测 (IQR, Z-score)
│   └── evaluation/          # 评估体系
│       ├── metrics.py       # 回归 + 分类指标
│       ├── backtest.py      # 回测框架
│       └── interpretability.py # SHAP/LIME 可解释性
│
├── services/                # 业务逻辑层
│   ├── simulator.py         # 传感器模拟器 (重命名)
│   ├── wqi_service.py
│   ├── alert_service.py
│   └── ai_assistant.py
│
├── data/                    # 数据层
│   ├── database.py          # SQLite 管理
│   └── repository.py        # 数据访问仓库模式
│
├── models/                  # 训练好的模型文件
├── templates/               # Jinja2 模板
└── static/                  # 前端资源
    ├── css/
    ├── js/
    │   ├── app.js           # 主入口
    │   ├── charts.js        # ECharts 封装
    │   ├── api.js           # API 请求封装
    │   └── components/      # UI 组件
    └── assets/
```

## 3. API 设计

### 3.1 实时数据
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/current` | 当前传感器读数 + WQI + 预测 + 异常 + 告警 |
| GET | `/api/history?minutes=60` | 历史时序数据 |

### 3.2 预测
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/train` | 训练溶解氧预测模型 |
| GET | `/api/forecast?hours=6` | 多步预测 (1h/3h/6h) |
| GET | `/api/model/info` | 模型元信息 |
| GET | `/api/model/importance` | 特征重要性 |

### 3.3 WQI
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/wqi/calculate` | 公式计算 (原 /api/wqi/formula) |
| POST | `/api/wqi/predict` | ML 预测 |
| POST | `/api/wqi/train` | 训练 WQI 模型 |
| GET | `/api/wqi/importance` | 特征重要性 |

### 3.4 异常告警
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/alert/rules` | 获取告警规则 |
| PUT | `/api/alert/rules` | 更新告警规则 |
| GET | `/api/anomaly/history?days=7` | 历史异常记录 |

### 3.5 AI 诊断
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/ai/diagnose` | 水质诊断 |
| POST | `/api/ai/predict` | 风险预测 |
| POST | `/api/ai/chat` | 自由对话 |

### 3.6 数据管理
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/import` | CSV 导入 |
| GET | `/api/export` | CSV 导出 |
| GET | `/api/health` | 健康检查 |

## 4. 算法改进路线图

### 4.1 短期 (当前迭代) — 提升预测精度
1. **特征工程增强**
   - 添加滞后特征 (t-1, t-2, t-3, t-24)
   - 添加滚动统计 (6h/24h 均值、标准差)
   - 添加昼夜节律编码 (sin/cos 变换替代 raw hour)
   - DO 变化率 (一阶差分)
   - 水体分层指标 (temp_surface - temp_bottom 的代理)

2. **模型架构改进**
   - xLSTM 增加残差连接 + LayerNorm
   - 调整 mLSTM 的 query/key 归一化方式
   - 增加 dropout 正则化 (当前无)
   - 学习率调度 (ReduceLROnPlateau)

3. **混合策略优化**
   - 当前：单权重加权 → 改进为动态权重 (根据预测置信度)
   - 使用 stacking ensemble (训练元学习器)
   - 对 XGBoost 做时序交叉验证 (TimeSeriesSplit)

4. **不确定性量化**
   - MC Dropout 替代当前的启发式 std
   - 提供预测区间而非单点估计

### 4.2 中期 — 模型可解释性
1. SHAP 分析 XGBoost 特征贡献
2. Integrated Gradients 分析 xLSTM
3. 特征重要性排序可视化
4. 预测结果溯源 (哪些历史时刻贡献了当前预测)

### 4.3 长期 — 全面评估体系
1. 多模型对比基准 (ARIMA, Prophet, GRU, Transformer)
2. 交叉验证策略 (按季节/年份分折)
3. 极端事件评估 (缺氧事件召回率)
4. 模型漂移检测

## 5. 前端增强

### 5.1 新增页面/组件
- **参数配置面板**：实时调整告警阈值、WQI权重
- **模型管理页**：查看模型列表、训练历史、指标对比
- **历史回放**：选择日期范围回放水质变化
- **对比视图**：多参数联动散点图 (如 DO vs Temp)
- **预测详情**：多步预测曲线 + 置信区间

### 5.2 交互增强
- WebSocket 推送替代轮询 (Flask-SocketIO)
- 响应式设计移动端适配
- 暗色/亮色主题切换
- 数据导出格式可选 (CSV/Excel/JSON)

## 6. 代码质量规范

### 6.1 命名约定
- 文件名：snake_case
- 类名：PascalCase
- 函数/变量：snake_case
- 私有方法：_leading_underscore
- 常量：UPPER_SNAKE_CASE

### 6.2 必须遵守
- 所有公共函数有类型注解
- API 返回统一格式 `{data, error, meta}`
- 数据库操作使用上下文管理器
- 模型输入输出做 shape 断言
- 关键路径记录 INFO 日志

### 6.3 禁止
- 裸 except
- print() 替代 logger
- 硬编码魔法数字
- model.py / models.py 命名混淆 (已重构)

## 7. 测试策略
- 单元测试：pytest，覆盖 core/ 模块
- 集成测试：API 端点 + 数据库
- 模型测试：合成数据验证训练/预测流程
- 前端测试：关键用户流程手动验证

## 8. 边界与约束
- Python 3.10+，Win/Linux 兼容
- PyTorch + XGBoost + scikit-learn 为核心依赖
- SQLite 单文件数据库，适合嵌入式部署
- DeepSeek API 为可选 AI 后端
- 不引入 Redis/消息队列 (保持轻量)
