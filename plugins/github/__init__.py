

from pathlib import Path

import nonebot

from .config import Config

# nonebot2 < 2.0.0-alpha.14


# store all github subplugins
_sub_plugins = set()
# load all github plugin config from global config
github_config = Config(**nonebot.get_driver().config.dict())

_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / "plugins").resolve()))

from . import apis
