#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple module to make the bot say things.

"""

import src.moduleBase
import src.utilities as util


class Say(src.moduleBase.ModuleBase):
    """Simple module to make the bot say things."""
    
    def __init__(self, cmdHandler, cmdName=None, cmdArgs=None):
        super(Say, self).__init__(
            cmdHandler,
            cmdArgs=cmdArgs,
            authRequired=[]
        )
        if cmdName is not None:
            self._execute(cmdName)
    
    def this(self):
        """Repeat what was just said. Usage: Say.this [text]."""
        self.reply(self.args)
