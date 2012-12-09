#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
User module. Implements a full authentication system, and project
tracking.

"""

import src.module
import src.commands.user.user
import src.utilities as util


class Project(src.module.ModuleBase):
    
    def __init__(self, cmdInstance, cmdName=None, cmdArgs=None):
        super(Project, self).__init__(
            cmdInstance,
            cmdArgs=cmdArgs,
            authRequired=['rm']
        )
        self.db = self._createDatabase('database.sqlite3')
        self._createTables([
            'CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, userId INTEGER, name TEXT, dir TEXT)'
        ])
        self.userModule = src.commands.user.user.User(cmdInstance)
        if cmdName is not None:
            self._execute(cmdName)
            
    def _addProject(self, username, projectName, path):
        self.db.insert(
            table='projects', 
            data={
                'userID': self.userModule._getUid(util.toBytes(username)), 
                'name': util.toBytes(projectName), 
                'dir': util.toBytes(path)
            }
        )
            
    def _removeProject(self, username, projectName):
        self.db.delete(
            table='projects', 
            filters={
                'userId': self.userModule._getUid(util.toBytes(username)),
                'name': util.toBytes(projectName)
            }
        )
            
    def _project(self, username, projectname):
        return self.db.fetchone(
            table='projects', 
            filters={
                'userId': self.userModule._getUid(util.toBytes(username)),
                'name': util.toBytes(projectname)
            }
        )
    
    def _projects(self, uid):
        return self.db.fetchall(
            table='projects', 
            filters={
                'userId': uid
            }
        )
    
    def project(self):
        """Reply with the project information. Usage: project.project <user> <project name>."""
        try:
            username, projectname = self.args.split()
        except ValueError:
            username = self.username
            projectname = self.args
        project = self._project(username, projectname)
        if project is not None:
            self.reply(project[0] + " : " + project[1])
        else:
            self.reply(
                "No project for %s name '%s'..." % (username, projectname)
            )
    
    def projects(self):
        """Reply with all the projects found in the database. Usage: project.projects [user]."""
        if self.args:
            users = [self.userModule._getUser(self.args)]
        else:
            users = self.userModule._users()
        projectsNotFound = True
        if users is not None:
            for user in users:
                projects = self._projects(user[0])
                if projects is not None:
                    self.reply("Owner: %s" % util.toUnicode(user[1]))
                i = 1
                for project in projects:
                    tree = '|-'
                    if i == len(projects):
                        tree = "'-"
                    self.reply(
                        "  %s Project Name: %s" % (
                            tree,
                            util.toUnicode(project[2])
                        )
                    )
                    projectsNotFound = False
                    i += 1
        if projectsNotFound:
            self.reply("No projects has been created yet! D: ...")

    def add(self):
        """Add a project to the database. Usage: project.addProject [user] <project name> <path>. If no user is supplied, it will be implied that the user is the command issuer."""
        try:
            user, projectName, path = self.args.split()
        except ValueError:
            user = self.username
            projectName, path = self.args.split()
        self.reply("Adding project '%s'" % (projectName,))
        self._addProject(user, projectName, path)
        
    def rm(self):
        """Remove a project from the database. Usage: project.rmProject [user] <project name>. If no user is supplied, it will be implied that the user is the command issuer."""
        try:
            user, projectName = self.args.split()
        except ValueError:
            user = self.username
            projectName = self.args
        self.reply("Deleting project %s" % (projectName,))
        self._removeProject(user, projectName)

