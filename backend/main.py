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
from routers import children, feeds, sleeps, health, plans, skill, recipes, milestones
from services.ai_service import ai_service

app.include_router(children.router)
app.include_router(feeds.router)
app.include_router(sleeps.router)
app.include_router(health.router)
app.include_router(plans.router)
app.include_router(skill.router)
app.include_router(recipes.router)
app.include_router(milestones.router)

@app.post("/api/chat")
async def chat_proxy_legacy(data: dict):
    """AI聊天代理 - 兼容旧版前端路径 /api/chat"""
    return await _chat_handler(data)

@app.post("/api/v1/chat")
async def chat_proxy(data: dict):
    """AI聊天代理 - 解决浏览器CORS问题"""
    return await _chat_handler(data)


async def _chat_handler(data: dict):
    """共享聊天逻辑"""
    messages = data.get("messages", [])
    child_info = data.get("child_info", {})
    api_key = data.get("api_key")  # 用户自定义key

    # 构建系统提示词
    system_prompt = f"""你是BabyGrow，温暖的AI育儿顾问。宝宝信息：小名{child_info.get('name','宝宝')}，月龄{child_info.get('months',0)}个月，喂养{child_info.get('feeding','未知')}。请用友好、温暖的语气用中文回答。回答尽量用列表或卡片式，方便阅读。"""

    # 如果用户提供了key，临时覆盖
    original_key = None
    original_provider = None
    if api_key:
        original_key = ai_service.api_key
        original_provider = ai_service.provider
        ai_service.api_key = api_key
        ai_service.provider = "stepfun"  # 默认用stepfun格式

    try:
        result = await ai_service.chat(messages, system_prompt)
        return {"reply": result["content"]}
    finally:
        if original_key is not None:
            ai_service.api_key = original_key
            ai_service.provider = original_provider


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
