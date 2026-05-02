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
import json
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
    # SQLite migration: 添加新列（如果不存在）
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # 检查 conversation_history 表是否有 agent 列
        cursor.execute("PRAGMA table_info(conversation_history)")
        columns = [row[1] for row in cursor.fetchall()]
        if 'agent' not in columns:
            cursor.execute("ALTER TABLE conversation_history ADD COLUMN agent TEXT")
            print("✅ 添加列: conversation_history.agent")
        if 'card_json' not in columns:
            cursor.execute("ALTER TABLE conversation_history ADD COLUMN card_json TEXT")
            print("✅ 添加列: conversation_history.card_json")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ Migration警告: {e}")


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

@app.get("/api/v1/children/{child_id}/chats")
async def get_chat_history(child_id: str, limit: int = 50):
    """获取聊天历史"""
    from models.database import get_session, ConversationHistory
    session = get_session()
    try:
        records = session.query(ConversationHistory).filter(
            ConversationHistory.child_id == child_id
        ).order_by(ConversationHistory.created_at.desc()).limit(limit).all()
        records.reverse()  # 按时间正序
        return [
            {
                "id": r.id,
                "role": r.role,
                "content": r.content,
                "agent": r.agent,
                "card": json.loads(r.card_json) if r.card_json else None,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in records
        ]
    finally:
        session.close()


async def _chat_handler(data: dict):
    """共享聊天逻辑 — 使用多Agent路由"""
    import uuid
    import json as json_mod
    from datetime import datetime
    from models.database import get_session, Child, FeedRecord, SleepRecord, HealthRecord, ConversationHistory
    from services.agent_router import AgentRouter
    from models.utils import calc_age_months

    messages = data.get("messages", [])
    child_id = data.get("child_id")
    child_info = data.get("child_info", {})
    api_key = data.get("api_key")
    conversation_history = data.get("conversation_history", [])

    # 获取最新用户消息
    user_message = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            user_message = msg.get("content", "")
            break

    if not user_message:
        return {"reply": "请输入您的问题", "card": None, "agent": "general"}

    # 构建宝宝档案
    child_profile = child_info
    context_records = {"feeds": [], "sleeps": [], "health": [], "weather": "晴"}

    if child_id:
        session = get_session()
        try:
            child = session.query(Child).filter(Child.id == child_id).first()
            if child:
                age_months = calc_age_months(child.birth_date)
                allergies_raw = child.allergies or "[]"
                try:
                    allergies = json_mod.loads(allergies_raw) if isinstance(allergies_raw, str) else allergies_raw
                except:
                    allergies = []
                child_profile = {
                    "name": child.name,
                    "age_months": age_months,
                    "feeding": child.notes or "混合喂养",
                    "weight": child.birth_weight,
                    "allergies": ", ".join(allergies) if allergies else "无",
                    "location": child.location or "杭州",
                    "gender": child.gender.value if child.gender else "male",
                }

                # 获取今日记录
                from datetime import date, timedelta
                today = date.today()
                today_start = datetime.combine(today, datetime.min.time())
                today_end = datetime.combine(today + timedelta(days=1), datetime.min.time())

                feeds = session.query(FeedRecord).filter(
                    FeedRecord.child_id == child_id,
                    FeedRecord.time >= today_start,
                    FeedRecord.time < today_end,
                ).all()
                context_records["feeds"] = [
                    {"type": f.type.value, "food_name": f.food_name, "amount": f.amount,
                     "unit": f.unit, "time": f.time.isoformat() if f.time else None}
                    for f in feeds
                ]

                sleeps = session.query(SleepRecord).filter(
                    SleepRecord.child_id == child_id,
                    SleepRecord.start_time >= today_start,
                    SleepRecord.start_time < today_end,
                ).all()
                context_records["sleeps"] = [
                    {"type": s.type.value, "start_time": s.start_time.isoformat() if s.start_time else None,
                     "end_time": s.end_time.isoformat() if s.end_time else None,
                     "quality": s.quality, "night_wakings": s.night_wakings}
                    for s in sleeps
                ]

                health_recs = session.query(HealthRecord).filter(
                    HealthRecord.child_id == child_id
                ).order_by(HealthRecord.date.desc()).limit(5).all()
                context_records["health"] = [
                    {"type": h.type.value, "value": h.value, "unit": h.unit,
                     "date": h.date.isoformat() if h.date else None}
                    for h in health_recs
                ]

                # 获取历史对话
                if not conversation_history:
                    hist_records = session.query(ConversationHistory).filter(
                        ConversationHistory.child_id == child_id
                    ).order_by(ConversationHistory.created_at.desc()).limit(10).all()
                    hist_records.reverse()
                    conversation_history = [
                        {"role": h.role, "content": h.content}
                        for h in hist_records
                    ]
        finally:
            session.close()

    # 使用用户自定义 API key
    from services.ai_service import ai_service
    original_key = None
    original_provider = None
    if api_key:
        original_key = ai_service.api_key
        original_provider = ai_service.provider
        ai_service.api_key = api_key
        ai_service.provider = "stepfun"

    try:
        # === 核心：使用 AgentRouter ===
        router = AgentRouter(ai_service)
        result = await router.route_and_respond(
            message=user_message,
            child_profile=child_profile,
            context_records=context_records,
            conversation_history=conversation_history,
        )

        # 保存对话记录
        if child_id:
            session = get_session()
            try:
                # 保存用户消息
                user_msg = ConversationHistory(
                    id=str(uuid.uuid4()),
                    child_id=child_id,
                    role="user",
                    content=user_message,
                )
                session.add(user_msg)
                # 保存 AI 回复
                ai_msg = ConversationHistory(
                    id=str(uuid.uuid4()),
                    child_id=child_id,
                    role="assistant",
                    content=result["reply"],
                    agent=result["agent"],
                    card_json=json_mod.dumps(result.get("card"), ensure_ascii=False) if result.get("card") else None,
                )
                session.add(ai_msg)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"保存聊天记录失败: {e}")
            finally:
                session.close()

        return result

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
