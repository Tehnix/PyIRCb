#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
User command...

"""


class User(object):

    def __init__(self, settingsInstance, commandInstance, cmdName, *args):
        super(User, self).__init__()
        self.settingsInstance = settingsInstance
        self.commandInstance = commandInstance
        if cmdName is not None:
            if args[0] is not None:
                getattr(self, cmdName)(*args)
            else:
                getattr(self, cmdName)()
    
    def testing(self):
        self.commandInstance.replyWithMessage(':D !')

    def say(self, *args):
        self.commandInstance.replyWithMessage(' '.join(args))
