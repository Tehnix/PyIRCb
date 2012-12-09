#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

User command...

"""

from src.database import Database

class User(object):
    
    def __init__(self, settingsInstance, commandInstance, cmdName, *args):
        super(User, self).__init__()
        self.settingsInstance = settingsInstance
        self.commandInstance = commandInstance
        self.db = Database(dbtype="SQLite", dbname="database.db")
        self.db.execute(sql="""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,nickname TEXT, password TEXT, server TEXT)""")
        self.db.execute(sql="""CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY,userId INTEGER, name TEXT, dir TEXT)""")
        if cmdName is not None:
            if args[0] is not None:
                getattr(self, cmdName)(*args)
            else:
                getattr(self, cmdName)()
    
    def testuser(self):
        self.commandInstance.replyWithMessage(
            self.commandInstance.user
        )

    def testchannel(self):
        self.commandInstance.replyWithMessage(
            self.commandInstance.channel
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

    def add(self, *args):
        """$user.add (user password server)"""
        self.commandInstance.replyWithMessage(" ".join(args))
        args = args[0].split()
        data = {"nickname": args[0],
                "password": args[1],
                "server": args[2]}
        self.db.insert(table="users", data=data)
            
    def rmrf(self, *args):
        """$user.rmrf (user)
        INB4 worst idea ever."""
        args = args[0].split()
        data = {"nickname": args[0]}
        self.db.delete(table="users", filters=data)
        
    def rmrfProject(self, *args):
        """$user.rmrf (user)
        INB4 worst idea ever."""
        args = args[0].split()
        data = {"name": args[0]}
        self.db.delete(table="projects", filters=data)
    
    def addProject(self, *args):
        """$user.addProject (user projectName path)"""
        args = args[0].split()
        user, projectName, path = args
        search = {"nickname": user}
        res = self.db.fetchone(table="users", filters=search)
        userid = res[0]
        data = {"userID": userid, "name": projectName, "dir": path}
        self.db.insert(table="projects", data=data)

    def printUser(self, *args):
        """$user.printUser (user)"""
        args = args[0].split()
        search = {"nickname": args[0]}
        res = self.db.fetchone(table="users", filters=search)
        self.commandInstance.replyWithMessage(res)

    def printProject(self, *args):
        """$user.printProject (project)"""
        args = args[0].split()
        search = {"name": args[0]}
        res = self.db.fetchone(table="projects", filters=search)
        self.commandInstance.replyWithMessage(res)
