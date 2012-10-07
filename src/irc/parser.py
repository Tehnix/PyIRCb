#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC messages...

"""

import src.irc.command


class Parser(object):
    """Parse IRC output and react to commands."""
    
    def __init__(self):
        """Prepare the object."""
        super(Parser, self).__init__()
        self.sock = None
        self.readBuffer = None
        self.todo = []
        self.commandInstance =  src.irc.command.Command()
    
    def parse(self):
        self.commandInstance.execute('test')
    
    @property
    def sock(self):
        """Getter for the _sock attribute."""
        return self._sock

    @sock.setter
    def sock(self, value):
        """Getter for the _sock attribute."""
        self._sock = value