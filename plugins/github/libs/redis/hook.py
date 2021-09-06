
from typing import Optional

from . import redis

REPO_HOOK_FORMAT = "github_hook_{repo_name}"


def set_repo_hook(hook_id: str, full_name: str) -> Optional[bool]:
    return redis.set(REPO_HOOK_FORMAT.format(repo_name=full_name), hook_id)


def delete_repo_hook(full_name: str) -> int:
    return redis.delete(REPO_HOOK_FORMAT.format(repo_name=full_name))


def exists_repo_hook(full_name: str) -> int:
    return redis.exists(REPO_HOOK_FORMAT.format(repo_name=full_name))


def get_repo_hook(full_name: str) -> Optional[str]:
    value = redis.get(REPO_HOOK_FORMAT.format(repo_name=full_name))
    return value if value is None else value.decode()
