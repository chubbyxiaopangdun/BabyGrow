"""
BabyGrow 知识库加载器
提供育儿知识查询接口，供AI服务调用
"""
import json
import os
from typing import Dict, List, Any, Optional

# 知识库路径
KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "knowledge")


def _load_json(filename: str) -> Dict:
    """加载知识库JSON文件"""
    filepath = os.path.join(KNOWLEDGE_DIR, filename)
    if not os.path.exists(filepath):
        return {}
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def get_milestone(age_months: int) -> Dict[str, Any]:
    """获取指定月龄的发育里程碑"""
    data = _load_json("milestones.json")
    milestones = data.get("milestones", {})

    # 根据月龄确定分组
    if age_months < 3:
        group = "0-3"
    elif age_months < 6:
        group = "3-6"
    elif age_months < 12:
        group = "6-12"
    elif age_months < 18:
        group = "12-18"
    elif age_months < 24:
        group = "18-24"
    else:
        group = "2-3"

    return {
        "age_group": group,
        "group_info": milestones.get(group, {}),
        "all_milestones": milestones
    }


def get_milestone_items(age_months: int) -> List[Dict]:
    """获取指定月龄的具体里程碑列表"""
    result = get_milestone(age_months)
    group_info = result.get("group_info", {})
    return group_info.get("items", [])


def get_recipes(age_group: str) -> Dict[str, Any]:
    """获取指定月龄段的食谱"""
    data = _load_json("recipes.json")
    recipes = data.get("recipes", {})

    # 匹配年龄组
    age_mapping = {
        "6-7": "6-7",
        "7-9": "7-9",
        "9-12": "9-12",
        "1-2": "1-2",
        "2-3": "2-3"
    }

    return {
        "recipes": recipes.get(age_group, {}),
        "all_recipes": recipes,
        "principles": data.get("principles", {})
    }


def get_recipe_by_id(recipe_id: str) -> Optional[Dict]:
    """根据ID获取食谱详情"""
    data = _load_json("recipes.json")
    recipes = data.get("recipes", {})

    for group_key, group_data in recipes.items():
        for recipe in group_data.get("meals", []):
            if recipe.get("id") == recipe_id:
                return recipe
    return None


def get_sleep_sop(age_months: int) -> Dict[str, Any]:
    """获取指定月龄的哄睡SOP"""
    data = _load_json("sleep_sop.json")
    sops = data.get("sops", {})

    # 确定SOP分组
    if age_months < 3:
        group = "0-3m"
    elif age_months < 6:
        group = "3-6m"
    elif age_months < 12:
        group = "6-12m"
    else:
        group = "1-2y"

    return {
        "sop": sops.get(group, {}),
        "sleep_reference": data.get("sleep_reference", {}),
        "common_issues": data.get("common_issues", {}),
        "safety_tips": data.get("safety_tips", [])
    }


def get_health_guide(topic: str) -> Optional[Dict]:
    """获取健康护理指南"""
    data = _load_json("health_guides.json")
    issues = data.get("common_issues", {})

    # 模糊匹配
    topic_lower = topic.lower()
    for key, value in issues.items():
        if topic_lower in key.lower():
            return {"topic": key, "guide": value}

    return None


def get_health_guides_all() -> Dict[str, Any]:
    """获取所有健康指南"""
    data = _load_json("health_guides.json")
    return {
        "common_issues": data.get("common_issues", {}),
        "vaccination": data.get("vaccination", {}),
        "growth_reference": data.get("growth_reference", {}),
        "daily_care": data.get("daily_care", {}),
        "disclaimers": data.get("disclaimers", [])
    }


def get_daily_schedule(age_months: int) -> Dict[str, Any]:
    """获取每日饮食安排"""
    data = _load_json("recipes.json")
    schedules = data.get("daily_schedule", {})

    if age_months < 7:
        return {"schedule": schedules.get("6-7m", {})}
    elif age_months < 9:
        return {"schedule": schedules.get("7-9m", {})}
    elif age_months < 12:
        return {"schedule": schedules.get("9-12m", {})}
    else:
        return {"schedule": schedules.get("1-2y", {})}


def search_knowledge(query: str) -> List[Dict[str, Any]]:
    """
    全局搜索知识库
    返回包含相关内容的条目
    """
    results = []
    query_lower = query.lower()

    # 搜索里程碑
    milestones_data = _load_json("milestones.json")
    for group_key, group_data in milestones_data.get("milestones", {}).items():
        for item in group_data.get("items", []):
            if (query_lower in item.get("title", "").lower() or
                    query_lower in item.get("description", "").lower() or
                    query_lower in item.get("category", "").lower()):
                results.append({
                    "type": "milestone",
                    "source": "milestones.json",
                    "age_group": group_key,
                    "item": item
                })

    # 搜索食谱
    recipes_data = _load_json("recipes.json")
    for group_key, group_data in recipes_data.get("recipes", {}).items():
        for recipe in group_data.get("meals", []):
            if (query_lower in recipe.get("name", "").lower() or
                    query_lower in str(recipe.get("ingredients", [])).lower()):
                results.append({
                    "type": "recipe",
                    "source": "recipes.json",
                    "age_group": group_key,
                    "item": recipe
                })

    # 搜索健康指南
    health_data = _load_json("health_guides.json")
    for topic, guide in health_data.get("common_issues", {}).items():
        if query_lower in topic.lower():
            results.append({
                "type": "health",
                "source": "health_guides.json",
                "topic": topic,
                "guide": guide
            })

    return results


def get_context_for_age(age_months: int, context_type: str = "all") -> Dict[str, Any]:
    """
    获取指定月龄的完整上下文，用于AI生成计划

    Args:
        age_months: 月龄
        context_type: "all" | "milestone" | "recipe" | "sleep" | "health"
    """
    result = {
        "age_months": age_months,
        "milestones": [],
        "recipes": [],
        "sleep_sop": {},
        "daily_schedule": {}
    }

    if context_type in ("all", "milestone"):
        result["milestones"] = get_milestone_items(age_months)

    if context_type in ("all", "recipe"):
        # 确定年龄组
        if age_months < 7:
            ag = "6-7"
        elif age_months < 9:
            ag = "7-9"
        elif age_months < 12:
            ag = "9-12"
        elif age_months < 24:
            ag = "1-2"
        else:
            ag = "2-3"
        result["recipes"] = get_recipes(ag)
        result["daily_schedule"] = get_daily_schedule(age_months)

    if context_type in ("all", "sleep"):
        result["sleep_sop"] = get_sleep_sop(age_months)

    return result
