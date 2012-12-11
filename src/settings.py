#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Settings file reader

"""

import sys
import json

import src.utilities as util


DEFAULT_SETTINGS_PATH = 'pybot.conf'
DEFAULT_CONF = '{\n\
    "nickname": "Innocence",\n\
    "realname": "Motoko Kusanagi",\n\
    "servers": {\n\
        "freenode": {\n\
            "admins": [],\n\
            "address": "irc.freenode.org",\n\
            "port": 6697,\n\
            "channels": [\n\
                "#python"\n\
            ],\n\
            "ssl": true,\n\
            "identify": false\n\
        }\n\
    },\n\
    "commands": {}\n\
}'

class Settings(object):
    """Reads the settings file, parses it and converts it into attributes."""
    
    def __init__(self, generateConf=False):
        """Set the initial settings file name."""
        super(Settings, self).__init__()
        if generateConf:
            self.writeSettingsFile(DEFAULT_CONF, path=DEFAULT_SETTINGS_PATH)
        else:
            try:
                self.settingsFilePath = DEFAULT_SETTINGS_PATH
            except IOError:
                self.writeSettingsFile(
                    DEFAULT_CONF,
                    path=DEFAULT_SETTINGS_PATH
                )
                util.write(
                    "No configuration file found, a default one has been generated at %s." % (DEFAULT_SETTINGS_PATH,),
                    priority=9
                )
                sys.exit(0)
    
    def reload(self):
        self.readSettingsFile()

    def writeSettingsFile(self, JSON, path=None):
        """Write the settings file as a JSON object."""
        if path is not None:
            settingsFilePath = path
        else:
            settingsFilePath = self.settingsFilePath
        with open(settingsFilePath, 'w') as settingsFile:
            settingsFile.write(JSON)

    def readSettingsFile(self):
        """Read the settings file and convert it to a dict."""
        with open(self.settingsFilePath, 'r') as settingsFile:
            self.settings = json.loads(settingsFile.read())

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

