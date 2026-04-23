"""
BabyGrow 发育里程碑路由
提供里程碑查询和记录 API
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime

from models.database import get_session, Child, MilestoneRecord
from models.schemas import MilestoneRecordCreate, MilestoneRecordResponse
from services.knowledge_service import get_milestone, get_milestone_items

router = APIRouter(prefix="/api/v1/children", tags=["milestones"])


def _build_milestone_response(child_id: str, age_months: int) -> dict:
    """构建里程碑响应，包含当前阶段+下一阶段提示"""
    data = get_milestone(age_months)
    group_info = data.get("group_info", {})
    all_milestones = data.get("all_milestones", {})

    # 找下一个阶段
    group_order = ["0-3", "3-6", "6-12", "12-18", "18-24", "2-3"]
    current_idx = group_order.index(data["age_group"]) if data["age_group"] in group_order else 0
    next_group = group_order[current_idx + 1] if current_idx + 1 < len(group_order) else None
    next_info = all_milestones.get(next_group, {}) if next_group else {}

    return {
        "child_id": child_id,
        "age_months": age_months,
        "current_group": data["age_group"],
        "group_name": group_info.get("name", ""),
        "group_description": group_info.get("description", ""),
        "items": group_info.get("items", []),
        "next_group": next_group,
        "next_group_name": next_info.get("name", "") if next_info else None,
        "next_group_description": next_info.get("description", "") if next_info else None,
    }


@router.get("/{child_id}/milestones")
async def get_child_milestones(child_id: str):
    """
    获取孩子的发育里程碑
    返回当前月龄对应的里程碑，以及下一个阶段预览
    """
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, detail="孩子不存在")

        from datetime import date
        age_months = (date.today().year - child.birth_date.year) * 12 + (date.today().month - child.birth_date.month)
        if date.today().day < child.birth_date.day:
            age_months -= 1
        age_months = max(0, age_months)

        result = _build_milestone_response(child_id, age_months)

        # 附加已记录的里程碑
        records = session.query(MilestoneRecord).filter(
            MilestoneRecord.child_id == child_id
        ).all()
        result["achieved_ids"] = [r.milestone_id for r in records]

        return result
    finally:
        session.close()


@router.post("/{child_id}/milestones/{milestone_id}/achieve")
async def achieve_milestone(child_id: str, milestone_id: str):
    """标记里程碑为已达成"""
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, detail="孩子不存在")

        # 检查是否已记录
        existing = session.query(MilestoneRecord).filter(
            MilestoneRecord.child_id == child_id,
            MilestoneRecord.milestone_id == milestone_id
        ).first()

        if existing:
            return {"message": "已达成", "id": existing.id}

        record = MilestoneRecord(
            id=f"mr_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            child_id=child_id,
            milestone_id=milestone_id,
            achieved=True,
            achieved_date=datetime.now().date()
        )
        session.add(record)
        session.commit()

        return {"message": "已记录", "id": record.id}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


@router.delete("/{child_id}/milestones/{milestone_id}/achieve")
async def unachieve_milestone(child_id: str, milestone_id: str):
    """取消里程碑达成记录"""
    session = get_session()
    try:
        record = session.query(MilestoneRecord).filter(
            MilestoneRecord.child_id == child_id,
            MilestoneRecord.milestone_id == milestone_id
        ).first()

        if record:
            session.delete(record)
            session.commit()

        return {"message": "已取消"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
