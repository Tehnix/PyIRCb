#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
User module. Implements a full authentication system, and project
tracking.

"""

import sys
import time

import src.utilities as util
from src.database import Database


class ModuleBase(object):
    
    def __init__(self, cmdHandler, cmdArgs=None, authRequired=None):
        super(ModuleBase, self).__init__()
        self.cmdHandler = cmdHandler
        self.reply = self.cmdHandler.replyWithMessage
        self.server = self.cmdHandler.server
        self.username = self.cmdHandler.user
        self.loggedInUsers = self.cmdHandler.server.loggedInUsers()
        self._db = None
        self.args = cmdArgs
        self.bargs = util.toBytes(cmdArgs)
        self.authRequired = []
        if authRequired is not None:
            self.authRequired = authRequired

    def _isLoggedIn(self, username):
        """Check if a user is logged in."""
        if util.stripUsername(username) in self.loggedInUsers:
            return True
        return False
    
    def _logout(self, username):
        """Logout a user. Returns True if the user was loggedin, else False."""
        username = util.stripUsername(username)
        if username in self.loggedInUsers:
            self.server.users[username].loggedIn = False
            return True
        return False
    
    def _logInUser(self, username):
        """Login a user."""
        username = util.stripUsername(username)
        if username not in self.loggedInUsers:
            self.server.users[username].loggedIn = True
            self.server.users[username].lastLogin = self.server.users[username].loggedInTime
            self.server.users[username].loggedInTime = time.time()
        
    def _execute(self, cmdName):
        try:
            if cmdName in self.authRequired and self._isLoggedIn(self.commandInstance.user):
                self._executeCommand(cmdName)
            elif cmdName not in self.authRequired:
                self._executeCommand(cmdName)
            else:
                self.reply("The command 'user.%s' requires that you are authenticated. Use the user.identify command to log in to the system, and try again." % cmdName)
        except Exception as e:
            util.writeException(sys.exc_info())

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

