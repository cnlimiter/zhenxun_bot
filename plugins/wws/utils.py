import gzip
import io
import os
import time
from collections import defaultdict
from datetime import datetime, timedelta

import nonebot
import pytz
from nonebot import Driver
from nonebot.adapters.onebot.v11 import MessageSegment

from plugins.sign_in.config import SIGN_TODAY_CARD_PATH
from plugins.wws.config import WSS_PATH, WSS_SEARCH_PATH
from utils.image_utils import BuildImage
from utils.message_builder import image
driver: Driver = nonebot.get_driver()


async def match_keywords(match_list, Lists):
    for List in Lists:
        for kw in List.keywords:
            for match_kw in match_list:
                if match_kw == kw or match_kw.upper() == kw.upper() or match_kw.lower() == kw.lower():
                    match_list.remove(match_kw)
                    return List.match_keywords, match_list
    return None, match_list


async def find_and_replace_keywords(match_list, Lists):
    for List in Lists:
        for kw in List.keywords:
            for i, match_kw in enumerate(match_list):
                if (match_kw.find(kw) + 1):
                    match_list[i] = str(match_kw).replace(kw, "")
                    if match_list[i] == '':
                        match_list.remove('')
                    return List.match_keywords, match_list
    return None, match_list


def encode_gzip(bytes):
    buf = io.BytesIO(bytes)
    gf = gzip.GzipFile(fileobj=buf)
    return gf.read().decode('utf-8')


class FreqLimiter:
    def __init__(self, default_cd_seconds):
        self.next_time = defaultdict(float)
        self.default_cd = default_cd_seconds

    def check(self, key) -> bool:
        return bool(time.time() >= self.next_time[key])

    def start_cd(self, key, cd_time=0):
        self.next_time[key] = time.time() + (cd_time if cd_time > 0 else self.default_cd)

    def left_time(self, key) -> float:
        return self.next_time[key] - time.time()


class DailyNumberLimiter:
    tz = pytz.timezone('Asia/Shanghai')

    def __init__(self, max_num):
        self.today = -1
        self.count = defaultdict(int)
        self.max = max_num

    def check(self, key) -> bool:
        now = datetime.now(self.tz)
        day = (now - timedelta(hours=5)).day
        if day != self.today:
            self.today = day
            self.count.clear()
        return bool(self.count[key] < self.max)

    def get_num(self, key):
        return self.count[key]

    def increase(self, key, num=1):
        self.count[key] += num

    def reset(self, key):
        self.count[key] = 0


@driver.on_startup
async def init_image():
    WSS_PATH.mkdir(parents=True, exist_ok=True)
    WSS_SEARCH_PATH.mkdir(exist_ok=True, parents=True)
    clear_wss_data_pic()


def clear_wss_data_pic():
    date = datetime.now().date()
    for file in os.listdir(WSS_SEARCH_PATH):
        if str(date) not in file:
            os.remove(WSS_SEARCH_PATH / file)


async def _gene_help_img(
    text: str,
    width: int,
    height: int
                  ) -> MessageSegment:
    current_date = datetime.now()
    data = current_date.date()
    info_img = BuildImage(width, height, color=(255, 255, 255, 0), font_size=15)
    info_img.text((0, 0), f"{text}")
    info_img.save(WSS_PATH / f"{data}_help.png")
    return image(f"{data}_help.png", "wss")


def _gene_info_img(

    group_id: int,
    user_id: int,
    text: str,
    width: int,
    height: int
                  ) -> MessageSegment:
    current_date = datetime.now()
    data = current_date.date()
    info_img = BuildImage(width, height, color=(255, 255, 255, 0), font_size=15)
    info_img.text((0, 0), f"{text}")
    info_img.save(SIGN_TODAY_CARD_PATH / f"{user_id}_{group_id}_{data}.png")
    return image(f"{user_id}_{group_id}_{data}.png", "sign/today_card")
