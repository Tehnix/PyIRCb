#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
User command...

"""

import grp


class User(object):
    """Something, something, something darkside...."""

    def __init__(self, settingsInstance, commandInstance, cmdName, *args):
        super(User, self).__init__()
        self.settingsInstance = settingsInstance
        self.commandInstance = commandInstance
        if cmdName is not None:
            if args[0] is not None:
                getattr(self, cmdName)(*args)
            else:
                getattr(self, cmdName)()
    
    def test(self):
        self.commandInstance.replyWithMessage(
            self.commandInstance.user
        )

    def users(self):
        """Get a list of users in the users group."""
        self.commandInstance.replyWithMessage(self._users())

    def _users(self, output='string'):
        for group in grp.getgrall():
            if group.gr_name == 'users':
                members = group.gr_mem
        if output == 'list':
            return members
        else:
            return ', '.join(members)

