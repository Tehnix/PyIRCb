#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC channels...

"""

import src.irc.userObject
import src.utilities as util


class ChannelObject(object):
    
    def __init__(self, server, name):
        super(ChannelObject, self).__init__()
        self.server = server
        self.name = name
        self.topic = ""
    
    def addUsers(self, nicknames):
        for nick in nicknames:
            self.addUser(nick)
   
    def addUser(self, nickname):
        snickname = util.stripUsername(nickname)
        if snickname not in self.server.users:
            self.server.users[snickname] = src.irc.userObject.UserObject(nickname)
        self.server.users[snickname].addChannel(self.name)
    
    def removeUser(self, nickname):
        snickname = util.stripUsername(nickname)
        self.server.users[snickname].removeFromChannel(self.name)

