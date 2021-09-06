

from typing import Optional

from . import BaseModel


class License(BaseModel):
    key: str
    name: str
    spdx_id: str
    url: Optional[str]
    node_id: str
