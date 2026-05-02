"""
BabyGrow Agent 路由引擎
将用户问题分类并路由到对应的专家 Agent

策略：关键词优先（0延迟） → LLM 兜底（处理模糊问题）
"""
import json
import re
from typing import Optional, Dict, Any

from services.agents import nutrition, sleep, schedule, health


# ============================================================
# 路由分类规则
# ============================================================

ROUTE_RULES = {
    "nutrition": {
        "keywords": [
            "辅食", "吃什么", "食谱", "奶量", "喂奶", "喂养",
            "营养", "菜谱", "做饭", "做饭", "米糊", "菜泥",
            "果泥", "加餐", "餐食", "断奶", "母乳", "配方奶",
            "补铁", "补钙", "维生素", "蛋白质", "食材",
            "鸡蛋", "肉泥", "鱼", "虾", "过敏食物",
            "一周食谱", "七天食谱", "采购", "买什么菜",
            "做法", "做法步骤", "怎么做",
        ],
        "patterns": [
            r"吃什么好",
            r"吃.+吗",
            r"可以吃.+吗",
            r"多久吃.+次",
            r"奶量.+多少",
            r"辅食.+推荐",
        ],
        "agent_name": "营养专家",
        "emoji": "🍖",
    },
    "sleep": {
        "keywords": [
            "睡觉", "睡眠", "午睡", "夜醒", "哄睡", "接觉",
            "入睡", "落地醒", "小睡", "夜觉", "作息",
            "睡不着", "睡不好", "翻来覆去", "磨牙",
            "昼夜颠倒", "自主入睡", "抱睡", "奶睡",
        ],
        "patterns": [
            r"睡.+不好",
            r"不睡觉",
            r"睡几个小时",
            r"几点睡",
            r"醒来.+次",
        ],
        "agent_name": "睡眠顾问",
        "emoji": "🌙",
    },
    "schedule": {
        "keywords": [
            "日程", "安排", "时间表", "SOP", "一天",
            "怎么安排", "几点做什么", "今天做什么",
            "作息时间", "时间线", "日常安排",
        ],
        "patterns": [
            r"今天.+安排",
            r"一天.+怎么",
            r"日程",
            r"时间表",
            r"几点.+几点",
        ],
        "agent_name": "日程管理专家",
        "emoji": "📋",
    },
    "health": {
        "keywords": [
            "发烧", "咳嗽", "生病", "疫苗", "湿疹", "腹泻",
            "呕吐", "鼻涕", "感冒", "体温", "拉肚子",
            "出牙", "长牙", "囟门", "发育", "体检",
            "儿保", "打针", "红屁股", "肠绞痛",
        ],
        "patterns": [
            r"发烧.+度",
            r"体温.+度",
            r"咳嗽.+天",
            r"拉.+次",
        ],
        "agent_name": "健康顾问",
        "emoji": "🏥",
    },
}


def classify_by_keywords(message: str) -> Optional[str]:
    """
    关键词分类（0延迟，覆盖80%场景）
    返回路由目标 or None
    """
    message_lower = message.lower()
    scores = {}
    
    for route, rules in ROUTE_RULES.items():
        score = 0
        # 关键词匹配
        for kw in rules["keywords"]:
            if kw in message_lower:
                score += 1
        # 正则匹配（权重更高）
        for pattern in rules["patterns"]:
            if re.search(pattern, message_lower):
                score += 2
        if score > 0:
            scores[route] = score
    
    if not scores:
        return None
    
    # 返回得分最高的路由
    return max(scores, key=scores.get)


