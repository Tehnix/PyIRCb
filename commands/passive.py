#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Holds all passively executed commands for the IRC bot.
"""

import threading

from databaselayer import database


cmd_database = database.Database('SQLite', 'database.sql')
TABLES = []

for table in TABLES:
    cmd_database.execute(table)


class PassiveCommands(threading.Thread):
    """
    Class which keeps track of all the commands that gets
    executed automatically (ie passively).
    
    A privat method (_ prepended) cannot be launched and
    is filtered away, only public methods are available.
    
    """
    
    def __init__(self):
        """Sets initial values"""
        threading.Thread.__init__(self)
        pass
    
    def router(self, data, *args):
        """
        Analyses the recieved input (using self._analyze), and routes it to
        the appropriate command.
        
        """
        pass
    
    def _analyze(self, data):
        """Analyses the data and returns where it's relevant"""
        pass
    
    def connect(self):
        """Gets executed whenever the bot connects to a server"""
        pass
    
    def disconnect(self):
        """Gets executed whenever the bot disconnects from a server"""
        pass
    
    def join(self):
        """Gets executed whenever a join is performed"""
        pass
    
    def part(self):
        """Gets executed whenever a part is performed"""
        pass
    
    def quit(self):
        """Gets executed whenever a quit is performed"""
        pass
    
    def room_message(self):
        """Gets executed whenever a person speaks in the room"""
        pass
    
    def private_message(self):
        """Gets executed whenever a person sends a PM to the bot"""
        pass
    
    def highlight(self):
        """Gets executed whenever a person highlights the bots nickname"""
        pass

