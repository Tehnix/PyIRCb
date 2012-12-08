#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Git commands!

"""

import subprocess       


class Git(object):
    def __init__(self, settingsInstance, commandInstance, cmdName, *args):
        super(Git, self).__init__()
        self.settingsInstance = settingsInstance
        self.commandInstance = commandInstance
        if cmdName is not None:
            if args[0] is not None:
                getattr(self, cmdName)(*args)
            else:
                getattr(self, cmdName)()

    def clone(self, *args):
        """Clone a repository into a directory. Usage git.clone <repository> <absolute path to dir> ."""
        path = None
        try:
            cmd = ["git", "clone", args[0]]
            path = ' '.join(args[1:])
            self.commandInstance.replyWithMessage(args)
            self.commandInstance.replyWithMessage(path)
            #p = subprocess.Popen(cmd, cwd=path, stdout=subprocess.PIPE)
            #self.commandInstance.replyWithMessage(p.stdout.read())
        except IndexError:
            self.commandInstance.replyWithMessage(
                "Usage: git.clone <repository> <absolute path to dir>"
            )



    def pull(self, *args):
        """Pull down updates. Usage: git.pull [absolute path to dir] ."""
        cmd = ["git", "pull", "origin", "master"]
        path = None
        if args:
            path = ' '.join(args)
        p = subprocess.Popen(cmd, cwd=path, stdout=subprocess.PIPE)
        self.commandInstance.replyWithMessage(p.stdout.read())
        
    
    

