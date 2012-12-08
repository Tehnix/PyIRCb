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
        pass

    def pull(self, *args):
        cmd = ["git", "pull", "origin", "master"]
        #for i in args:
        #    cmd.append(i)
        p = subprocess.Popen(cmd, cwd="/home/tenshi/PyBot", shell=True, stdout=subprocess.PIPE)
        self.commandInstance.replyWithMessage(p.stdout.read())
        
    
    

