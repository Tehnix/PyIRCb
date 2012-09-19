#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Settings file reader

"""

import ast


class Settings(object):
    """Reads the settings file, parses it and converts it into attributes."""

    servers = {}

    def __init__(self):
        """Initialize the super class, and read the settings file."""
        super(Settings, self).__init__()
        self.readSettingsFile()
        self.parseAttributes()

    def readSettingsFile(self):
        """Read the settings file and convert it to a dict."""
        with open('pybot.conf', 'r') as settingsFile:
            self.settingsFileData = ast.literal_eval(settingsFile.read())

    @property
    def settingsFileData(self):
        """Getter for the _settingsFileData attribute."""
        return self._settingsFileData

    @settingsFileData.setter
    def settingsFileData(self, value):
        """Getter for the _settingsFileData attribute."""
        self._settingsFileData = value

    def parseAttributes(self):
        for server, info in self.settingsFileData['servers'].items():
            self.servers[server] = ServerObject()
            self.addServerInfo(self.servers[server], server, info)
            self.addChannelInfo(self.servers[server], server)

    def addServerInfo(self, obj, server, info):
        try:
            obj.address = info['address']
        except KeyError:
            warning('No address specified for server "%s" in the settings file' % (server,))
        try:
            obj.port = info['port']
        except KeyError:
            pass
        try:
            obj.ssl = info['ssl']
        except KeyError:
            pass

    def addChannelInfo(self, obj, server):
        try:
            for channel in self.settingsFileData['channels'][server]:
                obj.channels[channel] = ChannelObject()
                obj.channels[channel].name = channel
        except KeyError:
            pass


class ServerObject(object):
    """Container for server data."""

    def __init__(self):
        super(ServerObject, self).__init__()
        self.address = None
        self.port = '6667'
        self.ssl = False
        self.channels = {}


class ChannelObject(object):
    """Container for channel data."""

    def __init__(self):
        self.name = None
        self.users = {}

    def usersInRoom(self):
        return len(self.users)


def warning(text):
    """Warn the user about an error."""
    print "Settings Error: %s" % (text,)
