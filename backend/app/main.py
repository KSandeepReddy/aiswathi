from __future__ import annotations

from fastapi import Depends, FastAPI, Header, HTTPException

from . import schemas
from .services import adaptive, analytics, auth, content, study_plan
from .store import store

app = FastAPI(title="Adaptive Practice API")


def get_user(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="missing token")
    user = auth.resolve_user(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="invalid token")
    return user


@app.post("/auth/register", response_model=schemas.AuthResponse)
def register(payload: schemas.AuthRequest):
    result = auth.register(payload.email, payload.password)
    return schemas.AuthResponse(token=result["token"])


@app.post("/auth/login", response_model=schemas.AuthResponse)
def login(payload: schemas.AuthRequest):
    token = auth.login(payload.email, payload.password)
    if not token:
        raise HTTPException(status_code=401, detail="invalid credentials")
    return schemas.AuthResponse(token=token)


@app.post("/topics")
def create_topic(payload: schemas.TopicCreate):
    return content.create_topic(payload.dict())


@app.get("/topics")
def get_topics():
    return content.list_topics()


@app.post("/questions")
def create_question(payload: schemas.QuestionCreate):
    if payload.answer_index >= len(payload.options):
        raise HTTPException(status_code=400, detail="answer_index out of bounds")
    return content.create_question(payload.dict())


@app.get("/topics/{topic_slug}/questions")
def questions_for_topic(topic_slug: str):
    return content.list_questions(topic_slug)


@app.post("/attempts")
def log_attempt(payload: schemas.AttemptPayload, user=Depends(get_user)):
    question = store.questions.get(payload.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    correct = payload.selected_index == question["answer_index"]
    attempt = store.record_attempt(user["id"], payload.question_id, correct, payload.time_spent_seconds)
    difficulty = question["metadata"].get("difficulty", 1500)
    adaptive.update_skill(user["id"], question["topic_slug"], difficulty, correct)
    adaptive.schedule_spaced_repetition(user["id"], payload.question_id, correct)
    return attempt


@app.post("/next-question")
def next_question(request: schemas.NextQuestionRequest, user=Depends(get_user)):
    question = adaptive.next_question(user["id"], mode=request.mode, topic_slug=request.topic_slug)
    if not question:
        raise HTTPException(status_code=404, detail="no questions available")
    return question


@app.get("/analytics")
def analytics_dashboard(user=Depends(get_user)):
    return {
        "topics": analytics.aggregate_user_metrics(user["id"]),
        "volatility": analytics.volatility(user["id"]),
        "recency": analytics.recency(user["id"]),
    }


@app.post("/study-plan")
def create_study_plan(payload: schemas.StudyPlanCreate, user=Depends(get_user)):
    return study_plan.create_plan(user["id"], payload.goals, payload.weeks)


@app.patch("/study-plan")
def update_study_plan(payload: schemas.StudyPlanUpdate, user=Depends(get_user)):
    return study_plan.update_plan(user["id"], goals=payload.goals, weeks=payload.weeks)


@app.get("/study-plan")
def get_plan(user=Depends(get_user)):
    return store.study_plans.get(user["id"], {})


@app.post("/study-plan/adherence")
def add_adherence(log: schemas.AdherenceLog, user=Depends(get_user)):
    return study_plan.log_adherence(user["id"], log.week, log.completed_tasks, log.reflections)
