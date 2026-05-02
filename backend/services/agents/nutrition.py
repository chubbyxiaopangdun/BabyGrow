"""
BabyGrow 营养专家 Agent
处理辅食、喂养、营养相关问题
"""

NUTRITION_SYSTEM_PROMPT = """你是一位专业的婴幼儿营养顾问，服务于{child_name}的家长。

## 宝宝信息
- 姓名: {child_name}
- 月龄: {age_months}个月
- 喂养方式: {feeding_type}
- 过敏史: {allergies}
- 体重: {weight}

## 你的职责
1. 根据宝宝月龄提供个性化的辅食建议
2. 严格避免过敏食物
3. 确保营养均衡（碳水+蛋白质+脂肪+维生素+矿物质）
4. 给出具体的做法和用量
5. 用温暖鼓励的语气，理解新手妈妈的辛苦

## 回复格式要求
- 用 emoji + 标题开头，如"🍖 豆豆的辅食建议"
- 内容用 Markdown 列表/表格组织
- 每道菜包含: 名称、食材、做法（简要）、营养点评
- 末尾加一句鼓励的话

## 月龄食物参考
- 6月龄: 米糊、菜泥、果泥（糊状）
- 7-8月龄: 碎末状食物、蛋黄、肉泥
- 9-10月龄: 小块软食、手指食物、蛋羹
- 11-12月龄: 接近大人食物质地、丰富种类

{context_records}"""


def build_prompt(child_profile: dict, records_context: str = "") -> str:
    """构建营养专家的系统提示词"""
    return NUTRITION_SYSTEM_PROMPT.format(
        child_name=child_profile.get("name", "宝宝"),
        age_months=child_profile.get("age_months", 0),
        feeding_type=child_profile.get("feeding", "未知"),
        allergies=child_profile.get("allergies", "无") or "无",
        weight=child_profile.get("weight", "未知") or "未知",
        context_records=records_context
    )


# 预置快捷回答（无需 LLM）
QUICK_ANSWERS = {
    "6月龄辅食": """🍼 6月龄辅食添加指南

**添加原则：**
1. 从一种开始，观察3天无过敏再加新食物
2. 由稀到稠、由少到多
3. 母乳/配方奶仍是主食

**推荐第一口辅食：**
- 🌾 高铁米粉（首选！补铁关键期）
- 🥔 土豆泥 / 红薯泥
- 🥦 西兰花泥
- 🍌 香蕉泥

**每日安排：**
- 上午：1顿辅食（米粉+菜泥）
- 奶量：600-800ml/天不变

💡 小提示：辅食是"尝味道+学吞咽"，别着急加太多哦~""",
}
