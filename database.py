# database.py — 已迁移到 data/database.py
# 此文件保留向后兼容，新代码请直接使用：
#   from data.database import DatabaseManager

import warnings

from data.database import DatabaseManager

warnings.warn(
    "database.py 已废弃，请改用 data.database",
    DeprecationWarning,
    stacklevel=2,
)
