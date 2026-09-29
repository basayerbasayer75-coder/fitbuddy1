from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
def utc_now(): return datetime.now(timezone.utc)
class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    user_id:Mapped[str]=mapped_column(String(80),unique=True,index=True,nullable=False)
    name:Mapped[str]=mapped_column(String(120),nullable=False)
    age:Mapped[int]=mapped_column(Integer,nullable=False)
    weight:Mapped[float]=mapped_column(Float,nullable=False)
    goal:Mapped[str]=mapped_column(String(80),nullable=False)
    intensity:Mapped[str]=mapped_column(String(20),nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utc_now)
    plans:Mapped[list["WorkoutPlan"]]=relationship(back_populates="user",cascade="all, delete-orphan")
class WorkoutPlan(Base):
    __tablename__="workout_plans"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    user_id:Mapped[str]=mapped_column(String(80),ForeignKey("users.user_id",ondelete="CASCADE"),index=True)
    original_plan:Mapped[str]=mapped_column(Text,nullable=False)
    updated_plan:Mapped[str|None]=mapped_column(Text,nullable=True)
    nutrition_tip:Mapped[str]=mapped_column(Text,nullable=False)
    feedback:Mapped[str|None]=mapped_column(Text,nullable=True)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utc_now)
    updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utc_now,onupdate=utc_now)
    user:Mapped["User"]=relationship(back_populates="plans")
