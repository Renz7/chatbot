#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/12/26 15:39
Author  : ren
"""
import os
from typing import Optional

from fastapi import FastAPI, WebSocket, Query, UploadFile, Depends, BackgroundTasks,Response 
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse

from app.model.user import User
from app.server import util
from app.server.util import load_chatbot,gen_talker

app = FastAPI(debug=True)


# @AuthJWT.load_config
# def get_jwt_config():
#     return [("authjwt_secret_key", "sanyhe"), ]


# @app.exception_handler(AuthJWTException)
# def authjwt_exception_handler(request: Request, exc: AuthJWTException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.message}
#     )


# @app.websocket("/ws")
# async def websocket_ep(ws: WebSocket, token: str = Query("token"), Authorize: AuthJWT = Depends()):
#     await ws.accept()
#     try:
#         Authorize.jwt_required("websocket", token)

#     except AuthJWTException as e:
#         await ws.send_text("login required.")
#         await ws.close()


@app.post("/communicate/{user}")
async def communicate(user: str, audio: Optional[UploadFile], background: BackgroundTasks):
    if not audio:
        # todo 返回默认语音文件
        return util.response_err("audio file required")
    else:
        question = await util.asr(audio)
        print(f"收到用户输入{question}")
        bot = await load_chatbot(user)
        answer = bot.predict(question)
        print(f"LLM 回答 {answer}")
        if not answer:
            return ""
        fname = await util.tts(answer)
        print(f"tts 结果 {fname}")
        # background.add_task(os.remove, fname)
        return FileResponse(path=fname)


@app.post("/face_rander")
async def face_rander(image:Optional[UploadFile],audio: Optional[UploadFile]):
    if not image or not audio:
        return util.response_err("input file required")
    try:
        result = await gen_talker(image, audio)
        return FileResponse(result)
    except Exception:
        return JSONResponse({"err_msg": "请检查参数或稍后再试"}, status_code=500)
        


@app.post("login")
async def login(user: User):
    pass
