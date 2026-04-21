from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime, date
import uuid

from models.database import get_session, FeedRecord, Child
from models.schemas import FeedRecordCreate, FeedRecordUpdate, FeedRecordResponse

router = APIRouter(prefix="/api/v1/children", tags=["feeds"])


@router.get("/{child_id}/feeds", response_model=List[FeedRecordResponse])
async def list_feeds(child_id: str, date_str: str = None):
    """获取孩子的喂养记录"""
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, message="孩子不存在")
        
        query = session.query(FeedRecord).filter(FeedRecord.child_id == child_id)
        
        if date_str:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            query = query.filter(
                FeedRecord.time >= datetime.combine(target_date, datetime.min.time()),
                FeedRecord.time < datetime.combine(target_date, datetime.max.time())
            )
        
        records = query.order_by(FeedRecord.time.desc()).all()
        return [FeedRecordResponse(
            id=r.id,
            child_id=r.child_id,
            type=r.type.value,
            food_name=r.food_name,
            amount=r.amount,
            unit=r.unit,
            time=r.time,
            eating_mode=r.eating_mode.value,
            new_food=r.new_food,
            new_food_observation_end=r.new_food_observation_end,
            notes=r.notes,
            created_at=r.created_at
        ) for r in records]
    finally:
        session.close()


@router.post("/{child_id}/feeds", response_model=FeedRecordResponse)
async def create_feed(child_id: str, feed: FeedRecordCreate):
    """添加喂养记录"""
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, message="孩子不存在")
        
        record_id = f"fr_{uuid.uuid4().hex[:8]}"
        db_record = FeedRecord(
            id=record_id,
            child_id=child_id,
            type=feed.type.value,
            food_name=feed.food_name,
            amount=feed.amount,
            unit=feed.unit,
            time=feed.time,
            eating_mode=feed.eating_mode.value,
            new_food=feed.new_food,
            new_food_observation_end=feed.new_food_observation_end,
            notes=feed.notes
        )
        
        session.add(db_record)
        session.commit()
        session.refresh(db_record)
        
        return FeedRecordResponse(
            id=db_record.id,
            child_id=db_record.child_id,
            type=db_record.type.value,
            food_name=db_record.food_name,
            amount=db_record.amount,
            unit=db_record.unit,
            time=db_record.time,
            eating_mode=db_record.eating_mode.value,
            new_food=db_record.new_food,
            new_food_observation_end=db_record.new_food_observation_end,
            notes=db_record.notes,
            created_at=db_record.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, message=str(e))
    finally:
        session.close()


@router.put("/{child_id}/feeds/{feed_id}", response_model=FeedRecordResponse)
async def update_feed(child_id: str, feed_id: str, feed: FeedRecordUpdate):
    """更新喂养记录"""
    session = get_session()
    try:
        record = session.query(FeedRecord).filter(FeedRecord.id == feed_id, FeedRecord.child_id == child_id).first()
        if not record:
            raise HTTPException(status_code=404, message="记录不存在")
        
        if feed.type is not None:
            record.type = feed.type.value
        if feed.food_name is not None:
            record.food_name = feed.food_name
        if feed.amount is not None:
            record.amount = feed.amount
        if feed.unit is not None:
            record.unit = feed.unit
        if feed.time is not None:
            record.time = feed.time
        if feed.eating_mode is not None:
            record.eating_mode = feed.eating_mode.value
        if feed.new_food is not None:
            record.new_food = feed.new_food
        if feed.new_food_observation_end is not None:
            record.new_food_observation_end = feed.new_food_observation_end
        if feed.notes is not None:
            record.notes = feed.notes
        
        session.commit()
        session.refresh(record)
        
        return FeedRecordResponse(
            id=record.id,
            child_id=record.child_id,
            type=record.type.value,
            food_name=record.food_name,
            amount=record.amount,
            unit=record.unit,
            time=record.time,
            eating_mode=record.eating_mode.value,
            new_food=record.new_food,
            new_food_observation_end=record.new_food_observation_end,
            notes=record.notes,
            created_at=record.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, message=str(e))
    finally:
        session.close()


@router.delete("/{child_id}/feeds/{feed_id}")
async def delete_feed(child_id: str, feed_id: str):
    """删除喂养记录"""
    session = get_session()
    try:
        record = session.query(FeedRecord).filter(FeedRecord.id == feed_id, FeedRecord.child_id == child_id).first()
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
