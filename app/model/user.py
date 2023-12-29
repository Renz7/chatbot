#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/12/29 17:06
Author  : ren
"""
from pydantic import BaseModel


class User(BaseModel):
    name: str
    password: str
    nickname: str = "未知用户"


