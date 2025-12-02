from typing import Dict, List

from ..store import store


def create_topic(payload: dict) -> dict:
    return store.create_topic(
        slug=payload["slug"],
        name=payload["name"],
        parent_slug=payload.get("parent_slug"),
        description=payload.get("description", ""),
    )


def create_question(payload: dict) -> dict:
    metadata = {
        "difficulty": payload.get("difficulty", 1500),
        "tags": payload.get("tags", []),
        "source": payload.get("source"),
    }
    return store.create_question(
        topic_slug=payload["topic_slug"],
        text=payload["text"],
        options=payload["options"],
        answer_index=payload["answer_index"],
        metadata=metadata,
    )


def list_topics() -> List[dict]:
    return list(store.topics.values())


def list_questions(topic_slug: str) -> List[dict]:
    return store.get_questions_by_topic(topic_slug)
