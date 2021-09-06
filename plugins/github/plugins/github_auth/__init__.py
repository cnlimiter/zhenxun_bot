

from nonebot.log import logger
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, PrivateMessageEvent, GroupMessageEvent

from ... import github_config as config

try:
    from ...libs.auth import get_auth_link
except ImportError:
    logger.warning("Plugin github auth is disabled!")
else:

    auth = on_command("auth", priority=config.github_command_priority)
    auth.__doc__ = """
    /auth
    授权 github 账号
    """

    @auth.handle()
    async def handle_private(bot: Bot, event: PrivateMessageEvent):
        await auth.finish("请前往以下链接进行授权：\n" + get_auth_link(event.get_user_id()))

    @auth.handle()
    async def handle_group(bot: Bot, event: GroupMessageEvent):
        await auth.finish("请私聊我并使用 /auth 命令授权你的 GitHub 账号")
