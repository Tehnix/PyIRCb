#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC users...

"""


class UserObject(object):
    
    def __init__(self, nickname):
        super(UserObject, self).__init__()
        self.online = True
        self.nickname = nickname
        self.channelPriviliges = ''
        self.loggedIn = False
        self.lastLogin = None
        self.failedLoginAttempts = 0
        self.loggedInTime = None
        self.channels = {}

    def addChannel(self, channel):
        self.channels[channel] = {
            'inChannel': True
        }
    
    def removeFromChannel(self, channel):
        self.channels[channel] = {
            'inChannel': False
        }
    
    @property
    def online(self):
        """Getter for _online. If a user is found in a channel, he is online."""
        for channel, info in self.channels.items():
            if info['inChannel']:
                return True
        return False
    
    @online.setter
    def online(self, value):
        """Setter for _online."""
        if value is False:
            self.loggedIn = False
            for channel, info in self.channels.items():
                self.channels[channel]['inChannel'] = False
        self._online = value

    @property
    def nickname(self):
        """Getter for the _nickname."""
        return self._nickname

    @nickname.setter
    def nickname(self, value):
        """Setter for the _nickname. Removes any leading @'s and such."""
        if value[0:1] in ['@', '%', '!']:
            self.channelPriviliges = value[0:1]
            self._nickname = value[1:]
        else:
            self._nickname = value