async def classify_by_llm(message: str, ai_service) -> Optional[str]:
    """
    LLM 分类兜底（处理关键词无法覆盖的模糊问题）
    用最轻量的 prompt 做分类
    """
    classify_prompt = f"""请判断以下育儿问题属于哪个类别，只回复类别名称（一个词）：

问题："{message}"

类别选项：
- nutrition: 营养、辅食、喂养、食谱相关
- sleep: 睡眠、作息、哄睡相关  
- schedule: 日程安排、时间表、今天做什么
- health: 生病、症状、疫苗、发育相关
- general: 以上都不匹配的综合问题

回复格式：只回复一个词，不要任何解释。"""

    try:
        messages = [{"role": "user", "content": classify_prompt}]
        result = await ai_service.chat(messages, temperature=0.1, max_tokens=20)
        route = result["content"].strip().lower()
        
        # 标准化
        for valid_route in ["nutrition", "sleep", "schedule", "health", "general"]:
            if valid_route in route:
                return valid_route
        return "general"
    except Exception:
        return "general"


# ============================================================
# Agent Router 核心
# ============================================================

class AgentRouter:
    """Agent 路由器：分类 → 路由 → 构建 Prompt → 调用 LLM"""
    
    def __init__(self, ai_service):
        self.ai_service = ai_service
    
    async def route_and_respond(
        self,
        message: str,
        child_profile: dict,
        context_records: dict = None,
        conversation_history: list = None,
    ) -> dict:
        """
        核心路由方法
        
        Args:
            message: 用户消息
            child_profile: 宝宝档案
            context_records: 相关记录 (feeds, sleeps, health等)
            conversation_history: 最近对话历史
            
        Returns:
            {
                "reply": str,           # AI回复文本
                "card": dict|None,      # 结构化卡片
                "agent": str,           # 路由到的agent名称
                "agent_name": str,      # agent中文名
                "agent_emoji": str,     # agent图标
                "severity": str,        # 安全等级
            }
        """
        context_records = context_records or {}
        conversation_history = conversation_history or []
        
        # Step 1: 分类
        route = classify_by_keywords(message)
        if route is None:
            route = await classify_by_llm(message, self.ai_service)
        
        # 获取路由元信息
        route_info = ROUTE_RULES.get(route, {})
        agent_name = route_info.get("agent_name", "育儿顾问")
        agent_emoji = route_info.get("emoji", "👶")
        
        # Step 2: 构建系统提示词
        system_prompt = self._build_system_prompt(
            route=route,
            child_profile=child_profile,
            context_records=context_records
        )
        
        # Step 3: 构建消息列表（含历史上下文）
        messages = []
        # 加入最近5条历史
        for hist in conversation_history[-5:]:
            messages.append({
                "role": hist.get("role", "user"),
                "content": hist.get("content", "")
            })
        messages.append({"role": "user", "content": message})
        
        # Step 4: 调用 LLM
        try:
            result = await self.ai_service.chat(
                messages=messages,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=2000
            )
            reply = result["content"]
        except Exception as e:
            reply = f"抱歉，AI 暂时无法回应，请稍后再试。错误：{str(e)}"
        
        # Step 5: 安全审核
        from services.safety_review import review_response
        safety = review_response(reply, message)
        reply = safety["content"]
        
        # Step 6: 构建结构化卡片
        card = self._build_card(
            route=route,
            agent_name=agent_name,
            agent_emoji=agent_emoji,
            content=reply,
            child_profile=child_profile,
            disclaimer=safety.get("disclaimer")
        )
        
        return {
            "reply": reply,  # 兼容旧前端的纯文本
            "card": card,
            "agent": route,
            "agent_name": agent_name,
            "agent_emoji": agent_emoji,
            "severity": safety["severity"],
        }
    
    def _build_system_prompt(
        self,
        route: str,
        child_profile: dict,
        context_records: dict
    ) -> str:
        """根据路由类型构建对应的系统提示词"""
        
        if route == "nutrition":
            records_str = self._format_feed_records(context_records.get("feeds", []))
            return nutrition.build_prompt(child_profile, records_str)
        
        elif route == "sleep":
            return sleep.build_prompt(
                child_profile,
                context_records.get("sleeps", [])
            )
        
        elif route == "schedule":
            records_str = self._format_today_records(context_records)
            return schedule.build_prompt(
                child_profile,
                context_records.get("weather", "晴"),
                records_str
            )
        
        elif route == "health":
            records_str = self._format_health_records(context_records.get("health", []))
            return health.build_prompt(child_profile, records_str)
        
        else:
            # 通用育儿顾问
            return self._general_prompt(child_profile)
    
    def _general_prompt(self, child_profile: dict) -> str:
        return f"""你是一位温暖、专业的AI育儿助手，名叫BabyGrow。

## 宝宝信息
- 姓名: {child_profile.get('name', '宝宝')}
- 月龄: {child_profile.get('age_months', 0)}个月
- 喂养方式: {child_profile.get('feeding', '未知')}
- 过敏史: {child_profile.get('allergies', '无') or '无'}

## 回复要求
1. 用温暖、鼓励的语气
2. 针对宝宝的月龄给出具体建议
3. 如果问题涉及专业领域，建议咨询对应专家
4. 用 Markdown 格式组织内容
5. 开头用 emoji + 称呼宝宝名字"""
    
    def _format_feed_records(self, feeds: list) -> str:
        if not feeds:
            return ""
        lines = ["\n## 今日喂养记录"]
        for f in feeds[-5:]:
            lines.append(
                f"- {f.get('type','?')}: {f.get('food_name','?')} "
                f"{f.get('amount',0)}{f.get('unit','')} "
                f"({f.get('time','?')})"
            )
        return "\n".join(lines)
    
    def _format_today_records(self, context: dict) -> str:
        lines = []
        feeds = context.get("feeds", [])
        sleeps = context.get("sleeps", [])
        if feeds:
            lines.append("## 今日已喂养")
            for f in feeds[-3:]:
                lines.append(f"- {f.get('food_name','?')} {f.get('amount',0)}{f.get('unit','')}")
        if sleeps:
            lines.append("## 今日睡眠")
            for s in sleeps[-2:]:
                lines.append(f"- {s.get('type','?')}: {s.get('start_time','?')}~{s.get('end_time','?')}")
        return "\n".join(lines) if lines else "暂无今日记录"
    
    def _format_health_records(self, health_records: list) -> str:
        if not health_records:
            return ""
        lines = ["\n## 近期健康记录"]
        for h in health_records[-5:]:
            lines.append(
                f"- {h.get('type','?')}: {h.get('value','?')}{h.get('unit','')} "
                f"({h.get('date','?')})"
            )
        return "\n".join(lines)
    
    def _build_card(
        self,
        route: str,
        agent_name: str,
        agent_emoji: str,
        content: str,
        child_profile: dict,
        disclaimer: str = None
    ) -> dict:
        """构建结构化卡片"""
        child_name = child_profile.get("name", "宝宝")
        age_months = child_profile.get("age_months", 0)
        
        # 根据路由类型生成不同的卡片标题
        title_map = {
            "nutrition": f"{agent_emoji} {child_name}的营养建议",
            "sleep": f"{agent_emoji} {child_name}的睡眠分析",
            "schedule": f"{agent_emoji} {child_name}的今日日程",
            "health": f"{agent_emoji} {child_name}的健康咨询",
        }
        
        title = title_map.get(route, f"{agent_emoji} BabyGrow育儿建议")
        subtitle = f"由{agent_name}为您解答 · {child_name} {age_months}月龄"
        
        # 动作按钮
        actions = []
        if route == "nutrition":
            actions.append({"label": "查看7天食谱", "type": "meal_plan"})
            actions.append({"label": "生成采购清单", "type": "shopping_list"})
        elif route == "schedule":
            actions.append({"label": "刷新日程", "type": "refresh_schedule"})
        elif route == "sleep":
            actions.append({"label": "记录睡眠", "type": "add_sleep"})
        
        return {
            "title": title,
            "subtitle": subtitle,
            "content": content,
            "actions": actions,
            "disclaimer": disclaimer,
        }
