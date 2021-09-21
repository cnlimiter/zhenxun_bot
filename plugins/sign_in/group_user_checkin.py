from datetime import datetime, timedelta
from models.sign_group_user import SignGroupUser
from models.group_member_info import GroupInfoUser
from models.bag_user import BagUser
from configs.config import NICKNAME
from nonebot.adapters.cqhttp import MessageSegment
from asyncio.exceptions import TimeoutError
from utils.image_utils import CreateImg
from services.db_context import db
from .utils import get_card, SIGN_TODAY_CARD_PATH
from services.log import logger
from .random_event import random_event
from io import BytesIO
import random
import aiohttp
import math
import asyncio
import os


async def group_user_check_in(
    nickname: str, user_qq: int, group: int
) -> MessageSegment:
    "Returns string describing the result of checking in"
    present = datetime.now()
    async with db.transaction():
        # 取得相应用户
        user = await SignGroupUser.ensure(user_qq, group, for_update=True)
        if (
            user.checkin_time_last + timedelta(hours=8)
        ).date() >= present.date() or f"{user}_{group}_sign_{datetime.now().date()}" in os.listdir(
            SIGN_TODAY_CARD_PATH
        ):
            gold = await BagUser.get_gold(user_qq, group)
            return await get_card(user, nickname, -1, gold, "")
        return await _handle_check_in(nickname, user_qq, group, present)  # ok


async def _handle_check_in(
    nickname: str, user_qq: int, group: int, present: datetime
) -> MessageSegment:
    user = await SignGroupUser.ensure(user_qq, group, for_update=True)
    impression_added = random.random()
    critx2 = random.random()
    add_probability = user.add_probability
    specify_probability = user.specify_probability
    if critx2 + add_probability > 0.97:
        impression_added *= 2
    elif critx2 < specify_probability:
        impression_added *= 2
    await SignGroupUser.sign(user, impression_added, present)
    gold = random.randint(1, 100)
    gift, gift_type = random_event(user.impression)
    if gift_type == "gold":
        await BagUser.add_gold(user_qq, group, gold + gift)
        gift = f"额外金币 + {gift}"
    else:
        await BagUser.add_props(user_qq, group, gift)
        gift += ' + 1'
    if critx2 + add_probability > 0.97 or critx2 < specify_probability:
        logger.info(
            f"(USER {user.user_qq}, GROUP {user.belonging_group})"
            f" CHECKED IN successfully. score: {user.impression:.2f} "
            f"(+{impression_added * 2:.2f}).获取金币：{gold + gift if gift == 'gold' else gold}"
        )
        return await get_card(user, nickname, impression_added, gold, gift, True)
    else:
        logger.info(
            f"(USER {user.user_qq}, GROUP {user.belonging_group})"
            f" CHECKED IN successfully. score: {user.impression:.2f} "
            f"(+{impression_added:.2f}).获取金币：{gold + gift if gift == 'gold' else gold}"
        )
        return await get_card(user, nickname, impression_added, gold, gift)


async def group_user_check(nickname: str, user_qq: int, group: int) -> MessageSegment:
    # heuristic: if users find they have never checked in they are probable to check in
    user = await SignGroupUser.ensure(user_qq, group)
    gold = await BagUser.get_gold(user_qq, group)
    return await get_card(user, nickname, None, gold, "", is_card_view=True)


async def group_impression_rank(group: int) -> str:
    result = "\t好感度排行榜\t\n"
    user_qq_list, impression_list, _ = await SignGroupUser.get_all_impression(group)
    _count = 11
    if user_qq_list and impression_list:
        for i in range(1, len(user_qq_list)):
            if len(user_qq_list) == 0 or len(impression_list) == 0 or i == _count:
                break
            impression = max(impression_list)
            index = impression_list.index(impression)
            user_qq = user_qq_list[index]
            try:
                user_name = (
                    await GroupInfoUser.get_member_info(user_qq, group)
                ).user_name
            except AttributeError:
                logger.info(f"USER {user_qq}, GROUP {group} 不在群内")
                _count += 1
                impression_list.remove(impression)
                user_qq_list.remove(user_qq)
                continue
            result += f"{i - _count + 11}. {user_name}: {impression:.2f}\n"
            impression_list.remove(impression)
            user_qq_list.remove(user_qq)
    return result[:-1]


