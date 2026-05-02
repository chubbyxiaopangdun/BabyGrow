# BabyGrow · 产品需求文档（PRD）

> 更新日期：2026-05-01 | 状态：定稿
> 用途：研发开发参考，功能模块详细说明

---

## 一、产品概述

### 1.1 产品定位
AI 多 Agent 个性化育儿助手，替代小红书育儿攻略。

### 1.2 核心功能
1. 多 Agent 协作对话
2. 个性化日程管理
3. 辅食食谱推荐
4. 睡眠问题诊断
5. 发育里程碑追踪
6. 城市化遛娃推荐

---

## 二、功能模块详细说明

### 模块 1：宝宝档案

**功能描述：** 创建和管理宝宝个人信息，作为所有个性化推荐的基础。

**字段定义：**

| 字段 | 类型 | 必填 | 校验规则 |
|------|------|------|---------|
| 姓名 | String | ✅ | 2-20 字符 |
| 出生日期 | Date | ✅ | 不晚于今天 |
| 性别 | Enum | ✅ | male/female |
| 喂养方式 | Enum | ✅ | breast/formula/mixed |
| 体重(kg) | Float | ❌ | 0-50 |
| 身高(cm) | Float | ❌ | 0-150 |
| 过敏史 | Array | ❌ | 食物/药物列表 |
| 疾病史 | Array | ❌ | 疾病列表 |
| 疫苗记录 | Array | ❌ | 已接种疫苗 |

**交互流程：**
```
首次打开 → Welcome 引导页 → 填写宝宝信息 → 创建档案 → 进入首页
已有档案 → 直接进入首页
```

---

### 模块 2：AI 对话（多 Agent）

**功能描述：** 用户通过自然语言提问，系统调用多个专业 Agent 协作回答。

**Agent 路由规则：**

| 问题类型 | 关键词示例 | 路由到 |
|---------|-----------|--------|
| 营养/辅食 | 辅食、吃什么、食谱、奶量 | 营养专家 |
| 睡觉/睡眠 | 午睡、夜醒、哄睡、睡眠 | 睡眠顾问 |
| 日程/安排 | 一天安排、几点做什么、SOP | 日程管理专家 |
| 发育/里程碑 | 会不会站、发育、早教 | 发育专家 |
| 健康/生病 | 发烧、咳嗽、疫苗、生病 | 健康顾问 |
| 遛娃/外出 | 去哪玩、周末、遛娃 | 城市服务 |
| 综合/其他 | 以上都不匹配 | 调度中心直接回答 |

**回复格式规范：**
```
结构化卡片:
  - 标题（简洁明了）
  - 副标题（补充说明）
  - 内容区（分点/列表）
  - 操作按钮（如有）

个性化元素:
  - 宝宝名字（如"豆豆"）
  - 月龄（如"10个月"）
  - 体重（如"9.2kg"）
  - 过敏信息（如有）

安全提示:
  - 涉及医疗：末尾加"请咨询医生"
  - 涉及用药：末尾加"用药请遵医嘱"
  - 紧急情况：建议立即就医
```

---

### 模块 3：日程管理

**功能描述：** 根据宝宝月龄、习惯、城市生成个性化每日 SOP。

**日程数据结构：**
```json
{
  "date": "2026-05-02",
  "city": "杭州",
  "weather": "晴 22°C",
  "baby_age_months": 10,
  "schedule": [
    {
      "time": "07:00",
      "duration_min": 30,
      "category": "feeding",
      "title": "起床+喂奶",
      "sop": "母乳/配方奶180ml，换尿布",
      "tips": "闹钟提前5分钟准备奶瓶",
      "icon": "🍼"
    }
  ]
}
```

**日程分类：**

| 分类 | 图标 | 颜色 | 包含内容 |
|------|------|------|---------|
| 喂养 | 🍼 | peach | 母乳/配方奶/辅食 |
| 睡眠 | 😴 | sky | 午睡/夜间睡眠 |
| 活动 | 🧸 | mint | 户外/早教/亲子 |
| 清洁 | 🛁 | lavender | 洗澡/换衣/清洁 |
| 自由 | 🎮 | rose | 自由探索/玩耍 |

---

### 模块 4：辅食食谱

**功能描述：** 根据宝宝月龄、过敏情况、已有饮食习惯生成 7 天个性化食谱。

**食谱数据结构：**
```json
{
  "baby_id": "uuid",
  "week_start": "2026-05-02",
  "days": [
    {
      "date": "2026-05-02",
      "meals": [
        {
          "type": "breakfast",
          "time": "07:30",
          "name": "南瓜小米粥",
          "ingredients": ["南瓜", "小米", "米粉"],
          "amount": "80g",
          "steps": "南瓜蒸熟压泥，小米煮粥，拌入南瓜泥和米粉",
          "prep_time_min": 15,
          "cook_time_min": 20,
          "image": null
        }
      ]
    }
  ],
  "shopping_list": {
    "items": [
      {"name": "南瓜", "amount": "半个", "category": "蔬菜"},
      {"name": "小米", "amount": "500g", "category": "主食"}
    ],
    "platform": "盒马鲜生",
    "store": "滨江宝龙店"
  }
}
```

**食谱生成规则：**
1. 避免过敏食物
2. 每日营养均衡（主食+蔬菜+肉类+水果）
3. 月龄适配（如 10 月龄无整颗坚果）
4. 逐步引入新食物（每周 1-2 种新食物）
5. 考虑已有饮食习惯（如上周开始吃南瓜泥）

