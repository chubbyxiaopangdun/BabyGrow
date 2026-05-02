# BabyGrow · 技术开发文档

> 更新日期：2026-05-01 | 状态：定稿
> 用途：研发团队技术实现参考

---

## 一、技术架构总览

### 1.1 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        客户端层                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  iOS App     │  │ Android App │  │  Web App     │        │
│  │  (Swift)     │  │ (Kotlin)    │  │ (React)      │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
└─────────┼────────────────┼────────────────┼─────────────────┘
          │                │                │
          └────────────────┼────────────────┘
                           │ HTTPS
┌──────────────────────────┼──────────────────────────────────┐
│                        API 层                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    Nginx 反向代理                     │   │
│  └──────────────────────────┬───────────────────────────┘   │
│                              │                               │
│  ┌──────────────────────────┼───────────────────────────┐   │
│  │              FastAPI (Python)                        │   │
│  │  - 认证授权  - 请求路由  - 参数校验  - 限流           │   │
│  └──────────────────────────┬───────────────────────────┘   │
└─────────────────────────────┼───────────────────────────────┘
                              │
┌─────────────────────────────┼───────────────────────────────┐
│                        业务层                                │
│  ┌──────────────────────────┼───────────────────────────┐   │
│  │              LangGraph StateGraph                    │   │
│  │                                                      │   │
│  │  [Triage] → [Expert Agents] → [Safety] → [Reply]   │   │
│  └──────────────────────────┬───────────────────────────┘   │
│                              │                               │
│  ┌──────────────┐  ┌───────┴───────┐  ┌──────────────┐    │
│  │  LLM Service │  │  Tool Service │  │  RAG Service  │    │
│  │  (Qwen/GLM)  │  │  (外部API)    │  │  (知识库)     │    │
│  └──────────────┘  └───────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────┼───────────────────────────────┐
│                        数据层                                │
│  ┌──────────────┐  ┌───────┴───────┐  ┌──────────────┐    │
│  │  PostgreSQL  │  │    Redis      │  │    Milvus     │    │
│  │  (业务数据)   │  │  (缓存/会话)  │  │  (向量数据库) │    │
│  └──────────────┘  └───────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 技术选型

| 层级 | 技术 | 版本 | 说明 |
|------|------|------|------|
| **前端** | React Native | 0.73+ | 跨平台 |
| **后端** | Python + FastAPI | 3.11+ / 0.109+ | 高性能异步 |
| **Agent框架** | LangGraph | 0.2+ | 多Agent编排 |
| **LLM** | Qwen-2.5-72B | - | 主力模型 |
| **轻量LLM** | Qwen-2.5-7B | - | 分类/简单任务 |
| **向量数据库** | Milvus | 2.3+ | 知识库检索 |
| **关系数据库** | PostgreSQL | 16+ | 业务数据 |
| **缓存** | Redis | 7+ | 会话/缓存 |
| **对象存储** | 阿里云 OSS | - | 图片/视频 |
| **消息队列** | RabbitMQ | - | 异步任务 |

---

## 二、多 Agent 实现

### 2.1 Agent 架构（LangGraph）

