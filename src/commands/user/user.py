#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

User command...

"""

import hashlib
import grp
from src.database import Database
import src.utilities as util


loggedInUsers = []


class User(object):
    
    def __init__(self, settingsInstance, commandInstance, cmdName, *args):
        super(User, self).__init__()
        self.settingsInstance = settingsInstance
        self.commandInstance = commandInstance
        self.db = Database(dbtype="SQLite", dbname="database.db")
        self.db.execute(
            'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,nickname TEXT, password TEXT, server TEXT)'
        )
        self.db.execute(
            'CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY,userId INTEGER, name TEXT, dir TEXT)'
        )
        if cmdName is not None:
            if args[0] is not None:
                getattr(self, cmdName)(*args)
            else:
                getattr(self, cmdName)()

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

    def _getUid(self, username):
        """Get the id of a specific user."""
        res = self.db.fetchone(
            table='users', 
            filters={
                'nickname': username,
                'server': self.commandInstance.server
            }
        )
        return res[0]

    def identify(self, *args):
        """Identify yourself to the system (do this in a pm to the bot). Usage: user.identify <password>."""
        global loggedInUsers
        password = hashlib.sha256(util.toBytes(args[0])).hexdigest()
        filters = {
            "nickname": self.commandInstance.user,
            "password": password,
            "server": self.commandInstance.server
        }
        res = self.db.fetchone(table='users', filters=filters)
        if res is not None:
            loggedInUsers.append(self.commandInstance.user)
            self.commandInstance.replyWithMessage(
                "You're now logged in!"
            )
        else:
            self.commandInstance.replyWithMessage(
                "Wrong user/password!"
            )


    def add(self, *args):
        """Add a user to the database. Usage: user.add <name> <password>."""
        user, password = args[0].split()
        self.commandInstance.replyWithMessage("Creating user %s" % (user,))
        self._add(*args)

    def _add(self, *args):
        nickname, password = util.toBytes(args[0]).split()
        password = hashlib.sha256(password).hexdigest()
        data = {
            "nickname": nickname,
            "password": password,
            "server": self.commandInstance.server
        }
        self.db.insert(table='users', data=data)
            
    def rm(self, *args):
        """Remove a user from the database. Usage: user.rm <username>."""
        self.commandInstance.replyWithMessage("Deleting user %s" % (args[0],))
        self._rm(*args)

    def _rm(self, *args):
        args = util.toBytes(args[0]).split()
        data = {
            "nickname": args[0],
            "server": self.commandInstance.server
        }
        self.db.delete(table="users", filters=data)
    
    def rmProject(self, *args):
        """Remove a project from the database. Usage: user.rmProject <user> <project name>."""
        user, projectName = args[0].split()
        self.commandInstance.replyWithMessage("Deleting project %s" % (projectName,))
        self._rmProject(*args)

    def _rmProject(self, *args):
        args = util.toBytes(args[0]).split()
        user, projectName = args
        self.db.delete(
            table="projects", 
            filters={
                'userId': self._getUid(user),
                'name': projectName
            }
        )
   
    def addProject(self, *args):
        """Add a project to the database. Usage: user.addProject <user> <project name> <path>."""
        user, projectName, path = args[0].split()
        self.commandInstance.replyWithMessage("Adding project '%s'" % (projectName,))
        self._addProject(*args)

    def _addProject(self, *args):
        args = util.toBytes(args[0]).split()
        user, projectName, path = args
        self.db.insert(
            table="projects", 
            data={
                "userID": self._getUid(user), 
                "name": projectName, 
                "dir": path
            }
        )
    
    def printUser(self, *args):
        """Reply with the user. Usage: user.printUser <user>."""
        self.commandInstance.replyWithMessage(
            self._printUser(*args)
        )

    def _printUser(self, *args):
        args = util.toBytes(args[0]).split()
        res = self.db.fetchone(
            table="users", 
            filters={
                'nickname': args[0],
                'server': self.commandInstance.server
            }
        )
        return res[1]

    def printProject(self, *args):
        """Reply with the project information. Usage: user.printProject <user> <project name>"""
        self.commandInstance.replyWithMessage(
            self._printProject(*args)
        )

    def _printProject(self, *args):
        args = util.toBytes(args[0]).split()
        user, projectName = args
        res = self.db.fetchone(
            table="projects", 
            filters={
                'userId': self._getUid(user),
                'name': projectName
            }
        )
        return res[2] + " : " + res[3] 

