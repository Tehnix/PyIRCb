#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC commands...

"""

import imp
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
        """Respond to a PING with a PONG."""
        pong = data.split(":")[1]
        self.sendRawMessage("PONG :%s" % (pong,))
 
    def ident(self):
        """Send the identification and nickname to the server."""
        util.write("Sending ident")
        nick = self.settingsInstance.settings['nickname']
        real = self.settingsInstance.settings['realname']
        host = self.botInstance.server.address
        self.sendRawMessage("NICK %s" % nick)
        self.sendRawMessage("USER %s %s +iw :%s" % (real, host, real,))
    
    def ctcp(self):
        """Respond to a CTCP request."""
        self.sendRawMessage("NOTICE %s :\001VERSION PyBot : v2.0 : Python 3\001" % self.user)

    def joinRooms(self, channelDict):
        """Loop through all the channels in channelDict, and join the rooms."""
        for name, obj in channelDict.items():
            self.joinRoom(obj.name)
    
    def joinRoom(self, room):
        """Make the bot join a room."""
        self.sendRawMessage("JOIN :%s" % (room,))
    
    def identify(self):
        """Identify the bot (login)."""
        pass
    
    def disconnect(self):
        """Disconnect from the IRC server."""
        self.sendRawMessage("QUIT")
    
    def sendRawMessage(self, text):
        """Send a raw message to the socket."""
        util.write(text)
        text = util.toBytes("%s\r\n" % (text,))
        self.sock.send(text)

    def replyWithMessage(self, text, msgType='PRIVMSG'):
        """Send a message to the channel from which we received the command."""
        util.write(text)
        text = util.toBytes("%s %s :%s\r\n" % (msgType, self.channel, text,))
        self.sock.send(text)
    
    def execute(self, command):
        """
        Execute the command by seperating it on '.' and then taking the first
        index, (e.g. test.testing) and use the module 'src.commands.test.test'
        and the class Test, then pass the second index 'testing' as an arg to
        the __init__ of the class, which then executes the method.

        """
        util.write("Executing %s" % (command,))
        cmd = command.split('.')
        try:
            if len(cmd) > 1:
                if not cmd[1].startswith('_'):
                    getattr(self.commandModules[cmd[0]], cmd[0].title())(self.settingsInstance, self, cmd[1])
            else:
                getattr(self.commandModules[command], command.title())(self.settingsInstance, self, None)
        except AttributeError:
            self.replyWithMessage("Command '%s' was not found" % (command,))
        except KeyError:
            self.replyWithMessage("Command '%s' was not found" % (command,))
        except Exception as e:
            self.replyWithMessage("Exception occured: %s " % (e,))
    
    def update(self):
        """
        Reload all the command modules previously imported and saved to the
        class variable commandModules.

        """
        for name, module in self.commandModules.items():
            imp.reload(module)

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
        
