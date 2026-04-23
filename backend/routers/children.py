from fastapi import APIRouter, HTTPException
from typing import List
from datetime import date
import uuid
import json

from models.database import get_session, Child, HealthRecord
from models.schemas import ChildCreate, ChildUpdate, ChildResponse
from models.utils import calc_age_months, calc_age_display

router = APIRouter(prefix="/api/v1/children", tags=["children"])


def _get_current_health(session, child_id: str) -> tuple:
    """获取孩子最新的身高和体重记录"""
    latest_height = (
        session.query(HealthRecord)
        .filter(HealthRecord.child_id == child_id, HealthRecord.type == "height")
        .order_by(HealthRecord.date.desc())
        .first()
    )
    latest_weight = (
        session.query(HealthRecord)
        .filter(HealthRecord.child_id == child_id, HealthRecord.type == "weight")
        .order_by(HealthRecord.date.desc())
        .first()
    )
    return (latest_height.value if latest_height else None,
            latest_weight.value if latest_weight else None)


def _build_child_response(child: Child, session=None) -> ChildResponse:
    """构建 ChildResponse，从健康记录查询 current_height/weight"""
    age_months = calc_age_months(child.birth_date)
    allergies = []
    if child.allergies:
        try:
            allergies = json.loads(child.allergies)
        except:
            allergies = []

    current_height = None
    current_weight = None
    if session:
        current_height, current_weight = _get_current_health(session, child.id)

    return ChildResponse(
        id=child.id,
        name=child.name,
        birth_date=child.birth_date,
        gender=child.gender.value if child.gender else "male",
        birth_height=child.birth_height,
        birth_weight=child.birth_weight,
        allergies=allergies,
        notes=child.notes or "",
        avatar_color=child.avatar_color or "#FF9B5E",
        location=child.location or "hangzhou:binjiang",
        transport_mode=child.transport_mode or "metro",
        age_months=age_months,
        age_display=calc_age_display(age_months),
        current_height=current_height,
        current_weight=current_weight,
        created_at=child.created_at
    )


@router.get("", response_model=List[ChildResponse])
async def list_children():
    """获取所有孩子列表"""
    session = get_session()
    try:
        children = session.query(Child).all()
        return [_build_child_response(c, session) for c in children]
    finally:
        session.close()


@router.get("/{child_id}", response_model=ChildResponse)
async def get_child(child_id: str):
    """获取指定孩子档案"""
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, detail="孩子不存在")
        return _build_child_response(child, session)
    finally:
        session.close()


@router.post("", response_model=ChildResponse)
async def create_child(child: ChildCreate):
    """创建孩子档案"""
    session = get_session()
    try:
        child_id = f"ch_{uuid.uuid4().hex[:8]}"
        allergies_json = json.dumps(child.allergies or [], ensure_ascii=False)
        
        db_child = Child(
            id=child_id,
            name=child.name,
            birth_date=child.birth_date,
            gender=child.gender.value,
            birth_height=child.birth_height,
            birth_weight=child.birth_weight,
            allergies=allergies_json,
            notes=child.notes or "",
            avatar_color=child.avatar_color or "#FF9B5E"
        )
        
        session.add(db_child)
        session.commit()
        session.refresh(db_child)
        return _build_child_response(db_child, session)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()


@router.put("/{child_id}", response_model=ChildResponse)
async def update_child(child_id: str, child: ChildUpdate):
    """更新孩子档案"""
    session = get_session()
    try:
        db_child = session.query(Child).filter(Child.id == child_id).first()
        if not db_child:
            raise HTTPException(status_code=404, detail="孩子不存在")

        if child.name is not None:
            db_child.name = child.name
        if child.birth_date is not None:
            db_child.birth_date = child.birth_date
        if child.gender is not None:
            db_child.gender = child.gender.value
        if child.birth_height is not None:
            db_child.birth_height = child.birth_height
        if child.birth_weight is not None:
            db_child.birth_weight = child.birth_weight
        if child.allergies is not None:
            db_child.allergies = json.dumps(child.allergies, ensure_ascii=False)
        if child.notes is not None:
            db_child.notes = child.notes
        if child.avatar_color is not None:
            db_child.avatar_color = child.avatar_color
        if child.location is not None:
            db_child.location = child.location
        if child.transport_mode is not None:
            db_child.transport_mode = child.transport_mode

        # 触发 updated_at 自动更新（显式设置会让 onupdate 生效）
        from datetime import datetime
        db_child.updated_at = datetime.utcnow()

        session.commit()
        session.refresh(db_child)
        return _build_child_response(db_child, session)
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()


@router.delete("/{child_id}")
async def delete_child(child_id: str):
    """删除孩子档案"""
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, detail="孩子不存在")
        
        session.delete(child)
        session.commit()
        return {"code": 0, "message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()
