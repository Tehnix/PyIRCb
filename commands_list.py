#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import sys

from databaselayer import database


class Commands(threading.Thread):
    """
    Class which keeps track of all the commands
    
    In the docstring of every method is how it's
    arguments are handled:
        arg  - required argument
        _arg - optional argument
        *arg - rest of arguments goes here
    
    """
    
    def __init__(self, socket):
        """ Sets initial values """
        self.sock = socket
    
    def _write(self, text):
        """ Write output to stdout """
        text = str(text) + "\n"
        sys.stdout.write(text)
        sys.stdout.flush()
    
    def _message(self, message, reciever=None, replyType="NOTICE"):
        """ Construct and send a message """
        if reciever is not None:
            self.sock.send("%s %s :%s\r\n" % (replyType, reciever, message,))
    
    def _get_nickname(self, data):
        """ Search through the IRC output for the nickname """
        return data.split("!")[0][1:]
    
    def _get_channel(self, data):
        """ Search through the IRC output for the channel name """
        for channel in self.channels:
            if channel == data.split()[2][1:]:
                return data.split()[2][1:]
        return False
    
    def _extract_note(self, data):
        """ Extract the note from the data """
        note = []
        tmpNote = ""
        i = 0
        for notes in data.split(":"):
            if i != 0 and i != 1:
                tmpNote = tmpNote + notes
            i = i + 1
        i = 0
        for notes in tmpNote.split(" "):
            if i != 0 and i != 1:
                note.append(notes)
            i = i + 1
        # Remove the last \r\n from the note
        note = " ".join(note)[0:-2]
        return note
    
    def note(self, data, recipient=None, *note):
        """ Usage: note <to nickname> <note> """
        nickname = self._get_nickname(data)
        note = self._extract_note(data)
        if recipient is not None and note != "":
            insertNote = db.insert('notes',
                                   {'recipient': recipient,
                                    'sender': nickname,
                                    'note': note,
                                    'status': '0'})
            self._message('Saving note: %s' % (note,),
                          self._get_nickname(data))
            self._write('Saving note: %s' % (note,))
        else:
            notes = db.fetchall('notes',
                                {'recipient': nickname, 'status': '0'})
            for note in notes:
                self._write('Note: %s' % (note,))
                self._message(note[3], nickname)
                try:
                    db.update('notes', {'status': '1'}, {'id': str(note[0])})
                except:
                    self._write('Exception raised in Commands.note()')


db = database.Database('SQLite', 'database.sql')
tables = [
        'CREATE TABLE IF NOT EXISTS admins (id INTEGER PRIMARY KEY, nickname TEXT, password TEXT)',
        'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, nickname TEXT)',
        'CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, recipient TEXT, sender TEXT, note TEXT, status TEXT)'
    ]

for table in tables:
    db.execute(table)