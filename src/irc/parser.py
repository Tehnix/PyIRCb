#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC messages...

"""


class Parser(object):
    
    def __init__(self):
        """Prepare the object."""
        super(Parser, self).__init__()
        self.sock = None
        self.readBuffer = None
        self.todo = []
    
    def parse(self):
        pass
    
    @property
    def sock(self):
        """Getter for the _sock attribute."""
        return self._sock

    @sock.setter
    def sock(self, value):
        """Getter for the _sock attribute."""
        self._sock = value