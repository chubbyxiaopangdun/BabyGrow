from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime, timedelta
import uuid

from models.database import get_session, SleepRecord, Child
from models.schemas import SleepRecordCreate, SleepRecordUpdate, SleepRecordResponse

router = APIRouter(prefix="/api/v1/children", tags=["sleeps"])


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
            raise HTTPException(status_code=404, message="孩子不存在")
        
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
            raise HTTPException(status_code=404, message="孩子不存在")
        
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
        raise HTTPException(status_code=400, message=str(e))
    finally:
        session.close()


@router.put("/{child_id}/sleeps/{sleep_id}", response_model=SleepRecordResponse)
async def update_sleep(child_id: str, sleep_id: str, sleep: SleepRecordUpdate):
    """更新睡眠记录"""
    session = get_session()
    try:
        record = session.query(SleepRecord).filter(SleepRecord.id == sleep_id, SleepRecord.child_id == child_id).first()
        if not record:
            raise HTTPException(status_code=404, message="记录不存在")
        
        if sleep.type is not None:
            record.type = sleep.type.value
        if sleep.start_time is not None:
            record.start_time = sleep.start_time
        if sleep.end_time is not None:
            record.end_time = sleep.end_time
        if sleep.night_wakings is not None:
            record.night_wakings = sleep.night_wakings
        if sleep.quality is not None:
            record.quality = sleep.quality
        if sleep.notes is not None:
            record.notes = sleep.notes
        
        session.commit()
        session.refresh(record)
        
        return SleepRecordResponse(
            id=record.id,
            child_id=record.child_id,
            type=record.type.value,
            start_time=record.start_time,
            end_time=record.end_time,
            night_wakings=record.night_wakings,
            quality=record.quality,
            notes=record.notes,
            duration_minutes=calc_duration(record),
            created_at=record.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, message=str(e))
    finally:
        session.close()


@router.delete("/{child_id}/sleeps/{sleep_id}")
async def delete_sleep(child_id: str, sleep_id: str):
    """删除睡眠记录"""
    session = get_session()
    try:
        record = session.query(SleepRecord).filter(SleepRecord.id == sleep_id, SleepRecord.child_id == child_id).first()
        if not record:
            raise HTTPException(status_code=404, message="记录不存在")
        
        session.delete(record)
        session.commit()
        return {"code": 0, "message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, message=str(e))
    finally:
        session.close()


@router.get("/{child_id}/sleeps/stats")
async def get_sleep_stats(child_id: str, days: int = 7):
    """获取睡眠统计"""
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, message="孩子不存在")
        
        from datetime import date
        start_date = date.today() - timedelta(days=days)
        
        records = session.query(SleepRecord).filter(
            SleepRecord.child_id == child_id,
            SleepRecord.start_time >= datetime.combine(start_date, datetime.min.time())
        ).all()
        
        total_minutes = 0
        night_waking_total = 0
        nap_count = 0
        
        for r in records:
            if r.end_time:
                total_minutes += calc_duration(r)
            if r.type.value != "night":
                nap_count += 1
            night_waking_total += r.night_wakings
        
        avg_sleep = total_minutes / days if days > 0 else 0
        
        return {
            "code": 0,
            "message": "ok",
            "data": {
                "days": days,
                "total_records": len(records),
                "avg_daily_sleep_minutes": round(avg_sleep, 1),
                "avg_daily_sleep_hours": round(avg_sleep / 60, 1),
                "total_night_wakings": night_waking_total,
                "avg_night_wakings": round(night_waking_total / days, 1),
                "nap_days": nap_count
            }
        }
    finally:
        session.close()
