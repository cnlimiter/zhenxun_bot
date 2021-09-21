

from typing import Optional, overload

from typing_extensions import Literal

from .models import LazyRepository, Repository
from .request import Requester

DEFAULT_BASE_URL = "https://api.github.com"
DEFAULT_STATUS_URL = "https://status.github.com"
DEFAULT_TIMEOUT = 15
DEFAULT_PER_PAGE = 30


class Github:

    def __init__(self,
                 token_or_client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 base_url: str = DEFAULT_BASE_URL,
                 timeout: int = DEFAULT_TIMEOUT,
                 user_agent: str = "Python/GitHub",
                 per_page: int = DEFAULT_PER_PAGE,
                 verify: bool = True):
        self._requester = Requester(token_or_client_id, client_secret, base_url,
                                    timeout, user_agent, per_page, verify)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        return await self._requester.close()

    @overload
    async def get_repo(self, full_name: str,
                       lazy: Literal[True]) -> LazyRepository:
        ...

    @overload
    async def get_repo(self, full_name: str,
                       lazy: Literal[False]) -> Repository:
        ...

    async def get_repo(self,
                       full_name: str,
                       lazy: bool = False) -> LazyRepository:
        """
        GET /repos/:owner/:repo

        https://docs.github.com/en/rest/reference/repos#get-a-repository
        """
        url = f"/repos/{full_name}"
        if lazy:
            return LazyRepository(full_name=full_name,
                                  requester=self._requester)
        response = await self._requester.request_json("GET", url)
        return Repository.parse_obj({
            "requester": self._requester,
            **response.json()
        })

    async def render_markdown(self,
                              text: str,
                              context: Optional[Repository] = None):
        """
        POST /markdown

        https://docs.github.com/en/rest/reference/markdown#render-a-markdown-document
        """
        data = {"text": text}
        # TODO
        # if context:
        #     data["mode"] = "gfm"
        #     data["context"] = context._identity
        response = await self._requester.request_json("POST",
                                                      "/markdown",
                                                      json=data)
        return response.text


