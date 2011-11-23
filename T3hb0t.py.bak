#!/usr/bin/env python
# -*- coding: utf-8 -*-

# General modules
from __future__ import division
from optparse import *
import threading
import socket
import socks # <-- socket module that supports proxy
import ssl
import time
import random
from hashlib import sha224
from inspect import *
from string import lower,upper
# BotUpdate, BotCommands
import os
# BotCommands
import sys
import platform
# BotUpdate
import urllib
import urllib2
import sqlite3
import signal
import zipfile

parser_desc = """
,----------------------------------------------------------------------------,
| .            .                    .      .           .        .            |
|     ///////////////////// .////////////////   .  //////               .    |
|    /////////////////////  //////////////////    //////      .     .        |  
|    .     //////   .        .         //////    //////                      |   
| .       //////        .      //////////////   //////////////////       .   |
|        //////   .          ///////////////   //////////////////            |
|       //////                    .  //////   //////      //////    .        |
|   .  //////            //////////////////  //////   .  //////             .|
|     //////    .       /////////////////   //////      //////   b0t         |
| .         .       .   Puppynix & Optical & Speakeasy     .     .     .     |
|----------------------------------------------------------------------------|
|                    T3hb0t - A Python based IRC bot                         |
|----------------------------------------------------------------------------|  
|Author: Puppynix,  (Optical and speakeasy)                                  |
|Info: T3hb0t is an IRC bot client capable of connecting to multiple servers |
|and channels. Easily customized and easy to add commands.                   | 
|                                                                            |
|Default operator prefix is ! . Can be set with -o option. If using -i <pass>|
|to identify, the nick must be registered beforehand (some servers require   |
|email activation !).                                                        |
|______-________-________-________-________-________-________-________-______|"""

parser_usg = """%prog [options]"""

parser = OptionParser(description = parser_desc, usage = parser_usg)
parser.add_option("-r", "--run", dest="run", default=False, action="store_true",
                  help="Start the bot with the saved settings (use -s to set settings)")
parser.add_option("-i", "--ident", dest="identify", action="store", nargs=1,
                  help="If set, the bot will try to identify with pass (must be run with -r). Usage: -i <pass>")
parser.add_option("-g", "--get", dest="get", default=False, action="store_true",
                  help="Print the variables set", metavar="get_variables")
parser.add_option("-c", "--clear", dest="clear", default=False, action="store_true",
                  help="Clear all variables", metavar="clear_variables")
parser.add_option("-l", "--ssl", dest="ssl", default=False, action="store_true",
                  help="Use SSL to connect", metavar="use_SSL")
parser.add_option("-j", "--just", dest="just", action="store", nargs=1,
                  help="Connect just to server with id. Usage: -j <id>")
parser.add_option("-o", "--operator", dest="cmd_op", action="store", nargs=1,
                  help="Sets operator sign to be used as prefix to commands. Usage: -o <operator>")                  
parser.add_option("-d", "--del", dest="del_id", action="store", nargs=1,
                  help="Deletes setting with id. Usage: -d <id>")
parser.add_option("-a", "--admin", dest="add_admin", action="store", nargs=2,
                  help="Adds admin to database. Usage: -a <username> <password>")
parser.add_option("-p", "--proxy", dest="proxy", action="store", nargs=3,
                  help="Set a proxy to use (types. SOCKS4 = 1, SOCKS5 = 2, HTTP = 3). Usage: -p <Proxy type> <server> <port>")             
parser.add_option("-u", "--use", dest="use", action="store", nargs=4,
                  help="Starts bot with specified settings. Usage: -u <nick> <host> <port> <channels>")
parser.add_option("-s", "--set", dest="set", action="store", nargs=5,
                  help="Saves a setting. Usage: -s <id> <nick> <host> <port> <channels>")

(options, args) = parser.parse_args()

# Bot version number
bot_version = "1.0.0"
# Bot deployment details
bot_deployment = ".py"
# For debugging
profiling = True
# The database file
sqldatabase = "BotDatabase.db"

class BotOptparse(threading.Thread):
    """Here we parse the command line options that are given to the bot !"""
    
    def __init__(self):
        if options.add_admin:
            self.admin()
        if options.set:
            self.set()
        if options.get:
            self.get()
        if options.clear:
            self.clear()
        if options.run or options.just or options.use:
            if options.just:
                self.just()
            elif options.run:
                self.run()
            # So we can do -r and -u at the same time !
            if options.use:
                self.use()
            # Keeps the program running
            while True:
                # This keeps the program from being listed as using 100% CPU
                time.sleep(0.5)
                pass
    
    def admin(self):
        print "\n\nAdding admin %s" % options.add_admin[0]
        botadmins.add_admin(options.add_admin[0], options.add_admin[1])
    
    def run(self):
        sqlcon = sqlite3.connect("BotDatabase.db")
        sqlcursor = sqlcon.cursor()
        sqlcursor.execute('SELECT * FROM settings')
        for row in sqlcursor:
            if profiling: print "\n\nStarting thread with id: %s" % row[0]
            ircbot = IrcBot(row[2], int(row[3]), row[1], row[1], row[1], row[4].split())
            thread = threading.Thread(target=ircbot.connect)
            thread.start()
    
    def use(self):
        # Check for valid port
        if options.use[2] != "6667" and options.use[2] != "6697":
            print "\n\nNote that the port is %s and not 6667 or 6697 !\n\n" % options.use[2]
        if profiling: print "\n\nStarting script with -u !"
        ircbot = IrcBot(options.use[1], int(options.use[2]), options.use[0], options.use[0], options.use[0], options.use[3].split())
        thread = threading.Thread(target=ircbot.connect)
        thread.start()
    
    def just(self):
        sqlcon = sqlite3.connect("BotDatabase.db")
        sqlcursor = sqlcon.cursor()
        search_query = [options.just]
        sqlcursor.execute('SELECT * FROM settings WHERE id=?', search_query)
        for row in sqlcursor:
            if profiling: print "\n\nStarting thread with id: %s" % row[0]
            ircbot = IrcBot(row[2], int(row[3]), row[1], row[1], row[1], row[4].split())
            thread = threading.Thread(target=ircbot.connect)
            thread.start()
    
    def delete(self):
        BotDatabase().del_id(options.del_id[0])
    
    def get(self):
        BotDatabase().get_db()
    
    def set(self):
        if options.set[3] != "6667" and options.set[3] != "6697":
            print "\n\nNote that the port is %s and not 6667 or 6697 !\n\n" % options.set[3]
        BotDatabase().set_db(options.set[0], options.set[1], options.set[2], options.set[3], options.set[4])
    
    def clear(self):
        BotDatabase().clear_db()
    




