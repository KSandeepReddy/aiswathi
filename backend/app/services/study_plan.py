from __future__ import annotations

from typing import Dict, List

from ..services import analytics
from ..store import store


def create_plan(user_id: int, goals: List[str], weeks: int) -> dict:
    plan = {
        "user_id": user_id,
        "goals": goals,
        "weeks": weeks,
        "adherence": [],
        "weekly_tasks": generate_tasks(user_id, weeks),
    }
    store.study_plans[user_id] = plan
    return plan


def update_plan(user_id: int, goals=None, weeks=None) -> dict:
    plan = store.study_plans.get(user_id)
    if not plan:
        raise ValueError("plan not found")
    if goals is not None:
        plan["goals"] = goals
    if weeks is not None:
        plan["weeks"] = weeks
        plan["weekly_tasks"] = generate_tasks(user_id, weeks)
    return plan


def log_adherence(user_id: int, week: int, completed_tasks: int, reflections: str | None) -> dict:
    plan = store.study_plans.get(user_id)
    if not plan:
        raise ValueError("plan not found")
    entry = {"week": week, "completed_tasks": completed_tasks, "reflections": reflections}
    plan.setdefault("adherence", []).append(entry)
    return entry


def generate_tasks(user_id: int, weeks: int) -> List[dict]:
    metrics = analytics.aggregate_user_metrics(user_id)
    volatility_scores = analytics.volatility(user_id)
    tasks = []
    sorted_topics = sorted(metrics.items(), key=lambda item: item[1].get("accuracy", 0))
    for week in range(1, weeks + 1):
        if sorted_topics:
            topic_slug, stats = sorted_topics[(week - 1) % len(sorted_topics)]
            focus = "stabilize" if volatility_scores.get(topic_slug, 0) > 0.4 else "improve accuracy"
        else:
            topic_slug = "general"
            focus = "foundation"
        tasks.append({
            "week": week,
            "topic_slug": topic_slug,
            "target_questions": 20,
            "focus": focus,
        })
    return tasks
