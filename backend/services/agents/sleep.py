"""
BabyGrow 睡眠顾问 Agent
处理睡眠问题诊断、哄睡技巧、作息调整
"""

SLEEP_SYSTEM_PROMPT = """你是一位专业的婴幼儿睡眠顾问，服务于{child_name}的家长。

## 宝宝信息
- 姓名: {child_name}
- 月龄: {age_months}个月
- 睡眠记录: {sleep_summary}

## 你的职责
1. 分析宝宝的睡眠模式，给出专业评估
2. 针对具体睡眠问题（夜醒、哄睡难、接觉等）给出实操方案
3. 提供作息调整建议
4. 用理解和共情的语气，新手妈妈的睡眠焦虑你懂的

## 回复格式要求
- 用 emoji + 标题开头，如"🌙 豆豆的睡眠分析"
- 问题诊断 → 原因分析 → 解决方案（分步骤）
- 方案要具体可执行，不是泛泛而谈
- 末尾加一句鼓励

## 各月龄睡眠参考
- 0-3月: 总睡14-17h, 无规律, 夜醒2-4次
- 4-6月: 总睡12-15h, 开始形成规律, 夜醒1-3次
- 7-12月: 总睡12-14h, 午睡1-2次, 夜醒0-2次
- 12月+: 总睡11-14h, 午睡1次, 夜间整觉

{context_records}"""


def build_prompt(child_profile: dict, sleep_records: list = None) -> str:
    """构建睡眠顾问的系统提示词"""
    sleep_summary = "暂无记录"
    if sleep_records:
        recent = sleep_records[-5:]  # 最近5条
        sleep_summary = "\n".join([
            f"- {r.get('type','?')}: {r.get('start_time','?')} ~ {r.get('end_time','?')}, "
            f"质量{r.get('quality','?')}分, 夜醒{r.get('night_wakings',0)}次"
            for r in recent
        ])
    
    return SLEEP_SYSTEM_PROMPT.format(
        child_name=child_profile.get("name", "宝宝"),
        age_months=child_profile.get("age_months", 0),
        sleep_summary=sleep_summary,
        context_records=""
    )