class BotAdmins(threading.Thread):
    """Creates and manages the admins, plus the loggedin dictionary."""
    
    def __init__(self):
        self.sqldatabase = sqldatabase
        # Predefined admins
        self.admins = {"Puppynix":"90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809",
                       "Optical":"90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809",
                       "OpticalForce":"90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809",
                       "Speakeasy":"90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809"}
        self.master_admins = {}
        for admin in self.admins:
            self.master_admins[admin] = self.admins[admin]
    
    def build_admins(self):
        self.sqlcon = sqlite3.connect(self.sqldatabase)
        self.sqlcursor = self.sqlcon.cursor()
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM settings)')
        self.sqlcursor.execute('SELECT * FROM settings')
        for row in self.sqlcursor:
            self.admins[row[1]] = row[2]
        self.sqlcursor.close()
        self.sqlcon.close()
        # Build the loggedin dict
        self.build_loggedin()
    
    def build_loggedin(self):
        self.loggedin = {}
        for admin in self.admins:
            self.loggedin[admin] = 0
    
    def check_loggedin(self, username):
        """Check if user is logged in or not."""
        try:
            if self.loggedin[username] == 1:
                return True
        except KeyError:
            return False
    
    def login(self, sock, recipient, reply_type, username,*text):
        self.readdata = text[0]
        """If the user want's to login or to check if already loggedin."""
        # See if the nickname is in the admins dict
        if username in self.admins:
            if len(self.readdata.split()) > 4:
                for admin in self.admins:
                    # Check if password matches the admin
                    if admin == username:
                        if sha224(self.readdata.split()[4]).hexdigest() == self.admins[admin]:
                            # Set login value in loggedin dict
                            self.loggedin[admin] = 1
                            sock.send("%s %s :You are now logged in !\r\n" % (reply_type, recipient))
                        else:
                            sock.send("%s %s :Login failed !\r\n" % (reply_type, recipient))
    
    def logout(self, username):
        """Logs out the user."""
        # If nickname was an admin, makes sure log out is done
        try:
            self.loggedin[username] = 0
        except KeyError:
            pass
    
    def add_admin(self, username, password):
        self.sqlcon = sqlite3.connect(self.sqldatabase)
        self.sqlcursor = self.sqlcon.cursor()
        password = sha224(password).hexdigest()
        search_query = [username]
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM admins WHERE username=?)', search_query)
        if self.sqlcursor.fetchone()[0] == 0:
            insertquery = [username, password]
            self.sqlcursor.execute('INSERT INTO admins VALUES (null,?,?)', insertquery)
            self.sqlcon.commit()
            print "\nAdmin has been added\n\n"
        else:
            updatequery = [username, password, username]
            self.sqlcursor.execute('UPDATE admins SET username=?, password=? WHERE username=?', updatequery)
            self.sqlcon.commit()
            print "\nAdmin %s has been updated !\n\n" % username
    




