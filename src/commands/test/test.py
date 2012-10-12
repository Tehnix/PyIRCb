#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test command...

"""


class Test(object):
    
    def __init__(self, commandInstance, cmdName):
        super(Test, self).__init__()
        self.commandInstance = commandInstance
        if cmdName is not None:
            getattr(self, cmdName)()
    
    def callMe(self):
        self.commandInstance.replyWithMessage(':DDDDDDDDD')
