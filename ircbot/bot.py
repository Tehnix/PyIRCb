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
import imp

import commands.active
import commands.passive


class BreakOutOfLoop(Exception):
    """Exception used to break out of loop"""
    pass


class IRCConnectionDropped(Exception):
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
        self.info = self._handle_info(info)
        self.sock = None
        self.output = False
        self.log = False
        self.hostname = host
        self.port = port
        self.use_ssl = use_ssl
        self.commands = commands.active.ActiveCommands()
        self.topic = None
        self.local_command_list = [
            'reload'
        ]

    def run_bot(self, output=True, log=False):
        """Initializes the IRC bot"""
        self.output = output
        self.log = log
        self.connect()

    def _handle_info(self, info=None):
        """
        Makes sure that all needed keys are in the info dictionary
        so we don't end up with IndexError exceptions all over the place.

        """
        if info is None:
            info = {}
        # Structure is: name: desired type
        expected_keys = {
            'channels': [],
            'nickname': '',
            'realname': '',
            'operator': '',
            'identify': ''
        }
        for name, key_type in expected_keys.items():
            if name not in info:
                info[name] = expected_keys[name]
        return info

    def _write(self, text):
        """Handle the output from the IRC bot"""
        if self.output:
            text = to_unicode(text)
            text = "[*] %s\n" % (text,)
            sys.stdout.write(text)
            sys.stdout.flush()

    def _message(self, message, reciever=None, reply_type="NOTICE"):
        """Construct and send a message"""
        if reciever is not None:
            text = "%s %s :[*] %s\r\n" % (reply_type, reciever, message,)
            self.sock.send(to_bytes(text))

    def _raw_message(self, text):
        """Construct an IRC message and send it"""
        text = "%s\r\n" % (text,)
        self.sock.send(to_bytes(text))

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
            except IRCConnectionDropped:
                continue
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
            raise IRCConnectionDropped()
        elif reason == "socket.timeout" or reason == "socket.error":
            self._write("""Lost Connection (socket.timeout/socket.error). \
                        Reconnecting...""")
            self.sock.close()
            raise IRCConnectionDropped()
        elif reason == "PART" or reason == "QUIT":
            self._raw_message(reason)
            self.sock.close()
            if timeout:
                time.sleep(int(timeout[0]))
                self.connect()

    def join_handler(self):
        """Join the channels in the IRC"""
        self._write("Join rooms...")
        # Send nickname and identification to the server
        self._raw_message("NICK %s" % (self.info['nickname'],))
        self._raw_message(
            "USER %s %s +iw :%s" %
            (self.info['realname'], self.hostname, self.info['realname'],)
        )
        # Join channels (if no CTCP)
        for room in self.info['channels']:
            self._join_room(room)

    def _join_room(self, room):
        """Joins the specified channel"""
        room = to_unicode(room)
        self._raw_message("JOIN :%s" % (room,))
        self._write("Joining room: %s" % (room,))

    def identify(self, password):
        """The bot identifies to the server"""
        text = "PRIVMSG nickserv :IDENTIFY %s" % (password,)
        self._raw_message(text)

    def register(self, password):
        """The bot identifies to the server"""
        text = "PRIVMSG nickserv :REGISTER %s blah@lortemail.dk" % (password,)
        self._raw_message(text)

    def listen(self):
        """Listen and handle the input"""
        if self.info['identify']:
                    self.identify(self.info['identify'])
        while True:
            try:
                readdata = self.sock.recv(4096)
                # Logging and output
                if self.log:
                    log_output(readdata)
                self._write(readdata)

                self.common_listens(readdata)
                self.parse_command(readdata)
                # Stop the program from eating all the CPU
                time.sleep(0.01)
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
        data = to_unicode(data)
        split_data = data.split(":")
        try:
            split_data_first = split_data[0]
        except IndexError:
            split_data_first = ""
        try:
            split_data_second = split_data[1]
        except IndexError:
            split_data_second = ""
        try:
            split_data_third = split_data[2]
        except IndexError:
            split_data_third = ""
        # Disconnected from the server
        if data == 0:
            self.disconnect(data)
        # PING PONG, so we don't get disconnected
        try:
            if "PING" in data[0:4]:
                self._pong(data)
            elif "PING" in data[0:8]:
                self._pong(data)
        except IndexError:
            pass
        if ("NickServ!NickServ@services. NOTICE %s" % (self.info['nickname'],) in data and
            "\x02Innocence\x02 is not a registered nickname.\r\n" in data):
            print('shiiiiaatttt')
            self.register(self.info['identify'])
            self.identify(self.info['identify'])
        # If nickname already in use, restart with a new nickname
        if ("* %s" % (self.info['nickname'],) in split_data_second and
            "Nickname is already in use" in split_data_third):
            self._change_nickname()
            raise BreakOutOfLoop()
        # Some servers request CTCP before we can connect to channels
        # We are then forced to retry the join
        if ("\x01VERSION\x01" in split_data_first or
            "\x01VERSION\x01" in split_data_second):
            self._ctcp()
        # Not registered message
        if "451 JOIN" in split_data_second:
            time.sleep(1)
            for room in self.info['channels']:
                self._join_room(room)
        # Get the topic of the channel
        if " 332 %s " % (self.info['nickname'],) in split_data_second:
            self.topic = get_topic(data)
        # User list of the channel upon join
        if " 353 %s" % (self.info['nickname'],) in split_data_second:
            chan = split_data_second.split("=")[1].replace(' ', '')
            nicknames = split_data_third.split()
            for nick in nicknames:
                if nick != self.info['nickname']:
                    self.commands._user_join(nick, chan)
        # A person joins the channel
        if "JOIN :" in split_data_second:
            nick = get_nickname(data)
            chan = get_channel(data, self.info['channels'])
            self.commands._user_join(nick, chan)
            if nick == self.info['nickname'] and chan in self.info['channels']:
                self._write("You succesfully joined channel: %s" % (chan,))
        # A person leaves the channel
        if "PART :" in split_data_second or "QUIT :" in split_data_second:
            nick = get_nickname(data)
            chan = get_channel(data, self.info['channels'])
            self.commands._user_left(nick, chan)
        # Automatically join a channel on invite
        if "INVITE %s" % (self.info['nickname'],) in split_data_second:
            try:
                room = data.split()[3][1:]
                self.info['channels'].append(room)
                self._join_room(room)
            except IndexError:
                pass
        # Disconnect and reconnect if we ping timeout for some reason
        if "Closing link" in split_data_second and "ERROR" in split_data_first:
            self.disconnect("QUIT", 5)

    def _pong(self, data):
        """Handle PINGs by sending back a PONG"""
        self._write("PONG %s\r\n" % data.split()[1])
        self._raw_message("PONG %s" % data.split()[1])

    def _ctcp(self):
        """Handle CTCP request"""
        self._write("CTCP request, sleeping and (re)joining channels !")
        time.sleep(2)
        for channel in self.info['channels']:
            self._raw_message("JOIN :%s" % (channel,))

    def _change_nickname(self, new_nick=None):
        """Change the nickname"""
        self._write(
            """Nickname already in use. Changing nick and reconnecting..."""
        )
        if new_nick is None:
            self.info['nickname'] = self.info['nickname'] + str(int(time.time()))[5:-2]
        else:
            self.info['nickname'] = new_nick
        self.sock.close()
        self.connect()

    def parse_command(self, data):
        """Search the IRC output looking for a command to execute"""
        data = to_unicode(data)
        if len(data.split()) < 3:
            return
        nick = get_nickname(data)
        try:
            command = data.split()[3].lower()
        except IndexError:
            command = False
        for cmd in command_list():
            # Check if the command is in the Command class
            if command == (":%s%s" % (self.info['operator'], cmd)).lower():
                # If it has arguments
                if len(data.split()) > 4:
                    self.execute_command(
                        cmd,
                        nick,
                        data,
                        cmd_args=data.split()[4:len(data.split())]
                    )
                else:
                    self.execute_command(cmd, nick, data)
        for cmd in self.local_command_list:
            if command == (":%s%s" % (self.info['operator'], cmd)).lower():
                self._write("Running local command: %s" % (cmd,))
                if command == ":%sreload" % (self.info['operator'],):
                    global commands
                    # Reload the Commands module
                    self._write("Reloading Commands module")
                    self._message("Reloading Commands module", nick)
                    # Get users so we can transfer them to the new instance
                    users = self.commands._users('get')
                    imp.reload(commands.active)
                    imp.reload(commands.passive)
                    import commands.active
                    import commands.passive
                    self.commands = commands.active.ActiveCommands()
                    self.commands._users('set', users)

    def execute_command(self, cmd, initiator, data, cmd_args=None):
        """Execute the command if it exists (and args are correct)"""
        if cmd_args is None:
            cmd_args = []
        self._write("Running Command: %s" % (cmd,))
        try:
            self.commands._data(self.sock, data, self.hostname, self.info['channels'])
            thread = threading.Thread(
                target=getattr(self.commands, cmd),
                args=cmd_args
            )
            thread.start()
        except Exception as catched:
            self._write("Exception when running command: %s" % (catched,))
            self._message(
                "Exception when running command: %s" % (catched,),
                initiator
            )


