
from typing import Any, Dict, Type, Union

from nonebot.matcher import Matcher
from nonebot.adapters import Message, MessageSegment

from ..libs.redis import set_message_info
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.exception import FinishedException
from nonebot.adapters.cqhttp import PrivateMessageEvent, GroupMessageEvent

async def send_github_message(
        matcher: Type[Matcher], owner: str, repo: str, number: int,
        message: Union[str, Message, MessageSegment]) -> Any:
    message_sent: Dict[str, Any] = await matcher.send(message)
    set_message_info(str(message_sent["message_id"]), owner, repo, number)
    return message_sent


async def only_private(bot: Bot, event: Event, state: T_State):
    return isinstance(event, PrivateMessageEvent)


async def only_group(bot: Bot, event: Event, state: T_State):
    return isinstance(event, GroupMessageEvent)


async def allow_cancel(bot: Bot, event: Event, state: T_State):
    """An args parser allows to finish the session."""
    message = str(event.get_message())
    if message == "取消":
        await bot.send(event, "已取消")
        raise FinishedException
    state[state["_current_key"]] = str(event.get_message())
