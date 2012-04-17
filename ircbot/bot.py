#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC Bot module. Initializes connection, joins channels and
takes care of commands given to it.
It works together with the command class from commands_list.py.

"""

import threading
import socket
import ssl
import time
import sys
import inspect

from commands_list import Commands


class BreakOutOfLoop(Exception):
    """Exception used to break out of loop"""
    pass


class IrcBot(threading.Thread):
    """
    Takes care of connection to the server and
    parses the IRC output, taking appropriate action
    accordingly to the commands recieved.
    
    Uses object threading.Thread allowing multiple instances of
    the IRC bot.
    
    """
    
    def __init__(self, host=None, port=None, info=None, use_ssl=False):
        """Sets the initial variables"""
        threading.Thread.__init__(self)
        if host is None:
            raise NameError('Host not specified!')
        if port is None:
            port = 6667
        if info is not None:
            try:
                self.operator = info['operator']
            except KeyError:
                self.operator = "$"
            try:
                self.channels = info['channels']
            except KeyError:
                self.channels = []
            try:
                self.nickname = info['nickname']
            except KeyError:
                self.nickname = "T3hb0t"
            try:
                self.realname = info['realname']
            except KeyError:
                self.realname = "T3hb0t"
        else:
            self.operator = "$"
            self.channels = []
            self.nickname = "T3hb0t"
            self.realname = "T3hb0t"
        self.readdata = None
        self.sock = None
        self.output = None
        self.command_list = None
        self.hostname = host
        self.port = port
        self.use_ssl = use_ssl
    
    def run_bot(self, output=True):
        """Initializes the IRC bot"""
        self.output = output
        self.connect()
    
    def _write(self, text):
        """Handle the output from the IRC bot"""
        if self.output:
            text = str(text) + "\n"
            sys.stdout.write(text)
            sys.stdout.flush()
    
    def _message(self, message, reciever=None, reply_type="NOTICE"):
        """Construct and send a message"""
        if reciever is not None:
            self.sock.send("%s %s :%s!\r\n" % (reply_type, reciever, message,))
    
    def connect(self):
        """Connects to the host:port specified earlier"""
        self._write("Connecting...")
        while True:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # If ssl is True, wrap the socket in ssl
            if self.use_ssl:
                self.sock = ssl.wrap_socket(self.sock)
            # Allow reuse of the socket
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Set timeout limit, so we can detect if we are disconnected
            self.sock.settimeout(300)
            # Try to establish the connection to the socket
            try:
                self.sock.connect((self.hostname, self.port))
            except socket.gaierror:
                self._write(
                    """Either wrong hostname or no connection. \
                    Trying again..."""
                )
                time.sleep(60)
                continue
            except ssl.SSLError:
                self._write(
                    """Problem has occured with SSL connecting to %s:%s !\
                    (check you're using the right port)""" %
                    (self.hostname, self.port,)
                )
                break
            else:
                # If all goes well, we continue to join
                self.join_handler()
                self.listen()
    
    def disconnect(self, reason, *timeout):
        """Disconnects the bot from the server"""
        # If we get disconnected from the server
        if reason == 0:
            self._write("Disconnected from server !")
            self.sock.close()
            raise BreakOutOfLoop()
        elif reason == "socket.timeout" or reason == "socket.error":
            self._write("""Lost Connection (socket.timeout/socket.error). \
                        Reconnecting...""")
            self.sock.close()
            raise BreakOutOfLoop()
        elif reason == "PART" or reason == "QUIT":
            self.sock.send("%s\r\n" % reason)
            self.sock.close()
            if timeout:
                time.sleep(int(timeout[0]))
                self.connect()
    
    def join_handler(self):
        """Join the channels in the IRC"""
        self._write("Join rooms...")
        # Send nickname and identification to the server
        self.sock.send("NICK %s\r\n" % (self.nickname,))
        self.sock.send(
            "USER %s %s +iw :%s\r\n" %
            (self.realname, self.hostname, self.realname,)
        )
        # Join channels (if no CTCP)
        for room in self.channels:
            self._join_room(room)
    
    def _join_room(self, room):
        """Joins the specified channel"""
        self.sock.send("JOIN :%s\r\n" % (room,))
        self._write("Joining room: %s" % (room,))
    
    def listen(self):
        """Listen and handle the input"""
        while True:
            try:
                self.readdata = self.sock.recv(4096)
                self._write(self.readdata)
                self.common_listens(self.readdata)
                self.parse_command(self.readdata)
            except socket.timeout:
                self.disconnect("socket.timeout")
                break
            except socket.error:
                self.disconnect("socket.error")
                break
            except (KeyboardInterrupt, SystemExit):
                self.disconnect("socket.timeout")
                break
            except UnicodeDecodeError:
                continue
            except BreakOutOfLoop:
                self.disconnect(0)
                break
    
    def common_listens(self, data):
        """Handles common listen items"""
        # Disconnected from the server
        if data == 0:
            self.disconnect(data)
        # PING PONG, so we don't get disconnected
        if data[0:4] == "PING":
            self._pong(data)
        # If nickname already in use, restart with a new nickname
        if "%s :Nickname is already in use" % self.nickname in data:
            self._change_nickname()
            raise BreakOutOfLoop()
        # Some servers request CTCP before we can connect to channels
        if "\x01VERSION\x01" in data:
            self._ctcp()
        if data.find("451 JOIN :You have not registered") != -1:
            self.sock.close()
            self.connect()
            raise BreakOutOfLoop()
        if " 332 %s " % self.nickname in self.readdata:
            pass
        if "JOIN :" in self.readdata:
            chan = self._get_channel(self.readdata)
            nick = get_nickname(self.readdata)
            if nick == self.nickname and chan in self.channels:
                self._write("You succesfully joined channel: %s" % (chan,))
        if "INVITE %s" % (self.nickname,) in self.readdata:
            room = self.readdata.split()[3][1:]
            self.channels.append(room)
            self._join_room(room)
    
    def _pong(self, data):
        """Handle PINGs by sending back a PONG"""
        self._write("PONG %s\r\n" % data.split()[1])
        self.sock.send("PONG %s\r\n" % data.split()[1])
    
    def _ctcp(self):
        """Handle CTCP request"""
        self._write("CTCP request, sleeping and (re)joining channels !")
        time.sleep(2)
        for channel in self.channels:
            self.sock.send("JOIN :%s\r\n" % channel)
    
    def _change_nickname(self, new_nick=None):
        """Change the nickname"""
        self._write("""Nickname already in use. Changing nick and \
                    reconnecting...""")
        if new_nick is None:
            self.nickname = self.nickname + str(time.time())[5:-3]
        else:
            self.nickname = new_nick
        self.sock.close()
        self.connect()
    
    def _get_channel(self, data):
        """Search through the IRC output for the channel name"""
        for channel in self.channels:
            if channel == data.split()[2][1:]:
                return data.split()[2][1:]
        return False
    
    def parse_command(self, data):
        """Search the IRC output looking for a command to execute"""
        if len(data.split()) < 3:
            return
        nick = get_nickname(data)
        try:
            command = data.split()[3].lower()
        except IndexError:
            command = False
        for cmd in command_list():
            # Check if the command is in the Command class
            if command == (":%s%s" % (self.operator, cmd)).lower():
                # If it has arguments
                if len(data.split()) > 4:
                    self.execute_command(
                        "%s" % cmd,
                        nick, data.split()[4:len(data.split())]
                    )
                else:
                    self.execute_command(cmd, nick)
    
    def execute_command(self, cmd, initiator, cmd_args=None):
        """Execute the command if it exists (and args are correct)"""
        if cmd_args is None:
            cmd_args = []
        self._write("Running Command: %s" % (cmd,))
        try:
            commands = Commands(self.sock, self.readdata)
            thread = threading.Thread(
                target=getattr(commands, cmd),
                args=cmd_args
            )
            thread.start()
        except Exception as catched:
            self._write("Exception when running command: %s" % (catched,))
            self._message(
                "Exception when running command: %s" % (catched,),
                initiator
            )