def to_bytes(text):
    """Convert string to bytes"""
    try:
        if type(text) != bytes:
            text = bytes(text, 'UTF-8')
    except TypeError:
        text = "\n[WARNING] : Failed to encode unicode!\n"
    return text


def to_unicode(text):
    """Converts bytes to unicode"""
    if type(text) != str:
        try:
            text = str(text, encoding='UTF-8')
        except UnicodeDecodeError:
            text = "\n[WARNING] : Failed to decode bytes!\n"
        except TypeError:
            text = "\n[WARNING] : Failed to decode bytes!\n"
    return text


def get_nickname(data):
    """Search through the IRC output for the nickname"""
    try:
        return data.split("!")[0][1:]
    except IndexError:
        return False


def get_channel(data, channels):
    """Search through the IRC output for the channel name"""
    chan = ""
    try:
        for channel in channels:
            if channel == data.split()[2].lower():
                chan = data.split()[2].lower()
        if chan is False:
            for channel in channels:
                if channel == data.split()[2].lower():
                    chan = data.split()[3][1:].lower()
    except IndexError:
        pass
    return chan.replace(' ', '')


def get_topic(self, data):
    """Extract the topic from the data"""
    try:
        return ":".join(data.split(":")[2:])
    except IndexError:
        return False


def command_list():
    """Construct a list of all the commands"""
    cmd_list = []
    # These are common to the class, but we do not need them
    cmd_list_ignores = [
        "daemon", "getName",
        "ident", "is_alive",
        "isAlive", "isDaemon",
        "join", "name",
        "run", "setDaemon",
        "setName", "start"
    ]
    Commands = commands.active.ActiveCommands
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
    Commands = commands.active.ActiveCommands
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


def log_output(text, file_name="bot_log.txt"):
    """Write text to file"""
    text = to_unicode(text)
    text = "[*] %s\n" % (text,)
    log = open(file_name, "a")
    log.write(text)
    log.close()
