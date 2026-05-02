# BabyGrow MVP 开发计划

> 生成日期：2026-05-01 | 目标：开发到可运行的 MVP 版本
> 基于：6份产品文档 + 现有代码库审计

---

## 一、现状审计

### ✅ 已完成（可复用）
| 模块 | 状态 | 说明 |
|------|------|------|
| 后端框架 | ✅ 完整 | FastAPI + SQLite, 8个router, 端口8765 |
| 宝宝档案 CRUD | ✅ 完整 | children router, 前端 onboarding + profile 页 |
| 喂养记录 | ✅ 完整 | feeds router, 前端记录+列表+弹窗 |
| 睡眠记录 | ✅ 完整 | sleeps router, 前端记录+列表+弹窗 |
| 健康记录 | ✅ 完整 | health router (身高/体重/体温/疫苗) |
| 发育里程碑 | ✅ 完整 | milestones router, 前端打勾+分类进度 |
| 日程生成(基础) | ✅ 基础 | planner service + skill router, 模板式生成 |
| 食谱(基础) | ✅ 基础 | recipes router |
| AI 对话 | ✅ 基础 | 单模型 passthrough, 支持 MiniMax/StepFun/Ollama |
| 知识库(基础) | ✅ 基础 | knowledge_service.py |
| 前端 UI | ✅ 完整 | 3600行 SPA, 色彩/动画/PWA 就绪 |

### ❌ MVP 缺失（需要开发）
| 模块 | 优先级 | 缺失内容 |
|------|--------|---------|
| 多 Agent 路由系统 | P0 | 无 Triage → Expert 路由, 单一模型回答所有问题 |
| 结构化卡片回复 | P0 | AI 返回纯文本, 无卡片/标题/操作按钮 |
| 安全审核层 | P0 | 无医疗免责声明自动注入 |
| 7天个性化食谱 | P0 | 需要按月龄+过敏+营养生成完整一周 |
| 采购清单生成 | P1 | 无从食谱→食材→购买渠道的链路 |
| 城市化遛娃 | P2 | 完全新功能 |
| 前端 Chat 增强 | P0 | 无 Agent 指示器、无卡片渲染、无快捷问题 |
| 会话历史持久化 | P1 | 当前 chat 无上下文保存 |

---

## 二、MVP 范围定义

**MVP = 能让一个新手妈妈打开 App → 创建宝宝档案 → 和 AI 聊育儿问题 → 看到个性化日程 → 获取7天食谱**

### MVP 功能清单
| # | 功能 | 优先级 | 开发量 |
|---|------|--------|--------|
| F1 | 多 Agent 路由（Triage → 4个专家Agent） | P0 | 🔴 大 |
| F2 | 结构化卡片回复渲染 | P0 | 🟡 中 |
| F3 | 安全审核层 | P0 | 🟢 小 |
| F4 | 前端 Chat 增强（快捷问题+卡片+Agent指示） | P0 | 🟡 中 |
| F5 | 7天个性化食谱生成 | P0 | 🟡 中 |
| F6 | 采购清单自动生成 | P1 | 🟢 小 |
| F7 | 日程 SOP 增强（天气+更细时间线） | P1 | 🟡 中 |
| F8 | 会话历史持久化 | P1 | 🟢 小 |

---

## 三、分阶段执行计划

### Phase 1: 多 Agent 路由系统（核心引擎）🔴
**时间：Day 1-3**
**目标：后端实现 Triage → Expert Agent 路由**

#### 任务 1.1: Agent 路由框架
- **文件**: 新建 `backend/services/agent_router.py`
- **做什么**:
  - 实现 `triage_agent()`: 用 LLM 或关键词分类用户问题 → 路由到对应 Expert
  - 路由类别: `nutrition` / `sleep` / `schedule` / `health` / `general`
  - 不引入 LangGraph（MVP 阶段过度工程化），用简单的 if/else + LLM 分类
- **代码骨架**:
  ```python
  class AgentRouter:
      async def route(self, message: str, child_profile: dict) -> str:
          # 快速关键词匹配（0延迟）
          if any(k in message for k in ['辅食','吃什么','食谱','奶量']):
              return 'nutrition'
          if any(k in message for k in ['睡觉','夜醒','哄睡']):
              return 'sleep'
          # 兜底: LLM 分类
          ...
  ```

#### 任务 1.2: 专家 Agent Prompt 模板
- **文件**: 新建 `backend/services/agents/` 目录
  - `nutrition_agent.py` — 营养专家 Prompt + 食谱生成逻辑
  - `sleep_agent.py` — 睡眠顾问 Prompt + 睡眠分析
  - `schedule_agent.py` — 日程管理专家 Prompt + SOP 生成
  - `health_agent.py` — 健康顾问 Prompt + 症状分级
- **每个 Agent 做什么**:
  - 接收: 用户消息 + 宝宝档案 + 相关记录
  - 输出: 结构化 JSON `{title, subtitle, content, actions[], disclaimer}`
  - Prompt 中注入宝宝姓名/月龄/过敏/体重等个性化信息

