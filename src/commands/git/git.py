#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Git commands!

"""

import subprocess       


class Git(object):
    """Interact with git."""
    
    def __init__(self, cmdInstance, cmdName=None, cmdArgs=None):
        super(Git, self).__init__(cmdInstance, cmdArgs=cmdArgs)
        if cmdName is not None:
            self._execute(cmdName)

    def clone(self):
        """Clone a repository into a directory. Usage git.clone <repository> <absolute path to dir>."""
        try:
            url, path = self.args.split()
            cmd = ["git", "clone", repos, path]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            self.reply(p.stdout.read())
        except ValueError:
            self.reply("Usage: git.clone <repository> <absolute path to dir>")

    def pull(self):
        """Pull down updates. Usage: git.pull [absolute path to dir]."""
        path = None
        if self.args:
            path = self.args
        cmd = ["git", "pull", "origin", "master"]
        p = subprocess.Popen(cmd, cwd=path, stdout=subprocess.PIPE)
        self.reply(p.stdout.read())
        
    
    

