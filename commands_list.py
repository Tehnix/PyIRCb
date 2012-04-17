#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Holds all the commands for the IRC bot.
"""

import threading
import sys
import time
import datetime
import inspect

from databaselayer import database


DB = database.Database('SQLite', 'database.sql')
TABLES = [
    'CREATE TABLE IF NOT EXISTS admins (id INTEGER PRIMARY KEY, nickname TEXT,\
     password TEXT)',
    'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, nickname TEXT)',
    'CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, recipient TEXT,\
     sender TEXT, note TEXT, status TEXT)',
    'CREATE TABLE IF NOT EXISTS back (id INTEGER PRIMARY KEY, nickname TEXT,\
     start_time TEXT, back_time TEXT)'
]

for table in TABLES:
    DB.execute(table)


class Commands(threading.Thread):
    """
    Class which keeps track of all the commands that gets
    executed by specific commands.
    
    A privat method (_ prepended) cannot be launched and
    is filtered away, only public methods are available.
    
    The docstring of the method gets printed when
    using self.help().
    
    """
    
    def __init__(self, socket, data):
        """ Sets initial values """
        threading.Thread.__init__(self)
        self.sock = socket
        self.readdata = data
    
    def help(self):
        """ Prints out the docstring of all the public methods """
        nickname = self._get_nickname()
        self._message("Displaying command list:", nickname)
        docstrings = get_docstring(quantity='all')
        for cmd, docstring in list(docstrings.items()):
            if cmd != 'help':
                self._message("%s :: %s" % (cmd, docstring,), nickname)
    
    def _message(self, message, reciever=None, reply_type="NOTICE"):
        """ Construct and send a message """
        if reciever is not None:
            self.sock.send("%s %s :%s\r\n" % (reply_type, reciever, message,))
    
    def _get_nickname(self):
        """ Search through the IRC output for the nickname """
        return self.readdata.split("!")[0][1:]
    
    def _extract_note(self):
        """ Extract the note from the data """
        note = []
        tmp_note = []
        i = 0
        for notes in self.readdata.split(":"):
            if i != 0 and i != 1:
                tmp_note.append(notes)
            i = i + 1
        i = 0
        tmp_note = ":".join(tmp_note)
        for notes in tmp_note.split(" "):
            if i != 0 and i != 1:
                note.append(notes)
            i = i + 1
        # Remove the last \r\n from the note
        note = " ".join(note)[0:-2]
        return note
    
    def note(self, recipient=None, *note):
        """ Usage: note <to nickname> <note> """
        nickname = self._get_nickname()
        note = self._extract_note()
        if recipient is not None and note != "":
            date_time = time.strftime("%b %d - %H:%M", time.localtime())
            prepend_note = "[%s - %s] :: " % (date_time, nickname,)
            note = prepend_note + note
            DB.insert(
                'notes',
                {
                    'recipient': recipient,
                    'sender': nickname,
                    'note': note,
                    'status': '0'
                }
            )
            self._message('Saving note: %s' % (note,), nickname)
            write('Saving note: %s' % (note,))
        else:
            notes = DB.fetchall('notes',
                                {'recipient': nickname, 'status': '0'})
            for note in notes:
                write('Note: %s' % (note,))
                self._message(note[3], nickname)
    
    def notelist(self):
        """ Usage: notelist """
        nickname = self._get_nickname()
        notes = DB.fetchall('notes', {'recipient': nickname})
        for note in notes:
            write('[id: %s] Note :: %s' % (note[0], note[3],))
            self._message("[id: %s] Note :: %s" % (note[0], note[3],),
                          nickname)
    
    def noteread(self, note_id=None):
        """ Usage: notelist """
        nickname = self._get_nickname()
        if note_id is not None:
            DB.update('notes',
                      {'status': '1'},
                      {'recipient': nickname, 'id': note_id})
            write("Note with id %s is now marked as read" % (note_id,))
            self._message("Note with id %s is now marked as read" % (note_id,),
                          nickname)
        else:
            write("Please specify an id")
            self._message("Please specify an id", nickname)
    
    def backin(self, back_in=None):
        """ Usage: backin <time> """
        nickname = self._get_nickname()
        if back_in is not None:
            start_time = int(time.time())
            DB.delete('back', {'nickname': nickname})
            DB.insert(
                'back',
                {
                    'nickname': nickname,
                    'start_time': start_time,
                    'back_time': back_in
                }
            )
            write("Saved: See you in %s" % (back_in,))
            self._message("Saved: See you in %s" % (back_in,), nickname)
        else:
            write("Please specify a time")
            self._message("Please specify a time", nickname)
    
    def back(self, nickname=None):
        """ Usage: back <nickname> """
        if nickname is not None:
            backin = DB.fetchone('back', {'nickname': nickname})
            if backin is not None:
                backin = back_in_time(backin[3], backin[2])
                write("%s will be back at %s" % (nickname, backin,))
                self._message("%s will be back at %s" % (nickname, backin,),
                               nickname)
            else:
                write("No entry found for %s" % (nickname,))
                self._message("No entry found for %s" % (nickname,), nickname)
        else:
            write("Please specify a nickname")
            self._message("Please specify a nickname", nickname)


def write(text):
    """ Write output to stdout """
    text = str(text) + "\n"
    sys.stdout.write(text)
    sys.stdout.flush()

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
    return docstring


def command_list():
    """ Construct a list of all the commands """
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

def back_in_time(backin, start_time):
    """ Converts string given to a usable time """
    if 'h' in backin:
        backin = int(start_time) + float(backin[0:-1]) * 3600
        backin = datetime.datetime.fromtimestamp(int(backin))
        backin = backin.strftime('%b %d - %H:%M')
        return "%s" % (backin,)
    elif 'm' in backin:
        backin = int(start_time) + float(backin[0:-1]) * 60
        backin = datetime.datetime.fromtimestamp(int(backin))
        backin = backin.strftime('%b %d - %H:%M')
        return "%s" % (backin,)
    else:
        start_time = datetime.datetime.fromtimestamp(int(start_time))
        start_time = start_time.strftime('%b %d - %H:%M')
        return "%s from %s" % (backin, start_time,)
