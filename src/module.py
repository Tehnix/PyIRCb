#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
User module. Implements a full authentication system, and project
tracking.

"""

import src.utilities as util
from src.database import Database


class ModuleBase(object):
    
    def __init__(self, cmdHandler, cmdArgs=None, authRequired=None):
        super(ModuleBase, self).__init__()
        self.cmdHandler = cmdHandler
        self.reply = self.cmdHandler.replyWithMessage
        self.server = self.cmdHandler.server
        self.username = self.cmdHandler.user
        self.loggedInUsers = self.cmdHandler.server.loggedInUsers
        self._db = None
        self.args = cmdArgs
        self.bargs = util.toBytes(cmdArgs)
        self.authRequired = []
        if authRequired is not None:
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
        
    def _createTables(self, tables):
        """Create tables from a list."""
        if self.db is not None:
            for table in tables:
                self.db.execute(table)

    @property
    def db(self):
        """Getter for the _sock attribute."""
        return self._db

    @db.setter
    def db(self, value):
        """
        Setter for the _db attribute. Connect to a database file and 
        create it if it doesn't exist.
        
        """
        self._db = Database(dbtype="SQLite", dbname=value)