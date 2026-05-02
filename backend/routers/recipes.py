"""
BabyGrow 食谱路由
提供辅食食谱查询和推荐 API
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import date

from services.knowledge_service import get_recipes, get_recipe_by_id
from models.database import get_session, Child

router = APIRouter(prefix="/api/v1", tags=["recipes"])


# ============ Schemas ============

class IngredientItem(BaseModel):
    name: str
    amount: str
    note: Optional[str] = None


class RecipeResponse(BaseModel):
    id: str
    name: str
    age: str
    ingredients: List[IngredientItem]
    steps: List[str]
    tips: Optional[str] = None


class AgeGroupResponse(BaseModel):
    age_group: str
    name: str
    description: str
    meals: List[RecipeResponse]


class RecipesListResponse(BaseModel):
    age_groups: List[AgeGroupResponse]
    total_count: int
    principles: dict


class RecipeRecommendResponse(BaseModel):
    breakfast: Optional[RecipeResponse] = None
    lunch: Optional[RecipeResponse] = None
    dinner: Optional[RecipeResponse] = None
    snack: Optional[RecipeResponse] = None
    daily_schedule: dict


# ============ 辅助函数 ============

def _calc_age_months(birth_date: date) -> int:
    """计算月龄"""
    today = date.today()
    months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
    if today.day < birth_date.day:
        months -= 1
    return max(0, months)


def _age_to_group(age_months: int) -> str:
    """根据月龄返回食谱年龄组"""
    if age_months < 7:
        return "6-7"
    elif age_months < 9:
        return "7-9"
    elif age_months < 12:
        return "9-12"
    elif age_months < 24:
        return "1-2"
    else:
        return "2-3"


def _parse_recipe(r: dict) -> RecipeResponse:
    return RecipeResponse(
        id=r.get("id", ""),
        name=r.get("name", ""),
        age=r.get("age", ""),
        ingredients=[IngredientItem(**i) for i in r.get("ingredients", [])],
        steps=r.get("steps", []),
        tips=r.get("tips")
    )


# ============ 路由 ============

@router.get("/recipes", response_model=RecipesListResponse)
async def list_recipes(
    age_months: Optional[int] = Query(None, description="孩子月龄，不传则返回全部")
):
    """
    获取食谱列表
    - 不传 age_months：返回所有年龄段食谱
    - 传 age_months：返回对应年龄段的食谱
    """
    if age_months is not None:
        ag = _age_to_group(age_months)
        data = get_recipes(ag)
        groups = []
        for key, group_data in data.get("all_recipes", {}).items():
            if key == ag:
                groups.append(AgeGroupResponse(
                    age_group=key,
                    name=group_data.get("name", ""),
                    description=group_data.get("description", ""),
                    meals=[_parse_recipe(m) for m in group_data.get("meals", [])]
                ))
        total = sum(len(g.meals) for g in groups)
        return RecipesListResponse(
            age_groups=groups,
            total_count=total,
            principles=data.get("principles", {})
        )
    else:
        # 返回所有年龄段
        all_data = get_recipes("6-7")
        age_groups_list = []
        total = 0
        for key, group_data in all_data.get("all_recipes", {}).items():
            meals = [_parse_recipe(m) for m in group_data.get("meals", [])]
            total += len(meals)
            age_groups_list.append(AgeGroupResponse(
                age_group=key,
                name=group_data.get("name", ""),
                description=group_data.get("description", ""),
                meals=meals
            ))
        return RecipesListResponse(
            age_groups=age_groups_list,
            total_count=total,
            principles=all_data.get("principles", {})
        )


@router.get("/recipes/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(recipe_id: str):
    """根据ID获取食谱详情"""
    recipe = get_recipe_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="食谱不存在")
    return _parse_recipe(recipe)


@router.get("/children/{child_id}/recipes/recommend", response_model=RecipeRecommendResponse)
async def recommend_recipes(child_id: str):
    """
    获取孩子的食谱推荐
    根据孩子月龄返回三餐推荐和每日饮食安排
    """
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, detail="孩子不存在")

        ag = _age_to_group(_calc_age_months(child.birth_date))
        data = get_recipes(ag)
        meals = data.get("recipes", {}).get("meals", [])
        schedule = data.get("daily_schedule", {})

        # 取该年龄段的前几个食谱作为三餐推荐
        breakfast = _parse_recipe(meals[0]) if len(meals) > 0 else None
        lunch = _parse_recipe(meals[1]) if len(meals) > 1 else None
        dinner = _parse_recipe(meals[2]) if len(meals) > 2 else None
        snack = _parse_recipe(meals[3]) if len(meals) > 3 else None

        return RecipeRecommendResponse(
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner,
            snack=snack,
            daily_schedule=schedule
        )
    finally:
        session.close()


@router.get("/children/{child_id}/recipes/shopping-list")
async def get_shopping_list(child_id: str):
    """
    生成采购清单
    根据孩子月龄和食谱推荐，生成需要购买的食材清单
    """
    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, detail="孩子不存在")

        ag = _age_to_group(_calc_age_months(child.birth_date))
        data = get_recipes(ag)
        meals = data.get("recipes", {}).get("meals", [])

        # 收集所有食材
        shopping = {}
        for meal in meals[:6]:  # 取推荐的前6个食谱
            for ing in meal.get("ingredients", []):
                name = ing.get("name", "")
                if name and name not in shopping:
                    shopping[name] = {
                        "name": name,
                        "amount": ing.get("amount", ""),
                        "note": ing.get("note", ""),
                        "from_recipes": [meal.get("name", "")]
                    }
                elif name in shopping:
                    shopping[name]["from_recipes"].append(meal.get("name", ""))

        # 按类别分组
        categories = {
            "肉禽": ["鸡", "猪", "牛", "羊", "鱼", "虾", "肉", "肝"],
            "蔬菜": ["南瓜", "土豆", "胡萝卜", "西兰花", "青菜", "菠菜", "番茄", "冬瓜", "山药", "香菇", "豌豆", "玉米", "黄瓜", "西葫芦", "洋葱"],
            "水果": ["苹果", "香蕉", "梨", "橙", "蓝莓"],
            "主食": ["米", "小米", "面", "面条", "馄饨", "意面", "面粉", "燕麦"],
            "蛋奶": ["鸡蛋", "蛋黄", "牛奶", "配方奶", "豆腐"],
            "其他": []
        }

        categorized = {k: [] for k in categories}
        uncategorized = []

        for item in shopping.values():
            name = item["name"]
            categorized_flag = False
            for cat, keywords in categories.items():
                if cat == "其他":
                    continue
                for kw in keywords:
                    if kw in name:
                        categorized[cat].append(item)
                        categorized_flag = True
                        break
                if categorized_flag:
                    break
            if not categorized_flag:
                categorized["其他"].append(item)

        return {
            "child_id": child_id,
            "child_age_months": _calc_age_months(child.birth_date),
            "shopping_list": {k: v for k, v in categorized.items() if v},
            "total_items": len(shopping),
            "tips": "食材采购后，按年龄添加，注意观察3天无过敏反应再继续"
        }
    finally:
        session.close()


# ============ 7天个性化食谱 ============

@router.get("/children/{child_id}/meal-plan")
async def get_7day_meal_plan(child_id: str):
    """生成7天个性化食谱"""
    from services.meal_planner import generate_7day_meal_plan as gen_plan
    import json as json_mod

    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, detail="孩子不存在")

        age_months = _calc_age_months(child.birth_date)
        allergies = []
        if child.allergies:
            try:
                allergies = json_mod.loads(child.allergies) if isinstance(child.allergies, str) else child.allergies
            except:
                allergies = []

        plan = gen_plan(
            age_months=age_months,
            allergies=allergies,
            child_name=child.name,
        )
        return plan
    finally:
        session.close()


@router.get("/children/{child_id}/shopping-list-gen")
async def generate_shopping_list_from_plan(child_id: str):
    """从7天食谱生成采购清单"""
    from services.meal_planner import generate_7day_meal_plan as gen_plan
    import json as json_mod

    session = get_session()
    try:
        child = session.query(Child).filter(Child.id == child_id).first()
        if not child:
            raise HTTPException(status_code=404, detail="孩子不存在")

        age_months = _calc_age_months(child.birth_date)
        allergies = []
        if child.allergies:
            try:
                allergies = json_mod.loads(child.allergies) if isinstance(child.allergies, str) else child.allergies
            except:
                allergies = []

        plan = gen_plan(age_months=age_months, allergies=allergies, child_name=child.name)
        return {
            "child_name": child.name,
            "age_months": age_months,
            "shopping_list": plan["shopping_list"],
        }
    finally:
        session.close()
