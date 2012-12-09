#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
User module. Implements a full authentication system, and project
tracking.

"""

import src.utilities as util
from src.database import Database


# Authenticated users are stored in the dictionary with the format:
# {
#     'username': {
#         'lastLogin': 'unixtimestamp', # The last time you were logged in
#         'failedLoginAttemptsSinceLastLogin': 0, # The number of failed login
#         # attempts since last login
#         'loggedTime': 'unixtimestamp' # The time you logged in, so total time can
#         # be calculated
#     }
# }
loggedInUsers = {}


class ModuleBase(object):
    
    def __init__(self, settingsInstance, commandInstance, authRequired, *args):
        super(ModuleBase, self).__init__()
        self.settingsInstance = settingsInstance
        self.commandInstance = commandInstance
        self.reply = self.commandInstance.replyWithMessage
        self.username = self.commandInstance.user
        self.db = None
        self.args = args[0]
        self.bars = util.toBytes(args[0])
        self.authRequired = authRequired

    def _execute(self, cmdName):
        if cmdName in self.authRequired and self._isLoggedIn(self.commandInstance.user):
            self._executeCommand(cmdName)
        elif cmdName not in self.authRequired:
            self._executeCommand(cmdName)
        else:
            self.reply(
            "The command 'user.%s' requires that you are authenticated. Use the user.identify command to log in to the system, and try again." % (cmdName,)
            )

    def _executeCommand(self, cmdName):
        if cmdName is None:
            return False
        try:
            getattr(self, cmdName)()
            return True
        except ValueError:
            self.reply(
                "Wrong number of arguments. See $help user.%s for help." % (cmdName,)
            )
        return False

    def _createDatabase(self, databaseName):
        """Create a database file."""
        return Database(dbtype="SQLite", dbname=databaseName)
    
    def _createTables(self, tables):
        """Create tables from a list."""
        if self.db is not None:
            for table in tables:
                self.db.execute(table)
