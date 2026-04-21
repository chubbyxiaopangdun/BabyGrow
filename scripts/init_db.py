"""
BabyGrow 数据库初始化脚本
运行此脚本初始化SQLite数据库
"""
import os
import sys

# 添加backend到path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models.database import Base, create_engine_conn
import config

def init_database():
    """初始化数据库"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'backend', config.DATABASE_PATH)
    db_path = os.path.normpath(db_path)
    
    # 确保目录存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # 创建引擎
    engine = create_engine_conn(f"sqlite:///{db_path}")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    print(f"✅ 数据库初始化成功: {db_path}")
    print("✅ 已创建以下表:")
    for table in Base.metadata.tables:
        print(f"   - {table}")


if __name__ == "__main__":
    init_database()