```python
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode

# 定义状态
class BabyGrowState(MessagesState):
    child_profile: dict        # 宝宝档案
    route: str                 # 路由目标
    agent_responses: list      # 多Agent响应
    safety_check: bool         # 安全审核结果

# 调度Agent
def triage_agent(state: BabyGrowState):
    """分类问题并决定路由"""
    message = state["messages"][-1]
    classification = classify_question(message.content)
    return {"route": classification}

# 营养专家Agent
def nutrition_agent(state: BabyGrowState):
    """处理营养/辅食相关问题"""
    child = state["child_profile"]
    message = state["messages"][-1]
    
    # 加载营养知识库
    knowledge = load_nutrition_knowledge(child["age_months"])
    
    # 生成个性化建议
    response = generate_nutrition_advice(
        question=message.content,
        child_profile=child,
        knowledge=knowledge
    )
    return {"messages": [response]}

# 睡眠顾问Agent
def sleep_agent(state: BabyGrowState):
    """处理睡眠相关问题"""
    # 类似营养专家的实现
    pass

# 日程管理Agent
def schedule_agent(state: BabyGrowState):
    """生成/查询日程SOP"""
    child = state["child_profile"]
    city = child.get("city", "杭州")
    
    # 生成日程
    schedule = generate_daily_schedule(
        age_months=child["age_months"],
        city=city,
        preferences=child.get("preferences", {})
    )
    return {"schedule": schedule}

# 安全审核Agent
def safety_agent(state: BabyGrowState):
    """审核所有输出的安全性"""
    response = state["messages"][-1]
    is_safe = check_safety(response.content)
    
    if not is_safe:
        # 添加安全免责声明
        response.content = add_safety_disclaimer(response.content)
    
    return {"safety_check": is_safe}

# 构建状态图
graph = StateGraph(BabyGrowState)

# 添加节点
graph.add_node("triage", triage_agent)
graph.add_node("nutrition", nutrition_agent)
graph.add_node("sleep", sleep_agent)
graph.add_node("schedule", schedule_agent)
graph.add_node("development", development_agent)
graph.add_node("health", health_agent)
graph.add_node("city_service", city_service_agent)
graph.add_node("safety", safety_agent)
graph.add_node("synthesis", synthesis_agent)

# 定义路由
graph.add_edge(START, "triage")
graph.add_conditional_edges(
    "triage",
    lambda state: state["route"],
    {
        "nutrition": "nutrition",
        "sleep": "sleep",
        "schedule": "schedule",
        "development": "development",
        "health": "health",
        "city_service": "city_service",
        "general": "synthesis",
    }
)

# 所有专家Agent都流向安全审核
for agent in ["nutrition", "sleep", "schedule", "development", "health", "city_service"]:
    graph.add_edge(agent, "safety")

graph.add_edge("safety", "synthesis")
graph.add_edge("synthesis", END)

# 编译
app = graph.compile()
```

### 2.2 Agent Prompt 模板

```python
NUTRITION_AGENT_PROMPT = """你是一位专业的婴幼儿营养顾问。

## 宝宝信息
- 姓名: {child_name}
- 月龄: {age_months}个月
- 体重: {weight}kg
- 喂养方式: {feeding_type}
- 过敏史: {allergies}

## 你的职责
1. 根据宝宝月龄和体重，提供个性化的辅食建议
2. 避免过敏食物
3. 确保营养均衡
4. 给出具体的做法和用量

## 回复格式
- 使用结构化卡片
- 包含宝宝名字
- 给出具体可执行的建议
- 末尾添加必要的安全提示
"""
```

### 2.3 知识库（RAG）

```python
# 知识库结构
knowledge_base = {
    "nutrition": {
        "source": "中国居民膳食指南（婴幼儿部分）",
        "chunks": [...],  # 文本分块
        "embeddings": [...]  # 向量化
    },
    "sleep": {
        "source": "AAP睡眠指南",
        "chunks": [...],
        "embeddings": [...]
    },
    "development": {
        "source": "Denver发育筛查量表",
        "chunks": [...],
        "embeddings": [...]
    },
    "health": {
        "source": "常见儿科疾病指南",
        "chunks": [...],
        "embeddings": [...]
    }
}

# RAG检索
def retrieve_knowledge(query: str, domain: str, top_k: int = 3):
    """检索相关知识"""
    query_embedding = embed(query)
    results = milvus_client.search(
        collection=domain,
        data=[query_embedding],
        limit=top_k
    )
    return [r.entity.get("text") for r in results]
```

---

## 三、API 实现

### 3.1 FastAPI 路由

```python
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI(title="BabyGrow API", version="1.0.0")

# 宝宝档案
@app.post("/api/v1/children")
async def create_child(child: ChildCreate, user = Depends(get_current_user)):
    """创建宝宝档案"""
    db_child = await child_service.create(child, user.id)
    return {"id": db_child.id, "name": db_child.name}

@app.get("/api/v1/children")
async def list_children(user = Depends(get_current_user)):
    """获取宝宝列表"""
    children = await child_service.list_by_user(user.id)
    return {"children": children}

# AI对话
@app.post("/api/v1/chat")
async def chat(message: ChatMessage, user = Depends(get_current_user)):
    """发送消息"""
    # 获取宝宝档案
    child = await child_service.get(message.child_id)
    
    # 调用Agent
    result = await agent_app.ainvoke({
        "messages": [{"role": "user", "content": message.content}],
        "child_profile": child.to_dict()
    })
    
    # 保存对话
    await chat_service.save(message.child_id, "user", message.content)
    await chat_service.save(message.child_id, "assistant", result["messages"][-1].content)
    
    return {"reply": result["messages"][-1].content}

# 日程管理
@app.post("/api/v1/schedule/generate")
async def generate_schedule(request: ScheduleRequest, user = Depends(get_current_user)):
    """生成日程"""
    child = await child_service.get(request.child_id)
    schedule = await schedule_service.generate(child, request.date)
    return {"schedule": schedule}

# 辅食食谱
@app.post("/api/v1/recipe/generate")
async def generate_recipe(request: RecipeRequest, user = Depends(get_current_user)):
    """生成食谱"""
    child = await child_service.get(request.child_id)
    recipe = await recipe_service.generate(child, request.week_start)
    return {"recipe": recipe}
```

