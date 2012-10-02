#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC servers...

"""


class Server(object):
    
    def __init__(self, info):
        super(Server, self).__init__()
        self.connect = True
        self.connected = False
        self.address = None
        self.port = 6667
        self.ssl = False
        self.handleInfo(info)
        
    def handleInfo(self, info):
        try:
            self.address = info['address']
        except KeyError:
            self.connect = False
        try:
            self.ssl = info['ssl']
        except KeyError:
            pass
        try:
            self.port = int(info['port'])
        except KeyError:
            pass
    