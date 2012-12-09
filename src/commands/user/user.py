#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
user command...

"""

from src.irc.database import Database

class user(object):
    def __init__(self, settingsInstance, commandInstance, cmdName, *args):
        super(user, self).__init__()
        self.settingsInstance = settingsInstance
        self.commandInstance = commandInstance
        if cmdName is not None:
            if args[0] is not None:
                getattr(self, cmdName)(*args)
            else:
                getattr(self, cmdName)()
        self.db = Database(dbtype="SQLite", dbname="database.db")
        self.db.execute(sql="""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,nickname TEXT, password TEXT, server TEXT)""")
        self.db.execute(sql="""CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY,userId INTEGER, name TEXT, dir TEXT)""")

    def add(self, *args):
        """$user.add (user password server)"""
        data = {"nickname": args[0],
                "password": args[1],
                "server": args[2]}
        self.db.insert(table="users", data=data)
            
    def rmrf(self, *args):
        """$user.rmrf (user)
        INB4 worst idea ever."""
        data = {"nickname": args[0]}
        self.db.delete(table="users", filters=data)
        
    def rmrfProject(self, *args):
        """$user.rmrf (user)
        INB4 worst idea ever."""
        data = {"name": args[0]}
        self.db.delete(table="projects", filters=data)
    
    def addProject(self, *args):
        """$user.addProject (user projectName path)"""
        user, projectName, path = args
        search = {"nickname": user}
        res = self.db.fetchone(table="users", filter=search)
        userid = res[0]
        data = {"userID": userid, "name": projectName, "dir": path}
        self.db.insert(table="projects", filter=data)

    def printUser(self, *args):
        """$user.printUser (user)"""
        search = {"nickname": args[0]}
        res = self.db.fetchone(table="users", filter=search)
        self.commandInstance.replyWithMessage(res)

    def printProject(self, *args):
        """$user.printProject (project)"""
        search = {"name": args[0]}
        res = self.db.fetchone(table="projects", filter=search)
        self.commandInstance.replyWithMessage(res)
