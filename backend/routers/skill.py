from fastapi import APIRouter, HTTPException
from datetime import datetime, date
import json

from models.database import get_session, Child, FeedRecord, SleepRecord
from models.schemas import SkillGeneratePlanRequest, SkillChatRequest
from models.utils import calc_age_months
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


def records_to_list(records, record_type="feed"):
    """将记录列表转换为字典"""
    result = []
    for r in records:
        if record_type == "feed":
            result.append({
                "type": r.type.value,
                "food_name": r.food_name,
                "amount": r.amount,
                "unit": r.unit,
                "time": r.time.isoformat() if r.time else None
            })
        elif record_type == "sleep":
            result.append({
                "type": r.type.value,
                "start_time": r.start_time.isoformat() if r.start_time else None,
                "end_time": r.end_time.isoformat() if r.end_time else None,
                "night_wakings": r.night_wakings,
                "quality": r.quality,
                "notes": r.notes
            })
    return result


@router.post("/generate_plan")
async def skill_generate_plan(req: SkillGeneratePlanRequest):
    """AI Agent Skill: 生成育儿计划（真正基于实时数据）"""
    from services.ai_service import ai_service

    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == req.child_id).first()
        if not child:
            raise HTTPException(status_code=404, detail="孩子不存在")

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

        # 先用模板生成基础计划
        plan_data = daily_planner.generate_plan(
            child_name=child.name,
            age_months=age_months,
            current_date=target_date,
            today_feed_records=records_to_list(feed_records, "feed"),
            today_sleep_records=records_to_list(sleep_records, "sleep"),
            context=req.context
        )

        # 构建今日记录摘要给 AI
        feed_summary = _build_feed_summary(feed_records, age_months)
        sleep_summary = _build_sleep_summary(sleep_records)

        # 让 AI 根据真实数据优化计划
        ai_prompt = f"""你是BabyGrow的AI育儿顾问，正在为{child.name}（{age_months}个月）生成今日育儿计划。

今日已有记录：
{feed_summary}

{sleep_summary}

基础计划：
{_format_plan_items(plan_data['items'])}

请根据今日已有记录，分析：
1. 奶量/辅食是否已足够，还差多少
2. 睡眠是否正常，有没有异常
3. 在基础计划基础上，给出针对性的调整建议（如果有）

请用JSON格式返回：
{{
  "analysis": "今日数据分析（2-3句话）",
  "adjustments": ["调整建议1", "调整建议2"],
  "final_plan": [
    {{"time": "07:00", "type": "meal", "title": "起床喝奶", "details": "...", "notes": "..."}},
    ...
  ],
  "reminders": [
    {{"type": "food", "content": "..."}},
    ...
  ],
  "ai_tips": "今日特别提示（1句话）"
}}

只返回JSON，不要其他内容。"""

        messages = [{"role": "user", "content": ai_prompt}]
        result = await ai_service.chat(messages=messages, system_prompt=SYSTEM_PROMPT, temperature=0.5)

        # 尝试解析AI返回的JSON
        plan_text = f"📅 {child.name}（{age_months}个月）的今日计划\n"
        plan_text += f"📆 {target_date.strftime('%Y年%m月%d日')}\n\n"

        try:
            import json as _json
            ai_data = _json.loads(result["content"])
            plan_text += f"💡 {ai_data.get('analysis', '')}\n\n"
            for item in ai_data.get("final_plan", plan_data["items"]):
                plan_text += f"🕐 {item.get('time','')}  {item.get('title','')}"
                if item.get('details'):
                    plan_text += f"\n   {item['details']}"
                if item.get('notes'):
                    plan_text += f"\n   💡 {item['notes']}"
                plan_text += "\n"
            if ai_data.get("adjustments"):
                plan_text += "\n✨ 调整建议：\n"
                for adj in ai_data["adjustments"]:
                    plan_text += f"• {adj}\n"
            if ai_data.get("reminders"):
                plan_text += "\n📌 今日提醒：\n"
                for rem in ai_data["reminders"]:
                    plan_text += f"• {rem.get('content', '')}\n"
            if ai_data.get("ai_tips"):
                plan_text += f"\n💡 {ai_data['ai_tips']}\n"
            final_plan = ai_data
        except Exception:
            # AI返回格式不对，用原始模板
            for item in plan_data["items"]:
                plan_text += f"🕐 {item['time']}  {item['title']}"
                if item.get('details'):
                    plan_text += f"\n   {item['details']}"
                if item.get('notes'):
                    plan_text += f"\n   💡 {item['notes']}"
                plan_text += "\n"
            final_plan = plan_data

        return {
            "code": 0,
            "message": "ok",
            "skill_name": "babygrow.generate_plan",
            "data": {
                "plan": final_plan,
                "plan_text": plan_text,
                "child_id": child.id,
                "child_name": child.name,
                "age_months": age_months,
                "date": target_date.isoformat()
            }
        }
    finally:
        session.close()


