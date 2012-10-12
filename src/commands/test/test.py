#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test command...

"""


class Test(object):
    
    def __init__(self, cmdName):
        super(Test, self).__init__()
        getattr(self, cmdName)()
    
    def callMe(self):
        print(':DDDDDDDD....')
