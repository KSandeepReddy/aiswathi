from __future__ import annotations

import hashlib
import itertools
import random
import string
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class InMemoryStore:
    """Simple in-memory data store used to avoid external dependencies.

    This is intentionally lightweight so the core product logic can be prototyped
    without standing up Postgres or Redis.
    """

    def __init__(self) -> None:
        self.users: Dict[int, dict] = {}
        self.sessions: Dict[str, int] = {}
        self.topics: Dict[str, dict] = {}
        self.questions: Dict[int, dict] = {}
        self.attempts: List[dict] = []
        self.study_plans: Dict[int, dict] = {}
        self.skill_ratings: Dict[int, Dict[str, float]] = {}
        self.review_schedule: Dict[int, List[dict]] = {}
        self._user_seq = itertools.count(1)
        self._question_seq = itertools.count(1)

    def create_user(self, email: str, password: str) -> int:
        user_id = next(self._user_seq)
        self.users[user_id] = {
            "id": user_id,
            "email": email,
            "password_hash": hashlib.sha256(password.encode()).hexdigest(),
            "created_at": datetime.utcnow(),
        }
        return user_id

    def authenticate(self, email: str, password: str) -> Optional[str]:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        for user in self.users.values():
            if user["email"] == email and user["password_hash"] == password_hash:
                token = self._issue_session(user["id"])
                return token
        return None

    def _issue_session(self, user_id: int) -> str:
        token = "sess_" + "".join(random.choices(string.ascii_letters + string.digits, k=32))
        self.sessions[token] = user_id
        return token

    def get_user(self, token: str) -> Optional[dict]:
        user_id = self.sessions.get(token)
        if user_id:
            return self.users.get(user_id)
        return None

    def create_topic(self, slug: str, name: str, parent_slug: Optional[str], description: str) -> dict:
        topic = {
            "slug": slug,
            "name": name,
            "parent_slug": parent_slug,
            "description": description,
        }
        self.topics[slug] = topic
        return topic

    def create_question(self, topic_slug: str, text: str, options: List[str], answer_index: int, metadata: dict) -> dict:
        question_id = next(self._question_seq)
        question = {
            "id": question_id,
            "topic_slug": topic_slug,
            "text": text,
            "options": options,
            "answer_index": answer_index,
            "metadata": metadata,
        }
        self.questions[question_id] = question
        return question

    def record_attempt(self, user_id: int, question_id: int, correct: bool, time_spent: float) -> dict:
        attempt = {
            "user_id": user_id,
            "question_id": question_id,
            "correct": correct,
            "time_spent": time_spent,
            "timestamp": datetime.utcnow(),
        }
        self.attempts.append(attempt)
        return attempt

    def update_skill(self, user_id: int, topic_slug: str, delta: float) -> float:
        ratings = self.skill_ratings.setdefault(user_id, {})
        base = ratings.get(topic_slug, 1200.0)
        new_rating = base + delta
        ratings[topic_slug] = new_rating
        return new_rating

    def schedule_review(self, user_id: int, question_id: int, due_at: datetime, interval: int) -> None:
        queue = self.review_schedule.setdefault(user_id, [])
        queue.append({"question_id": question_id, "due_at": due_at, "interval": interval})

    def pop_due_review(self, user_id: int, now: Optional[datetime] = None) -> Optional[int]:
        now = now or datetime.utcnow()
        queue = self.review_schedule.get(user_id, [])
        queue.sort(key=lambda item: item["due_at"])
        if queue and queue[0]["due_at"] <= now:
            item = queue.pop(0)
            return item["question_id"]
        return None

    def get_questions_by_topic(self, topic_slug: str) -> List[dict]:
        return [q for q in self.questions.values() if q["topic_slug"] == topic_slug]

    def get_attempts_for_user(self, user_id: int) -> List[dict]:
        return [a for a in self.attempts if a["user_id"] == user_id]


store = InMemoryStore()
