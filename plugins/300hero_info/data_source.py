import traceback
from pathlib import Path

from .utils import get_hero_name

dir_path = Path(__file__).parent
template_path = dir_path / "template"


async def set_role_info_params(List):
    try:
        if List['MatchSportsList']['MID'] != 254:  # jjc
            return
        my_hero_1_name = get_hero_name(List['MatchSportsList']['MatchSports']['MyHeros'][0]['HeroID'])
        my_hero_1_total = List['MatchSportsList']['MatchSports']['MyHeros'][0]['Total']
        my_hero_1_win = List['MatchSportsList']['MatchSports']['MyHeros'][0]['Win']
        my_hero_2_name = get_hero_name(List['MatchSportsList']['MatchSports']['MyHeros'][1]['HeroID'])
        my_hero_2_total = List['MatchSportsList']['MatchSports']['MyHeros'][1]['Total']
        my_hero_2_win = List['MatchSportsList']['MatchSports']['MyHeros'][1]['Win']
        my_hero_3_name = get_hero_name(List['MatchSportsList']['MatchSports']['MyHeros'][2]['HeroID'])
        my_hero_3_total = List['MatchSportsList']['MatchSports']['MyHeros'][2]['Total']
        my_hero_3_win = List['MatchSportsList']['MatchSports']['MyHeros'][2]['Win']

        jjc_total = List['MatchSportsList']['MatchSports']['Total']
        jjc_win = List['MatchSportsList']['MatchSports']['Win']
        jjc_per = jjc_win / jjc_total
        team_score = List['TeamScore']

        hero_count = List['HeroCount']
        skin_count = List['SkinCount']
        win_100 = List['Win100Title']
        win_300 = List['Win300Title']
        result = {
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
            "HeroWin1": my_hero_1_win,
            "HeroWin2": my_hero_2_win,
            "HeroWin3": my_hero_3_win,
            "HeroPercent1": my_hero_1_win / my_hero_1_total,
            "HeroPercent2": my_hero_2_win / my_hero_2_total,
            "HeroPercent3": my_hero_3_win / my_hero_3_total,
        }

        return result
    except Exception:
        traceback.print_exc()
