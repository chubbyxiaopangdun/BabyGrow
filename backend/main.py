"""
BabyGrow - AI育儿助手 后端服务
FastAPI + SQLite，本地部署，数据自主
"""
import os
import sys

# 确保backend目录在path中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uvicorn

import config
from models.database import Base, make_engine as create_engine, init_db

# 创建FastAPI应用
app = FastAPI(
    title="BabyGrow API",
    description="AI育儿助手 - 每个家庭的专属育儿顾问",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本地部署，允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
db_path = os.path.join(os.path.dirname(__file__), config.DATABASE_PATH)
os.makedirs(os.path.dirname(db_path), exist_ok=True)

engine = create_engine(f"sqlite:///{db_path}")


@app.on_event("startup")
async def startup():
    """启动时初始化数据库"""
    init_db(engine)
    print(f"✅ 数据库初始化完成: {db_path}")


# 挂载前端静态文件
frontend_path = os.path.join(os.path.dirname(__file__), config.FRONTEND_PATH)
if os.path.exists(frontend_path):
    app.mount("/web", StaticFiles(directory=frontend_path, html=True), name="web")


# 注册路由
from routers import children, feeds, sleeps, health, plans, skill

app.include_router(children.router)
app.include_router(feeds.router)
app.include_router(sleeps.router)
app.include_router(health.router)
app.include_router(plans.router)
app.include_router(skill.router)


@app.get("/")
async def root():
    """根路径：重定向到前端"""
    frontend_index = os.path.join(frontend_path, "index.html")
    if os.path.exists(frontend_index):
        return RedirectResponse(url="/web/index.html")
    return {
        "name": "BabyGrow",
        "version": "0.1.0",
        "description": "AI育儿助手 - 每个家庭的专属育儿顾问",
        "docs": "/docs"
    }


@app.get("/api/v1/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "version": "0.1.0",
        "database": db_path
    }


if __name__ == "__main__":
    print(f"""
╔═══════════════════════════════════════════════════╗
║                                                   ║
║   👶 BabyGrow - AI育儿助手                       ║
║                                                   ║
║   本地育儿顾问，守护每个家庭                     ║
║                                                   ║
║   文档: http://localhost:{config.PORT}/docs       ║
║   前端: http://localhost:{config.PORT}/web        ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=config.DEBUG
    )
