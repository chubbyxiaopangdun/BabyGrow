from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime, date, timedelta
import uuid

from models.database import get_session, SleepRecord, Child
from models.schemas import SleepRecordCreate, SleepRecordUpdate, SleepRecordResponse

router = APIRouter(prefix="/api/v1/children", tags=["sleeps"])


def calc_age_months(birth_date) -> int:
    """计算月龄"""
    today = date.today()
    months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
    if today.day < birth_date.day:
        months -= 1
    return max(0, months)


def calc_duration(record: SleepRecord) -> int:
    """计算睡眠时长（分钟）"""
    if not record.end_time:
        return 0
    delta = record.end_time - record.start_time
    return int(delta.total_seconds() / 60)


@router.get("/{child_id}/sleeps", response_model=List[SleepRecordResponse])
async def list_sleeps(child_id: str, date_str: str = None):
    """获取孩子的睡眠记录"""
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, detail="孩子不存在")

        query = session.query(SleepRecord).filter(SleepRecord.child_id == child_id)

        if date_str:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            query = query.filter(
                SleepRecord.start_time >= datetime.combine(target_date, datetime.min.time()),
                SleepRecord.start_time < datetime.combine(target_date, datetime.max.time())
            )

        records = query.order_by(SleepRecord.start_time.desc()).all()
        return [SleepRecordResponse(
            id=r.id,
            child_id=r.child_id,
            type=r.type.value,
            start_time=r.start_time,
            end_time=r.end_time,
            night_wakings=r.night_wakings,
            quality=r.quality,
            notes=r.notes,
            duration_minutes=calc_duration(r),
            created_at=r.created_at
        ) for r in records]
    finally:
        session.close()


@router.post("/{child_id}/sleeps", response_model=SleepRecordResponse)
async def create_sleep(child_id: str, sleep: SleepRecordCreate):
    """添加睡眠记录"""
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, detail="孩子不存在")

        record_id = f"sr_{uuid.uuid4().hex[:8]}"
        db_record = SleepRecord(
            id=record_id,
            child_id=child_id,
            type=sleep.type.value,
            start_time=sleep.start_time,
            end_time=sleep.end_time,
            night_wakings=sleep.night_wakings,
            quality=sleep.quality,
            notes=sleep.notes
        )

        session.add(db_record)
        session.commit()
        session.refresh(db_record)

        return SleepRecordResponse(
            id=db_record.id,
            child_id=db_record.child_id,
            type=db_record.type.value,
            start_time=db_record.start_time,
            end_time=db_record.end_time,
            night_wakings=db_record.night_wakings,
            quality=db_record.quality,
            notes=db_record.notes,
            duration_minutes=calc_duration(db_record),
            created_at=db_record.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()


@router.post("/{child_id}/sleeps/analyze")
async def analyze_child_sleep(child_id: str, days: int = 7):
    """AI分析孩子的睡眠健康，给出详细报告和改进建议"""
    from services.ai_service import ai_service

    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, detail="孩子不存在")

        target_date = date.today()
        start_date = target_date - timedelta(days=days - 1)

        records = session.query(SleepRecord).filter(
            SleepRecord.child_id == child.id,
            SleepRecord.start_time >= datetime.combine(start_date, datetime.min.time()),
            SleepRecord.start_time <= datetime.combine(target_date, datetime.max.time())
        ).order_by(SleepRecord.start_time).all()

        if len(records) < 2:
            return {
                "code": 0,
                "message": "ok",
                "data": {
                    "child_id": child.id,
                    "child_name": child.name,
                    "age_months": calc_age_months(child.birth_date),
                    "period_days": len(records),
                    "report": f"数据不足（仅{len(records)}条记录），请记录至少2天睡眠数据后再分析。",
                    "summary": {"total_sleep_hours": 0, "avg_night_wakings": 0, "sleep_quality": "数据不足"},
                    "tips": []
                }
            }

        # 构建睡眠数据摘要
        summary = _build_sleep_analysis_summary(records, child.birth_date, child.name)

        # 让AI生成分析报告
        ai_prompt = f"""你是BabyGrow的AI睡眠顾问，为{summary['child_name']}（{summary['age_months']}个月）分析最近{summary['period_days']}天的睡眠数据。

睡眠数据摘要：
- 总记录数：{summary['total_records']}条
- 平均每日睡眠：{summary['avg_daily_sleep_hours']}小时
- 平均夜醒次数：{summary['avg_night_wakings']:.1f}次
- 夜间睡眠：{summary.get('avg_night_sleep_hours', 0):.1f}小时（平均）
- 白天小睡：{summary.get('avg_nap_count', 0):.1f}次/天
- 睡眠质量评分：{summary.get('sleep_quality', '数据不足')}

按天明细：
{summary.get('daily_details', '')}

请分析：
1. 睡眠总量是否达标（{summary['age_months']}个月建议11-14小时）
2. 夜醒是否过多，原因可能是什么
3. 小睡安排是否合理
4. 给出3-5条针对性改进建议

请用JSON格式返回：
{{
  "report": "整体睡眠评估（3-5句话，包含与月龄建议值的对比）",
  "summary": {{
    "total_sleep_hours": 平均总睡眠小时数（数字）,
    "avg_night_wakings": 平均夜醒次数（数字）,
    "sleep_quality": "良好/一般/需改善/数据不足",
    "meets_recommendation": true/false（是否达到月龄建议值）
  }},
  "tips": [
    {{"category": "睡眠环境", "content": "具体建议"}},
    {{"category": "作息调整", "content": "具体建议"}},
    {{"category": "家长行动", "content": "具体建议"}}
  ],
  "next_review_date": "建议下次复查日期（YYYY-MM-DD）"
}}

只返回JSON，不要其他内容。"""

        messages = [{"role": "user", "content": ai_prompt}]
        result = await ai_service.chat(messages=messages, system_prompt="你是一位专业的婴幼儿睡眠顾问", temperature=0.5)

        try:
            import json as _json
            ai_data = _json.loads(result["content"])
            return {
                "code": 0,
                "message": "ok",
                "data": {
                    "child_id": child.id,
                    "child_name": child.name,
                    "age_months": summary["age_months"],
                    "period_days": summary["period_days"],
                    "raw_summary": summary,
                    **ai_data
                }
            }
        except Exception:
            return {
                "code": 0,
                "message": "ok",
                "data": {
                    "child_id": child.id,
                    "child_name": child.name,
                    "age_months": summary["age_months"],
                    "period_days": summary["period_days"],
                    "report": f"数据分析完成。平均每日睡眠{summary['avg_daily_sleep_hours']}小时，夜醒{summary['avg_night_wakings']:.1f}次。数据不足无法生成详细AI报告。",
                    "summary": {
                        "total_sleep_hours": summary["avg_daily_sleep_hours"],
                        "avg_night_wakings": summary["avg_night_wakings"],
                        "sleep_quality": "数据不足",
                        "meets_recommendation": None
                    },
                    "tips": []
                }
            }
    finally:
        session.close()


