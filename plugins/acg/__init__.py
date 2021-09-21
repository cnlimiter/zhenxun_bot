from nonebot.adapters.cqhttp import Bot, Event, Message, GROUP
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.log import logger

import httpx

__plugin_name__ = 'acg'
__plugin_usage__ = '用法：发送‘acg’'


acg = on_command('acg', aliases={'动漫'}, permission=GROUP, priority=5, block=True)


@acg.handle()
async def handle_event(bot: Bot, event: Event, state: T_State):
    at_ = "[CQ:at,qq={}]".format(event.get_user_id())
    async with httpx.AsyncClient() as client:
        resp = await client.get('https://api.mtyqx.cn/api/random.php?return=json')
        logger.debug(resp.json())
        imgurl = resp.json()['imgurl']
        cqimg = f"[CQ:image,file=1.{imgurl.split('.')[1]},url={imgurl}]"
        await acg.send(Message(at_ + cqimg))