### 3.2 数据库操作

```python
# SQLAlchemy 模型
from sqlalchemy import Column, String, Date, Float, JSON, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Child(Base):
    __tablename__ = "children"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String(20), nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    feeding_type = Column(String(10), nullable=False)
    weight = Column(Float)
    height = Column(Float)
    allergies = Column(JSON, default=[])
    medical_history = Column(JSON, default=[])
    created_at = Column(TIMESTAMP, server_default="now()")
    updated_at = Column(TIMESTAMP, server_default="now()")
```

---

## 四、部署架构

### 4.1 云服务（阿里云）

```
┌─────────────────────────────────────────────────┐
│                  阿里云                          │
│                                                  │
│  ┌──────────────┐  ┌──────────────┐            │
│  │  ECS (2台)    │  │  RDS (PostgreSQL) │       │
│  │  - API服务    │  │  - 业务数据       │       │
│  │  - Agent服务  │  │                  │       │
│  └──────────────┘  └──────────────┘            │
│                                                  │
│  ┌──────────────┐  ┌──────────────┐            │
│  │  Redis        │  │  Milvus       │            │
│  │  - 缓存       │  │  - 向量数据    │            │
│  │  - 会话       │  │              │            │
│  └──────────────┘  └──────────────┘            │
│                                                  │
│  ┌──────────────┐  ┌──────────────┐            │
│  │  OSS          │  │  SLB          │            │
│  │  - 图片/视频  │  │  - 负载均衡    │            │
│  └──────────────┘  └──────────────┘            │
│                                                  │
│  ┌──────────────┐                               │
│  │  百炼/Qwen   │                               │
│  │  - LLM API   │                               │
│  └──────────────┘                               │
└─────────────────────────────────────────────────┘
```

### 4.2 CI/CD

```yaml
# .github/workflows/deploy.yml
name: Deploy BabyGrow

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: pytest tests/
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to ECS
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.ECS_HOST }}
          username: ${{ secrets.ECS_USER }}
          key: ${{ secrets.ECS_KEY }}
          script: |
            cd /opt/babygrow
            git pull
            pip install -r requirements.txt
            systemctl restart babygrow-api
```

---

## 五、监控与日志

### 5.1 监控指标

| 指标 | 告警阈值 | 说明 |
|------|---------|------|
| API 响应时间 | > 3s | P99 延迟 |
| LLM 响应时间 | > 10s | 首字时间 |
| 错误率 | > 1% | 5xx 错误 |
| CPU 使用率 | > 80% | 服务器负载 |
| 内存使用率 | > 85% | 服务器负载 |
| 数据库连接数 | > 80% | 连接池 |

### 5.2 日志规范

```python
import logging

logger = logging.getLogger("babygrow")

# 请求日志
logger.info(f"chat_request | child_id={child_id} | user_id={user_id}")

# Agent日志
logger.info(f"agent_routing | question_type={route} | agent={agent_name}")

# 性能日志
logger.info(f"llm_response | model={model} | latency={latency_ms}ms")
```

---

## 六、安全规范

| 安全项 | 措施 |
|--------|------|
| 数据加密 | HTTPS + 数据库字段加密 |
| 认证授权 | JWT Token + 权限控制 |
| 输入校验 | Pydantic 模型校验 |
| SQL注入 | SQLAlchemy ORM |
| XSS攻击 | 前端转义 + 后端校验 |
| 限流 | Redis + 令牌桶算法 |
| 医疗安全 | Agent输出必须经过安全审核 |

---

> 本文档为研发团队技术实现参考。
