#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC import handler...

"""

import imp
import pkgutil
import importlib


class ImportHandler(object):
    """Manage module imports and updates."""
    
    def __init__(self, cmdHandler):
        super(ImportHandler, self).__init__()
        self.reply = cmdHandler.replyWithMessage
        self.importedModules = {}
        self.loadTheModules()
    
    def update(self, mod=None):
        """
        Reload all the command modules previously imported and saved to the
        class variable commandModules.

        """
        self.loadTheModules()
        moduleNotFound = True
        for name, module in self.importedModules.items():
            if mod is None or name == mod:
                imp.reload(module)
                moduleNotFound = False
        if moduleNotFound: 
            self.reply("No module named %s." % (mod,))
        else:
            self.reply("Modules have been updated!")


    def loadTheModules(self):
        """
        Dynamically load all the packages/modules in src/commands and add them
        to the class variable commandModules in the format: 
            name: moduleObject
        So we can easily refer to them later.
        
        """
        for importer, package_name, _ in pkgutil.iter_modules(['src/modules']):
            module = importlib.import_module(
                'src.modules.%s.%s' % (package_name, package_name)
            )
            self.importedModules[package_name.lower()] = module
