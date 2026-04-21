from fastapi import APIRouter, HTTPException
from typing import List
from datetime import date
import uuid
import json

from models.database import get_session, Child
from models.schemas import ChildCreate, ChildUpdate, ChildResponse

router = APIRouter(prefix="/api/v1/children", tags=["children"])


def calc_age_months(birth_date: date) -> int:
    """计算月龄"""
    today = date.today()
    months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
    if today.day < birth_date.day:
        months -= 1
    return max(0, months)


def calc_age_display(age_months: int) -> str:
    """计算月龄显示"""
    if age_months < 12:
        return f"{age_months}个月"
    years = age_months // 12
    months = age_months % 12
    if months == 0:
        return f"{years}岁"
    return f"{years}岁{months}个月"


@router.get("", response_model=List[ChildResponse])
async def list_children():
    """获取所有孩子列表"""
    session = get_session()
    try:
        children = session.query(Child).all()
        result = []
        for c in children:
            age_months = calc_age_months(c.birth_date)
            allergies = []
            if c.allergies:
                try:
                    allergies = json.loads(c.allergies)
                except:
                    allergies = []
            result.append(ChildResponse(
                id=c.id,
                name=c.name,
                birth_date=c.birth_date,
                gender=c.gender.value if c.gender else "male",
                birth_height=c.birth_height,
                birth_weight=c.birth_weight,
                allergies=allergies,
                notes=c.notes or "",
                avatar_color=c.avatar_color or "#FF9B5E",
                age_months=age_months,
                age_display=calc_age_display(age_months),
                created_at=c.created_at
            ))
        return result
    finally:
        session.close()


@router.get("/{child_id}", response_model=ChildResponse)
async def get_child(child_id: str):
    """获取指定孩子档案"""
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, message="孩子不存在")
        
        age_months = calc_age_months(child.birth_date)
        allergies = []
        if child.allergies:
            try:
                allergies = json.loads(child.allergies)
            except:
                allergies = []
        
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
            age_months=age_months,
            age_display=calc_age_display(age_months),
            created_at=child.created_at
        )
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
        
        age_months = calc_age_months(db_child.birth_date)
        return ChildResponse(
            id=db_child.id,
            name=db_child.name,
            birth_date=db_child.birth_date,
            gender=db_child.gender.value,
            birth_height=db_child.birth_height,
            birth_weight=db_child.birth_weight,
            allergies=child.allergies or [],
            notes=db_child.notes or "",
            avatar_color=db_child.avatar_color or "#FF9B5E",
            age_months=age_months,
            age_display=calc_age_display(age_months),
            created_at=db_child.created_at
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, message=str(e))
    finally:
        session.close()


@router.put("/{child_id}", response_model=ChildResponse)
async def update_child(child_id: str, child: ChildUpdate):
    """更新孩子档案"""
    session = get_session()
    try:
        db_child = session.query(Child).filter(Child.id == child_id).first()
        if not db_child:
            raise HTTPException(status_code=404, message="孩子不存在")
        
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
        
        session.commit()
        session.refresh(db_child)
        
        age_months = calc_age_months(db_child.birth_date)
        allergies = []
        if db_child.allergies:
            try:
                allergies = json.loads(db_child.allergies)
            except:
                allergies = []
        
        return ChildResponse(
            id=db_child.id,
            name=db_child.name,
            birth_date=db_child.birth_date,
            gender=db_child.gender.value,
            birth_height=db_child.birth_height,
            birth_weight=db_child.birth_weight,
            allergies=allergies,
            notes=db_child.notes or "",
            avatar_color=db_child.avatar_color or "#FF9B5E",
            age_months=age_months,
            age_display=calc_age_display(age_months),
            created_at=db_child.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, message=str(e))
    finally:
        session.close()


@router.delete("/{child_id}")
async def delete_child(child_id: str):
    """删除孩子档案"""
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, message="孩子不存在")
        
        session.delete(child)
        session.commit()
        return {"code": 0, "message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, message=str(e))
    finally:
        session.close()