class IrcBot(threading.Thread):
    """Main class to execute the connection, join and listen part of the bot.
    Will automatically connect, and then start to listen.
    """
    
    def __init__(self, host, port, nick, ident, realname, chan):
        """Defines initial values and ties them to the class"""
        # Set the command operator prefix
        if options.cmd_op:
            print "Operator prefix set to: %s" % options.cmd_op
            self.cmd_operator = options.cmd_op
        else:
            self.cmd_operator = "!"
        # Set the connection and identification values
        self.hostname = host
        self.port = port
        self.realname = realname
        self.nickname = nick
        self.idents = ident
        self.channels = chan
        # Help message
        self.help_list = [self.cmd_operator+"Login <password> :: Logs in the nickname.",
                          self.cmd_operator+"Logout :: Logs out the nickname.",
                          self.cmd_operator+"Help :: List of general commands (you're in it)",
                          self.cmd_operator+"Commands :: Get a list of all commands.",
                          self.cmd_operator+"Updatebot <new version> <url> :: Makes the bot check for an updated version.",
                          self.cmd_operator+"All command <args> :: Runs the specified command name where target is all bots.",
                          self.cmd_operator+"Nickname command <args> :: Runs the specified command name where target is the specified nickname."]
        # What we listen for
        self.listen_to_list = ["Login",
                               "Logout",
                               "Commands",
                               "Help",
                               "addbook",
                               "addtut",
                               "addtool",
                               "addrequest",
                               "getbooks",
                               "gettuts",
                               "gettools",
                               "getrequests",
                               "deleteitem",
                               "Updatebot",
                               "All",
                               self.nickname]
        # Commands that doesn't require login to execute
        self.public_commands = ["addbook",
                                "addtut",
                                "addtool",
                                "addrequest",
                                "getbooks",
                                "gettuts",
                                "gettools",
                                "getrequests"]
        # Set if bot will identify
        if options.identify:
            print "The bot will try to identify with password %s !" % options.identify
            self.bot_identify = True
            self.bot_password = options.identify
        else:
            self.bot_identify = False
        # Define the readbuffer
        self.readbuffer = ""
        threading.Thread.__init__(self)
    
    def connect(self):
        """Tries to connect to the server. Retries if fails, otherwise, just moves onto self.join()"""
        if profiling: print "Starting connect !"
        while True:
            # Proxy connection
            if options.proxy:
                self.sock = socks.socksocket()
                print options.proxy
                self.proxy_host = socket.gethostbyaddr(options.proxy[1])[0]
                print "Using %s proxy through %s:%s !" % (options.proxy[0], self.proxy_host, options.proxy[2],)
                if options.proxy[0] == "1":
                    self.proxy_type = socks.PROXY_TYPE_SOCKS4
                elif options.proxy[0] == "2":
                    self.proxy_type = socks.PROXY_TYPE_SOCKS5
                elif options.proxy[0] == "3":
                    self.proxy_type = socks.PROXY_TYPE_HTTP
                self.sock.setproxy(self.proxy_type, self.proxy_host, int(options.proxy[2]))
            # Regular connection
            else:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if options.ssl:
                    if profiling: print "Wrapping socket in SSL !"
                    self.sock = ssl.wrap_socket(self.sock)
                # This allows the socket address to be reused and sets the timeout value
                # so we know if we lost the connection.
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.sock.settimeout(300)
            try:
                self.sock.connect((self.hostname, self.port))
            except socket.gaierror:
                if profiling: print "Either wrong hostname or no connection. Trying again..."
                time.sleep(10)
                continue
            except ssl.SSLError:
                if profiling: print "Problem has occured with SSL connecting to %s:%s ! (check you're using the right port)" % (self.hostname, self.port,)
                break
            else:
                self.join()
    
    def disconnect(self, reason,*time):
        """Disconnects handled here for the various ways we might loose or drop the connection."""
        # If we get disconnected from the server
        if reason == 0:
            if profiling: print "Disconnected from server !"
            self.sock.close()
            self.connect()
        # If the socket times out
        elif reason == "socket.timeout" or reason == "socket.error":
            if profiling: print "Lost Connection (socket.timeout/socket.error). Reconnecting..."
            self.connect()
        elif reason == "PART" or reason == "QUIT":
            self.sock.send("%s\r\n" % reason)
            self.sock.close()
            if time:
                time.sleep(int(time[0]))
                self.connect()
    
    def join(self):
        """Here we set the nickname and userinfo, and joins the channels. Upon succes self.listen() is started."""
        if profiling: print "Starting join !"
        # Send nickname and userinfo to the server
        self.sock.send("NICK %s\r\n" % self.nickname)
        self.sock.send("USER %s %s +iw :%s\r\n" % (self.idents, self.hostname, self.realname))
        if self.bot_identify:
            self.sock.send("PRIVMSG NICKSERV IDENTIFY %s\r\n" % self.bot_password)
        # Join channels (if no CTCP)
        for channel in self.channels:
            self.sock.send("JOIN :%s\r\n" % channel)
        while True:
            try:
                self.readdata = self.sock.recv(4096)
                if profiling: print self.readdata
                self.disconnect(self.readdata)
                # PING PONG, so we don't get disconnected
                if self.readdata[0:4] == "PING":
                    self.sock.send("PONG  %s\r\n" % self.readdata.split()[1])
                # If nickname already in use, restart the process with a new nickname
                if "%s :Nickname is already in use" % self.nickname in self.readdata:
                    if profiling: print "Nickname already in use. Changing nick and reconnecting..."
                    self.nickname = self.nickname + str(time.time())[5:-3]
                    self.sock.close()
                    self.connect()
                    break
                # Some servers request CTCP before we can connect to channels
                if "\x01VERSION\x01" in self.readdata:
                    if profiling: print "CTCP request, waiting and joining channels !"
                    time.sleep(2)
                    for channel in self.channels:
                        self.sock.send("JOIN :%s\r\n" % channel)
                if self.readdata.find("451 JOIN :You have not registered") != -1:
                    time.sleep(4)
                    for channel in self.channels:
                        self.sock.send("JOIN :%s\r\n" % channel)
                if "JOIN :" in self.readdata and self.nickname == self.readdata.split("!")[0][1:]:
                    if self.readdata.split()[2][1:] in self.channels:
                        self.listen()
            except socket.timeout:
                self.disconnect("socket.timeout")
                break
            except UnicodeDecodeError:
                continue
    
    def listen(self):
        """This is were we define what commands or other things we need to look for."""             
        if profiling: print "Starting listen !"
        while True:
            self.readdata = self.sock.recv(4096)
            if profiling: print self.readdata
            self.disconnect(self.readdata)
            self.sender_nickname = self.readdata.split("!")[0][1:]
            try:
                # Look for matches in listen_to_list
                if len(self.readdata.split()) > 3:
                    for listen_item in self.listen_to_list:
                        # If the item matches
                        if lower(self.readdata.split()[3]) == lower(":%s%s" % (self.cmd_operator, listen_item)):
                            # If it has arguments
                            if len(self.readdata.split()) > 4:
                                # If All or Nickname, the command is another place than other cases
                                if listen_item == "All" and  len(self.readdata.split()) > 4 or listen_item == self.nickname and len(self.readdata.split()) > 4:
                                    self.executecommand("%s" % self.readdata.split()[4], self.readdata.split()[5:len(self.readdata.split())])
                                else:
                                    self.executecommand("%s" % listen_item, self.readdata.split()[4:len(self.readdata.split())])
                            # No arguments
                            else:
                                self.executecommand(listen_item)
                # PING PONG, so we don't get disconnected
                if self.readdata[0:4] == "PING":
                    self.sock.send("PONG  %s\r\n" % self.readdata.split()[1])
                # Check if admin QUITs or PARTs
                if " PART " in self.readdata or " QUIT " in self.readdata:
                    if self.readdata.split()[1] == "PART" or self.readdata.split()[1] == "QUIT":
                        botadmins.logout(self.sender_nickname)
                # Look for commands in the topic
                if " 332 %s " % self.nickname in self.readdata:
                    self.readtopic()
            except socket.timeout:
                if profiling: print "Lost Connection (socket timeout). Reconnecting..."
                self.disconnect("socket.timeout")
                break
            except (KeyboardInterrupt, SystemExit):
                self.disconnect("socket.timeout")
                break
            except socket.error:
                self.disconnect("socket.error")
                break
    
    def readtopic(self):
        """Method that is invoked if there is a command in the topic."""
        self.recipient = self.readdata.split()[3]
        self.reply_type = "PRIVMSG"
        if " ::!Hello Thar" in self.readdata:
            self.sock.send("%s %s :Lol, Topic just told me to say hello :)\r\n" % (self.reply_type, self.recipient))
    
    def composemessage(self, msg,*text):
        """Here we put together the message that is to be sent."""
        if profiling: print "Starting composemessage !"
        # Sort message
        self.msg = msg
        self.textdata = " ".join(text)
        self.reply_type = "NOTICE"
        #self.reply_type = self.textdata.split()[1] <-- if both PRIVMSG and NOTICE
        self.sender_nickname = text[0].split("!")[0][1:]
        self.recipient = self.sender_nickname
        self.sendmessage()
    
    def sendmessage(self):
        """Simply sending the message (usually from self.composemessage() )"""
        if profiling: print "Starting sendmessage !"
        self.sock.send("%s %s :%s\r\n" % (self.reply_type, self.recipient, self.msg))
    
    def executecommand(self, command,*args):
        """Here we execute the various commands that is looked for in self.listen(). It automagically registers new commands in BotCommands class."""
        if profiling: print "Starting executecommand !"
        # Create list of commands sorted alphabetically
        command_list = []
        command_list_ignores = ["daemon", "getName", "ident", "is_alive", "isAlive", "isDaemon",
                                "join", "name", "run", "setDaemon", "setName", "start"]
        for i in range(len(getmembers(BotCommands))):
            if getmembers(BotCommands)[i][0].startswith("_") or getmembers(BotCommands)[i][0] in command_list_ignores:
                pass
            else:
                command_list.append(getmembers(BotCommands)[i][0])
        command_list.sort(key=lambda x: x.lower())
        if command == "Commands":
            for cmd in command_list:
                print command_list
                text = "%s : %s" % (str(cmd), cleandoc(getdoc(getattr(BotCommands, cmd))))
                self.composemessage(text, self.readdata)
                # So we don't flood
                if len(command_list) < 15:
                    time.sleep(0.5)
                else:
                    time.sleep(1)
        elif command == "Help":
            for item in self.help_list:
                self.composemessage(item, self.readdata)
                time.sleep(0.5)   
        elif command == "Login":
            botadmins.login(self.sock, self.sender_nickname, "NOTICE", self.sender_nickname, self.readdata)
        elif command == "Logout":
            botadmins.logout(self.sender_nickname) 
        else:
            # Because all methods in BotCommands are lowercase
            command = lower(command)
            if botadmins.check_loggedin(self.sender_nickname) or command in self.public_commands:
                if command in command_list:
                    # Initial arguments to be supplied
                    command_args = [self.sock, self.sender_nickname, "NOTICE"]
                    # Split the arguments into a tuple
                    if args:
                        for i in range(len(args[0])):
                            command_args.append(args[0][i])
                    command_args = tuple(command_args)
                    # Make the string act as a function
                    exec_command = getattr(BotCommands, command)
                    # Check if enough arguments is given
                    exec_command_length = len(getargspec(exec_command)[0])
                    if len(command_args) < (exec_command_length - 1):
                        self.composemessage("Too few arguments (%s needed, %s given). Please use !Commands for help." % ((exec_command_length - 4), (len(command_args) - 3)), self.readdata)
                    elif getargspec(exec_command)[1] is None and len(command_args) > (exec_command_length - 1):
                        self.composemessage("Too many arguments (%s needed, %s given). Please use !Commands for help." % ((exec_command_length - 4), (len(command_args) - 3)), self.readdata)
                    else:
                        # Notify that we've started the thread
                        self.composemessage("Running Command: %s" % command, self.readdata)
                        # Start the command in a thread
                        botcmd = BotCommands()
                        thread = threading.Thread(target=getattr(botcmd, command), args=command_args)
                        thread.start()
                else:
                    self.composemessage("No such command is found !", self.readdata)
            else:
                self.composemessage("Not logged in !", self.readdata)
    




