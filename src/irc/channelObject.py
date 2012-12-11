#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC channels...

"""

import src.irc.userObject


class ChannelObject(object):
    
    def __init__(self, name):
        super(ChannelObject, self).__init__()
        self.name = name
        self.topic = ""
        self.users = {}
    
    def addUser(self, nickname):
        self.users[nickname] = src.irc.userObject.UserObject(nickname)
    
    def removeUser(self, nickname):
        del self.users[nickname]