#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test command...

"""

import src.module


class Test(src.module.ModuleBase):
    """
    This is a simple test class. It can serve as inspiration to 
    how a module could look.
    
    """
    
    def __init__(self, cmdInstance, cmdName=None, cmdArgs=None):
        super(Test, self).__init__(cmdInstance, cmdArgs=cmdArgs)
        if cmdName is not None:
            self._execute(cmdName)
    
    def testing(self):
        """Reply with a good ol' jolly emoticon: Usage: test.testing."""
        self.commandInstance.replyWithMessage(':D !')
    
    def say(self):
        """Repeat the received sentence. Usage: test.say <sentence>."""
        self.commandInstance.replyWithMessage(self.args)
        
