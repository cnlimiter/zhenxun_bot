

from typing import Union
from typing_extensions import Literal

from . import BaseModel


class Person(BaseModel):
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool


class User(Person):
    type: Literal["User"]


class Bot(Person):
    type: Literal["Bot"]


class Organization(Person):
    type: Literal["Organization"]


Actor = Union[User, Bot, Organization]
