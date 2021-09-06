

from typing import Optional
from datetime import timedelta

from . import redis

USER_STATE_FORMAT = "github_state_{state}"


def set_state_bind_user(user_id: str, state: int) -> Optional[bool]:
    return redis.set(USER_STATE_FORMAT.format(state=state), user_id,
                     timedelta(minutes=5))


def get_state_bind_user(state: int) -> Optional[str]:
    value = redis.get(USER_STATE_FORMAT.format(state=state))
    return value if value is None else value.decode()
