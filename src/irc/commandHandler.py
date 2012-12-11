#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC command handler...

"""

import sys
import time

import main as pybotmain
import src.settings
import src.modules
import src.utilities as util
import src.irc.importHandler


class CommandHandler(object):
    
    def __init__(self, server):
        """Prepare the object and load all the command modules."""
        super(CommandHandler, self).__init__()
        self.server = server
        self.sock = None
        self.running = False
        self.user = ""
        self.channel = ""
        self.msgType = "PRIVMSG"
        self.importHandler = src.irc.importHandler.ImportHandler()
    
    def pong(self, data):
        """Respond to a PING with a PONG."""
        pong = data.split(":")[1]
        self.sendRawMessage("PONG :%s" % (pong,))
 
    def ident(self):
        """Send the identification and nickname to the server."""
        util.write("Sending ident")
        self.sendRawMessage("NICK %s" % self.server.nickname)
        self.sendRawMessage("USER %s %s +iw :%s" % (
            self.server.realname,
            self.server.address,
            self.server.realname
        ))
    
    def ctcp(self):
        """Respond to a CTCP request."""
        version = pybotmain.__VERSION__
        self.sendRawMessage("NOTICE %s :\001VERSION PyBot : v%s : Python 3\001" % (self.user, version))

    def joinRooms(self, channelDict):
        """Loop through all the channels in channelDict, and join the rooms."""
        for name, obj in channelDict.items():
            self.joinRoom(obj.name)
    
    def joinRoom(self, room):
        """Make the bot join a room."""
        self.sendRawMessage("JOIN :%s" % room)
    
    def topic(self, text):
        """Return or set the topic of the channel."""
        if text:
            self.sendRawMessage('TOPIC %s :%s' % (self.channel, text))
            self.replyWithMessage('Topic has been set to %s' % text)
        else:
            self.replyWithMessage(
                "Topic: %s" % self.server.channels[self.channel].topic
            )

    def displayUsers(self):
        """Display the current users in the server object."""
        self.replyWithMessage('Users online:')
        for user, info in self.server.users.items():
            if info.online:
                self.replyWithMessage('  ' + info.nickname)

    def identify(self):
        """Identify the bot (login)."""
        pass
    
    def disconnect(self):
        """Disconnect from the IRC server."""
        self.sendRawMessage("QUIT")
    
    def sendRawMessage(self, text):
        """Send a raw message to the socket."""
        text = "%s\r\n" % text
        util.write(text)
        self.sock.send(util.toBytes(text))

    def replyWithMessage(self, text, msgType=None):
        """Send a message to the channel from which we received the command."""
        text = util.toUnicode(text)
        recipient = self.user
        if self.channel.startswith("#"):
            recipient = self.channel
        if msgType is None:
            msgType = self.msgType
        # Avoid flooding of a channel
        splitText = text.split("\n")
        timeout = 0.2
        if len(splitText) > 10:
            timeout = 0.5
        for txt in splitText:
            txt = "%s %s :%s\r\n" % (msgType, recipient, txt)
            util.write(txt)
            self.sock.send(util.toBytes(txt))
            time.sleep(timeout)
            
    def _splitCommand(self, command):
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
        
    def execute(self, command):
        """
        Execute the command by seperating it on '.' and then taking the first
        index, (e.g. test.testing) and use the module 'src.modules.test.test'
        and the class Test, then pass the second index 'testing' as an arg to
        the __init__ of the class, which then executes the method.

        """
        cmdClass, cmdMethod, cmdArgs = self._splitCommand(command)
        util.write("Executing %s.%s with args: %s" % (
            cmdClass,
            cmdMethod,
            cmdArgs
        ))
        try:
            # If there is only a module (ie $test)
            if cmdMethod is None:
                publicMethods = util.publicMethods(
                    getattr(
                        self.importHandler.importedModules[cmdClass], 
                        cmdClass.title()
                    )
                )
                self.replyWithMessage(
                    "%s: %s" % (command.title(), publicMethods)
                )
            # If there is also a method on the module, and it isn't a private
            # method (ie $test.testing)
            elif not cmdMethod.startswith('_'):
                getattr(
                    self.importHandler.importedModules[cmdClass],
                    cmdClass.title()
                )(self, cmdName=cmdMethod, cmdArgs=cmdArgs)
            else:
                self.replyWithMessage(
                    "Methods starting with _ are private methods!"
                )
        except (AttributeError, KeyError):
            if cmdMethod is not None:
                self.replyWithMessage(
                    "Command %s.%s was not found" % (cmdClass, cmdMethod)
                )
            else:
                self.replyWithMessage(
                    "Module '%s' was not found" % cmdClass
                )
        except Exception as e:
            self.replyWithMessage("Exception occured during command execution: %s " % e)
            util.writeException(sys.exc_info())
    
    def help(self, command):
        """
        Look up the docstring for a given module or method from a module.
        """
        command = command[5:]
        cmdClass, cmdMethod, cmdArgs = self._splitCommand(command)
        util.write("Finding docstring for %s.%s" % (cmdClass, cmdMethod))
        try:
            # If there is only a module (ie $test)
            if cmdMethod is None:
                docString = util.getDocstring(
                    getattr(
                        self.importHandler.importedModules[cmdClass], 
                        cmdClass.title()
                    )
                )
                self.replyWithMessage(
                    "%s: %s" % (command.title(), docString)
                )
            # If there is also a method on the module, and it isn't a private
            # method (ie $test.testing)
            elif not cmdMethod.startswith('_'):
                docString = util.getDocstring(
                    cmdMethod,
                    targetClass=getattr(
                    self.importHandler.importedModules[cmdClass],
                    cmdClass.title()
                    )
                )
                self.replyWithMessage(
                    "%s.%s: %s" % (cmdClass.title(), cmdMethod, docString)
                )
            else:
                self.replyWithMessage(
                    "Docstring: Methods starting with _ are private methods!"
                )
        except (AttributeError, KeyError):
            if cmdMethod is not None:
                self.replyWithMessage(
                    "Docstring: Command %s.%s was not found" % (cmdClass, cmdMethod)
                )
            else:
                self.replyWithMessage(
                    "Docstring: Module '%s' was not found" % cmdClass
                )
        except Exception as e:
            self.replyWithMessage("Docstring: Exception occured: %s " % e)
            util.writeException(sys.exc_info())
