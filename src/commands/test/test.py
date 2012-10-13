#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test command...

"""


class Test(object):
    
    def __init__(self, settingsInstance, commandInstance, cmdName):
        super(Test, self).__init__()
        self.settingsInstance = settingsInstance
        self.commandInstance = commandInstance
        if cmdName is not None:
            getattr(self, cmdName)()
    
    def testing(self):
        self.commandInstance.replyWithMessage(':D !')