#### 任务 1.3: 安全审核层
- **文件**: 新建 `backend/services/safety_review.py`
- **做什么**:
  - 关键词检测: 发烧/咳嗽/用药/呕吐/腹泻 → 自动追加免责声明
  - 规则: "以上建议仅供参考，具体情况请咨询儿科医生"
  - 严重症状: "建议尽快就医"

#### 任务 1.4: 重构 Chat API
- **文件**: 修改 `backend/main.py` 的 `/api/v1/chat`
- **改动**:
  ```
  旧: 直接调用 ai_service.chat(messages) → 返回纯文本
  新: 调用 AgentRouter.route() → 路由到 Expert Agent → 安全审核 → 返回结构化 JSON
  ```
- **新的 API 响应格式**:
  ```json
  {
    "reply": "Markdown 文本（兼容旧前端）",
    "card": {
      "title": "🍖 10月龄宝宝辅食建议",
      "subtitle": "针对豆豆的个性化推荐",
      "content": "## 今日推荐\n1. 南瓜小米粥\n2. 蒸蛋羹\n...",
      "actions": [{"label": "查看完整食谱", "type": "recipe"}],
      "disclaimer": null
    },
    "agent": "nutrition",
    "agent_name": "营养专家"
  }
  ```

**Phase 1 验收标准**:
- [ ] 发送"宝宝吃什么辅食好" → 路由到 nutrition agent
- [ ] 发送"宝宝夜醒频繁" → 路由到 sleep agent
- [ ] 回复包含宝宝名字、月龄等个性化信息
- [ ] 涉及疾病的问题自动附加免责声明
- [ ] API 返回结构化 card JSON

---

### Phase 2: 前端 Chat 增强 🟡
**时间：Day 4-5**
**目标：前端能渲染 Agent 结构化回复 + 快捷问题**

#### 任务 2.1: Chat 页面卡片渲染
- **文件**: 修改 `web/index.html` 的 chat 相关 JS
- **做什么**:
  - 解析 API 返回的 `card` 字段
  - 渲染卡片: 标题 + 副标题 + 内容(Markdown→HTML) + 操作按钮
  - Agent 指示器: 显示"正在由 营养专家 回答..."
  - 兼容: 无 card 字段时降级为纯文本气泡

#### 任务 2.2: 快捷问题
- **文件**: 修改 `web/index.html`
- **做什么**:
  - 首页/Chat 页显示 4 个快捷问题按钮
  - 根据宝宝月龄动态生成:
    - 6月龄: "今天辅食吃什么？" / "宝宝总是夜醒怎么办？"
    - 10月龄: "一周食谱推荐" / "今天怎么安排？"
  - 点击快捷问题 → 自动发送到 Chat

#### 任务 2.3: Markdown 渲染
- **文件**: 修改 `web/index.html`
- **做什么**:
  - 引入轻量 Markdown 渲染（~2KB，内联即可）
  - 支持: 标题/列表/加粗/emoji → 转 HTML
  - AI 回复中的 Markdown 正确显示

**Phase 2 验收标准**:
- [ ] AI 回复以卡片形式展示（标题+内容+按钮）
- [ ] 首页/Chat 显示 4 个快捷问题
- [ ] 点击快捷问题自动发送
- [ ] Markdown 内容正确渲染

---

### Phase 3: 7天食谱 + 采购清单 🟡
**时间：Day 6-7**
**目标：生成个性化一周食谱 + 自动采购清单**

#### 任务 3.1: 7天食谱生成服务
- **文件**: 修改 `backend/services/planner.py` 或新建 `backend/services/meal_planner.py`
- **做什么**:
  - 根据月龄生成 7 天 × 3 餐 + 加餐 的食谱
  - 考虑: 月龄适配(6月/8月/10月不同) + 过敏规避 + 营养均衡
  - 每道菜: 名称 + 做法 + 食材 + 用量
  - 输出: JSON 结构化数据

#### 任务 3.2: 采购清单 API
- **文件**: 新建路由或扩展 `backend/routers/recipes.py`
- **做什么**:
  - 从 7 天食谱自动提取所有食材
  - 合并重复食材、计算总用量
  - 按类别分组: 蔬菜/肉类/主食/调料/水果
  - 推荐购买渠道: 盒马/美团/菜市场

#### 任务 3.3: 食谱前端页面
- **文件**: 修改 `web/index.html`
- **做什么**:
  - 新增"食谱"Tab 或页面
  - 7 天时间轴视图，每天显示 3 餐
  - 点击菜品 → 展开做法详情
  - 底部"生成采购清单"按钮 → 弹出清单列表

**Phase 3 验收标准**:
- [ ] 生成 7 天食谱，每天包含早/午/晚 + 加餐
- [ ] 食物适合当前月龄
- [ ] 自动排除过敏食物
- [ ] 采购清单按类别分组
- [ ] 前端可查看食谱和清单

---

### Phase 4: 日程 SOP 增强 + 会话持久化 🟢
**时间：Day 8-9**
**目标：完善日程 + 保存聊天记录**

