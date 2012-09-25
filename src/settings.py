#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Settings file reader

"""

import ast


class Settings(object):
    """Reads the settings file, parses it and converts it into attributes."""
    
    def __init__(self):
        """Initialize the super class, and read the settings file."""
        super(Settings, self).__init__()
        try:
            self.settingsFilePath = 'pybot.conf'
        except IOError:
            self.settings = {}
    
    def reload(self):
        self.readSettingsFile()

    def readSettingsFile(self):
        """Read the settings file and convert it to a dict."""
        with open(self.settingsFilePath, 'r') as settingsFile:
            self.settings = ast.literal_eval(settingsFile.read())

    @property
    def settingsFilePath(self):
        """Getter for the _settingsFileData attribute."""
        return self._settingsFilePath

    @settingsFilePath.setter
    def settingsFilePath(self, value):
        """Getter for the _settingsFileData attribute."""
        self._settingsFilePath = value
        self.readSettingsFile()
        
    @property
    def settings(self):
        """Getter for the _settingsFileData attribute."""
        return self._settings

    @settings.setter
    def settings(self, value):
        """Getter for the _settingsFileData attribute."""
        self._settings = value


def warning(text):
    """Warn the user about an error."""
    print "Settings Error: %s" % (text,)