class BotCommands(threading.Thread):
    """This is were the commands for the bot resides,
    everything will be handled by threads.
    """
    
    def __init__(self):
        """Sets initial variables based on environment"""
        platform.mac_ver() # Fix on Mac OS X, else causes "Trace/BPT trap" error
        # Set platform
        self.platforms = sys.platform
        self.is_windows = self.is_mac = self.is_linux = False
        # Set variables that depends on OS
        if self.platforms.startswith("win32"):
            self.operatingsystem = "Windows"
            self.os_version = sys.getwindowsversion()[4]
            self.username = os.getenv('USERNAME')
            self.is_windows = True
        elif self.platforms.startswith("darwin"):
            self.operatingsystem = "Mac OS X"
            self.os_version = platform.mac_ver()[0]
            self.username = os.getenv('USER')
            self.is_mac = True
        elif self.platforms.startswith("linux"):
            self.operatingsystem = dist()[0]
            self.os_version = platform.linux_distribution()[1]
            self.username = os.getenv('USER')
            self.is_linux = True
        # Set machine
        self.mach = platform.machine()
    
    def repeat(self, sock, recipient, reply_type,*text):
        """Usage: repeat <text>"""
        if text:
            send_text = ""
            for i in range(len(text)):
                    send_text += text[i]+" "
        else:
            send_text = "Sup?"
        sock.send("%s %s :%s\r\n" % (reply_type, recipient, send_text))
    
    def add_admin(self, sock, recipient, reply_type, username, password):
        """Usage: add_admin <username> <password>"""
        if recipient in botadmins.master_admins:
            botadmins.add_admin(username, password)
            sock.send("%s %s :Admin has been added !\r\n" % (reply_type, recipient))
    
    def addbook(self, sock, recipient, reply_type, book_name, book_link):
        """Usage: addbook <book name> <book link>"""
        BotDatabase().database_addbook(sock, recipient, reply_type, recipient, book_name, book_link)
    
    def addrequest(self, sock, recipient, reply_type, req_name, req_catagory):
        """Usage: addrequest <request> <request catagory>"""
        BotDatabase().database_addrequest(sock, recipient, reply_type, recipient, req_name, req_catagory)
    
    def addtut(self, sock, recipient, reply_type, tut_name, tut_link):
        """Usage: addtut <tutorial name> <tutorial link>"""
        BotDatabase().database_addtut(sock, recipient, reply_type, recipient, tut_name, tut_link)
    
    def addtool(self, sock, recipient, reply_type, tool_name, tool_link):
        """Usage: addtool <tool name> <tool link>"""
        BotDatabase().database_addtool(sock, recipient, reply_type, recipient, tool_name, tool_link)    
    
    def getbooks(self, sock, recipient, reply_type):
        """Usage: getbooks"""
        BotDatabase().database_getbooks(sock, recipient, reply_type)
    
    def gettuts(self, sock, recipient, reply_type):
        """Usage: gettuts"""
        BotDatabase().database_gettuts(sock, recipient, reply_type)
    
    def gettools(self, sock, recipient, reply_type):
        """Usage: gettools"""
        BotDatabase().database_gettools(sock, recipient, reply_type)
    
    def getrequests(self, sock, recipient, reply_type):
        """Usage: getrequests"""
        BotDatabase().database_getrequests(sock, recipient, reply_type)
    
    def deleteitem(self, sock, recipient, reply_type, table, id):
        """Usage: deleteitem <table> <id>"""
        table = lower(table)
        BotDatabase().database_deleteitem(sock, recipient, reply_type, table, id)
    




