"""
BabyGrow 每日计划生成引擎
根据孩子月龄、喂养记录、睡眠记录生成个性化每日计划
"""
import json
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
from services.knowledge_service import get_milestone_items, get_recipes, get_sleep_sop, get_context_for_age


class DailyPlanner:
    """每日计划生成器"""

    # 0-3岁各月龄的标准作息
    SLEEP_SCHEDULE = {
        # 0-3个月
        "0-3": {
            "wake": "07:00",
            "morning_nap": ("08:30", "10:00"),
            "afternoon_nap1": ("12:00", "14:00"),
            "afternoon_nap2": ("16:00", "17:00"),
            "night_sleep": "19:30"
        },
        # 3-6个月
        "3-6": {
            "wake": "07:00",
            "morning_nap": ("09:00", "10:30"),
            "afternoon_nap": ("13:00", "15:00"),
            "night_sleep": "20:00"
        },
        # 6-12个月
        "6-12": {
            "wake": "07:00",
            "morning_nap": ("09:30", "11:00"),
            "afternoon_nap": ("13:30", "15:00"),
            "night_sleep": "20:30"
        },
        # 12-18个月
        "12-18": {
            "wake": "07:00",
            "morning_nap": ("10:00", "11:30"),
            "afternoon_nap": ("14:00", "15:30"),
            "night_sleep": "21:00"
        },
        # 18-24个月
        "18-24": {
            "wake": "07:00",
            "afternoon_nap": ("13:00", "15:00"),
            "night_sleep": "21:00"
        },
        # 2-3岁
        "2-3": {
            "wake": "07:30",
            "afternoon_nap": ("13:30", "15:30"),
            "night_sleep": "21:30"
        }
    }

    # 各月龄奶量参考
    MILK_SCHEDULE = {
        "0-3": {"times": 7, "amount": 120, "unit": "ml"},
        "3-6": {"times": 6, "amount": 150, "unit": "ml"},
        "6-12": {"times": 4, "amount": 180, "unit": "ml"},
        "12-18": {"times": 3, "amount": 200, "unit": "ml"},
        "18-24": {"times": 2, "amount": 200, "unit": "ml"},
        "2-3": {"times": 2, "amount": 350, "unit": "ml"}
    }

    # 辅食安排
    MEAL_SCHEDULE = {
        "6-12": [
            {"time": "08:00", "name": "早餐", "type": "solid"},
            {"time": "12:00", "name": "午餐", "type": "solid"},
            {"time": "18:00", "name": "晚餐", "type": "solid"}
        ],
        "12-24": [
            {"time": "08:00", "name": "早餐", "type": "solid"},
            {"time": "12:00", "name": "午餐", "type": "solid"},
            {"time": "18:30", "name": "晚餐", "type": "solid"}
        ],
        "2-3": [
            {"time": "08:00", "name": "早餐", "type": "solid"},
            {"time": "12:00", "name": "午餐", "type": "solid"},
            {"time": "18:30", "name": "晚餐", "type": "solid"}
        ]
    }

    def get_age_group(self, age_months: int) -> str:
        """根据月龄获取作息分组"""
        if age_months < 3:
            return "0-3"
        elif age_months < 6:
            return "3-6"
        elif age_months < 12:
            return "6-12"
        elif age_months < 18:
            return "12-18"
        elif age_months < 24:
            return "18-24"
        else:
            return "2-3"

    def get_milk_schedule(self, age_months: int) -> List[Dict]:
        """获取今日奶量安排"""
        for age_range, schedule in self.MILK_SCHEDULE.items():
            start, end = map(int, age_range.split("-"))
            if start <= age_months < end:
                times = schedule["times"]
                amount = schedule["amount"]
                unit = schedule["unit"]
                break
        else:
            times, amount, unit = 1, 200, "ml"

        return {
            "times": times,
            "amount": amount,
            "unit": unit
        }

    def get_meal_schedule(self, age_months: int) -> List[Dict]:
        """获取今日辅食安排"""
        if age_months < 6:
            return []
        elif age_months < 12:
            return self.MEAL_SCHEDULE["6-12"]
        elif age_months < 24:
            return self.MEAL_SCHEDULE["12-24"]
        else:
            return self.MEAL_SCHEDULE["2-3"]

    def _get_recipes_for_age(self, age_months: int) -> List[Dict]:
        """从知识库获取适龄食谱"""
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
        try:
            data = get_recipes(ag)
            return data.get("recipes", {}).get("meals", [])
        except Exception:
            return []

    def _get_milestones_for_age(self, age_months: int) -> List[Dict]:
        """从知识库获取适龄发育里程碑"""
        try:
            return get_milestone_items(age_months)
        except Exception:
            return []

    def _get_sleep_sop_for_age(self, age_months: int) -> Dict:
        """从知识库获取哄睡SOP"""
        try:
            return get_sleep_sop(age_months)
        except Exception:
            return {}

    def get_outdoor_time(self, age_months: int) -> int:
        """获取建议户外时长（分钟）"""
        if age_months < 6:
            return 30
        elif age_months < 12:
            return 60
        else:
            return 90

    def generate_plan(
        self,
        child_name: str,
        age_months: int,
        current_date: date,
        today_feed_records: List[Dict] = [],
        today_sleep_records: List[Dict] = [],
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        生成每日计划

        Args:
            child_name: 孩子名字
            age_months: 月龄
            current_date: 计划日期
            today_feed_records: 今日已记录喂养
            today_sleep_records: 今日已记录睡眠
            context: 知识库上下文 dict（来自 KNOWLEDGE.buildSOPContext），
                     包含 season, isWeekend, framework, seasonalIngredients,
                     nearbyParks, nearbyIndoor, nearbyHospitals, metro, 
                     activityTemplates, specialScenarios

        Returns:
            包含items、reminders、ai_tips的字典
        """
        age_group = self.get_age_group(age_months)
        schedule = self.SLEEP_SCHEDULE.get(age_group, self.SLEEP_SCHEDULE["6-12"])
        milk_schedule = self.get_milk_schedule(age_months)
        meal_schedule = self.get_meal_schedule(age_months)
        outdoor_minutes = self.get_outdoor_time(age_months)

        # 从知识库获取真实数据
        kb_milestones = get_milestone_items(age_months)
        kb_sleep_sop = get_sleep_sop(age_months)
        kb_sop = kb_sleep_sop.get("sop", {})

        # 解包知识库上下文
        kb = context or {}
        season = kb.get("season", self._get_season(current_date))
        is_weekend = kb.get("isWeekend", current_date.weekday() >= 5)
        framework = kb.get("framework", {})
        seasonal_ingredients = kb.get("seasonalIngredients", [])
        nearby_parks = kb.get("nearbyParks", [])
        nearby_indoor = kb.get("nearbyIndoor", [])
        nearby_hospitals = kb.get("nearbyHospitals", [])
        activity_templates = kb.get("activityTemplates", {})
        special_scenarios = kb.get("specialScenarios", {})

        # 框架时间（覆盖默认时间）
        wake_time = framework.get("wake", schedule.get("wake", "07:00"))
        night_sleep_time = framework.get("sleep", schedule.get("night_sleep", "20:00"))

        # 应季食材前3
        top_ingredients = [i.get("name", "") for i in seasonal_ingredients[:3]] if seasonal_ingredients else []

        # 推荐公园（取前2）
        recommended_parks = nearby_parks[:2] if nearby_parks else []

        # 户外时长决策
        outdoor_decision = kb.get("outdoorDecision", {})
        outdoor_ok = outdoor_decision.get("go_outdoor", True) if outdoor_decision else True
        outdoor_reason = outdoor_decision.get("reason", "") if outdoor_decision else ""

        # 确定辅食年龄组
        if age_months < 7:
            kb_age_group = "6-7"
        elif age_months < 9:
            kb_age_group = "7-9"
        elif age_months < 12:
            kb_age_group = "9-12"
        elif age_months < 24:
            kb_age_group = "1-2"
        else:
            kb_age_group = "2-3"
        kb_recipes = get_recipes(kb_age_group)
        kb_meals = kb_recipes.get("recipes", {}).get("meals", []) if kb_recipes.get("recipes") else []

        # 提取辅食建议（按三餐顺序取对应食谱）
        recipe_suggestions = kb_meals[:3]  # 取前3个食谱匹配三餐

        items = []

        # 起床 + 奶（使用框架时间）
        items.append({
            "time": wake_time,
            "type": "wake",
            "title": "起床",
            "details": f"喝奶（{milk_schedule['amount']}{milk_schedule['unit']}）",
            "notes": None
        })

        # 早餐 - 使用真实辅食数据 + 应季食材
        if meal_schedule:
            breakfast = meal_schedule[0]
            recipe = recipe_suggestions[0] if len(recipe_suggestions) > 0 else None
            recipe_name = recipe.get('name', '高铁辅食') if recipe else "根据月龄推荐食材"
            ingredients = [i['name'] for i in (recipe.get('ingredients', []) if recipe else [])[:3]]
            # 混入应季食材
            if top_ingredients:
                ingredients = (ingredients + top_ingredients)[:4]
            items.append({
                "time": breakfast["time"],
                "type": "meal",
                "title": breakfast["name"],
                "details": recipe_name,
                "nutrition": recipe.get('tips', f"月龄{age_months}个月，以泥糊状为主") if recipe else None,
                "preparation": "→".join(recipe.get('steps', [])[:2]) if recipe else None,
                "notes": "、".join(ingredients) if ingredients else None
            })

        # 上午小睡
        morning_nap = schedule.get("morning_nap") or schedule.get("morning_nap1")
        if morning_nap:
            nap_start, nap_end = morning_nap if isinstance(morning_nap, tuple) else schedule.get("morning_nap1", ("09:00", "10:30"))
            sleep_tips = kb_sop.get("tips", ["注意接觉"])
            items.append({
                "time": nap_start,
                "type": "sleep",
                "title": "上午小睡",
                "details": f"约{self._calc_duration(nap_start, nap_end)}分钟",
                "notes": sleep_tips[0] if sleep_tips else "注意接觉"
            })

            # 小睡后户外（使用推荐公园 + 天气决策）
            outdoor_time = self._add_minutes(nap_end, 30)
            if outdoor_ok and recommended_parks:
                park_name = recommended_parks[0].get("name", "公园")
                park_note = recommended_parks[0].get("notes", "")
                items.append({
                    "time": outdoor_time,
                    "type": "outdoor",
                    "title": "户外活动",
                    "details": f"去{park_name}（{int(outdoor_minutes/2)}分钟）",
                    "notes": park_note if park_note else outdoor_reason
                })
            elif outdoor_ok:
                items.append({
                    "time": outdoor_time,
                    "type": "outdoor",
                    "title": "户外活动",
                    "details": f"遛弯{int(outdoor_minutes/2)}分钟",
                    "notes": outdoor_reason if outdoor_reason else None
                })
            else:
                # 天气不适合户外 → 推荐室内
                indoor_name = nearby_indoor[0].get("name", "室内乐园") if nearby_indoor else "室内活动"
                items.append({
                    "time": outdoor_time,
                    "type": "outdoor",
                    "title": "室内活动（天气原因）",
                    "details": f"去{indoor_name}",
                    "notes": outdoor_reason if outdoor_reason else "室外AQI不佳，建议室内"
                })

        # 午餐 - 使用真实辅食数据
        if len(meal_schedule) > 1:
            lunch = meal_schedule[1]
            recipe = recipe_suggestions[1] if len(recipe_suggestions) > 1 else None
            recipe_name = recipe.get('name', '辅食') if recipe else "根据月龄推荐食材"
            ingredients = [i['name'] for i in (recipe.get('ingredients', []) if recipe else [])[:3]]
            items.append({
                "time": lunch["time"],
                "type": "meal",
                "title": lunch["name"],
                "details": recipe_name,
                "nutrition": recipe.get('tips', f"月龄{age_months}个月，注意铁摄入") if recipe else None,
                "preparation": "→".join(recipe.get('steps', [])[:2]) if recipe else None,
                "notes": "、".join(ingredients) if ingredients else None
            })

        # 下午小睡
        if "afternoon_nap" in schedule:
            nap_start, nap_end = schedule["afternoon_nap"]
            sleep_tips = kb_sop.get("tips", ["保证充足睡眠"])
            items.append({
                "time": nap_start,
                "type": "sleep",
                "title": "下午小睡",
                "details": f"约{self._calc_duration(nap_start, nap_end)}分钟",
                "notes": sleep_tips[0] if sleep_tips else "保证充足睡眠"
            })
        elif "afternoon_nap1" in schedule:
            # 多个下午小睡（婴儿期）
            nap_start, nap_end = schedule["afternoon_nap1"]
            items.append({
                "time": nap_start,
                "type": "sleep",
                "title": "下午第一次小睡",
                "details": f"约{self._calc_duration(nap_start, nap_end)}分钟",
                "notes": None
            })

        # 下午户外（使用第2个推荐公园 + 天气决策）
        nap_end = None
        if "afternoon_nap" in schedule:
            nap_end = schedule["afternoon_nap"][1]
        elif "afternoon_nap1" in schedule:
            nap_end = schedule["afternoon_nap1"][1]
        outdoor_time = self._add_minutes(nap_end if nap_end else "15:00", 30)
        if outdoor_ok and len(recommended_parks) > 1:
            park = recommended_parks[1]
            items.append({
                "time": outdoor_time,
                "type": "outdoor",
                "title": "户外活动",
                "details": f"去{park.get('name', '公园')}（{int(outdoor_minutes/2)}分钟）",
                "notes": park.get('notes', '') or outdoor_reason
            })
        elif outdoor_ok:
            items.append({
                "time": outdoor_time,
                "type": "outdoor",
                "title": "户外活动",
                "details": f"公园/小区{int(outdoor_minutes/2)}分钟",
                "notes": outdoor_reason if outdoor_reason else None
            })
        else:
            indoor_name = nearby_indoor[0].get("name", "室内乐园") if nearby_indoor else "室内活动"
            items.append({
                "time": outdoor_time,
                "type": "outdoor",
                "title": "室内活动（天气原因）",
                "details": f"去{indoor_name}",
                "notes": outdoor_reason if outdoor_reason else "室外AQI不佳，建议室内"
            })

        # 晚餐 - 使用真实辅食数据 + 应季食材
        if len(meal_schedule) > 2:
            dinner = meal_schedule[2]
            recipe = recipe_suggestions[2] if len(recipe_suggestions) > 2 else None
            recipe_name = recipe.get('name', '辅食') if recipe else "根据月龄推荐食材"
            ingredients = [i['name'] for i in (recipe.get('ingredients', []) if recipe else [])[:3]]
            # 混入应季食材
            if top_ingredients and len(top_ingredients) >= 2:
                ingredients = (ingredients + [top_ingredients[1]])[:4]
            items.append({
                "time": dinner["time"],
                "type": "meal",
                "title": dinner["name"],
                "details": recipe_name,
                "nutrition": recipe.get('tips', f"晚餐清淡易消化") if recipe else None,
                "preparation": "→".join(recipe.get('steps', [])[:2]) if recipe else None,
                "notes": "、".join(ingredients) if ingredients else None
            })

        # 睡前奶
        if age_months < 24:
            items.append({
                "time": night_sleep_time,
                "type": "meal",
                "title": "睡前奶",
                "details": f"喝奶（{milk_schedule['amount']}{milk_schedule['unit']}）",
                "notes": None
            })

        # 入睡 - 使用框架时间 + 真实睡眠SOP
        items.append({
            "time": night_sleep_time,
            "type": "bath",
            "title": "洗漱",
            "details": "洗澡/洗脸/刷牙",
            "notes": None
        })

        sleep_routine = kb_sop.get("description", "建立睡前仪式")
        sleep_notes = kb_sop.get("tips", ["关灯，保持安静"])[0] if kb_sop.get("tips") else "关灯，保持安静"
        items.append({
            "time": self._add_minutes(night_sleep_time, 30),
            "type": "sleep",
            "title": "入睡",
            "details": sleep_routine,
            "notes": sleep_notes
        })

        # 按时间排序
        items.sort(key=lambda x: x["time"])

        # 生成提醒
        reminders = self._generate_reminders(age_months, kb)

        # AI Tips - 融入里程碑上下文
        ai_tips = self._generate_tips(age_months, kb, kb_milestones)

        return {
            "items": items,
            "reminders": reminders,
            "ai_tips": ai_tips
        }

    def _calc_duration(self, start: str, end: str) -> int:
        """计算时间差（分钟）"""
        start_h, start_m = map(int, start.split(":"))
        end_h, end_m = map(int, end.split(":"))
        return (end_h * 60 + end_m) - (start_h * 60 + start_m)

    def _add_minutes(self, time_str: str, minutes: int) -> str:
        """时间加分钟"""
        h, m = map(int, time_str.split(":"))
        total_mins = h * 60 + m + minutes
        return f"{total_mins // 60:02d}:{total_mins % 60:02d}"

    def _get_season(self, d: date) -> str:
        """根据日期判断季节"""
        m = d.month
        if m in (3, 4, 5):
            return "spring"
        elif m in (6, 7, 8):
            return "summer"
        elif m in (9, 10, 11):
            return "autumn"
        return "winter"

    def _generate_reminders(self, age_months: int, kb: Optional[Dict] = None) -> List[Dict]:
        """生成今日提醒"""
        reminders = []
        kb = kb or {}

        # 新食材观察提醒
        if age_months >= 6:
            reminders.append({
                "type": "food",
                "content": "新食材每次只加一种，观察3天是否过敏"
            })

        # 户外提醒
        reminders.append({
            "type": "health",
            "content": "每天户外活动不少于2小时（累计）"
        })

        # 6个月以上补铁
        if 6 <= age_months < 12:
            reminders.append({
                "type": "nutrition",
                "content": "注意补铁：红肉、动物肝脏每周1-2次"
            })

        # 季节性提醒
        season = kb.get("season", "")
        if season == "spring":
            reminders.append({
                "type": "health",
                "content": "春季花粉高发期，外出回来记得洗脸洗手"
            })
        elif season == "autumn":
            reminders.append({
                "type": "health",
                "content": "秋季干燥，注意给宝宝补充水分"
            })

        # 附近医院提醒（如果有）
        hospitals = kb.get("nearbyHospitals", [])
        if hospitals:
            h = hospitals[0]
            reminders.append({
                "type": "health",
                "content": f"附近医院：{h.get('name', '')}（如需可就近就医）"
            })

        # 特殊上下文（支持 dict 和 str 两种格式）
        context = kb.get("context") or kb.get("specialContexts")
        if context:
            if isinstance(context, str):
                ctx_lower = context.lower()
            else:
                ctx_lower = str(context).lower()
            if "疫苗" in ctx_lower or "vaccine" in ctx_lower:
                reminders.append({
                    "type": "vaccine",
                    "content": "打疫苗当天注意观察体温，辅食清淡为主"
                })
            if "发烧" in ctx_lower or "fever" in ctx_lower:
                reminders.append({
                    "type": "health",
                    "content": "发烧期间多补充水分，辅食以流质/软烂为主"
                })

        return reminders

    def _generate_tips(self, age_months: int, kb: Optional[Dict] = None, milestones: List[Dict] = None) -> str:
        """生成AI小贴士"""
        tips = []
        kb = kb or {}

        # 月龄基础贴士
        if age_months < 3:
            tips.append("这个阶段的宝宝以奶为主，辅食是尝试性质，不要强迫")
        elif age_months < 6:
            tips.append("开始添加辅食了，从高铁米粉开始，每次只加一种新食材")
        elif age_months < 12:
            tips.append("1岁前辅食不加盐糖，辅食性状可以从泥糊→碎末→小块过渡")
        else:
            tips.append("1岁后可以跟家人一起吃饭了，注意少油少盐，养成良好进食习惯")

        # 应季食材推荐
        seasonal_ingredients = kb.get("seasonalIngredients", [])
        if seasonal_ingredients:
            names = [i.get("name", "") for i in seasonal_ingredients[:3] if i.get("name")]
            if names:
                tips.append(f"【应季食材】现在适合吃：{'、'.join(names)}")

        # 户外建议（天气决策）
        outdoor_decision = kb.get("outdoorDecision", {})
        if outdoor_decision:
            reason = outdoor_decision.get("reason", "")
            if reason:
                tips.append(f"【户外建议】{reason}")

        # 融入当前发育里程碑
        if milestones:
            for m in milestones[:1]:
                if m.get("month", 0) <= age_months:
                    tips.append(f"【发育重点】{m.get('category','')}：{m.get('title','')}")
                    break

        # 特殊上下文
        context = kb.get("context") or kb.get("specialContexts")
        if context:
            tips.append(f"今日特殊情况：{context}")

        return " | ".join(tips)


# 全局单例
daily_planner = DailyPlanner()


def generate_daily_plan(
    child_name: str,
    age_months: int,
    current_date: date,
    today_feed_records: List[Dict] = [],
    today_sleep_records: List[Dict] = [],
    context: Optional[Dict] = None
) -> Dict[str, Any]:
    """生成每日计划的便捷函数"""
    return daily_planner.generate_plan(
        child_name=child_name,
        age_months=age_months,
        current_date=current_date,
        today_feed_records=today_feed_records,
        today_sleep_records=today_sleep_records,
        context=context
    )
