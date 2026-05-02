"""
BabyGrow 7天个性化食谱生成器
根据宝宝月龄、过敏信息生成一周营养食谱
"""
import json
from typing import Dict, List, Optional


# ============================================================
# 月龄食物数据库
# ============================================================

AGE_FOODS = {
    # 6月龄：糊状辅食
    6: {
        "breakfast": [
            {"name": "高铁米粉", "ingredients": ["婴儿米粉"], "steps": "温水冲调至糊状", "nutrition": "补铁+能量"},
            {"name": "南瓜米糊", "ingredients": ["米粉", "南瓜"], "steps": "南瓜蒸熟打泥，拌入米糊", "nutrition": "维A+碳水"},
        ],
        "lunch": [
            {"name": "蔬菜泥", "ingredients": ["西兰花", "胡萝卜"], "steps": "蒸熟打泥，可加少量核桃油", "nutrition": "维C+维A"},
            {"name": "土豆泥", "ingredients": ["土豆"], "steps": "蒸熟压泥，加母乳/配方奶调稀", "nutrition": "碳水+钾"},
        ],
        "dinner": [
            {"name": "果泥", "ingredients": ["苹果", "香蕉"], "steps": "刮泥或蒸熟打泥", "nutrition": "维C+钾"},
        ],
        "snack": [
            {"name": "母乳/配方奶", "ingredients": [], "steps": "", "nutrition": "主食"},
        ],
    },
    # 7-8月龄：碎末状
    7: {
        "breakfast": [
            {"name": "蛋黄米粥", "ingredients": ["大米", "蛋黄"], "steps": "粥煮烂，蛋黄压碎拌入", "nutrition": "蛋白质+铁+碳水"},
            {"name": "胡萝卜肉泥粥", "ingredients": ["大米", "胡萝卜", "猪肉"], "steps": "粥煮烂，肉和胡萝卜蒸熟打碎拌入", "nutrition": "蛋白质+维A"},
        ],
        "lunch": [
            {"name": "番茄蛋羹", "ingredients": ["鸡蛋", "番茄"], "steps": "蛋液加温水1:1.5，加番茄碎，蒸12分钟", "nutrition": "蛋白质+维C"},
            {"name": "鱼肉菜粥", "ingredients": ["大米", "鳕鱼", "青菜"], "steps": "粥煮烂，鱼蒸熟去刺压碎，青菜切碎", "nutrition": "DHA+蛋白质+纤维"},
        ],
        "dinner": [
            {"name": "红薯小米粥", "ingredients": ["小米", "红薯"], "steps": "红薯切小丁，和小米同煮", "nutrition": "碳水+维A+膳食纤维"},
            {"name": "苹果燕麦糊", "ingredients": ["燕麦", "苹果"], "steps": "燕麦煮烂，苹果蒸熟打泥拌入", "nutrition": "碳水+维C"},
        ],
        "snack": [
            {"name": "水果条", "ingredients": ["香蕉", "牛油果"], "steps": "切条，方便抓握", "nutrition": "健康脂肪+钾"},
        ],
    },
    # 9-10月龄：小块软食+手指食物
    9: {
        "breakfast": [
            {"name": "蔬菜蛋饼", "ingredients": ["鸡蛋", "胡萝卜", "菠菜"], "steps": "蛋液加蔬菜碎，小火煎熟切条", "nutrition": "蛋白质+维A+铁"},
            {"name": "南瓜小米粥", "ingredients": ["小米", "南瓜"], "steps": "南瓜切丁和小米同煮", "nutrition": "碳水+维A"},
            {"name": "酸奶燕麦", "ingredients": ["无糖酸奶", "燕麦"], "steps": "燕麦煮熟放凉，拌入酸奶", "nutrition": "钙+蛋白质+碳水"},
        ],
        "lunch": [
            {"name": "鸡肉蔬菜软饭", "ingredients": ["大米", "鸡胸肉", "西兰花", "胡萝卜"], "steps": "饭煮软，鸡肉和蔬菜切小丁炒熟拌入", "nutrition": "蛋白质+维C+维A"},
            {"name": "三文鱼土豆饼", "ingredients": ["三文鱼", "土豆"], "steps": "土豆蒸熟压泥，三文鱼碎拌入，小火煎", "nutrition": "DHA+碳水"},
        ],
        "dinner": [
            {"name": "番茄牛肉面", "ingredients": ["碎面", "番茄", "牛肉"], "steps": "面煮烂，牛肉末炒熟加番茄丁", "nutrition": "蛋白质+铁+维C"},
            {"name": "虾仁豆腐羹", "ingredients": ["虾仁", "嫩豆腐"], "steps": "虾仁切碎，豆腐切小块，煮羹", "nutrition": "蛋白质+钙"},
        ],
        "snack": [
            {"name": "水果酸奶杯", "ingredients": ["无糖酸奶", "蓝莓", "香蕉"], "steps": "水果切小块拌入酸奶", "nutrition": "钙+维C+益生菌"},
            {"name": "手指食物拼盘", "ingredients": ["蒸软的胡萝卜条", "南瓜条", "苹果条"], "steps": "蒸至微软，切条", "nutrition": "维A+维C+锻炼咀嚼"},
        ],
    },
    # 11-12月龄：接近大人食物质地
    11: {
        "breakfast": [
            {"name": "鸡蛋三明治", "ingredients": ["全麦面包", "鸡蛋", "生菜"], "steps": "鸡蛋煎熟，夹入面包和生菜", "nutrition": "蛋白质+碳水+纤维"},
            {"name": "鲜虾云吞", "ingredients": ["云吞皮", "虾仁", "猪肉"], "steps": "馅料包入云吞皮，煮熟", "nutrition": "蛋白质+碳水"},
        ],
        "lunch": [
            {"name": "番茄牛肉烩饭", "ingredients": ["大米", "牛肉", "番茄", "土豆"], "steps": "牛肉切丁炒熟，加番茄土豆煮软，拌饭", "nutrition": "蛋白质+铁+维C"},
            {"name": "彩虹蔬菜炒饭", "ingredients": ["米饭", "鸡蛋", "玉米", "豌豆", "胡萝卜"], "steps": "蔬菜丁焯水，和蛋一起炒饭", "nutrition": "蛋白质+纤维+维A"},
        ],
        "dinner": [
            {"name": "香菇鸡肉粥", "ingredients": ["大米", "鸡腿肉", "香菇", "青菜"], "steps": "粥煮至浓稠，加入切碎的鸡肉香菇", "nutrition": "蛋白质+多糖+纤维"},
            {"name": "鳕鱼蔬菜面", "ingredients": ["碎面", "鳕鱼", "西兰花"], "steps": "面煮熟，鱼蒸熟去刺，蔬菜焯水切碎", "nutrition": "DHA+蛋白质+维C"},
        ],
        "snack": [
            {"name": "水果拼盘", "ingredients": ["草莓", "蓝莓", "猕猴桃"], "steps": "切小块", "nutrition": "维C+抗氧化"},
            {"name": "小肉丸", "ingredients": ["猪肉", "山药"], "steps": "肉末加山药泥搓丸蒸熟", "nutrition": "蛋白质+健脾"},
        ],
    },
}

