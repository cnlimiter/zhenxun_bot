from dataclasses import dataclass
import time
from collections import defaultdict
from datetime import datetime, timedelta


import pytz


@dataclass
class matching:
    keywords: str
    match_keywords: int


async def get_hero_name(hero_id: int, Lists):
    for List in Lists:
        for kw in List.match_keywords:
            if  hero_id == kw:
                return List.keywords
    return "未找到"


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


heros = [
    matching("申屠子夜", 290),
    matching("莉姆", 289),
    matching("闻人飒悬", 288),
    matching("赛贝斯", 287),
    matching("食蜂操祈", 286),
    matching("吉良吉影", 285),
    matching("托尔", 284),
    matching("帕秋莉诺蕾姬", 283),
    matching("和真&慧慧", 282),
    matching("藤原妹红", 281),
    matching("王也", 280),
    matching("涂山红红", 279),
    matching("C.C.", 278),
    matching("蓬莱山辉夜", 275),
    matching("蝴蝶忍", 274),
    matching("机械神梅普露", 273),
    matching("梅普露", 272),
    matching("环彩羽", 271),
    matching("迪奥·布兰度", 270),
    matching("尤吉欧", 269),
    matching("射命丸文", 268),
    matching("灶门炭治郎", 267),
    matching("冯宝宝", 266),
    matching("格蕾", 265),
    matching("美游", 264),
    matching("莉法", 260),
    matching("真红", 263),
    matching("爱丽丝·玛格特罗依德", 262),
    matching("结城友奈", 261),
    matching("柒", 259),
    matching("波风水门", 258),
    matching("妮姆芙", 257),
    matching("琦玉", 256),
    matching("乔鲁诺·乔巴纳", 255),
    matching("爱丽丝", 249),
    matching("间桐樱", 254),
    matching("美杜莎", 253),
    matching("蕾西亚", 251),
    matching("伍六七", 250),
    matching("夜斗", 239),
    matching("琉璃", 248),
    matching("迪斯卓尔", 247),
    matching("少司命", 246),
    matching("曹焱兵", 245),
    matching("常宣灵", 244),
    matching("常昊灵", 243),
    matching("潘多拉", 242),
    matching("我妻由乃", 241),
    matching("西行寺幽幽子", 240),
    matching("爱蜜莉娅", 238),
    matching("雅儿贝德", 237),
    matching("佩姬", 236),
    matching("神裂火织", 235),
    matching("塞巴斯蒂安", 228),
    matching("康娜", 234),
    matching("珂朵莉", 233),
    matching("阿尔泰尔", 232),
    matching("芙兰朵露", 230),
    matching("安兹乌尔恭", 229),
    matching("阿库娅", 231),
    matching("黑崎一护", 227),
    matching("塞巴斯蒂安", 228),
    matching("库丘林", 226),
    matching("夜雨声烦", 225),
    matching("君莫笑", 224),
    matching("三千院凪", 223),
    matching("玉藻前", 222),
    matching("贞德", 219),
    matching("白贞德(Ruler),", 220),
    matching("黑贞德(Avenger),", 221),
    matching("雾雨魔理沙", 218),
    matching("白", 215),
    matching("空", 216),
    matching("阿斯托尔福", 217),
    matching("爱德华", 203),
    matching("武藤游戏", 204),
    matching("水银灯", 201),
    matching("鲁路修", 213),
    matching("香风智乃", 214),
    matching("赤瞳", 212),
    matching("艾露莎", 211),
    matching("司波达也", 209),
    matching("周防尊", 202),
    matching("赵云", 210),
    matching("八神疾风", 208),
    matching("蕾米莉亚", 207),
    matching("欧根亲王", 206),
    matching("无名", 205),
    matching("优克莉伍德", 199),
    matching("洛克李", 200),
    matching("伊斯坎达尔(Rider),", 198),
    matching("缇米", 197),
    matching("柏崎星奈", 196),
    matching("沢田纲吉", 195),
    matching("伊莎", 193),
    matching("栗山未来", 194),
    matching("牧濑红莉栖", 192),
    matching("一方通行", 191),
    matching("蒂塔", 190),
    matching("诱宵美九", 189),
    matching("PLAY1", 187),
    matching("大傻", 183),
    matching("亚里亚", 184),
    matching("诺瓦露", 185),
    matching("克子", 186),
    matching("巴麻美", 181),
    matching("菲特", 169),
    matching("魂魄妖梦", 188),
    matching("黑雪姬", 164),
    matching("高町奈叶", 165),
    matching("四糸乃", 172),
    matching("鸢一折纸", 174),
    matching("尼禄", 180),
    matching("伊莉雅", 168),
    matching("远坂凛", 160),
    matching("朝田诗乃", 167),
    matching("美树沙耶加", 162),
    matching("佐仓杏子", 166),
    matching("奇犽", 161),
    matching("五河琴里", 170),
    matching("金木研", 171),
    matching("两仪式", 155),
    matching("八云紫", 151),
    matching("空条承太郎", 163),
    matching("战斗暴龙兽", 159),
    matching("岛风", 158),
    matching("卫宫士郎(Archer),", 156),
    matching("奈亚子", 152),
    matching("五更琉璃", 157),
    matching("白岩射手", 153),
    matching("白井黑子", 147),
    matching("梦梦", 149),
    matching("鹿目圆香", 150),
    matching("晓美焰", 143),
    matching("樱满集", 148),
    matching("夜刀神十香", 142),
    matching("立华奏", 154),
    matching("涅普顿", 146),
    matching("金色之暗", 144),
    matching("纏流子", 145),
    matching("小鸟游六花", 140),
    matching("江户川柯南", 139),
    matching("伊卡洛斯", 138),
    matching("坂田银时", 137),
    matching("夜夜", 136),
    matching("十六夜咲夜", 135),
    matching("喜羊羊", 128),
    matching("时崎狂三", 134),
    matching("陈美嘉", 131),
    matching("吕子乔", 130),
    matching("胡一菲", 129),
    matching("不知火舞", 126),
    matching("强袭自由", 122),
    matching("绯村剑心", 121),
    matching("姬丝秀忒", 120),
    matching("李小狼", 119),
    matching("黑", 118),
    matching("桂木桂马", 117),
    matching("杀生丸", 115),
    matching("萨菲罗斯", 113),
    matching("小悟空", 112),
    matching("格雷", 110),
    matching("夏娜", 109),
    matching("楪祈", 108),
    matching("三笠", 107),
    matching("秋山澪", 105),
    matching("吉尔伽美什", 104),
    matching("桐人", 102),
    matching("黑岩射手", 101),
    matching("博丽灵梦", 100),
    matching("御坂美琴", 96),
    matching("月之女祭司", 94),
    matching("达克尼斯", 93),
    matching("无头骑士", 92),
    matching("天草四郎时贞", 91),
    matching("美狄亚", 90),
    matching("舰队统帅", 88),
    matching("幻刺D露西", 89),
    matching("幻刺L莉莉", 87),
    matching("死神", 86),
    matching("佐罗", 85),
    matching("战士娃", 84),
    matching("猎人娃", 83),
    matching("牧师娃", 82),
    matching("骑士娃", 81),
    matching("盗贼娃", 78),
    matching("术士娃", 80),
    matching("法师娃", 79),
    matching("结城明日奈", 76),
    matching("纳兹", 75),
    matching("卡殿下", 72),
    matching("胡子船长", 71),
    matching("青丘国主", 70),
    matching("左二少", 69),
    matching("自来也", 68),
    matching("火拳S", 67),
    matching("蛇血舞姬", 66),
    matching("蛇叔", 65),
    matching("白鬼院凛凛蝶", 64),
    matching("梅比斯", 63),
    matching("张飞", 62),
    matching("貂蝉", 61),
    matching("吕布", 60),
    matching("库奇", 59),
    matching("神目黑刀", 58),
    matching("乔帮主", 57),
    matching("巴依老爷", 56),
    matching("雅典娜", 55),
    matching("夏洛特", 54),
    matching("阿尔托利亚(Saber),", 53),
    matching("我受罗", 52),
    matching("匹诺曹", 51),
    matching("黑羽快斗", 50),
    matching("草帽小子", 48),
    matching("深渊之眼", 47),
    matching("莉娜·因巴斯", 46),
    matching("雾影射手", 45),
    matching("食之忍者", 44),
    matching("弗兰肯斯坦", 43),
    matching("缇娜", 42),
    matching("赫拉克勒斯", 41),
    matching("战场原黑仪", 40),
    matching("土间埋", 39),
    matching("风音日和", 38),
    matching("司波深雪", 37),
    matching("富樫勇太", 36),
    matching("桔梗", 35),
    matching("姬冬雪菜", 34),
    matching("凸守早苗", 33),
    matching("美猴王", 32),
    matching("天天", 31),
    matching("哈桑(Assassin),", 30),
    matching("沙耶", 29),
    matching("齐天小剩", 23),
    matching("阿尔冯斯", 20),
    matching("唐僧", 18),
    matching("平和岛静雄", 17),
    matching("记忆金属", 13)

]




