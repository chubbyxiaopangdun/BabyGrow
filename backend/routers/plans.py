from fastapi import APIRouter, HTTPException
from datetime import datetime, date

from models.database import get_session, Child, FeedRecord, SleepRecord
from models.schemas import DailyPlanResponse
from models.utils import calc_age_months
from services.planner import daily_planner

router = APIRouter(prefix="/api/v1/children", tags=["plans"])


def records_to_dicts(records):
    """将记录对象转换为字典"""
    result = []
    for r in records:
        if hasattr(r, '__dict__'):
            d = {}
            for key in dir(r):
                if not key.startswith('_'):
                    try:
                        val = getattr(r, key)
                        if not callable(val):
                            if isinstance(val, (datetime, date)):
                                d[key] = val.isoformat() if val else None
                            else:
                                d[key] = val
                    except:
                        pass
            result.append(d)
    return result


@router.get("/{child_id}/plan/today", response_model=DailyPlanResponse)
async def get_today_plan(child_id: str, kb: str = None):
    """获取今日育儿计划"""
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, detail="孩子不存在")
        
        today = date.today()
        kb_context = None
        if kb:
            import json as _json
            try:
                kb_context = _json.loads(kb)
            except:
                pass
        return await _generate_plan(session, child, today, kb_context)
    finally:
        session.close()


@router.get("/{child_id}/plan/{plan_date}", response_model=DailyPlanResponse)
async def get_plan_by_date(child_id: str, plan_date: str, kb: str = None):
    """获取指定日期的育儿计划"""
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, detail="孩子不存在")
        
        try:
            target_date = datetime.strptime(plan_date, "%Y-%m-%d").date()
        except:
            raise HTTPException(status_code=400, detail="日期格式错误，请使用YYYY-MM-DD")
        
        kb_context = None
        if kb:
            import json as _json
            try:
                kb_context = _json.loads(kb)
            except:
                pass
        return await _generate_plan(session, child, target_date, kb_context)
    finally:
        session.close()


async def _generate_plan(session, child, target_date: date, kb_context=None):
    """内部：生成计划"""
    # 获取今日已有的记录
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
    
    # 使用planner生成计划（传入知识库上下文）
    plan_data = daily_planner.generate_plan(
        child_name=child.name,
        age_months=age_months,
        current_date=target_date,
        today_feed_records=records_to_dicts(feed_records),
        today_sleep_records=records_to_dicts(sleep_records),
        context=kb_context
    )
    
    return DailyPlanResponse(
        date=target_date.isoformat(),
        child_id=child.id,
        child_name=child.name,
        child_age_months=age_months,
        items=plan_data["items"],
        reminders=plan_data["reminders"],
        ai_tips=plan_data["ai_tips"]
    )
