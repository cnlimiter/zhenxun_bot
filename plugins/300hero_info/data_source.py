import traceback
from pathlib import Path

dir_path = Path(__file__).parent
template_path = dir_path / "template"

async def set_role_info_params(List):
    try:

        result = {
            "template_path": template_path,
        }
        return result
    except Exception:
        traceback.print_exc()
