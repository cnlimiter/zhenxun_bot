
import nonebot
from fastapi import FastAPI

try:
    from ..libs.auth import _decode_state, get_token_by_code, set_user_token
except ImportError:
    pass
else:

    app: FastAPI = nonebot.get_app()

    @app.get("/api/github/auth")
    async def auth(code: str, state: str):
        try:
            username = _decode_state(state)
        except Exception:
            return {"message": "invalid state"}
        if not username:
            return {"message": "oauth session expired"}
        token = await get_token_by_code(code)
        set_user_token(username, token)
        return {"message": "ok"}
