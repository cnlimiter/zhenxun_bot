

from typing import Optional

from utils.github import Github
from .. import github_config as config
from utils.github.models import Repository


async def get_repo(owner: str,
                   repo_name: str,
                   token: Optional[str] = None) -> Repository:
    if token:
        g = Github(token)
    elif config.github_client_id and config.github_client_secret:
        g = Github(config.github_client_id, config.github_client_secret)
    else:
        g = Github()

    async with g:
        return await g.get_repo(f"{owner}/{repo_name}", False)