---

### 模块 5：睡眠管理

**功能描述：** 记录和分析宝宝睡眠数据，提供个性化睡眠建议。

**睡眠记录字段：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| 类型 | Enum | ✅ | nap/afternoon_nap/night |
| 开始时间 | DateTime | ✅ | 睡眠开始时间 |
| 结束时间 | DateTime | ✅ | 睡眠结束时间 |
| 备注 | String | ❌ | 自由备注 |

**AI 分析输出：**
- 睡眠质量评分（0-100）
- 平均时长
- 日均次数
- 夜醒次数
- 改善建议

---

### 模块 6：发育里程碑

**功能描述：** 追踪宝宝发育进度，提供个性化早教建议。

**里程碑数据结构：**
```json
{
  "categories": [
    {
      "name": "大运动",
      "icon": "🏃",
      "milestones": [
        {"text": "扶站", "done": true},
        {"text": "独坐稳定", "done": true},
        {"text": "独站片刻", "done": false},
        {"text": "扶走", "done": false}
      ]
    }
  ]
}
```

**发育评估标准：**
- 参考 Denver 发育筛查量表
- 参考中国儿童发育里程碑标准
- 按月龄区间划分（0-3/3-6/6-12/12-18/18-24 月）

---

### 模块 7：周末遛娃

**功能描述：** 根据用户城市、天气、宝宝月龄推荐周末遛娃方案。

**遛娃方案数据结构：**
```json
{
  "city": "杭州",
  "date": "2026-05-03",
  "weather": "晴 24°C",
  "plans": [
    {
      "type": "indoor",
      "activities": [
        {
          "time": "09:30-11:00",
          "location": "杭州大厦亲子乐园",
          "address": "杭州市下城区武林广场21号",
          "activity": "室内游乐+爬行区",
          "cost": "约80元/次",
          "transport": "打车15分钟",
          "suitable_age": "6-36月龄",
          "photo": null
        }
      ]
    }
  ]
}
```

**城市数据来源：**
- 高德地图 API（POI 搜索）
- 大众点评 API（亲子场所）
- 天气 API（天气联动）

---

## 三、API 接口定义

### 3.1 宝宝档案

```
POST   /api/v1/children          创建宝宝档案
GET    /api/v1/children          获取宝宝列表
GET    /api/v1/children/:id      获取宝宝详情
PUT    /api/v1/children/:id      更新宝宝信息
DELETE /api/v1/children/:id      删除宝宝
```

### 3.2 AI 对话

```
POST   /api/v1/chat              发送消息
GET    /api/v1/chat/history      获取对话历史
POST   /api/v1/chat/quick        快捷问题
```

### 3.3 日程管理

```
POST   /api/v1/schedule/generate 生成日程
GET    /api/v1/schedule/today    获取今日日程
GET    /api/v1/schedule/:date    获取指定日期日程
```

### 3.4 辅食食谱

```
POST   /api/v1/recipe/generate   生成食谱
GET    /api/v1/recipe/week       获取本周食谱
GET    /api/v1/recipe/shopping   获取采购清单
```

### 3.5 睡眠管理

```
POST   /api/v1/sleep             添加睡眠记录
GET    /api/v1/sleep             获取睡眠记录
GET    /api/v1/sleep/stats       获取睡眠统计
GET    /api/v1/sleep/analysis    获取AI分析
```

### 3.6 发育里程碑

```
GET    /api/v1/milestone         获取里程碑列表
PUT    /api/v1/milestone/:id     更新里程碑状态
GET    /api/v1/milestone/summary 获取发育摘要
```

### 3.7 周末遛娃

```
POST   /api/v1/outing/generate   生成遛娃方案
GET    /api/v1/outing/recommend  获取推荐地点
```

---

## 四、数据模型

### 4.1 核心表

```sql
-- 宝宝档案
CREATE TABLE children (
  id UUID PRIMARY KEY,
  name VARCHAR(20) NOT NULL,
  birth_date DATE NOT NULL,
  gender ENUM('male','female') NOT NULL,
  feeding_type ENUM('breast','formula','mixed') NOT NULL,
  weight DECIMAL(4,1),
  height DECIMAL(4,1),
  allergies JSONB,
  medical_history JSONB,
  vaccination_record JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- 对话记录
CREATE TABLE conversations (
  id UUID PRIMARY KEY,
  child_id UUID REFERENCES children(id),
  role ENUM('user','assistant') NOT NULL,
  content TEXT NOT NULL,
  agent_type VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW()
);

-- 睡眠记录
CREATE TABLE sleep_records (
  id UUID PRIMARY KEY,
  child_id UUID REFERENCES children(id),
  type ENUM('nap','afternoon_nap','night') NOT NULL,
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP NOT NULL,
  note TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 里程碑
CREATE TABLE milestones (
  id UUID PRIMARY KEY,
  child_id UUID REFERENCES children(id),
  category VARCHAR(50) NOT NULL,
  text VARCHAR(100) NOT NULL,
  done BOOLEAN DEFAULT FALSE,
  done_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 五、错误处理

| 错误码 | 含义 | 处理 |
|--------|------|------|
| 400 | 请求参数错误 | 提示用户修改输入 |
| 401 | 未登录 | 跳转登录页 |
| 404 | 资源不存在 | 提示用户 |
| 429 | 请求过于频繁 | 提示稍后重试 |
| 500 | 服务器错误 | 提示用户联系客服 |

---

> 本文档为研发开发参考，功能模块详细说明。