#### 任务 4.1: 日程 SOP 增强
- **文件**: 修改 `backend/services/planner.py`
- **做什么**:
  - 每个时间段包含具体操作步骤（不仅是标题）
  - 天气联动: 晴天→户外活动, 雨天→室内活动
  - 基于宝宝已有记录动态调整（如已喂过奶则跳过）
  - 前端时间轴 UI 优化

#### 任务 4.2: 会话历史持久化
- **文件**: 新建 `backend/models/chat_history.py` + 新路由
- **做什么**:
  - SQLite 存储: child_id + role + content + agent + timestamp
  - API: `GET /api/v1/children/{id}/chats` 获取历史
  - 前端: Chat 页加载历史消息
  - 保留最近 50 条对话上下文给 Agent

#### 任务 4.3: 前端整体打磨
- **做什么**:
  - Loading 状态优化（AI 思考时显示呼吸动画）
  - 错误处理完善（网络断开、API 超时）
  - 页面切换动画优化
  - PWA manifest 完善

**Phase 4 验收标准**:
- [ ] 日程包含详细操作步骤
- [ ] 天气影响户外/室内活动
- [ ] 聊天记录关闭后重新打开不丢失
- [ ] AI 思考时有加载动画

---

### Phase 5: 集成测试 + 上线准备 🔧
**时间：Day 10**
**目标：全链路测试 + 部署准备**

#### 任务 5.1: 全链路测试
- [ ] 新用户首次使用: Welcome → 创建宝宝 → 进入首页
- [ ] AI 对话: 问 5 个不同类型问题 → 验证路由正确
- [ ] 日程: 生成今日日程 → 验证 SOP 详情
- [ ] 食谱: 生成 7 天食谱 → 验证月龄适配
- [ ] 采购: 从食谱生成清单 → 验证分类
- [ ] 记录: 添加喂养/睡眠记录 → 验证显示
- [ ] 里程碑: 打勾 → 验证进度更新

#### 任务 5.2: 部署准备
- requirements.txt 更新（添加新依赖）
- .env 配置文档
- 启动脚本 `start.sh`
- README 更新

---

## 四、文件变更清单

### 新建文件
```
backend/services/agent_router.py        # Agent 路由核心
backend/services/safety_review.py       # 安全审核
backend/services/agents/__init__.py     # Agent 包
backend/services/agents/nutrition.py    # 营养专家 Agent
backend/services/agents/sleep.py        # 睡眠顾问 Agent
backend/services/agents/schedule.py     # 日程管理 Agent
backend/services/agents/health.py       # 健康顾问 Agent
backend/services/meal_planner.py        # 7天食谱生成
backend/models/chat_history.py          # 聊天记录模型
backend/routers/chat.py                 # Chat 路由（从 main.py 提取）
```

### 修改文件
```
backend/main.py                         # 重构 chat handler → 使用 AgentRouter
backend/routers/recipes.py              # 扩展: 7天食谱 + 采购清单 API
backend/services/planner.py             # 增强: SOP 详情 + 天气联动
web/index.html                          # Chat 增强 + 食谱页 + Markdown 渲染
```

---

## 五、技术决策

| 决策 | 选择 | 理由 |
|------|------|------|
| Agent 编排 | 简单路由（不用 LangGraph） | MVP 阶段, LangGraph 过重, 后续可迁移 |
| LLM 分类 | 关键词优先 + LLM 兜底 | 0延迟分类常见问题, 减少 API 调用 |
| Markdown 渲染 | 内联轻量解析 (~2KB) | 不引入 marked.js 等库, 保持轻量 |
| 数据库 | SQLite (已有) | MVP 够用, 后续迁移 PostgreSQL |
| 会话存储 | SQLite chat_history 表 | 简单可靠, 不引入 Redis |
| 结构化回复 | JSON card 字段 + 兼容纯文本 | 渐进增强, 不破坏现有前端 |

---

## 六、风险与应对

| 风险 | 概率 | 应对 |
|------|------|------|
| LLM 分类准确率不高 | 中 | 关键词规则覆盖 80% 场景, LLM 只处理模糊问题 |
| AI 响应慢(>3s) | 低 | 用 StepFun fast 模型, 流式响应备选 |
| 食谱质量不高 | 中 | 预置高质量模板 + LLM 微调 |
| 前端改动量大 | 低 | 渐进增强, card 渲染是增量不破坏现有 |

---

## 七、里程碑

| 里程碑 | 日期 | 交付 |
|--------|------|------|
| M1: Agent 引擎就绪 | Day 3 | 后端多 Agent 路由可运行 |
| M2: Chat 体验升级 | Day 5 | 前端卡片渲染 + 快捷问题 |
| M3: 食谱系统完成 | Day 7 | 7天食谱 + 采购清单 |
| M4: 全功能联调 | Day 9 | 日程增强 + 历史持久化 |
| M5: MVP 发布 | Day 10 | 全链路测试通过, 可部署 |
