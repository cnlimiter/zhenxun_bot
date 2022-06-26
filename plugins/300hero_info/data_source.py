import traceback
from pathlib import Path

dir_path = Path(__file__).parent
template_path = dir_path / "template"

hero = {
    290: "申屠子夜",
    289: "莉姆",
    288: "闻人飒悬",
    287: "赛贝斯",
    286: "食蜂操祈",
    285: "吉良吉影",
    284: "托尔",
    283: "帕秋莉诺蕾姬",
    282: "和真&慧慧",
    281: "藤原妹红",
    280: "王也",
    279: "涂山红红",
    278: "C.C.",
    275: "蓬莱山辉夜",
    274: "蝴蝶忍",
    273: "机械神梅普露",
    272: "梅普露",
    271: "环彩羽",
    270: "迪奥·布兰度",
    269: "尤吉欧",
    268: "射命丸文",
    267: "灶门炭治郎",
    266: "冯宝宝",
    265: "格蕾",
    264: "美游",
    260: "莉法",
    263: "真红",
    262: "爱丽丝·玛格特罗依德",
    261: "结城友奈",
    259: "柒",
    258: "波风水门",
    257: "妮姆芙",
    256: "琦玉",
    255: "乔鲁诺·乔巴纳",
    249: "爱丽丝",
    254: "间桐樱",
    253: "美杜莎",
    251: "蕾西亚",
    250: "伍六七",
    239: "夜斗",
    248: "琉璃",
    247: "迪斯卓尔",
    246: "少司命",
    245: "曹焱兵",
    244: "常宣灵",
    243: "常昊灵",
    242: "潘多拉",
    241: "我妻由乃",
    240: "西行寺幽幽子",
    238: "爱蜜莉娅",
    237: "雅儿贝德",
    236: "佩姬",
    235: "神裂火织",
    228: "塞巴斯蒂安",
    234: "康娜",
    233: "珂朵莉",
    232: "阿尔泰尔",
    230: "芙兰朵露",
    229: "安兹乌尔恭",
    231: "阿库娅",
    227: "黑崎一护",
    226: "库丘林",
    225: "夜雨声烦",
    224: "君莫笑",
    223: "三千院凪",
    222: "玉藻前",
    219: "贞德",
    220: "白贞德(Ruler)",
    221: "黑贞德(Avenger)",
    218: "雾雨魔理沙",
    215: "白",
    216: "空",
    217: "阿斯托尔福",
    203: "爱德华",
    204: "武藤游戏",
    201: "水银灯",
    213: "鲁路修",
    214: "香风智乃",
    212: "赤瞳",
    211: "艾露莎",
    209: "司波达也",
    202: "周防尊",
    210: "赵云",
    208: "八神疾风",
    207: "蕾米莉亚",
    206: "欧根亲王",
    205: "无名",
    199: "优克莉伍德",
    200: "洛克李",
    198: "伊斯坎达尔(Rider)",
    197: "缇米",
    196: "柏崎星奈",
    195: "沢田纲吉",
    193: "伊莎",
    194: "栗山未来",
    192: "牧濑红莉栖",
    191: "一方通行",
    190: "蒂塔",
    189: "诱宵美九",
    187: "PLAY1",
    183: "大傻",
    184: "亚里亚",
    185: "诺瓦露",
    186: "克子",
    181: "巴麻美",
    169: "菲特",
    188: "魂魄妖梦",
    164: "黑雪姬",
    165: "高町奈叶",
    172: "四糸乃",
    174: "鸢一折纸",
    180: "尼禄",
    168: "伊莉雅",
    160: "远坂凛",
    167: "朝田诗乃",
    162: "美树沙耶加",
    166: "佐仓杏子",
    161: "奇犽",
    170: "五河琴里",
    171: "金木研",
    155: "两仪式",
    151: "八云紫",
    163: "空条承太郎",
    159: "战斗暴龙兽",
    158: "岛风",
    156: "卫宫士郎(Archer)",
    152: "奈亚子",
    157: "五更琉璃",
    153: "白岩射手",
    147: "白井黑子",
    149: "梦梦",
    150: "鹿目圆香",
    143: "晓美焰",
    148: "樱满集",
    142: "夜刀神十香",
    154: "立华奏",
    146: "涅普顿",
    144: "金色之暗",
    145: "纏流子",
    140: "小鸟游六花",
    139: "江户川柯南",
    138: "伊卡洛斯",
    137: "坂田银时",
    136: "夜夜",
    135: "十六夜咲夜",
    128: "喜羊羊",
    134: "时崎狂三",
    131: "陈美嘉",
    130: "吕子乔",
    129: "胡一菲",
    126: "不知火舞",
    122: "强袭自由",
    121: "绯村剑心",
    120: "姬丝秀忒",
    119: "李小狼",
    118: "黑",
    117: "桂木桂马",
    115: "杀生丸",
    113: "萨菲罗斯",
    112: "小悟空",
    110: "格雷",
    109: "夏娜",
    108: "楪祈",
    107: "三笠",
    105: "秋山澪",
    104: "吉尔伽美什",
    102: "桐人",
    101: "黑岩射手",
    100: "博丽灵梦",
    96: "御坂美琴",
    94: "月之女祭司",
    93: "达克尼斯",
    92: "无头骑士",
    91: "天草四郎时贞",
    90: "美狄亚",
    88: "舰队统帅",
    89: "幻刺D露西",
    87: "幻刺L莉莉",
    86: "死神",
    85: "佐罗",
    84: "战士娃",
    83: "猎人娃",
    82: "牧师娃",
    81: "骑士娃",
    78: "盗贼娃",
    80: "术士娃",
    79: "法师娃",
    76: "结城明日奈",
    75: "纳兹",
    72: "卡殿下",
    71: "胡子船长",
    70: "青丘国主",
    69: "左二少",
    68: "自来也",
    67: "火拳S",
    66: "蛇血舞姬",
    65: "蛇叔",
    64: "白鬼院凛凛蝶",
    63: "梅比斯",
    62: "张飞",
    61: "貂蝉",
    60: "吕布",
    59: "库奇",
    58: "神目黑刀",
    57: "乔帮主",
    56: "巴依老爷",
    55: "雅典娜",
    54: "夏洛特",
    53: "阿尔托利亚(Saber)",
    52: "我受罗",
    51: "匹诺曹",
    50: "黑羽快斗",
    48: "草帽小子",
    47: "深渊之眼",
    46: "莉娜·因巴斯",
    45: "雾影射手",
    44: "食之忍者",
    43: "弗兰肯斯坦",
    42: "缇娜",
    41: "赫拉克勒斯",
    40: "战场原黑仪",
    39: "土间埋",
    38: "风音日和",
    37: "司波深雪",
    36: "富樫勇太",
    35: "桔梗",
    34: "姬冬雪菜",
    33: "凸守早苗",
    32: "美猴王",
    31: "天天",
    30: "哈桑(Assassin)",
    29: "沙耶",
    23: "齐天小剩",
    20: "阿尔冯斯",
    18: "唐僧",
    17: "平和岛静雄",
    13: "记忆金属",

}


