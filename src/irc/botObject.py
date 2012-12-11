#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC bot...

"""

import socket
import ssl
import time

import src.utilities as util
import src.irc.serverObject
import src.irc.channelObject
import src.irc.dataParser


class BotObject(object):
    
    def __init__(self, globalInfo, info):
        """Prepare the object."""
        super(BotObject, self).__init__()
        self.dataParser = None # set when the socket is not None
        self.sock = None
        self.server = src.irc.serverObject.ServerObject(globalInfo, info)
    
    def connectToServer(self):
        """Connect to the address and pass the socket to the listener."""
        if self.server.connect:
            util.write("Initializing connection to %s" % (self.server.address,))
        while self.server.connect:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.server.ssl:
                sock = ssl.wrap_socket(sock)
            # Allow reuse of the socket
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Set timeout limit, so we can detect if we are disconnected
            sock.settimeout(300)
            try:
                sock.connect((self.server.address, self.server.port))
                self.sock = sock
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
                self.dataParser.parse()
                
    def destroy(self):
        """
        Prepare the object for destruction by sending a disconnect to the 
        server and closing the socket.
        
        """
        if self.dataParser is not None:
            self.dataParser.disconnect()
        self.sock.close()
        self.sock = None

    @property
    def sock(self):
        """Getter for the _sock attribute."""
        return self._sock

    @sock.setter
    def sock(self, value):
        """
        Setter for the _sock attribute. If the socket is not set to 
        none, then also create the parser instance and set its socket.
        
        """
        self._sock = value
        if value is not None:
            self.dataParser = src.irc.dataParser.DataParser(self.server)
            self.dataParser.sock = self.sock
