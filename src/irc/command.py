#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC commands...

"""

import pkgutil
import sys
import importlib

import src.utilities as util
import src.commands


class Command(object):
    
    commandModules = {}
    
    def __init__(self):
        """Prepare the object and load all the command modules."""
        super(Command, self).__init__()
        self.running = False
        self.loadTheModules()
        
    def loadTheModules(self):
        """
        Dynamically load all the packages/modules in src/commands and add them
        to the class variable commandModules in the format: 
            name: moduleObject
        So we can easily refer to them later.
        
        """
        for importer, package_name, _ in pkgutil.iter_modules(['src/commands']):
            full_pkg_name = 'src.commands.%s.%s' % (package_name, package_name)
            if full_pkg_name not in sys.modules:
                module = importlib.import_module(full_pkg_name)
                commandModules[package_name] = module
    
    def execute(self, command):
        src.commands.test.test.Test()
        
