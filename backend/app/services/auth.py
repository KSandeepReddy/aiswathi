from typing import Optional

from ..store import store


def register(email: str, password: str) -> dict:
    user_id = store.create_user(email, password)
    token = store.authenticate(email, password)
    return {"id": user_id, "token": token}


def login(email: str, password: str) -> Optional[str]:
    return store.authenticate(email, password)


def resolve_user(token: str) -> Optional[dict]:
    return store.get_user(token)