def _build_sleep_analysis_summary(records, birth_date, child_name: str = ""):
    """构建睡眠分析摘要"""
    total_mins = 0
    night_wakings = 0
    nap_count = 0
    night_sleep_mins = 0
    daily_details = []

    day_records = {}
    for r in records:
        d = r.start_time.date()
        if d not in day_records:
            day_records[d] = []
        day_records[d].append(r)

    for day, recs in sorted(day_records.items()):
        day_naps = 0
        day_night_mins = 0
        day_total = 0
        day_wakings = 0
        for r in recs:
            mins = calc_duration(r)
            day_total += mins
            if r.type.value != "night":
                day_naps += 1
            else:
                day_night_mins = mins
            day_wakings += r.night_wakings or 0
        total_mins += day_total
        night_wakings += day_wakings
        nap_count += day_naps if day_naps > 0 else 0
        night_sleep_mins += day_night_mins
        daily_details.append(
            f"  {day.strftime('%m/%d')}: 总睡眠{day_total // 60}h{day_total % 60}m, "
            f"小睡{day_naps}次, 夜睡{day_night_mins // 60}h{day_night_mins % 60}m, 夜醒{day_wakings}次"
        )

    days = len(day_records)
    age_m = calc_age_months(birth_date)

    return {
        "child_name": child_name,
        "age_months": age_m,
        "period_days": days,
        "total_records": len(records),
        "avg_daily_sleep_hours": round(total_mins / days / 60, 1) if days > 0 else 0,
        "avg_night_wakings": round(night_wakings / days, 1) if days > 0 else 0,
        "avg_night_sleep_hours": round(night_sleep_mins / days / 60, 1) if days > 0 else 0,
        "avg_nap_count": round(nap_count / days, 1) if days > 0 else 0,
        "sleep_quality": _rate_sleep_quality(total_mins / days / 60 if days > 0 else 0,
                                              night_wakings / days if days > 0 else 0, age_m),
        "daily_details": "\n".join(daily_details)
    }


def _rate_sleep_quality(avg_hours, avg_night_wakings, age_months):
    """评估睡眠质量"""
    if age_months <= 6:
        ideal_min, ideal_max = 14, 18
    elif age_months <= 12:
        ideal_min, ideal_max = 12, 15
    elif age_months <= 24:
        ideal_min, ideal_max = 11, 14
    else:
        ideal_min, ideal_max = 10, 13

    if ideal_min <= avg_hours <= ideal_max and avg_night_wakings < 2:
        return "良好"
    elif avg_hours < ideal_min - 2 or avg_night_wakings >= 4:
        return "需改善"
    else:
        return "一般"
