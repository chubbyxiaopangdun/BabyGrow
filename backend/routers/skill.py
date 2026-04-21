from fastapi import APIRouter, HTTPException
from datetime import datetime, date
import json

from models.database import get_session, Child, FeedRecord, SleepRecord
from models.schemas import SkillGeneratePlanRequest, SkillChatRequest
from services.planner import daily_planner

router = APIRouter(prefix="/api/v1/skill", tags=["skill"])


SYSTEM_PROMPT = """你是一位专业、温暖、有耐心的AI育儿助手，服务于有0-12岁孩子的家庭。

你的特点：
1. **专业**：基于WHO儿童生长标准、中国营养学会指南、美国儿科学会（AAP）发育里程碑
2. **温暖**：理解新手爸妈的辛苦，给建议时肯定他们的付出，不说教、不批评
3. **务实**：给出的建议是可执行的、符合实际情况的，不是理想化的
4. **简洁**：用清晰的结构回答，不要长篇大论，让忙碌的家长能快速理解

你的职责：
- 根据孩子的月龄和具体情况，给出每日育儿建议
- 回答辅食制作、喂养技巧、睡眠调整、发育里程碑等常见问题
- 记录和追踪孩子的成长数据
- 提供哄睡、哭闹应对等实用SOP

安全边界：
- 涉及疾病诊断、用药建议时，引导家长就医
- 不给具体的医疗建议，只提供护理知识
- 强调科学育儿，但尊重家长的选择

记住：你是一个贴心的"数字育儿顾问"，用专业和温暖陪伴每个家庭。
"""


def calc_age_months(birth_date: date) -> int:
    today = date.today()
    months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
    if today.day < birth_date.day:
        months -= 1
    return max(0, months)


def records_to_list(records):
    result = []
    for r in records:
        if hasattr(r, 'type'):
            result.append({
                "type": r.type.value,
                "food_name": r.food_name,
                "amount": r.amount,
                "unit": r.unit,
                "time": r.time.isoformat() if r.time else None
            })
    return result


@router.post("/generate_plan")
async def skill_generate_plan(req: SkillGeneratePlanRequest):
    """AI Agent Skill: 生成育儿计划"""
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == req.child_id).first()
        if not child:
            raise HTTPException(status_code=404, message="孩子不存在")

        target_date = date.today()
        if req.date:
            try:
                target_date = datetime.strptime(req.date, "%Y-%m-%d").date()
            except:
                pass

        feed_records = session.query(FeedRecord).filter(
            FeedRecord.child_id == child.id,
            FeedRecord.time >= datetime.combine(target_date, datetime.min.time()),
            FeedRecord.time < datetime.combine(target_date, datetime.max.time())
        ).all()

        sleep_records = session.query(SleepRecord).filter(
            SleepRecord.child_id == child.id,
            SleepRecord.start_time >= datetime.combine(target_date, datetime.min.time()),
            SleepRecord.start_time < datetime.combine(target_date, datetime.max.time())
        ).all()

        age_months = calc_age_months(child.birth_date)

        plan_data = daily_planner.generate_plan(
            child_name=child.name,
            age_months=age_months,
            current_date=target_date,
            today_feed_records=records_to_list(feed_records),
            today_sleep_records=[],
            context=req.context
        )

        # 构建格式化的计划文本
        plan_text = f"📅 {child.name}（{age_months}个月）的今日计划\n"
        plan_text += f"📆 {target_date.strftime('%Y年%m月%d日')}\n\n"

        for item in plan_data["items"]:
            plan_text += f"🕐 {item['time']}  {item['title']}"
            if item.get('details'):
                plan_text += f"\n   {item['details']}"
            if item.get('notes'):
                plan_text += f"\n   💡 {item['notes']}"
            plan_text += "\n"

        if plan_data["reminders"]:
            plan_text += "\n📌 今日提醒：\n"
            for rem in plan_data["reminders"]:
                plan_text += f"• {rem['content']}\n"

        if plan_data["ai_tips"]:
            plan_text += f"\n💡 {plan_data['ai_tips']}\n"

        return {
            "code": 0,
            "message": "ok",
            "skill_name": "babygrow.generate_plan",
            "data": {
                "plan": plan_data,
                "plan_text": plan_text,
                "child_id": child.id,
                "child_name": child.name,
                "age_months": age_months,
                "date": target_date.isoformat()
            }
        }
    finally:
        session.close()


@router.post("/chat")
async def skill_chat(req: SkillChatRequest):
    """AI Agent Skill: 通用育儿问答"""
    from services.ai_service import ai_service

    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == req.child_id).first()
        if not child:
            raise HTTPException(status_code=404, message="孩子不存在")

        age_months = calc_age_months(child.birth_date)

        # 构建上下文
        context = f"""当前孩子信息：
- 姓名：{child.name}
- 月龄：{age_months}个月
- 出生日期：{child.birth_date}
- 过敏原：{child.allergies or '无'}
- 特殊情况：{child.notes or '无'}

用户问题：{req.message}"""

        messages = [{"role": "user", "content": context}]
        
        result = await ai_service.chat(
            messages=messages,
            system_prompt=SYSTEM_PROMPT,
            temperature=0.7
        )

        return {
            "code": 0,
            "message": "ok",
            "skill_name": "babygrow.chat",
            "data": {
                "reply": result["content"],
                "child_id": child.id,
                "child_name": child.name
            }
        }
    finally:
        session.close()
