#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC users...

"""


class UserObject(object):
    
    def __init__(self, nickname):
        super(UserObject, self).__init__()
        self.nickname = nickname
