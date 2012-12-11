#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
User module. Implements a full authentication system, and project
tracking.

"""

import src.module
import src.modules.user.user
import src.utilities as util


class Project(src.module.ModuleBase):
    
    def __init__(self, cmdInstance, cmdName=None, cmdArgs=None):
        super(Project, self).__init__(
            cmdInstance,
            cmdArgs=cmdArgs,
            authRequired=['rm']
        )
        self.db = 'database.sqlite3'
        self._createTables([
            'CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, userId INTEGER, name TEXT, dir TEXT)'
        ])
        self.userModule = src.modules.user.user.User(cmdInstance)
        if cmdName is not None:
            self._execute(cmdName)
            
    def _addProject(self, username, projectName, path):
        user = self.userModule._getUid(util.toBytes(username))
        if user is not None:
            self.db.insert(
                table='projects', 
                data={
                    'userID': user, 
                    'name': util.toBytes(projectName), 
                    'dir': util.toBytes(path)
                }
            )
            return True
        return False
            
    def _removeProject(self, username, projectName):
        user = self.userModule._getUid(util.toBytes(username))
        if user is not None:
            self.db.delete(
                table='projects', 
                filters={
                    'userId': user,
                    'name': util.toBytes(projectName)
                }
            )
            return True
        return False
            
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
        """Reply with the project information. Usage: project.project <project name> [user]."""
        try:
            projectname, username = self.args.split()
        except ValueError:
            username = self.username
            projectname = self.args
        project = self._project(username, projectname)
        if project is not None:
            self.reply(project[0] + " : " + project[1])
        else:
            self.reply(
                "No project '%s' found under user %s..." % (projectname, username)
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
        """Add a project to the database. Usage: project.add <project name> <path> [user]. If no user is supplied, it will be implied that the user is the command issuer."""
        try:
            projectName, path, user = self.args.split()
        except ValueError:
            user = self.username
            projectName, path = self.args.split()
        if self._addProject(user, projectName, path):
            self.reply("Added project '%s' to user %s" % (projectName, user,))
        else:
            self.reply("Please create a user account for '%s' first." % (user,))
        
    def rm(self):
        """Remove a project from the database. Usage: project.rm <project name> [here]. If no user is supplied, it will be implied that the user is the command issuer."""
        try:
            projectName, user = self.args.split()
        except ValueError:
            user = self.username
            projectName = self.args
        if self._removeProject(user, projectName):
            self.reply("Deleted project '%s' from user %s" % (projectName, user,))
        else:
            self.reply("Project '%s' wasn't found under user %s" % (projectName, user,))


