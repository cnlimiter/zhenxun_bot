import traceback

from nonebot import on_command, on_message, get_driver, require, logger
from nonebot.adapters.onebot.v11 import GROUP, MessageEvent
from nonebot.exception import ActionFailed
from nonebot.params import CommandArg
from nonebot.permission import Message

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

bot = on_command("sbty", block=True, aliases={"Sbty"}, permission=GROUP, priority=5)
bot_listen = on_message(priority=5)
driver = get_driver()


@bot.handle()
async def selet_command(ev: MessageEvent, matchmsg: Message = CommandArg()):
    try:
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