async def set_role_info_params(List, heros: dict):
    try:
        # if List['MatchSportsList']['MID'] != 254:  # jjc
        #     return
        role_name = List["RoleName"]
        level = int(List["MasterLv"])
        v_level = int(List["LvVIP"])

        my_hero_1_id = int(List['MatchSportsList'][0]['MatchSports']['MyHeros'][0]['HeroID'])
        my_hero_1_name = hero.setdefault(my_hero_1_id, "无名氏~")
        my_hero_1_total = int(List['MatchSportsList'][0]['MatchSports']['MyHeros'][0]['Total'])
        my_hero_1_win = int(List['MatchSportsList'][0]['MatchSports']['MyHeros'][0]['Win'])
        my_hero_1_per = round(my_hero_1_win * 100 / my_hero_1_total, 2)

        my_hero_2_id = int(List['MatchSportsList'][0]['MatchSports']['MyHeros'][1]['HeroID'])
        my_hero_2_name = hero.setdefault(my_hero_2_id, "无名氏~")
        my_hero_2_total = int(List['MatchSportsList'][0]['MatchSports']['MyHeros'][1]['Total'])
        my_hero_2_win = int(List['MatchSportsList'][0]['MatchSports']['MyHeros'][1]['Win'])
        my_hero_2_per = round(my_hero_2_win * 100 / my_hero_2_total, 2)

        my_hero_3_id = int(List['MatchSportsList'][0]['MatchSports']['MyHeros'][2]['HeroID'])
        my_hero_3_name = hero.setdefault(my_hero_3_id, "无名氏~")
        my_hero_3_total = int(List['MatchSportsList'][0]['MatchSports']['MyHeros'][2]['Total'])
        my_hero_3_win = int(List['MatchSportsList'][0]['MatchSports']['MyHeros'][2]['Win'])
        my_hero_3_per = round(my_hero_3_win * 100 / my_hero_3_total, 2)

        # logger.info(f"name:{my_hero_1_name}")

        jjc_total = int(List['MatchSportsList'][0]['MatchSports']['Total'])
        jjc_win = int(List['MatchSportsList'][0]['MatchSports']['Win'])
        jjc_per = round(jjc_win * 100 / jjc_total, 2)
        team_score = int(List['TeamScore'])

        hero_count = int(List['HeroCount'])
        skin_count = int(List['SkinCount'])
        win_100 = int(List['Win100Title'])
        win_300 = int(List['Win300Title'])

        result = {
            "RoleName": role_name,
            "MasterLv": level,
            "VipLv": v_level,
            "template_path": template_path,
            "JJCTotal": jjc_total,
            "JJCWin": jjc_win,
            "JJCPercent": jjc_per,
            "TeamScore": team_score,
            "HaveHeros": hero_count,
            "HaveSkins": skin_count,
            "NoHeros": 227 - hero_count,
            "NoSkins": 730 - skin_count,
            "Have100": win_100,
            "Have300": win_300,
            "No100": 227 - win_100,
            "No300": 227 - win_300,
            "HeroName1": my_hero_1_name,
            "HeroName2": my_hero_2_name,
            "HeroName3": my_hero_3_name,
            "HeroTotal1": my_hero_1_total,
            "HeroTotal2": my_hero_2_total,
            "HeroTotal3": my_hero_3_total,
            "HeroWin1": my_hero_1_win,
            "HeroWin2": my_hero_2_win,
            "HeroWin3": my_hero_3_win,
            "HeroPercent1": my_hero_1_per,
            "HeroPercent2": my_hero_2_per,
            "HeroPercent3": my_hero_3_per,
            "MyHero": [

            ]
        }

        return result
    except Exception:
        traceback.print_exc()
