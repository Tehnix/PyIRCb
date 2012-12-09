#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
User module. Implements a full authentication system, and project
tracking.

"""

import hashlib
import grp

import src.module
import src.utilities as util


class User(src.module.ModuleBase):
    
    def __init__(self, cmdInstance, cmdName=None, cmdArgs=None):
        super(User, self).__init__(
            cmdInstance,
            cmdArgs=cmdArgs,
            authRequired=['rm']
        )
        self.db = self._createDatabase('database.sqlite3')
        self._createTables([
            'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, nickname TEXT, password TEXT, server TEXT)'
        ])
        if cmdName is not None:
            self._execute(cmdName)
            
    def _userExists(self, username):
        if self._getUser(util.toBytes(username)) is not None:
            return True
        return False
        
    def _getUser(self, username):
        """Get the id of a specific user."""
        return self.db.fetchone(
            table='users', 
            filters={
                'nickname': util.toBytes(username),
                'server': self.cmdInstance.server
            }
        )
    
    def _getUserById(self, uid):
        """Get the id of a specific user."""
        return self.db.fetchone(
            table='users', 
            filters={
                'id': uid,
                'server': self.cmdInstance.server
            }
        )

    def _getUid(self, username):
        """Get the id of a specific user."""
        user = self._getUser(util.toBytes(username)) 
        if user is not None:
            return user[0]
        return None

    def _isLoggedIn(self, username):
        if username in src.module.loggedInUsers:
            return True
        return False
        
    def _addUser(self, username, password):
        self.db.insert(
            table='users', 
            data={
                'nickname': util.toBytes(username),
                'password': hashlib.sha256(util.toBytes(password)).hexdigest(),
                'server': self.cmdInstance.server
            }
        )
        
    def _removeUser(self, username):
        self.db.delete(
            table='users', 
            filters={
                'nickname': util.toBytes(username),
                'server': self.cmdInstance.server
            }
        )

    def _users(self):
        return self.db.fetchall(
            table='users', 
            filters={
                'server': self.cmdInstance.server
            }
        )
    
    def _vpsUsers(self, output='string'):
        for group in grp.getgrall():
            if group.gr_name == 'users':
                members = group.gr_mem
        if output == 'list':
            return members
        else:
            return ', '.join(members)
    
    def userExists(self):
        """Check if a user exists. Usage: user.userExists <user>."""
        user = self.args
        if self._userExists(user):
            self.reply(
                "User '%s' exists in the system." % (user,)
            )
        else:
            self.reply(
                "User '%s' does *not* exist in the system." % (user,)
            )
    
    def identify(self):
        """Identify yourself to the system (do this in a pm to the bot). Usage: user.identify <password>."""
        user = self._getUser(self.username)
        if user is not None:
            if user[2] == hashlib.sha256(util.toBytes(self.args)).hexdigest():
                # TODO: replace the unixtimestamps with actual unix timestamps
                src.module.loggedInUsers[self.username] = {
                    'lastLogin': 'unixtimestamp',
                    'failedLoginAttemptsSinceLastLogin': 0,
                    'loggedTime': 'unixtimestamp'
                }
                self.reply("You're now logged in :D")
            else:
                self.reply("Incorrect password :/")
        else:
            self.reply(
                "No user with nickname '%s' was found :(" % (self.username,)
            )

    def isLoggedIn(self):
        """Check if a user is logged in. Usage: user.isLoggedIn <user>."""
        user = self.args
        if self._isLoggedIn(user):
            self.reply("%s is logged in." % (user,))
        else:
            self.reply("%s is *not* logged in." % (user,))
    
    def vpsUsers(self):
        """Get a list of users in the users group on the VPS."""
        self.reply(self._vpsUsers())
        
    def users(self):
        """Reply with all the users found in the database. Usage: user.users."""
        noUsers = True
        for user in self._users():
            self.reply("id: %s, user: %s" % (
                    user[0], 
                    util.toUnicode(user[1])
                )
            )
            noUsers = False
        if noUsers:
            self.reply("There are no users yet!...")
    
    def add(self):
        """Add a user to the database. Usage: user.add <name> <password>."""
        username, password = self.args.split()
        if self._userExists(username):
            self.reply(
                "User '%s' already exists in the system D: ..." % (username,)
            )
        else:
            self._addUser(username, password)
            self.reply("Added user '%s' to the system :)" % (username,))
            
    def rm(self):
        """Remove a user from the database. Usage: user.rm <username>."""
        user = self.args
        if self._userExists(user):
            self._removeUser(user)
            self.reply("Delete user '%s' from the system :'( ..." % (user,))
        else:
            self.reply("User '%s' dosn't exist in the system :) ..." % (user,))
