#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC messages...

"""

import sys
import time
import socket

from main import UpdateSourceCode
import src.utilities as util
import src.irc.commandHandler


class BreakOutOfLoop(Exception):
    pass


class DataParser(object):
    """Parse IRC output and react to commands."""
    
    def __init__(self, server):
        """Prepare the object."""
        super(DataParser, self).__init__()
        self.server = server
        self.commandHandler = None # set when the socket is not None
        self.sock = None
        self.readBuffer = None
        self.todo = []
    
    def parse(self):
        """
        Read the data from the socket, split it by \r\n and send it to the
        parseData() method.
        
        """
        while True:
            try:
                # if the last element in the split isn't a '', then it didn't
                # end on a \r\n.
                stream = util.toUnicode(self.sock.recv(4096)).split('\r\n')
                for data in stream:
                    util.write(data)
                    self.parseData(data)
                time.sleep(0.1)
            except (socket.timeout, socket.error, BreakOutOfLoop):
                self.server.connect = False
                break
            except (KeyboardInterrupt, SystemExit):
                self.commandHandler.replyWithMessage('Shutting down the bot')
                self.server.connect = False
                break
            except UnicodeDecodeError:
                continue
            except UnicodeEncodeError:
                continue
    
    def parseData(self, data):
        """Parse through the data stream received from the socket."""
        if self.server.node is None:
            self.server.node = data.split()[0][1:]
        # Server messages start with :node (eg :verne.freenode.net), so we
        # check for this and can then be confident it's from the server
        if data.startswith("PING :"):
            self.commandHandler.pong(data)
        elif data.startswith("\x01VERSION\x01"):
            self.commandHandler.ctcp()
        elif data.startswith("ERROR :Closing Link:"):
            raise BreakOutOfLoop
        elif data.startswith(":%s" % self.server.node):
            self.serverActions(data)
        else:
            try:
                self.userActions(data)
            except IndexError:
                pass

    def serverActions(self, data):
        """Commands invoked by the server."""
        ndata = data[len(self.server.node)+2:]
        if ndata.startswith("376 %s :End of /MOTD command." % self.server.nickname):
            self.commandHandler.joinRooms(self.server.channels)
        elif ndata.startswith("332"):
            channel = ndata.split()[2]
            self.server.channels[channel].topic = (':'.join(ndata.split(':')[1:]))
        elif ndata.startswith("353"):
            channel = ndata.split()[3]
            users = (':'.join(ndata.split(':')[1:])).split()
            self.server.channels[channel].addUsers(users)
        elif "* :*** No Ident response" in data:
            self.commandHandler.ident()
            self.commandHandler.joinRooms(self.server.channels)

    def userActions(self, data):
        """Commands invoked by the user."""
        data = data.split(':')
        cmd = ':'.join(data[2:])[1:]
        if data[1].split()[1] in ['PRIVMSG', 'NOTICE']:
            self.commandHandler.user = data[1].split()[0].split('!')[0]
            self.commandHandler.channel = data[1].split()[2]
            self.commandHandler.msgType = data[1].split()[1]
            if data[2].lower().startswith('%supdate' % self.server.operator):
                update = cmd.lower().split()
                try:
                    self.commandHandler.importHandler.update(update[1])
                except IndexError:
                    self.commandHandler.importHandler.update()
            elif data[2].startswith('%shelp' % self.server.operator):
                self.commandHandler.help(cmd)
            elif data[2].startswith('%stopic' % self.server.operator):
                self.commandHandler.topic(cmd[6:])
            #elif data[2].startswith('%ssource' % self.server.operator):
            #    raise UpdateSourceCode
            elif data[2].startswith(self.server.operator):
                self.commandHandler.execute(cmd)
        elif data[1].split()[1] in ['INVITE', 'PART', 'QUIT', 'KICK', 'JOIN', 'NICK']:
            action = data[1].split()[1]
            user = data[1].split()[0].split('!')[0]
            if action == 'INVITE':
                self.commandHandler.joinRoom(data[2])
            elif action == 'PART':
                self.server.channels[data[1].split()[2]].removeUser(user)
            elif action == 'QUIT':
                self.server.userQuit(user)
            elif action == 'JOIN':
                self.server.channels[data[2]].addUser(user)
            elif action == 'KICK':
                self.server.channels[data[1].split()[2]].removeUser(user)
            elif action == 'NICK':
                self.server.nickChange(user, data[2])
    
    def disconnect(self):
        """Invoke the disconnect command on the Command object."""
        self.commandHandler.disconnect()
    
    @property
    def sock(self):
        """Getter for the _sock attribute."""
        return self._sock

    @sock.setter
    def sock(self, value):
        """Setter for the _sock attribute."""
        self._sock = value
        if value is not None:
            self.commandHandler = src.irc.commandHandler.CommandHandler(
                self.server
            )
            self.commandHandler.sock = value
            self.commandHandler.ident()
