

from . import BaseModel


class Permissions(BaseModel):
    pull: bool
    push: bool
    admin: bool
