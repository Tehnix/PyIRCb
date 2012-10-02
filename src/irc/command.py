#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC commands...

"""


class Command(object):
    
    def __init__(self, command):
        super(Channel, self).__init__()
        self.command = command
