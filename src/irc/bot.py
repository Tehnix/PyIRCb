#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC bot...

"""

import socket
import ssl
import time

import src.utilities as util
import src.irc.server
import src.irc.channel
import src.irc.parser


class Bot(object):
    
    def __init__(self, settingsInstance, info):
        """Prepare the object."""
        super(Bot, self).__init__()
        self.parserInstance = src.irc.parser.Parser(settingsInstance, self)
        self.settingsInstance = settingsInstance
        self.info = info
        self.sock = None
        self.server = None
        self.channels = {}
        self.operator = '$'
        self.handleInfo()
    
    def handleInfo(self):
        """
        Pass the information from self.info and the settings into the
        appropriate instance variables.
        
        """
        self.server = src.irc.server.Server(self.info)
        try:
            for name in self.info['channels']:
                self.channels[name] = src.irc.channel.Channel(name)
        except KeyError:
            pass
        try:
            self.operator = self.info['operator']
        except KeyError:
            try:
                self.operator = self.settingsInstance.settings['operator']
            except KeyError:
                pass
        
    def connectToServer(self):
        """Connect to the address and pass the socket to the listener."""
        if self.server.connect:
            util.write("Initializing connection to %s" % (self.server.address,))
        while self.server.connect:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.server.ssl:
                self.sock = ssl.wrap_socket(self.sock)
            # Allow reuse of the socket
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Set timeout limit, so we can detect if we are disconnected
            self.sock.settimeout(300)
            try:
                self.sock.connect((self.server.address, self.server.port))
            except socket.gaierror:
                util.write(
                    "Either wrong hostname or no connection. Trying again.",
                    outputType="Warning"
                )
                time.sleep(60)
                continue
            except ssl.SSLError:
                util.write(
                    "Problem has occured with SSL connecting to %s:%s !\
(check you're using the right port)" %
                    (self.server.address, self.server.port,),
                    outputType="Warning"
                )
                break
            else:
                # We have succesfully connected, so we can start parsing
                self.parserInstance.commandInstance.ident()
                self.parserInstance.parse()
                
    def destroy(self):
        """
        Prepare the object for destruction by sending a disconnect to the 
        server and closing the socket.
        
        """
        self.parserInstance.disconnect()
        self.sock.close()
        self.sock = None
    
    @property
    def sock(self):
        """Getter for the _sock attribute."""
        return self._sock

    @sock.setter
    def sock(self, value):
        """Getter for the _sock attribute."""
        self._sock = value
        self.parserInstance.sock = self.sock

