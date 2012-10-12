#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC commands...

"""

import pkgutil
import sys
import importlib

import src.utilities as util
import src.settings
import src.commands


class Command(object):
    
    commandModules = {}
    
    def __init__(self, settingsInstance, botInstance):
        """Prepare the object and load all the command modules."""
        super(Command, self).__init__()
        self.settingsInstance = settingsInstance
        self.botInstance = botInstance
        self.sock = None
        self.running = False
        self.loadTheModules()
        self.user = ""
        self.channel = ""
    
    def pong(self, data):
        pong = data.split(":")[1]
        self.sendRawMessage("PONG :%s" % (pong,))
 
    def ident(self):
        util.write("Sending ident")
        nick = self.settingsInstance.settings['nickname']
        real = self.settingsInstance.settings['realname']
        host = self.botInstance.server.address
        self.sendRawMessage("NICK %s" % nick)
        self.sendRawMessage("USER %s %s +iw :%s" % (real, host, real,))
    
    def joinRooms(self, channelDict):
        for name, obj in channelDict.items():
            self.joinRoom(obj.name)
    
    def joinRoom(self, room):
        self.sendRawMessage("JOIN :%s" % (room,))
    
    def identify(self):
        pass
    
    def disconnect(self):
        pass
    
    def sendRawMessage(self, text):
        util.write(text)
        text = util.toBytes("%s\r\n" % (text,))
        self.sock.send(text)

    def replyWithMessage(self, text, msgType='PRIVMSG'):
        util.write(text)
        text = util.toBytes("%s %s :%s\r\n" % (msgType, self.channel, text,))
        self.sock.send(text)
    
    def execute(self, command):
        util.write("Executing %s" % (command,))
        cmd = command.split('.')
        try:
            if len(cmd) > 1:
                getattr(self.commandModules[cmd[0]], cmd[0].title())(self, cmd[1])
            else:
                getattr(self.commandModules[command], command.title())(self, None)
        except AttributeError:
            self.replyWithMessage("Command '%s' was not found" % (command,))
    
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
                self.commandModules[package_name] = module
    
    @property
    def sock(self):
        """Getter for the _sock attribute."""
        return self._sock

    @sock.setter
    def sock(self, value):
        """Getter for the _sock attribute."""
        self._sock = value
        
