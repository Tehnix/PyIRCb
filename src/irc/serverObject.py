#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC servers...

"""

import src.irc.channelObject


# NOTE: The logged in users dict loggedInUsers are in this format:
# {
#     'username': {
#         'lastLogin': 'unixtimestamp', # The last time you were logged in
#         'failedLoginAttemptsSinceLastLogin': 0, # The number of failed login
#         # attempts since last login
#         'loggedTime': 'unixtimestamp' # The time you logged in, so total time can
#         # be calculated
#     }
# }


class ServerObject(object):
    
    def __init__(self, globalInfo, info):
        super(ServerObject, self).__init__()
        self.channels = {}
        self.connect = True
        self.connected = False
        self.address = None
        self.port = 6667
        self.ssl = False
        try:
            self.address = info['address']
        except KeyError:
            self.connect = False
        self.node = None
        self.nickname = 'PyBot'
        self.realname = 'PyBot'
        self.identify = False
        self.operator = '$'
        self.admins = []
        self.loggedInUsers = {}
        self.manageSettings(globalInfo, info)
        
    def manageSettings(self, globalInfo, info):
        ignoredAttributes = [
            'channels',
            'node',
            'loggedInUsers'
        ]
        defaultToGlobalSettings = [
            'nickname',
            'realname',
            'operator'
        ]
        # Iterate through the object's attributes and replace them with
        # their matching settings values
        for attribute in dir(self):
            if attribute.startswith('_') or attribute in ignoredAttributes:
                continue
            try:
                setattr(self, attribute, info[attribute])
            except KeyError:
                if attribute in defaultToGlobalSettings:
                    try:
                        setattr(self, attribute, globalInfo[attribute])
                    except KeyError:
                        pass
        try:
            for name in info['channels']:
                self.addChannel(name)
        except KeyError:
            pass
    
    def addChannel(self, name):
        self.channels[name] = src.irc.channelObject.ChannelObject(name)
    
    def removeChannel(self, name):
        del self.channels[name]
