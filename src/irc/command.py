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
        text = "%s\r\n" % (text,)
        util.write(text)
        self.sock.send(util.toBytes(text))

    def replyWithMessage(self, text, msgType='PRIVMSG'):
        """Send a message to the channel from which we received the command."""
        text = "%s %s :%s\r\n" % (msgType, self.channel, text,)
        util.write(text)
        self.sock.send(util.toBytes(text))
    
    def execute(self, command):
        """
        Execute the command by seperating it on '.' and then taking the first
        index, (e.g. test.testing) and use the module 'src.commands.test.test'
        and the class Test, then pass the second index 'testing' as an arg to
        the __init__ of the class, which then executes the method.

        """
        cmd = self.splitCommand(command)
        util.write("Executing %s.%s with args: %s" % (cmd[0], cmd[1], cmd[2],))
        try:
            if cmd[1] is None:
                publicMethods = util.publicMethods(
                    getattr(
                        self.commandModules[cmd[0]], 
                        cmd[0].title()
                    )
                )
                self.replyWithMessage(
                    "%s: %s" % (command.title(), publicMethods)
                )
            elif not cmd[1].startswith('_'):
                getattr(
                    self.commandModules[cmd[0]],
                    cmd[0].title()
                )(self.settingsInstance, self, cmd[1], cmd[2])
            else:
                self.replyWithMessage(
                    "Methods starting with _ are private methods!"
                )
        except (AttributeError, KeyError):
            if cmd[1] is not None:
                self.replyWithMessage(
                    "Command %s.%s was not found" % (cmd[0], cmd[1],)
                )
            else:
                self.replyWithMessage(
                    "Module '%s' was not found" % (cmd[0],)
                )
        except Exception as e:
            self.replyWithMessage("Exception occured: %s " % (e,))
    
    def splitCommand(self, command):
        """
        Split the command up into three parts at three indexes:
            0: class name
            1: method name
            2: arguments
        and return it.
        
        """
        cmd = [None, None, None]
        if '.' in command:
            tCmd = command.split('.')
            cmd[0] = tCmd[0].lower()
            tCmd[1] = '.'.join(tCmd[1:])
            cmd[1] = tCmd[1]
            if ' ' in tCmd[1]:
                cmd[1] = tCmd[1].split(' ')[0]
                cmd[2] = ' '.join(tCmd[1].split(' ')[1:])
        else:
            cmd[0] = command.lower()
        return cmd
    
    def update(self):
        """
        Reload all the command modules previously imported and saved to the
        class variable commandModules.

        """
        self.loadTheModules()
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
                self.commandModules[package_name.lower()] = module
        
