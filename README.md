# BabyGrow - AI育儿助手

> 每个家庭的专属AI育儿顾问，开源、本地部署、个性化。

## 一句话定位

**BabyGrow** — 0-12岁儿童家庭专属AI育儿顾问，通过自然对话和移动Web双入口，把养孩子的所有细节SOP化、自动化、个性化，让新手爸妈养娃不焦虑、不迷茫。

## 核心特性

- 🤖 **AI驱动** — 不是信息展示，是能对话、会思考的育儿顾问
- 📱 **移动Web** — 部署后在手机浏览器直接使用，单手操作友好
- 🔒 **本地部署** — 所有数据存在本地，不上传任何儿童信息
- 🔌 **Agent集成** — 可被AI Agent调用，封装成独立Skill
- 🌐 **开源开放** — MIT协议，代码公开，可审计、可定制

## 快速开始

### 方式一：Docker一键部署（推荐）

```bash
git clone https://github.com/yourname/babygrow.git
cd babygrow
docker-compose up -d
# 浏览器打开 http://localhost:8765
```

### 方式二：本地运行

```bash
cd backend
pip install -r requirements.txt
python main.py
# 浏览器打开 http://localhost:8765
```

### 方式三：纯前端（无需后端）

```bash
# 直接用浏览器打开 web/index.html
# 数据会保存在浏览器 localStorage 中
```

## 使用场景

### 场景1：AI对话

```
用户：今天豆豆怎么安排？
Agent：
┌──────────────────────────────────┐
│  👶 豆豆（1岁1个月）今日计划      │
│  📅 2026-04-21                  │
├──────────────────────────────────┤
│  07:00 起床 + 喝奶（180ml）      │
│  08:00 早餐：南瓜小米粥          │
│  09:30 上午小睡（~1小时）        │
│  ...                             │
└──────────────────────────────────┘
```

### 场景2：移动Web查看

部署后在手机浏览器打开，查看今日计划、记录数据、看里程碑。

## 目标用户

- 🎯 **独自带娃的新手爸妈**（Primary）
- 🎯 **双职工家庭的主要照看人**
- 🎯 **家有0-12岁幼儿，想科学喂养的家长**
- 🎯 **AI Agent开发者**（集成育儿Skill）

## 四个核心关键词

| 关键词 | 含义 |
|--------|------|
| **开源** | 代码公开，可审计、可定制 |
| **本地** | 数据不出设备，隐私安全 |
| **AI驱动** | 不是信息展示，是能对话的顾问 |
| **个性化** | 每个孩子定制方案，不是通用建议 |

## 产品路线图

```
v0.1  MVP骨架（目录/Docker/FastAPI）
v0.2  记录功能（喂养/睡眠/健康）
v0.3  AI核心（计划生成/对话引擎）
v0.4  辅食+里程碑（0-3岁核心功能）
v1.0  第一个可用版本
v1.x  睡眠分析/哄睡助手/周末计划
v2.0  6-12岁扩展（学习管理/行为习惯）
```

## 技术栈

| 组件 | 技术选型 |
|------|----------|
| 前端 | 纯HTML5 + CSS3 + Vanilla JS |
| 后端 | Python 3.10+ + FastAPI |
| 数据库 | SQLite（本地文件） |
| AI | MiniMax / StepFun / Ollama（可插拔）|
| 部署 | Docker + docker-compose |

## 项目结构

```
babygrow/
├── README.md
├── LICENSE (MIT)
├── docker-compose.yml
├── backend/
│   ├── main.py
│   ├── routers/       # API路由
│   ├── services/      # 业务逻辑
│   ├── models/        # 数据模型
│   └── knowledge/     # 育儿知识库
├── web/
│   └── index.html     # 移动Web入口
└── skill/
    └── prompts/       # Agent Skill模板
```

## 鸣谢

- WHO 儿童生长标准
- 中国营养学会
- 美国儿科学会（AAP）
- 所有开源贡献者

## License

MIT License - 可商用、可修改、可分发，无需告知
