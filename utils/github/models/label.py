

from typing import Optional

from . import BaseModel


class Label(BaseModel):
    id: int
    node_id: str
    url: str
    name: str
    description: Optional[str]
    color: str
    default: bool
