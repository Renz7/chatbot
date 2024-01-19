#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/12/30 16:19
Author  : ren
"""
import os
import sys

sad_talker_git = "https://github.com/OpenTalker/SadTalker.git"

pwd = os.path.dirname(os.path.abspath(__file__))
sad_talker_path = os.path.join(pwd, "sad_talker")


def clone_module():
    if not os.path.exists(os.path.join(pwd, "sad_talker")):
        print(f"clone sad_talker to {sad_talker_path}")
        os.system(f"git clone  --depth 1 {sad_talker_git} {sad_talker_path}")


def import_lib():
    sys.path.append(sad_talker_path)
    # python = sys.executable
    # os.system(f"{python} -m pip install -r {os.path.join(sad_talker_path, 'requirements.txt')}")


def prepare_sad_talker():
    clone_module()
    os.system(f"sh {os.path.join(sad_talker_path, 'scripts/download_models.sh')}")


if __name__ == '__main__':
    prepare_sad_talker()
