import threading
from inspect import *
from string import lower
import sys
import platform
import os


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
    