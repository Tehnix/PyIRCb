#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC bot...

"""

import src.settings


class BotDispatcher(object):
    
    def __init__(self):
        super(BotDispatcher, self).__init__()
        self.settingsInstance = src.settings.Settings()
        self.settings = self.settingsInstance.settings
        self.dispatch()
        
    def dispatch(self):
        pass
    
    def destroyBot(self):
        pass
    
    def reload(self):
        pass