#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/12/30 16:37
Author  : ren
"""

from supports.facerander.script import prepare_sad_talker

prepare_sad_talker()


async def face_rander(image: str, audio: str, **kwargs):
    from supports.facerander.sad_talker.src.gradio_demo import SadTalker

    sad_talker = SadTalker()
    return sad_talker.test(source_image=image, driven_audio=audio, result_dir="./data/result", **kwargs)
