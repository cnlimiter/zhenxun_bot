import html
import re
import traceback

from nonebot import on_command, on_message, get_driver, require, logger
from nonebot.adapters.onebot.v11 import GROUP, MessageEvent, PrivateMessageEvent, MessageSegment
from nonebot.exception import ActionFailed
from nonebot.params import CommandArg
from nonebot.permission import Message
from .utils import DailyNumberLimiter, FreqLimiter
from .role_info import get_RoleInfo

scheduler = require("nonebot_plugin_apscheduler").scheduler

__zx_plugin_name__ = "300英雄战绩"
__plugin_usage__ = """
usage：
    300英雄战绩查询
    指令：
        sbty
""".strip()
__plugin_des__ = "300英雄查询"
__plugin_cmd__ = ["sbty"]
__plugin_version__ = 0.1
__plugin_author__ = "cnlimiter"
_max = 20
EXCEED_NOTICE = f'您今天已经冲过{_max}次了，请明早5点后再来！'
_nlmt = DailyNumberLimiter(_max)
_flmt = FreqLimiter(3)


bot = on_command("sbty", block=True, aliases={"Sbty"}, permission=GROUP, priority=5)
bot_listen = on_message(priority=5)
user_token: str = get_driver().config.ty_user_token


@bot.handle()
async def selet_command(ev: MessageEvent, matchmsg: Message = CommandArg()):
    try:
        msg = ''
        if isinstance(ev, PrivateMessageEvent):  # 如果是私聊则取消
            return
        qqid = ev.user_id
        if not _nlmt.check(qqid):
            await bot.send(EXCEED_NOTICE, at_sender=True)
            return
        if not _flmt.check(qqid):
            await bot.send('您冲得太快了，请稍候再冲', at_sender=True)
            return
        _flmt.start_cd(qqid)
        _nlmt.increase(qqid)

        search_main = html.unescape(str(matchmsg)).strip()
        match = re.search(r"sbty (.+)", search_main)
        if match:
            search_name = search_main.split()[1]
            msg = await get_RoleInfo(user_token, search_name)

        else:
            await bot.send('你输入的玩家名有问题哦~')

        if msg:
            if isinstance(msg, str):
                await bot.send(msg)
                return
            else:
                await bot.send(MessageSegment.image(msg))
                return
        else:
            await bot.send('呜呜呜发生了错误，可能是网络问题，如果过段时间不能恢复请联系主人哦~')
            return
    except ActionFailed:
        logger.warning(traceback.format_exc())
        try:
            await bot.send('发不出图片，可能被风控了QAQ')
        except Exception:
            pass
        return
    except Exception:
        logger.error(traceback.format_exc())
        await bot.finish('呜呜呜发生了错误，可能是网络问题，如果过段时间不能恢复请联系主人哦~')