class BotUpdate(threading.Thread):
    """Here resides the methods to update the bot, or check if an older bot
    exists, and remove it if so.
    """
    
    
    def __init__(self):
        """Sets the environment variables and others."""
        self.deployment = bot_deployment
        if sys.platform.startswith('win32'):
            self.slash = "\\"
        else:
            self.slash = "/"
        if self.deployment == ".app":
            self.current_location = self.slash.join(sys.path[0].split(self.slash)[:-2])
            self.resources = sys.path[0]
            self.base_location = self.slash.join(sys.path[0].split(self.slash)[:-3])
        else:
            self.current_location = sys.path[0]
            self.resources = sys.path[0]
            self.base_location = sys.path[0]
        self.cur_pid = os.getpid()
        self.sqldatabase = self.resources + self.slash + sqldatabase
        self.sqldump = self.base_location + self.slash + "temp_dump.sql"
        
    def setupdatabase(self):
        """Sets up the initial database to be used for the bots information."""
        sqlcon = sqlite3.connect(self.sqldatabase)
        sqlcursor = sqlcon.cursor()
        sqlcursor.execute('CREATE TABLE IF NOT EXISTS information (id INTEGER PRIMARY KEY, version VARCHAR(250), old_filepath VARCHAR(250), old_pid VARCHAR(250), deleted VARCHAR(250), db_imported VARCHAR(250))')
        # If no entries, then create first entry in database
        sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM information LIMIT 1)')
        if sqlcursor.fetchone()[0] == 0:
            insertquery = [str(bot_version), str(self.current_location), str(self.cur_pid), "NO", "NO"]
            sqlcursor.execute('INSERT INTO information VALUES (null,?,?,?,?,?)', insertquery)
            sqlcon.commit()
        sqlcursor.close()
        sqlcon.close()
    
    def exportdatabase(self):
        """Exports the SQLite database to an external file."""
        # Export the SQLite DB
        if profiling: print "Exporting the SQL to %s" % self.sqldump
        sqlcon = sqlite3.connect(self.sqldatabase)
        with open(self.sqldump, 'w') as f:
            for line in sqlcon.iterdump():
                f.write('%s\n' % line)
        sqlcon.close()
        
    def importdatabase(self):
        """Imports an external file into the SQLite database"""
        # Make sure content is erased in file before trying to import
        open(self.sqldatabase, 'w').close()
        # Import the SQLite DB
        sqlcon = sqlite3.connect(self.sqldatabase)
        f = open(self.dumpsql,'r')
        sql = f.read()
        sqlcon.executescript(sql)
        sqlcon.commit()
        sqlcursor.close()
        sqlcon.close()
        if profiling: print "Imported the SQL from %s" % self.dumpsql
        os.remove(sys.path[0] + self.slash + self.dumpsql)
        if profiling: print "Removed the temporary dump: %s" % self.dumpsql
            
    def checkforoldbot(self):
        """Checks to see if an old bot is present (and removes it) and imports the database if it hasn't been done."""
        # Check if the old DB has been imported or not
        if os.path.isfile(sys.path[0] + self.slash + self.sqldump):
            if profiling: print "Importing Database"
            self.importdatabase()
            sqlcon = sqlite3.connect(self.sqldatabase)
            sqlcursor = sqlcon.cursor()
            updatequery = [str("YES")]
            sqlcursor.execute('UPDATE information SET db_imported=?', updatequery)
            sqlcon.commit()
            db_imported = "YES"
            if db_imported == "YES":
                # Get variables
                sqlcursor.execute('SELECT * FROM information')
                db_imported = sqlcursor.fetchone()[5]
                sqlcursor.execute('SELECT * FROM information')
                deleted = sqlcursor.fetchone()[4]
                sqlcursor.execute('SELECT * FROM information')
                old_filepath = sqlcursor.fetchone()[2]
                sqlcursor.execute('SELECT * FROM information')
                old_id = sqlcursor.fetchone()[3]
                # Check if old program is deleted
                if deleted == "NO":
                    if profiling: print "Killing old application !"
                    # Kill the program
                    os.kill(int(old_id), signal.SIGHUP)
                    # Delete the old file
                    if profiling: print "Deleting old application at: " + old_filepath
                    os.remove(old_filepath)
                    # Update DB to reflect changes
                    updatequery = [str(bot_version), str("YES")]
                    sqlcursor.execute('UPDATE information SET version=?,deleted=?', updatequery)
                    sqlcon.commit()
            sqlcursor.close()
            sqlcon.close()
            if profiling: print "Application updated successfully !"
        else:
            self.setupdatabase()
            
    def updatebot(self, sock, recipient, reply_type, new_version, url):
        """Checks to see if the bot needs to be updated, and does so if needed."""
        #Make DB connection
        sqlcon = sqlite3.connect(self.sqldatabase)
        sqlcursor = sqlcon.cursor()
        sqlcursor.execute('SELECT * FROM information')
        # Check if NEW_VERSION is newer
        if new_version > bot_version:
            if profiling: print "Updating !"
            # Download new version
            while 1:
                try:
                    f = urllib2.urlopen(urllib2.Request(url))
                    link_working = True
                    if profiling: print "Link is working"
                    break
                except:
                    link_working = False
                    if profiling: print "Link is not working !"
                    break
            if link_working:
                if profiling: print "Downloading file"
                new_file_path = self.base_location + self.slash + url.split("/")[-1:][0]
                urllib.urlretrieve (url, new_file_path)
                # Unzip file
                while zipfile.is_zipfile(new_file_path):
                        try:
                            if profiling: print "Unzipping file..."
                            zippedfile = zipfile.ZipFile(new_file_path)
                            if self.deployment == ".app":
                                # Remove trailing / (.app is a folder)
                                new_file = self.base_location + self.slash + zippedfile.namelist()[0][:-1]
                            else:
                                new_file =  self.base_location + self.slash + zippedfile.namelist()[0]
                            zippedfile.extractall(BASE_LOCATION)
                            break
                        except OSError:
                            if profiling: print "File already unzipped"
                            break
                # Update DB, and put info about current program
                updatequery = [str(self.current_location), str(self.cur_pid), str("NO")]
                sqlcursor.execute('UPDATE information SET old_filepath=?,old_pid=?,deleted=?', updatequery)
                sqlcon.commit()
                # Export the SQL DB
                if profiling: print "Exporting Database"
                exportsqlitedb(irc, SPEC_CHAN)
                # Start program
                if profiling: print "Starting Program"
                if self.deployment == ".py":
                    os.system("python %s" % new_file)
                else:
                    os.system("open %s" % new_file)
        else:
            if profiling: print "Already updated !"   
        # Close the DB connection
        sqlcursor.close()
        sqlcon.close()




