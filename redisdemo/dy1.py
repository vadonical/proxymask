#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/5/14 14:54
# @File     : dy1.py
# @IDE      : PyCharm


from redisdemo.demo import RedisHelper

obj = RedisHelper()
redis_sub = obj.subscribe()

while True:
    msg = redis_sub.parse_response()
    print(str(msg))