#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/12/29 17:56
Author  : ren
"""
import asyncio
import contextlib
import json as pjson
import os
import tempfile
from collections import OrderedDict

import filetype
from fastapi import UploadFile

from supports.asr import OpenAIASR
from supports.chat import OpenAIChat
from supports.facerander.util import face_rander
from supports.tts import EdgeTTS

ASR = OpenAIASR("base")
TTS = EdgeTTS()
TTS_DEF_VOCICE = "zh-CN-XiaoxiaoNeural"

TTS_VOCICE_DICT = {
    "male": "zh-CN-YunyangNeural",
    "female": "zh-CN-XiaoxiaoNeural"
}

CHAT_BOT_CACHE = OrderedDict()
bot_lock = asyncio.Lock()


async def asr(audio: UploadFile):
    filetype.audio_match(audio.file)
    with create_temp_file() as fname:
        with open(fname, "wb") as f:
            if audio:
                f.write(await audio.read())
                return ASR.transcribe(fname)


async def tts(text, gender):
    voice = TTS_VOCICE_DICT.get(gender, TTS_DEF_VOCICE)
    with create_temp_file(delete=False) as fname:
        await TTS.apredict(text, voice, fname)
        return fname


async def load_chatbot(uid):
    async with bot_lock:
        if uid in CHAT_BOT_CACHE:
            CHAT_BOT_CACHE.move_to_end(uid)
            return CHAT_BOT_CACHE[uid]
        else:
            bot = OpenAIChat(uid)
            if len(CHAT_BOT_CACHE) >= 10:
                CHAT_BOT_CACHE.popitem()
            CHAT_BOT_CACHE[uid] = bot
            return bot


async def gen_talker(image: UploadFile, audio: UploadFile):
    _, img_f = tempfile.mkstemp(suffix="." + image.filename.split(".")[-1])
    _, audio_f = tempfile.mkstemp(suffix="." + audio.filename.split(".")[-1])
    print(img_f, audio_f)
    print(image.size, audio.size)
    with open(img_f, "wb") as f:
        f.write(await image.read())
    with open(audio_f, "wb") as f:
        f.write(await audio.read())
    return face_rander(img_f, audio_f)


@contextlib.contextmanager
def create_temp_file(suffix=".wav", delete=True):
    _, fname = tempfile.mkstemp(dir=cur_data_dir(), suffix=suffix)
    yield fname
    print(f"remove tem file {fname}")
    try:
        delete and os.remove(fname)
    except Exception as e:
        print(e)


def cur_data_dir():
    import os
    pwd = os.getcwd()
    data_dir = os.path.join(pwd, "data")
    if not os.path.exists(data_dir):
        print(f"creating data dir {data_dir}")
        os.mkdir(data_dir)
    return data_dir


# responses

def response_err(msg="", code=100):
    return {
        "code": code,
        "err": msg,
        "data": ""
    }


def response_json(data="", code=0):
    return {
        "code": code,
        "err": "",
        "data": pjson.dumps(data)
    }
