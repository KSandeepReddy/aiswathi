from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List

from ..store import store


def aggregate_user_metrics(user_id: int) -> Dict[str, dict]:
    per_topic: Dict[str, dict] = defaultdict(lambda: {"attempts": 0, "correct": 0, "time_spent": 0.0})
    for attempt in store.get_attempts_for_user(user_id):
        question = store.questions.get(attempt["question_id"], {})
        topic = question.get("topic_slug")
        if topic:
            stats = per_topic[topic]
            stats["attempts"] += 1
            stats["correct"] += 1 if attempt["correct"] else 0
            stats["time_spent"] += attempt["time_spent"]
    for topic, stats in per_topic.items():
        stats["accuracy"] = stats["correct"] / max(1, stats["attempts"])
        stats["avg_time"] = stats["time_spent"] / max(1, stats["attempts"])
    return per_topic


def volatility(user_id: int) -> Dict[str, float]:
    per_topic = aggregate_user_metrics(user_id)
    vol = {}
    for topic, stats in per_topic.items():
        attempts = [a for a in store.attempts if a["user_id"] == user_id and store.questions[a["question_id"]]["topic_slug"] == topic]
        streak_changes = sum(1 for i in range(1, len(attempts)) if attempts[i]["correct"] != attempts[i-1]["correct"])
        vol[topic] = streak_changes / max(1, len(attempts))
    return vol


def recency(user_id: int) -> Dict[str, float]:
    recency_scores: Dict[str, float] = {}
    now = datetime.utcnow()
    for attempt in store.get_attempts_for_user(user_id):
        question = store.questions.get(attempt["question_id"], {})
        topic = question.get("topic_slug")
        if not topic:
            continue
        age_days = (now - attempt["timestamp"]).total_seconds() / 86400
        score = max(0.0, 1 - age_days / 30)
        recency_scores[topic] = max(recency_scores.get(topic, 0.0), score)
    return recency_scores
