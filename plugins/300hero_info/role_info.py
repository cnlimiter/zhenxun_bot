import traceback
from pathlib import Path

import httpx
import jinja2
from httpx import ConnectTimeout
from nonebot import logger
from nonebot_plugin_htmlrender import html_to_pic
from .data_source import set_role_info_params

dir_path = Path(__file__).parent
template_path = dir_path / "template"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path), enable_async=True
)


async def get_RoleInfo(token: str, name):
    try:
        url, params = '', ''
        url = 'https://m300wxapp.jumpw.com/battle/searchNormal?type=wx'
        params = {
            "token": token,
            "RoleName": str(name)
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, timeout=None)
            result = resp.json()
            logger.info(f"状态码:{result['code']}")
        if result['code'] == 1 and result['data']:
            template = env.get_template("role-info.html")
            template_data = await set_role_info_params(result['data'])
            content = await template.render_async(template_data)
            return await html_to_pic(content, wait=0, viewport={"width": 920, "height": 1000})
        elif result['code'] == 500:
            return f"请输入查询对象哦"
        else:
            return f"{result['message']}"
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
        return '请求超时了，请过会儿再尝试哦~'
    except Exception:
        logger.error(traceback.format_exc())
        return '出了点问题，请联系真寻的主人解决'
