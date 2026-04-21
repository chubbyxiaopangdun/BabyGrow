from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


# ============ Child Schemas ============

class GenderEnum(str, Enum):
    male = "male"
    female = "female"


class ChildBase(BaseModel):
    name: str
    birth_date: date
    gender: GenderEnum = GenderEnum.male
    birth_height: Optional[float] = None
    birth_weight: Optional[float] = None
    allergies: Optional[List[str]] = []
    notes: Optional[str] = ""
    avatar_color: Optional[str] = "#FF9B5E"


class ChildCreate(ChildBase):
    pass


class ChildUpdate(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[GenderEnum] = None
    birth_height: Optional[float] = None
    birth_weight: Optional[float] = None
    allergies: Optional[List[str]] = None
    notes: Optional[str] = None
    avatar_color: Optional[str] = None


class ChildResponse(ChildBase):
    id: str
    age_months: int = Field(default=0)
    age_display: str = ""
    current_height: Optional[float] = None
    current_weight: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Feed Schemas ============

class FeedTypeEnum(str, Enum):
    breast_milk = "breast_milk"
    formula = "formula"
    solid = "solid"
    fruit = "fruit"
    snack = "snack"


class EatingModeEnum(str, Enum):
    self = "self"
    spoon = "spoon"
    bottle = "bottle"
    refused = "refused"


class FeedRecordBase(BaseModel):
    type: FeedTypeEnum
    food_name: Optional[str] = None
    amount: Optional[float] = None
    unit: str = "g"
    time: datetime
    eating_mode: EatingModeEnum = EatingModeEnum.spoon
    new_food: bool = False
    new_food_observation_end: Optional[date] = None
    notes: Optional[str] = None


class FeedRecordCreate(FeedRecordBase):
    child_id: str


class FeedRecordUpdate(BaseModel):
    type: Optional[FeedTypeEnum] = None
    food_name: Optional[str] = None
    amount: Optional[float] = None
    unit: Optional[str] = None
    time: Optional[datetime] = None
    eating_mode: Optional[EatingModeEnum] = None
    new_food: Optional[bool] = None
    new_food_observation_end: Optional[date] = None
    notes: Optional[str] = None


class FeedRecordResponse(FeedRecordBase):
    id: str
    child_id: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Sleep Schemas ============

class SleepTypeEnum(str, Enum):
    nap = "nap"
    afternoon = "afternoon"
    night = "night"


class SleepRecordBase(BaseModel):
    type: SleepTypeEnum
    start_time: datetime
    end_time: Optional[datetime] = None
    night_wakings: int = 0
    quality: Optional[int] = None  # 1-5
    notes: Optional[str] = None


class SleepRecordCreate(SleepRecordBase):
    child_id: str


class SleepRecordUpdate(BaseModel):
    type: Optional[SleepTypeEnum] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    night_wakings: Optional[int] = None
    quality: Optional[int] = None
    notes: Optional[str] = None


class SleepRecordResponse(SleepRecordBase):
    id: str
    child_id: str
    duration_minutes: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Health Schemas ============

class HealthTypeEnum(str, Enum):
    height = "height"
    weight = "weight"
    temperature = "temperature"
    vaccine = "vaccine"


class HealthRecordBase(BaseModel):
    type: HealthTypeEnum
    value: Optional[float] = None
    unit: Optional[str] = None
    date: date
    notes: Optional[str] = None


class HealthRecordCreate(HealthRecordBase):
    child_id: str


class HealthRecordResponse(HealthRecordBase):
    id: str
    child_id: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Milestone Schemas ============

class MilestoneRecordBase(BaseModel):
    milestone_id: str
    achieved: bool = False
    achieved_date: Optional[date] = None
    notes: Optional[str] = None


class MilestoneRecordCreate(MilestoneRecordBase):
    child_id: str


class MilestoneRecordUpdate(BaseModel):
    achieved: Optional[bool] = None
    achieved_date: Optional[date] = None
    notes: Optional[str] = None


class MilestoneRecordResponse(MilestoneRecordBase):
    id: str
    child_id: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Daily Plan Schemas ============

class PlanItem(BaseModel):
    time: str
    type: str  # wake, meal, sleep, outdoor, bath, etc.
    title: str
    details: Optional[str] = None
    nutrition: Optional[str] = None
    preparation: Optional[str] = None
    notes: Optional[str] = None


class ReminderItem(BaseModel):
    type: str  # food, vaccine, health, etc.
    content: str


class DailyPlanResponse(BaseModel):
    date: str
    child_id: str
    child_name: str
    child_age_months: int
    items: List[PlanItem]
    reminders: List[ReminderItem] = []
    ai_tips: Optional[str] = None


# ============ AI Skill Schemas ============

class SkillGeneratePlanRequest(BaseModel):
    child_id: str
    date: Optional[str] = None
    context: Optional[str] = None


class SkillAnalyzeSleepRequest(BaseModel):
    child_id: str
    date: Optional[str] = None
    issue: Optional[str] = None


class SkillSuggestMealRequest(BaseModel):
    child_id: str
    meal_type: Optional[str] = None  # breakfast, lunch, dinner, snack
    preferences: Optional[str] = None


class SkillChatRequest(BaseModel):
    child_id: str
    message: str
    conversation_history: Optional[List[dict]] = None


# ============ Common Response ============

class APIResponse(BaseModel):
    code: int = 0
    message: str = "ok"
    data: Optional[dict] = None


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "0.1.0"