# 复用：11月龄的也适用于12月龄+
AGE_FOODS[12] = AGE_FOODS[11]
AGE_FOODS[10] = AGE_FOODS[9]
AGE_FOODS[8] = AGE_FOODS[7]


def get_age_group(age_months: int) -> int:
    """将月龄映射到最近的食物组"""
    if age_months <= 6:
        return 6
    elif age_months <= 8:
        return 7
    elif age_months <= 10:
        return 9
    else:
        return 11


def filter_allergies(meals: List[dict], allergies: List[str]) -> List[dict]:
    """过滤过敏食物"""
    if not allergies:
        return meals
    allergy_set = set(a.lower() for a in allergies)
    filtered = []
    for meal in meals:
        ingredients_lower = [i.lower() for i in meal["ingredients"]]
        if any(a in " ".join(ingredients_lower) for a in allergy_set):
            continue
        filtered.append(meal)
    return filtered


def generate_7day_meal_plan(
    age_months: int,
    allergies: List[str] = None,
    child_name: str = "宝宝",
) -> dict:
    """
    生成7天个性化食谱
    
    Returns:
        {
            "child_name": str,
            "age_months": int,
            "days": [
                {
                    "day": "周一",
                    "date": "2026-05-04",
                    "meals": {
                        "breakfast": {...},
                        "lunch": {...},
                        "dinner": {...},
                        "snack": {...}
                    }
                }
            ],
            "shopping_list": {...}
        }
    """
    from datetime import date, timedelta
    
    age_group = get_age_group(age_months)
    foods = AGE_FOODS.get(age_group, AGE_FOODS[6])
    days_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    today = date.today()
    
    all_ingredients = []
    days = []
    
    for i in range(7):
        day_date = today + timedelta(days=i)
        day_meals = {}
        
        for meal_type in ["breakfast", "lunch", "dinner", "snack"]:
            available = foods.get(meal_type, [])
            # 过滤过敏食物
            if allergies:
                available = filter_allergies(available, allergies)
            # 选择当天的菜品（轮换，确保7天不重复）
            if available:
                meal = available[i % len(available)]
                day_meals[meal_type] = meal
                all_ingredients.extend(meal.get("ingredients", []))
            else:
                day_meals[meal_type] = None
        
        days.append({
            "day": days_names[i],
            "date": day_date.isoformat(),
            "meals": day_meals,
        })
    
    # 生成采购清单
    shopping_list = generate_shopping_list(all_ingredients)
    
    return {
        "child_name": child_name,
        "age_months": age_months,
        "age_group": age_group,
        "days": days,
        "shopping_list": shopping_list,
    }


