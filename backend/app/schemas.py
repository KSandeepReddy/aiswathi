from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    token: str


class TopicCreate(BaseModel):
    slug: str
    name: str
    parent_slug: Optional[str] = None
    description: str


class QuestionCreate(BaseModel):
    topic_slug: str
    text: str
    options: List[str]
    answer_index: int
    difficulty: int = Field(1500, ge=800, le=2400)
    tags: List[str] = []
    source: Optional[str] = None


class AttemptPayload(BaseModel):
    question_id: int
    selected_index: int
    time_spent_seconds: float


class StudyPlanCreate(BaseModel):
    goals: List[str]
    weeks: int = Field(4, ge=1)


class StudyPlanUpdate(BaseModel):
    goals: Optional[List[str]] = None
    weeks: Optional[int] = None


class AdherenceLog(BaseModel):
    week: int
    completed_tasks: int
    reflections: Optional[str] = None


class WeeklyTask(BaseModel):
    topic_slug: str
    target_questions: int
    focus: str


class NextQuestionRequest(BaseModel):
    mode: str = Field("practice", description="practice|adaptive|review")
    topic_slug: Optional[str] = None
