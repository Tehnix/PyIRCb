#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC messages...

"""

import sys
import time
import socket

import src.utilities as util
import src.irc.command


class BreakOutOfLoop(Exception):
    pass


class Parser(object):
    """Parse IRC output and react to commands."""
    
    def __init__(self, settingsInstance, botInstance):
        """Prepare the object."""
        super(Parser, self).__init__()
        self.settingsInstance = settingsInstance
        self.botInstance = botInstance
        self.commandInstance = src.irc.command.Command(
            settingsInstance,
            botInstance
        )
        self.sock = None
        self.readBuffer = None
        self.todo = []
        self.node = None
    
    def parse(self):
        while True:
            try:
                readbuffer = util.toUnicode(self.sock.recv(4096)).split('\r\n')
                for data in readbuffer:
                    print(data)
                    self._parse(data)
                time.sleep(0.1)
            except socket.timeout:
                break
            except socket.error:
                break
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)
            except UnicodeDecodeError:
                continue
            except BreakOutOfLoop:
                self.botInstance.server.connect = False
                break
    
    def _parse(self, data):
        nick = self.settingsInstance.settings['nickname']
        if self.node is None:
            self.node = data.split()[0][1:]
        # Server messages start with :node (eg :verne.freenode.net), so we
        # check for this and can then be confident it's from the server
        if data.startswith("PING :"):
            self.commandInstance.pong(data)
        if data.startswith(":%s" % self.node):
            if "376 %s :End of /MOTD command." % (self.settingsInstance.settings['nickname'],):
                self.commandInstance.joinRooms(self.botInstance.channels)
            if "* :*** No Ident response" in data:
                self.commandInstance.ident()
                self.commandInstance.joinRooms(self.botInstance.channels)
        if data.startswith("ERROR :Closing Link:"):
            raise BreakOutOfLoop
    
    def disconnect(self):
        self.commandInstance.disconnect()
    
    @property
    def sock(self):
        """Getter for the _sock attribute."""
        return self._sock

    @sock.setter
    def sock(self, value):
        """Getter for the _sock attribute."""
        self._sock = value
        self.commandInstance.sock = value