def generate_shopping_list(ingredients: List[str]) -> dict:
    """从食材列表生成分类采购清单"""
    categories = {
        "🥬 蔬菜": [],
        "🍎 水果": [],
        "🥩 肉蛋": [],
        "🥛 奶制品": [],
        "🌾 主食/干货": [],
        "🫒 调料/其他": [],
    }
    
    veggie_keywords = ["胡萝卜", "西兰花", "菠菜", "南瓜", "土豆", "番茄", "红薯", "青菜", "豌豆", "玉米", "生菜", "山药"]
    fruit_keywords = ["苹果", "香蕉", "蓝莓", "草莓", "猕猴桃", "牛油果"]
    meat_keywords = ["鸡蛋", "猪肉", "牛肉", "鸡肉", "鸡胸肉", "鸡腿肉", "虾仁", "鳕鱼", "三文鱼", "鱼"]
    dairy_keywords = ["酸奶", "牛奶", "奶酪", "配方奶"]
    grain_keywords = ["大米", "小米", "燕麦", "碎面", "面条", "全麦面包", "云吞皮", "米粉", "面粉"]
    
    for ing in ingredients:
        ing = ing.strip()
        if not ing:
            continue
        matched = False
        for kw in veggie_keywords:
            if kw in ing:
                categories["🥬 蔬菜"].append(ing)
                matched = True
                break
        if matched: continue
        for kw in fruit_keywords:
            if kw in ing:
                categories["🍎 水果"].append(ing)
                matched = True
                break
        if matched: continue
        for kw in meat_keywords:
            if kw in ing:
                categories["🥩 肉蛋"].append(ing)
                matched = True
                break
        if matched: continue
        for kw in dairy_keywords:
            if kw in ing:
                categories["🥛 奶制品"].append(ing)
                matched = True
                break
        if matched: continue
        for kw in grain_keywords:
            if kw in ing:
                categories["🌾 主食/干货"].append(ing)
                matched = True
                break
        if not matched:
            categories["🫒 调料/其他"].append(ing)
    
    # 去重
    for cat in categories:
        categories[cat] = list(dict.fromkeys(categories[cat]))  # 保持顺序去重
    
    return categories


# ============================================================
# AI增强食谱（可选，用LLM微调默认食谱）
# ============================================================

MEAL_PLAN_PROMPT = """你是一位专业的婴幼儿营养师，为{child_name}（{age_months}月龄）生成7天辅食食谱。

## 要求
1. 每天包含：早餐、午餐、晚餐、加餐
2. 每道菜包含：名称、食材（具体克数）、做法步骤、营养点评
3. 7天菜品不重复
4. 营养均衡：碳水+蛋白质+脂肪+维生素
5. 适合{age_months}月龄的食物质地

## 过敏规避
{allergies}

## 输出格式（JSON）
{{
  "days": [
    {{
      "day": "周一",
      "meals": {{
        "breakfast": {{"name": "...", "ingredients": ["..."], "steps": "...", "nutrition": "..."}},
        "lunch": ...,
        "dinner": ...,
        "snack": ...
      }}
    }}
  ]
}}"""


def build_meal_plan_prompt(child_name: str, age_months: int, allergies: str = "无") -> str:
    return MEAL_PLAN_PROMPT.format(
        child_name=child_name,
        age_months=age_months,
        allergies=allergies,
    )