def _build_feed_summary(feed_records, age_months):
    """构建喂养记录摘要"""
    if not feed_records:
        return "今日暂无喂养记录"

    total_milk = 0
    total_solid = 0
    food_list = []
    for r in feed_records:
        if r.type.value in ("breast_milk", "formula"):
            total_milk += r.amount or 0
        elif r.type.value in ("solid", "fruit", "snack"):
            total_solid += 1
        food_list.append(f"  - {r.time.strftime('%H:%M')} {r.type.value} {'+新食材' if r.new_food else ''} {r.food_name or ''} {r.amount or ''}{r.unit or ''}")

    return f"""今日喂养记录（截止目前）：
{chr(10).join(food_list) if food_list else '  暂无'}

奶量合计：{total_milk}ml（{age_months}个月建议每日{total_milk}ml左右）"""


def _build_sleep_summary(sleep_records):
    """构建睡眠记录摘要"""
    if not sleep_records:
        return "今日暂无睡眠记录"

    naps = []
    night_sleep = None
    total_sleep_mins = 0
    total_night_wakings = 0

    for r in sleep_records:
        if r.type.value == "night":
            night_sleep = r
            if r.end_time and r.start_time:
                mins = int((r.end_time - r.start_time).total_seconds() / 60)
                total_sleep_mins += mins
                total_night_wakings += r.night_wakings or 0
        else:
            naps.append(r)
            if r.end_time and r.start_time:
                mins = int((r.end_time - r.start_time).total_seconds() / 60)
                total_sleep_mins += mins

    lines = []
    for n in naps:
        start = n.start_time.strftime("%H:%M") if n.start_time else "?"
        end = n.end_time.strftime("%H:%M") if n.end_time else "?"
        lines.append(f"  - {start}-{end} {n.type.value}（夜醒{n.night_wakings}次）")

    night_line = ""
    if night_sleep:
        start = night_sleep.start_time.strftime("%H:%M") if night_sleep.start_time else "?"
        end = night_sleep.end_time.strftime("%H:%M") if night_sleep.end_time else "?"
        night_line = f"  - 夜睡 {start}-{end}（夜醒{total_night_wakings}次）"

    return f"""今日睡眠记录（截止目前）：
{chr(10).join(lines)}
{night_line}
已睡总时长：约{total_sleep_mins // 60}小时{total_sleep_mins % 60}分钟"""


def _format_plan_items(items):
    """格式化计划条目"""
    lines = []
    for item in items:
        lines.append(f"  {item['time']} {item['title']}: {item.get('details','')}")
    return chr(10).join(lines)


@router.post("/chat")
async def skill_chat(req: SkillChatRequest):
    """AI Agent Skill: 通用育儿问答"""
    from services.ai_service import ai_service

    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == req.child_id).first()
        if not child:
            raise HTTPException(status_code=404, detail="孩子不存在")

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
