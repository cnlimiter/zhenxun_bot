

import nonebot
from nonebot.log import logger
from fastapi import FastAPI, Body

app: FastAPI = nonebot.get_app()


@app.post("/api/github/hook/{hook_id}")
async def hook(hook_id: str, data: dict = Body(...)):
    # TODO
    logger.info(f"Received event hook:", data)
    return {"message": "ok"}
