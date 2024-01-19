#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/12/30 16:37
Author  : ren
"""
import os

pwd = os.path.dirname(os.path.abspath(__file__))
cfg_dir = os.path.join(pwd,"sad_talker/src/config")


def face_rander(image: str, audio: str, **kwargs):
    from src.gradio_demo import SadTalker

    sad_talker = SadTalker("./checkpoints",cfg_dir)
    return sad_talker.test(source_image=image, driven_audio=audio, result_dir="./data/result", still_mode=True, **kwargs)
