#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC channels...

"""

import src.irc.user


class Channel(object):
    
    def __init__(self, name):
        super(Channel, self).__init__()
        self.name = name
        self.users = {}
        self.topic = ""
    
    def addUser(self, nickname):
        self.users[nickname] = src.irc.user.User(nickname)
    
    def removeUser(self, nickname):
        del self.users[nickname]