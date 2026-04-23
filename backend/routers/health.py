from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
import uuid

from models.database import get_session, HealthRecord, Child
from models.schemas import HealthRecordCreate, HealthRecordResponse

router = APIRouter(prefix="/api/v1/children", tags=["health"])


@router.get("/{child_id}/health", response_model=List[HealthRecordResponse])
async def list_health_records(child_id: str, type_filter: str = None):
    """获取孩子的健康记录"""
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, detail="孩子不存在")
        
        query = session.query(HealthRecord).filter(HealthRecord.child_id == child_id)
        
        if type_filter:
            from models.database import HealthTypeEnum
            try:
                type_enum = HealthTypeEnum(type_filter)
                query = query.filter(HealthRecord.type == type_enum)
            except ValueError:
                pass  # 忽略无效的type_filter
        
        records = query.order_by(HealthRecord.date.desc()).limit(100).all()
        return [HealthRecordResponse(
            id=r.id,
            child_id=r.child_id,
            type=r.type.value,
            value=r.value,
            unit=r.unit,
            date=r.date,
            notes=r.notes,
            created_at=r.created_at
        ) for r in records]
    finally:
        session.close()


@router.post("/{child_id}/health", response_model=HealthRecordResponse)
async def create_health_record(child_id: str, health: HealthRecordCreate):
    """添加健康记录"""
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, detail="孩子不存在")
        
        record_id = f"hr_{uuid.uuid4().hex[:8]}"
        db_record = HealthRecord(
            id=record_id,
            child_id=child_id,
            type=health.type.value,
            value=health.value,
            unit=health.unit,
            date=health.date,
            notes=health.notes
        )
        
        session.add(db_record)
        session.commit()
        session.refresh(db_record)
        
        return HealthRecordResponse(
            id=db_record.id,
            child_id=db_record.child_id,
            type=db_record.type.value,
            value=db_record.value,
            unit=db_record.unit,
            date=db_record.date,
            notes=db_record.notes,
            created_at=db_record.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()


@router.delete("/{child_id}/health/{health_id}")
async def delete_health_record(child_id: str, health_id: str):
    """删除健康记录"""
    session = get_session()
    try:
        record = session.query(HealthRecord).filter(HealthRecord.id == health_id, HealthRecord.child_id == child_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="记录不存在")
        
        session.delete(record)
        session.commit()
        return {"code": 0, "message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()
