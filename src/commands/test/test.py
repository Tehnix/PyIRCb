#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test command...

"""


class Test(object):
    
    def __init__(self, settingsInstance, commandInstance, cmdName, *args):
        super(Test, self).__init__()
        self.settingsInstance = settingsInstance
        self.commandInstance = commandInstance
        if cmdName is not None:
            if args[0] is not None:
                getattr(self, cmdName)(*args)
            else:
                getattr(self, cmdName)()
    
    def testing(self, *args):
        self.commandInstance.replyWithMessage(':D !')
    
    def say(self, *args):
        self.commandInstance.replyWithMessage(' '.join(args))
        