async def random_gold(user_id, group_id, impression):
    if impression < 1:
        impression = 1
    gold = random.randint(1, 100) + random.randint(1, int(impression))
    if await BagUser.add_gold(user_id, group_id, gold):
        return gold
    else:
        return 0


# 签到总榜
async def impression_rank(group_id: int, data: dict):
    user_qq_list, impression_list, group_list = await SignGroupUser.get_all_impression(
        group_id
    )
    users, impressions, groups = [], [], []
    num = 0
    for i in range(105 if len(user_qq_list) > 105 else len(user_qq_list)):
        impression = max(impression_list)
        index = impression_list.index(impression)
        user = user_qq_list[index]
        group = group_list[index]
        user_qq_list.pop(index)
        impression_list.pop(index)
        group_list.pop(index)
        if user not in users and impression < 100000:
            if user not in data["0"]:
                users.append(user)
                impressions.append(impression)
                groups.append(group)
            else:
                num += 1
    for i in range(num):
        impression = max(impression_list)
        index = impression_list.index(impression)
        user = user_qq_list[index]
        group = group_list[index]
        user_qq_list.pop(index)
        impression_list.pop(index)
        group_list.pop(index)
        if user not in users and impression < 100000:
            users.append(user)
            impressions.append(impression)
            groups.append(group)
    return (await asyncio.gather(*[_pst(users, impressions, groups)]))[0]


async def _pst(users: list, impressions: list, groups: list):
    lens = len(users)
    count = math.ceil(lens / 33)
    width = 10
    idx = 0
    A = CreateImg(1740, 3300, color="#FFE4C4")
    async with aiohttp.ClientSession() as session:
        for _ in range(count):
            col_img = CreateImg(550, 3300, 550, 100, color="#FFE4C4")
            for _ in range(33 if int(lens / 33) >= 1 else lens % 33 - 1):
                idx += 1
                if idx > 100:
                    break
                impression = max(impressions)
                index = impressions.index(impression)
                user = users[index]
                group = groups[index]
                impressions.pop(index)
                users.pop(index)
                groups.pop(index)
                try:
                    user_name = (
                        await GroupInfoUser.get_member_info(user, group)
                    ).user_name
                except AttributeError:
                    user_name = f"我名字呢？"
                user_name = user_name if len(user_name) < 11 else user_name[:10] + "..."
                impression = (
                    str(impression)[:4] if len(str(impression)) > 4 else impression
                )
                try:
                    async with session.get(
                        f"http://q1.qlogo.cn/g?b=qq&nk={user}&s=160", timeout=5
                    ) as response:
                        ava = CreateImg(
                            50, 50, background=BytesIO(await response.read())
                        )
                except TimeoutError:
                    ava = CreateImg(50, 50, color="white")
                ava.circle()
                bk = CreateImg(550, 100, color="#FFE4C4", font_size=30)
                font_w, font_h = bk.getsize(f"{idx}")
                bk.text((5, int((100 - font_h) / 2)), f"{idx}.")
                bk.paste(ava, (55, int((100 - 50) / 2)), True)
                bk.text((120, int((100 - font_h) / 2)), f"{user_name}")
                bk.text((460, int((100 - font_h) / 2)), f"[{impression}]")
                col_img.paste(bk)
            A.paste(col_img, (width, 0))
            lens -= 33
            width += 580
    W = CreateImg(1740, 3700, color="#FFE4C4", font_size=130)
    W.paste(A, (0, 260))
    font_w, font_h = W.getsize(f"{NICKNAME}的好感度总榜")
    W.text((int((1740 - font_w) / 2), int((260 - font_h) / 2)), f"{NICKNAME}的好感度总榜")
    return W.pic2bs4()