def get_nickname(data):
    """Search through the IRC output for the nickname"""
    return data.split("!")[0][1:]

def command_list():
    """Construct a list of all the commands"""
    cmd_list = []
    # These are common to the class, but we do not need them
    cmd_list_ignores = ["daemon", "getName",
                      "ident", "is_alive",
                      "isAlive", "isDaemon",
                      "join", "name",
                      "run", "setDaemon",
                      "setName", "start"]
    for i in range(len(inspect.getmembers(Commands))):
        if (inspect.getmembers(Commands)[i][0].startswith("_") or
            inspect.getmembers(Commands)[i][0] in cmd_list_ignores):
            pass
        else:
            cmd_list.append(inspect.getmembers(Commands)[i][0])
    # Sort the command list alphabetically
    cmd_list.sort(key=lambda x: x.lower())
    return cmd_list

def get_docstring(cmd=None, quantity='one'):
    """
    Fetches the docstring of the given method
        
    Arg [quantity] specifies how many to fetch:
        one - fetches the given cmd
        all - fetches all cmds in Commands class
        
    """
    docstring = {}
    if quantity == 'one' and cmd is not None:
        command_doc = inspect.getdoc(getattr(Commands, cmd))
        docstring[cmd] = inspect.cleandoc(command_doc)
    elif quantity == 'all':
        for cmd in command_list():
            command_doc = inspect.getdoc(getattr(Commands, cmd))
            docstring[cmd] = inspect.cleandoc(command_doc)
    else:
        docstring = ''
    return docstring