class BotDatabase(threading.Thread):
    """Handles the database actions of the bot."""
    
    def __init__(self):
        self.sqldatabase = sqldatabase
        self.sqlcon = sqlite3.connect(self.sqldatabase)
        self.sqlcursor = self.sqlcon.cursor()
    
    def setupdatabase(self):
        """Sets up the initial database to be used for the bots information."""
        sqlcon = sqlite3.connect(self.sqldatabase)
        sqlcursor = sqlcon.cursor()
        sqlcursor.execute('CREATE TABLE IF NOT EXISTS admins (id INTEGER PRIMARY KEY, username VARCHAR(250), password VARCHAR(250))')
        sqlcursor.execute('CREATE TABLE IF NOT EXISTS settings (id VARCHAR(250), nickname VARCHAR(250), hostname VARCHAR(250), port VARCHAR(250), channels VARCHAR(250))')
        sqlcursor.execute('CREATE TABLE IF NOT EXISTS bookcase (id INTEGER PRIMARY KEY, nickname VARCHAR(250), book_name VARCHAR(250), book_link VARCHAR(250))')
        sqlcursor.execute('CREATE TABLE IF NOT EXISTS tutorials (id INTEGER PRIMARY KEY, nickname VARCHAR(250), tut_name VARCHAR(250), tut_link VARCHAR(250))')
        sqlcursor.execute('CREATE TABLE IF NOT EXISTS tools (id INTEGER PRIMARY KEY, nickname VARCHAR(250), tool_name VARCHAR(250), tool_link VARCHAR(250))')
        sqlcursor.execute('CREATE TABLE IF NOT EXISTS requests (id INTEGER PRIMARY KEY, nickname VARCHAR(250), req_name VARCHAR(250), req_catagory VARCHAR(250))')
        sqlcon.commit()
        sqlcursor.close()
        sqlcon.close()
    
    def get_db(self,*hilight):
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM settings)')
        if self.sqlcursor.fetchone()[0] == 0:
            print "\n\nNo settings has been saved yet !\n\n"
        else:
            print "\n\n"
            print "     ,----,,----------------------,,---------------------------,,----------,,---------------------------------------,"
            print "     | id ||       Nickname       ||          Hostname         ||   port   ||              channels                 |"
            print "     '----''----------------------''---------------------------''----------''---------------------------------------'"
            self.sqlcursor.execute('SELECT * FROM settings')
            for row in self.sqlcursor:
                x = "     "
                if hilight:
                    if row[0] == hilight[0]:
                        x = "---> "
                print x+"| %s ||    %s    ||      %s     ||  %s  ||         %s          |" % (row[0].center(2), row[1].center(14), row[2].center(16), row[3].center(6), row[4].center(20),)
                print "     '----''----------------------''---------------------------''----------''---------------------------------------'"
            print "\n\n"
        self.sqlcursor.close()
        self.sqlcon.close()
    
    def set_db(self, db_id, nickname, hostname, port, channels):
        search_query = [db_id]
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM settings WHERE id=?)', search_query)
        if self.sqlcursor.fetchone()[0] == 0:
            insertquery = [db_id, nickname, hostname, port, channels]
            self.sqlcursor.execute('INSERT INTO settings VALUES (?,?,?,?,?)', insertquery)
            self.sqlcon.commit()
            print "\n\nSetting has been added."
            self.get_db(db_id)
        else:
            updatequery = [nickname, hostname, port, channels, db_id]
            self.sqlcursor.execute('UPDATE settings SET nickname=?, hostname=?, port=?, channels=? WHERE id=?', updatequery)
            self.sqlcon.commit()
            print "\n\nSetting has been updated !"
            self.get_db(db_id)
    
    def clear_db(self):
        self.sqlcursor.execute('TRUNCATE TABLE settings')
        print "\n\nCleared database !\n\n"
        self.sqlcon.commit()
        self.sqlcursor.close()
        self.sqlcon.close()
    
    def del_id(self, db_id):
        search_query = [db_id]
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM settings WHERE id=?)', search_query)
        if self.sqlcursor.fetchone()[0] == 0:
            print "\n\nNo setting with id: %s !\n\n" % db_id
        else:
            delete_query = [db_id]
            self.sqlcursor.execute('DELETE FROM settings WHERE id=?', delete_query)
            self.sqlcon.commit()
            print "\n\nDeleted setting with id %s.\n\n" % db_id
        self.sqlcursor.close()
        self.sqlcon.close()
    
    def database_addbook(self, sock, recipient, reply_type, nickname, book_name, book_link):
        # Check if the tutorial has already been added (to avoid duplicates)
        search_query = [book_name]
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM bookcase WHERE book_name=?)', search_query)
        if self.sqlcursor.fetchone()[0] == 0:
            insertquery = [nickname, book_name, book_link]
            self.sqlcursor.execute('INSERT INTO bookcase VALUES (null,?,?,?)', insertquery)
            self.sqlcon.commit()
            send_text = "Book %s has been added under the catagory %s with the link %s" % (book_name, book_link,)
        else:
            send_text = "Seems as though this book has already been added"
        sock.send("%s %s :%s\r\n" % (reply_type, recipient, send_text))
        self.sqlcursor.close()
        self.sqlcon.close()
    
    def database_getbooks(self, sock, recipient, reply_type):
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM bookcase)')
        if self.sqlcursor.fetchone()[0] == 0:
            sock.send("%s %s :Nothing here yet !\r\n" % (reply_type, recipient))
        else:
            send_text = []
            # Get list of requests and add them to list object send_text
            self.sqlcursor.execute('SELECT * FROM bookcase')
            for row in self.sqlcursor:
                send_text.append("Book: %s (%s) from %s (id:%s)" % (row[2], row[3], row[1], row[0],))
            # Now for each item in send_text, send with speed depending on how many there are (avoid flooding).
            for text in send_text:
                sock.send("%s %s :%s\r\n" % (reply_type, recipient, text))
                if 10 < len(send_text):
                    time.sleep(1)
                else:
                    time.sleep(0.5)
            self.sqlcursor.close()
            self.sqlcon.close()
    
    def database_addtut(self, sock, recipient, reply_type, nickname, tut_name, tut_link):
        # Check if the tutorial has already been added (to avoid duplicates)
        search_query = [tut_name]
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM tutorials WHERE tut_name=?)', search_query)
        if self.sqlcursor.fetchone()[0] == 0:
            insertquery = [nickname, tut_name, tut_link]
            self.sqlcursor.execute('INSERT INTO tutorials VALUES (null,?,?,?)', insertquery)
            self.sqlcon.commit()
            send_text = "Tutorial %s has been added with the link %s" % (tut_name, tut_link,)
        else:
            send_text = "Seems as though this tutorial has already been added"
        sock.send("%s %s :%s\r\n" % (reply_type, recipient, send_text))
        self.sqlcursor.close()
        self.sqlcon.close()
    
    def database_gettuts(self, sock, recipient, reply_type):
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM tutorials)')
        if self.sqlcursor.fetchone()[0] == 0:
            sock.send("%s %s :Nothing here yet !\r\n" % (reply_type, recipient))
        else:
            send_text = []
            # Get list of requests and add them to list object send_text
            self.sqlcursor.execute('SELECT * FROM tutorials')
            for row in self.sqlcursor:
                send_text.append("Tut: %s (%s) from %s (id:%s)" % (row[2], row[3], row[1], row[0],))
            # Now for each item in send_text, send with speed depending on how many there are (avoid flooding).
            for text in send_text:
                sock.send("%s %s :%s\r\n" % (reply_type, recipient, text))
                if 10 < len(send_text):
                    time.sleep(1)
                else:
                    time.sleep(0.5)
            self.sqlcursor.close()
            self.sqlcon.close()
    
    def database_addtool(self, sock, recipient, reply_type, nickname, tool_name, tool_link):
        # Check if the tutorial has already been added (to avoid duplicates)
        search_query = [tool_name]
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM tools WHERE tool_name=?)', search_query)
        if self.sqlcursor.fetchone()[0] == 0:
            insertquery = [nickname, tool_name, tool_link]
            self.sqlcursor.execute('INSERT INTO tools VALUES (null,?,?,?)', insertquery)
            self.sqlcon.commit()
            send_text = "Tool %s has been added with the link %s" % (tool_name, tool_link,)
        else:
            send_text = "Seems as though this tool has already been added"
        sock.send("%s %s :%s\r\n" % (reply_type, recipient, send_text))
        self.sqlcursor.close()
        self.sqlcon.close()
    
    def database_gettools(self, sock, recipient, reply_type):
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM tools)')
        if self.sqlcursor.fetchone()[0] == 0:
            sock.send("%s %s :Nothing here yet !\r\n" % (reply_type, recipient))
        else:
            send_text = []
            # Get list of requests and add them to list object send_text
            self.sqlcursor.execute('SELECT * FROM tools')
            for row in self.sqlcursor:
                send_text.append("Tool: %s (%s) from %s (id:%s)" % (row[2], row[3], row[1], row[0],))
            # Now for each item in send_text, send with speed depending on how many there are (avoid flooding).
            for text in send_text:
                sock.send("%s %s :%s\r\n" % (reply_type, recipient, text))
                if 10 < len(send_text):
                    time.sleep(1)
                else:
                    time.sleep(0.5)
            self.sqlcursor.close()
            self.sqlcon.close()
    
    def database_addrequest(self, sock, recipient, reply_type, nickname, req_name, req_catagory):
        # Check if the request has already been made (to avoid duplicates)
        search_query = [req_name]
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM requests WHERE req_name=?)', search_query)
        if self.sqlcursor.fetchone()[0] == 0:
            insertquery = [nickname, req_name, req_catagory]
            self.sqlcursor.execute('INSERT INTO requests VALUES (null,?,?,?)', insertquery)
            self.sqlcon.commit()
            send_text = "Request %s has been added under the catagory %s" % (req_name, req_catagory,)
        else:
            send_text = "Sorry, a request has already been made for this tutorial."
        sock.send("%s %s :%s\r\n" % (reply_type, recipient, send_text))
        self.sqlcursor.close()
        self.sqlcon.close()
    
    def database_getrequests(self, sock, recipient, reply_type):
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM requests)')
        if self.sqlcursor.fetchone()[0] == 0:
            sock.send("%s %s :Nothing here yet !\r\n" % (reply_type, recipient))
        else:
            send_text = []
            # Get list of requests and add them to list object send_text
            self.sqlcursor.execute('SELECT * FROM requests')
            for row in self.sqlcursor:
                send_text.append("%s requested tutorial about %s under catagory %s (id:%s)" % (row[1], row[2], row[3], row[0],))
            # Now for each item in send_text, send with speed depending on how many there are (avoid flooding).
            for text in send_text:
                sock.send("%s %s :%s\r\n" % (reply_type, recipient, text))
                if 10 < len(send_text):
                    time.sleep(1)
                else:
                    time.sleep(0.5)
            self.sqlcursor.close()
            self.sqlcon.close()
    
    def database_deleteitem(self, sock, recipient, reply_type, table, id):
        delete_query = [id]
        if table == "bookcase":
            self.sqlcursor.execute('DELETE FROM bookcase WHERE id=?', delete_query)
        elif table == "tutorials":
            self.sqlcursor.execute('DELETE FROM tutorials WHERE id=?', delete_query)
        elif table == "tools":
            self.sqlcursor.execute('DELETE FROM tools WHERE id=?', delete_query)
        elif table == "requests":
            self.sqlcursor.execute('DELETE FROM requests WHERE id=?', delete_query)
        self.sqlcon.commit()
        sock.send("%s %s :Deleted item with id %s from %s\r\n" % (reply_type, recipient, id, table))
        self.sqlcursor.close()
        self.sqlcon.close()
    



if __name__=="__main__":
    # Create database
    BotDatabase().setupdatabase()
    BotUpdate().setupdatabase()
    # Builds the admin and loggedin dictionaries
    botadmins = BotAdmins()
    botadmins.build_admins()
    # Check for arguments parsed through
    BotOptparse()