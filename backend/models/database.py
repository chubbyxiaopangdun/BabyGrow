from sqlalchemy import create_engine, Column, String, Float, Integer, Boolean, Date, DateTime, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum
import os

Base = declarative_base()

# 数据库路径
_db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "data.db")


def _get_default_engine():
    """获取默认引擎（懒加载）"""
    db_url = f"sqlite:///{_db_path}"
    return create_engine(db_url, echo=False)


def create_engine_conn(db_url):
    """创建数据库引擎"""
    engine = create_engine(db_url, echo=False)
    return engine


def get_session_db(engine):
    """获取数据库会话"""
    Session = sessionmaker(bind=engine)
    return Session()


# 方便外部调用的函数（避免与SQLAlchemy的create_engine同名）
def make_engine(db_url):
    """创建数据库引擎"""
    engine = create_engine_conn(db_url)
    return engine


def get_session(db_engine=None):
    """获取数据库会话"""
    if db_engine is None:
        db_engine = _get_default_engine()
    Session = sessionmaker(bind=db_engine)
    return Session()


# 全局默认引擎（用于需要直接引用engine的场景）
engine = _get_default_engine()


class GenderEnum(enum.Enum):
    male = "male"
    female = "female"


class FeedTypeEnum(enum.Enum):
    breast_milk = "breast_milk"
    formula = "formula"
    solid = "solid"
    fruit = "fruit"
    snack = "snack"


class EatingModeEnum(enum.Enum):
    self = "self"
    spoon = "spoon"
    bottle = "bottle"
    refused = "refused"


class SleepTypeEnum(enum.Enum):
    nap = "nap"           # 上午小睡
    afternoon = "afternoon"  # 下午小睡
    night = "night"       # 夜睡


class HealthTypeEnum(enum.Enum):
    height = "height"
    weight = "weight"
    temperature = "temperature"
    vaccine = "vaccine"


class Child(Base):
    __tablename__ = "children"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(Enum(GenderEnum), default=GenderEnum.male)
    birth_height = Column(Float, nullable=True)
    birth_weight = Column(Float, nullable=True)
    allergies = Column(Text, nullable=True)  # JSON数组
    notes = Column(Text, nullable=True)
    avatar_color = Column(String, default="#FF9B5E")
    location = Column(String, default="hangzhou:binjiang")  # 城市:区县
    transport_mode = Column(String, default="metro")  # metro / driving / walking
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    feed_records = relationship("FeedRecord", back_populates="child", cascade="all, delete-orphan")
    sleep_records = relationship("SleepRecord", back_populates="child", cascade="all, delete-orphan")
    health_records = relationship("HealthRecord", back_populates="child", cascade="all, delete-orphan")
    milestone_records = relationship("MilestoneRecord", back_populates="child", cascade="all, delete-orphan")
    daily_plans = relationship("DailyPlan", back_populates="child", cascade="all, delete-orphan")


class FeedRecord(Base):
    __tablename__ = "feed_records"

    id = Column(String, primary_key=True)
    child_id = Column(String, ForeignKey("children.id"), nullable=False)
    type = Column(Enum(FeedTypeEnum), nullable=False)
    food_name = Column(String, nullable=True)
    amount = Column(Float, nullable=True)
    unit = Column(String, default="g")
    time = Column(DateTime, nullable=False)
    eating_mode = Column(Enum(EatingModeEnum), default=EatingModeEnum.spoon)
    new_food = Column(Boolean, default=False)
    new_food_observation_end = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    child = relationship("Child", back_populates="feed_records")


class SleepRecord(Base):
    __tablename__ = "sleep_records"

    id = Column(String, primary_key=True)
    child_id = Column(String, ForeignKey("children.id"), nullable=False)
    type = Column(Enum(SleepTypeEnum), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    night_wakings = Column(Integer, default=0)
    quality = Column(Integer, nullable=True)  # 1-5
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    child = relationship("Child", back_populates="sleep_records")


class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(String, primary_key=True)
    child_id = Column(String, ForeignKey("children.id"), nullable=False)
    type = Column(Enum(HealthTypeEnum), nullable=False)
    value = Column(Float, nullable=True)
    unit = Column(String, nullable=True)
    date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    child = relationship("Child", back_populates="health_records")


class MilestoneRecord(Base):
    __tablename__ = "milestone_records"

    id = Column(String, primary_key=True)
    child_id = Column(String, ForeignKey("children.id"), nullable=False)
    milestone_id = Column(String, nullable=False)
    achieved = Column(Boolean, default=False)
    achieved_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    child = relationship("Child", back_populates="milestone_records")


class DailyPlan(Base):
    __tablename__ = "daily_plans"

    id = Column(String, primary_key=True)
    child_id = Column(String, ForeignKey("children.id"), nullable=False)
    date = Column(Date, nullable=False)
    plan_json = Column(Text, nullable=False)  # 完整计划JSON
    generated_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    child = relationship("Child", back_populates="daily_plans")


class ConversationHistory(Base):
    __tablename__ = "conversation_history"

    id = Column(String, primary_key=True)
    child_id = Column(String, ForeignKey("children.id"), nullable=False)
    role = Column(String, nullable=False)  # "user" / "assistant"
    content = Column(Text, nullable=False)
    agent = Column(String, nullable=True)  # "nutrition" / "sleep" / "schedule" / "health" / "general"
    card_json = Column(Text, nullable=True)  # 结构化卡片 JSON
    created_at = Column(DateTime, default=datetime.utcnow)

    child = relationship("Child")


# 数据库初始化
def init_db(engine):
    Base.metadata.create_all(bind=engine)
