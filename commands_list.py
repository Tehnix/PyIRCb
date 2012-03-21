#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import sys
import time
import datetime
import inspect

from databaselayer import database


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
        self.sock = socket
        self.readdata = data
    
    def help(self):
        """ Prints out the docstring of all the public methods """
        nickname = self._get_nickname()
        self._message("Displaying command list:", nickname)
        docstrings = self._get_docstring(quantity='all')
        for cmd, docstring in docstrings.iteritems():
            if cmd != 'help':
                self._message("%s :: %s" % (cmd, docstring,), nickname)
    
    def _get_docstring(self, cmd=None, quantity='one'):
        """
        Fetches the docstring of the given method
        
        Arg [quantity] specifies how many to fetch:
            one - fetches the given cmd
            all - fetches all cmds in Commands class
        
        """
        docstring = {}
        if quantity == 'one' and cmd is not None:
            docstring[cmd] = inspect.cleandoc(inspect.getdoc(getattr(Commands, cmd)))
        elif quantity == 'all':
            for cmd in self._command_list():
                docstring[cmd] = inspect.cleandoc(inspect.getdoc(getattr(Commands, cmd)))
        return docstring
    
    def _command_list(self):
        """ Construct a list of all the commands """
        cmdList = []
        # These are common to the class, but we do not need them
        cmdListIgnores = ["daemon", "getName",
                          "ident", "is_alive",
                          "isAlive", "isDaemon",
                          "join", "name",
                          "run", "setDaemon",
                          "setName", "start"]
        for i in range(len(inspect.getmembers(Commands))):
            if (inspect.getmembers(Commands)[i][0].startswith("_") or
                inspect.getmembers(Commands)[i][0] in cmdListIgnores):
                pass
            else:
                cmdList.append(inspect.getmembers(Commands)[i][0])
        # Sort the command list alphabetically
        cmdList.sort(key=lambda x: x.lower())
        return cmdList
    
    def _write(self, text):
        """ Write output to stdout """
        text = str(text) + "\n"
        sys.stdout.write(text)
        sys.stdout.flush()
    
    def _message(self, message, reciever=None, replyType="NOTICE"):
        """ Construct and send a message """
        if reciever is not None:
            self.sock.send("%s %s :%s\r\n" % (replyType, reciever, message,))
    
    def _get_nickname(self):
        """ Search through the IRC output for the nickname """
        return self.readdata.split("!")[0][1:]
    
    def _get_channel(self):
        """ Search through the IRC output for the channel name """
        for channel in self.channels:
            if channel == self.readdata.split()[2][1:]:
                return self.readdata.split()[2][1:]
        return False
    
    def _extract_note(self):
        """ Extract the note from the data """
        note = []
        tmpNote = []
        i = 0
        for notes in self.readdata.split(":"):
            if i != 0 and i != 1:
                tmpNote.append(notes)
            i = i + 1
        i = 0
        tmpNote = ":".join(tmpNote)
        for notes in tmpNote.split(" "):
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
            dateTime = time.strftime("%b %d - %H:%M", time.localtime())
            prependNote = "[%s - %s] :: " % (dateTime, nickname,)
            note = prependNote + note
            insertNote = db.insert('notes',
                                   {'recipient': recipient,
                                    'sender': nickname,
                                    'note': note,
                                    'status': '0'})
            self._message('Saving note: %s' % (note,), nickname)
            self._write('Saving note: %s' % (note,))
        else:
            notes = db.fetchall('notes',
                                {'recipient': nickname, 'status': '0'})
            for note in notes:
                self._write('Note: %s' % (note,))
                self._message(note[3], nickname)
    
    def notelist(self):
        """ Usage: notelist """
        nickname = self._get_nickname()
        notes = db.fetchall('notes', {'recipient': nickname})
        for note in notes:
            self._write('[id: %s] Note :: %s' % (note[0], note[3],))
            self._message("[id: %s] Note :: %s" % (note[0], note[3],),
                          nickname)
    
    def noteread(self, noteId=None):
        """ Usage: notelist """
        nickname = self._get_nickname()
        if noteId is not None:
            db.update('notes',
                      {'status': '1'},
                      {'recipient': nickname, 'id': noteId})
            self._write("Note with id %s is now marked as read" % (noteId,))
            self._message("Note with id %s is now marked as read" % (noteId,),
                          nickname)
        else:
            self._write("Please specify an id")
            self._message("Please specify an id", nickname)
    
    def backin(self, backIn=None):
        """ Usage: backin <time> """
        nickname = self._get_nickname()
        if backIn is not None:
            startTime = int(time.time())
            deleteBack = db.delete('back', {'nickname': nickname})
            insertBack = db.insert('back',
                                   {'nickname': nickname,
                                    'start_time': startTime,
                                    'back_time': backIn})
            self._write("Saved: See you in %s" % (backIn,))
            self._message("Saved: See you in %s" % (backIn,), nickname)
        else:
            self._write("Please specify a time")
            self._message("Please specify a time", nickname)
    
    def _back_in_time(self, backin, startTime):
        """ Converts string given to a usable time """
        if 'h' in backin:
            backin = int(startTime) + float(backin[0:-1]) * 3600
            backin = datetime.datetime.fromtimestamp(int(backin))
            backin = backin.strftime('%b %d - %H:%M')
            return "%s" % (backin,)
        elif 'm' in backin:
            backin = int(startTime) + float(backin[0:-1]) * 60
            backin = datetime.datetime.fromtimestamp(int(backin))
            backin = backin.strftime('%b %d - %H:%M')
            return "%s" % (backin,)
        else:
            startTime = datetime.datetime.fromtimestamp(int(startTime))
            startTime = startTime.strftime('%b %d - %H:%M')
            return "%s from %s" % (backin, startTime,)
    
    def back(self, nickname=None):
        """ Usage: back <nickname> """
        if nickname is not None:
            backin = db.fetchone('back', {'nickname': nickname})
            if backin is not None:
                backin = self._back_in_time(backin[3], backin[2])
                self._write("%s will be back at %s" % (nickname, backin,))
                self._message("%s will be back at %s" % (nickname, backin,),
                               nickname)
            else:
                self._write("No entry found for %s" % (nickname,))
                self._message("No entry found for %s" % (nickname,), nickname)
        else:
            self._write("Please specify a nickname")
            self._message("Please specify a nickname", nickname)




db = database.Database('SQLite', 'database.sql')
tables = [
        'CREATE TABLE IF NOT EXISTS admins (id INTEGER PRIMARY KEY, nickname TEXT, password TEXT)',
        'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, nickname TEXT)',
        'CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, recipient TEXT, sender TEXT, note TEXT, status TEXT)',
        'CREATE TABLE IF NOT EXISTS back (id INTEGER PRIMARY KEY, nickname TEXT, start_time TEXT, back_time TEXT)'
    ]

for table in tables:
    db.execute(table)