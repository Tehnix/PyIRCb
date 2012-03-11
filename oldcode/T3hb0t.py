#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from optparse import *
import threading
import socket
import ssl
import time
from hashlib import sha224
from inspect import *
from string import lower
import sys
import platform
import os

from updater import *
from databaselayer import database
from usersystem import users
from commands import *

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
| .         .       .         . Zeal Development     .     .     .     .     |
|----------------------------------------------------------------------------|
|                    T3hb0t - A Python based IRC bot                         |
|----------------------------------------------------------------------------|
|Author: Chrules at Zeal                                                     |
|Info: T3hb0t is an IRC bot client capable of connecting to multiple servers |
|and channels. Easily customized and easy to add commands.                   |
|                                                                            |
|Default operator prefix is ! . Can be set with -o option. If using -i <pass>|
|to identify, the nick must be registered beforehand (some servers require   |
|email activation !).                                                        |
|______-________-________-________-________-________-________-________-______|
"""

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
parser.add_option("-u", "--use", dest="use", action="store", nargs=4,
                  help="Starts bot with specified settings. Usage: -u <nick> <host> <port> <channels>")
parser.add_option("-s", "--set", dest="set", action="store", nargs=5,
                  help="Saves a setting. Usage: -s <id> <nick> <host> <port> <channels>")

(options, args) = parser.parse_args()

# Bot version number
BOT_VERSION = "1.0.0"
# Bot deployment details
BOT_DEPLOYMENT = ".py"
# For debugging
PROFILING = True
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
            if PROFILING: print "\n\nStarting thread with id: %s" % row[0]
            ircbot = IrcBot(row[2], int(row[3]), row[1], row[1], row[1], row[4].split())
            thread = threading.Thread(target=ircbot.connect)
            thread.start()
    
    def use(self):
        # Check for valid port
        if options.use[2] != "6667" and options.use[2] != "6697":
            print "\n\nNote that the port is %s and not 6667 or 6697 !\n\n" % options.use[2]
        if PROFILING: print "\n\nStarting script with -u !"
        ircbot = IrcBot(options.use[1], int(options.use[2]), options.use[0], options.use[0], options.use[0], options.use[3].split())
        thread = threading.Thread(target=ircbot.connect)
        thread.start()
    
    def just(self):
        sqlcon = sqlite3.connect("BotDatabase.db")
        sqlcursor = sqlcon.cursor()
        search_query = [options.just]
        sqlcursor.execute('SELECT * FROM settings WHERE id=?', search_query)
        for row in sqlcursor:
            if PROFILING: print "\n\nStarting thread with id: %s" % row[0]
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
        if PROFILING: print "Starting connect !"
        while True:
            # Regular connection
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if options.ssl:
                if PROFILING: print "Wrapping socket in SSL !"
                self.sock = ssl.wrap_socket(self.sock)
            # This allows the socket address to be reused and sets the timeout value
            # so we know if we lost the connection.
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.settimeout(300)
            try:
                self.sock.connect((self.hostname, self.port))
            except socket.gaierror:
                if PROFILING: print "Either wrong hostname or no connection. Trying again..."
                time.sleep(10)
                continue
            except ssl.SSLError:
                if PROFILING: print "Problem has occured with SSL connecting to %s:%s ! (check you're using the right port)" % (self.hostname, self.port,)
                break
            else:
                self.join()
    
    def disconnect(self, reason,*time):
        """Disconnects handled here for the various ways we might loose or drop the connection."""
        # If we get disconnected from the server
        if reason == 0:
            if PROFILING: print "Disconnected from server !"
            self.sock.close()
            self.connect()
        # If the socket times out
        elif reason == "socket.timeout" or reason == "socket.error":
            if PROFILING: print "Lost Connection (socket.timeout/socket.error). Reconnecting..."
            self.connect()
        elif reason == "PART" or reason == "QUIT":
            self.sock.send("%s\r\n" % reason)
            self.sock.close()
            if time:
                time.sleep(int(time[0]))
                self.connect()
    
    def join(self):
        """Here we set the nickname and userinfo, and joins the channels. Upon succes self.listen() is started."""
        if PROFILING: print "Starting join !"
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
                if PROFILING: print self.readdata
                self.disconnect(self.readdata)
                # PING PONG, so we don't get disconnected
                if self.readdata[0:4] == "PING":
                    self.sock.send("PONG  %s\r\n" % self.readdata.split()[1])
                # If nickname already in use, restart the process with a new nickname
                if "%s :Nickname is already in use" % self.nickname in self.readdata:
                    if PROFILING: print "Nickname already in use. Changing nick and reconnecting..."
                    self.nickname = self.nickname + str(time.time())[5:-3]
                    self.sock.close()
                    self.connect()
                    break
                # Some servers request CTCP before we can connect to channels
                if "\x01VERSION\x01" in self.readdata:
                    if PROFILING: print "CTCP request, waiting and joining channels !"
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
        if PROFILING: print "Starting listen !"
        while True:
            self.readdata = self.sock.recv(4096)
            if PROFILING: print self.readdata
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
                if PROFILING: print "Lost Connection (socket timeout). Reconnecting..."
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
        if PROFILING: print "Starting composemessage !"
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
        if PROFILING: print "Starting sendmessage !"
        self.sock.send("%s %s :%s\r\n" % (self.reply_type, self.recipient, self.msg))
    
    def executecommand(self, command,*args):
        """Here we execute the various commands that is looked for in self.listen(). It automagically registers new commands in BotCommands class."""
        if PROFILING: print "Starting executecommand !"
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
    





if __name__=="__main__":
    # Create database
    BotDatabase().setupdatabase()
    botupdate = BotUpdate(BOT_DEPLOYMENT, BOT_VERSION, sqldatabase)
    botupdate.setupdatabase()
    # Builds the admin and loggedin dictionaries
    botadmins = BotAdmins()
    botadmins.build_admins()
    # Check for arguments parsed through
    BotOptparse()
