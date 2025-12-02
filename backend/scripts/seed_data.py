from __future__ import annotations

from backend.app.store import store


def seed_topics():
    topics = [
        ("physics", "Physics", None, "IIT JEE Physics"),
        ("physics/kinematics", "Kinematics", "physics", "Motion in one and two dimensions"),
        ("chemistry", "Chemistry", None, "IIT JEE Chemistry"),
        ("math", "Mathematics", None, "IIT JEE Mathematics"),
    ]
    for slug, name, parent, desc in topics:
        store.create_topic(slug, name, parent, desc)


def seed_questions():
    questions = [
        {
            "topic_slug": "physics/kinematics",
            "text": "A body starts from rest and accelerates at 2 m/s^2. What is its velocity after 5 s?",
            "options": ["2 m/s", "5 m/s", "10 m/s", "20 m/s"],
            "answer_index": 2,
            "metadata": {"difficulty": 1400, "tags": ["kinematics", "velocity"]},
        },
        {
            "topic_slug": "chemistry",
            "text": "What is the hybridization of carbon in methane?",
            "options": ["sp", "sp2", "sp3", "sp3d"],
            "answer_index": 2,
            "metadata": {"difficulty": 1300, "tags": ["bonding"]},
        },
        {
            "topic_slug": "math",
            "text": "Evaluate the derivative of sin(x).",
            "options": ["cos(x)", "-cos(x)", "sin(x)", "-sin(x)"],
            "answer_index": 0,
            "metadata": {"difficulty": 1200, "tags": ["calculus"]},
        },
    ]
    for q in questions:
        store.create_question(**q)


if __name__ == "__main__":
    seed_topics()
    seed_questions()
    print(f"Seeded {len(store.topics)} topics and {len(store.questions)} questions.")
