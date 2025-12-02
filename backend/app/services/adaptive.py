from __future__ import annotations

import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from ..store import store

K_FACTOR = 24


def _expected_score(rating: float, difficulty: float) -> float:
    return 1 / (1 + math.pow(10, (difficulty - rating) / 400))


def update_skill(user_id: int, topic_slug: str, difficulty: float, correct: bool) -> float:
    rating = store.skill_ratings.get(user_id, {}).get(topic_slug, 1200.0)
    expected = _expected_score(rating, difficulty)
    actual = 1.0 if correct else 0.0
    delta = K_FACTOR * (actual - expected)
    return store.update_skill(user_id, topic_slug, delta)


def schedule_spaced_repetition(user_id: int, question_id: int, correct: bool, previous_interval: int = 1) -> None:
    interval = max(1, previous_interval * 2) if correct else 1
    due_at = datetime.utcnow() + timedelta(days=interval)
    store.schedule_review(user_id, question_id, due_at, interval)


def next_question(user_id: int, mode: str, topic_slug: Optional[str] = None) -> Optional[dict]:
    if mode == "review":
        review_id = store.pop_due_review(user_id)
        if review_id:
            return store.questions.get(review_id)
    if topic_slug:
        candidates = store.get_questions_by_topic(topic_slug)
    else:
        candidates = list(store.questions.values())
    if not candidates:
        return None
    if mode == "adaptive":
        user_skills = store.skill_ratings.get(user_id, {})
        def score(question: dict) -> float:
            topic_rating = user_skills.get(question["topic_slug"], 1200.0)
            difficulty = question["metadata"].get("difficulty", 1500)
            return abs(topic_rating - difficulty)
        candidates.sort(key=score)
    else:
        candidates.sort(key=lambda q: q["metadata"].get("difficulty", 1500), reverse=True)
    return candidates[0]
