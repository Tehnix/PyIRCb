#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Holds all the actively executed commands for the IRC bot.
"""

import threading
import sys
import time
import datetime
import inspect
import random

from databaselayer import database


cmd_database = database.Database('SQLite', 'database.sql')
TABLES = [
    'CREATE TABLE IF NOT EXISTS admins (id INTEGER PRIMARY KEY, nickname TEXT,\
     password TEXT, server TEXT, channel TEXT)',
    'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, nickname TEXT,\
     server TEXT, channel TEXT)',
    'CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, recipient TEXT,\
     sender TEXT, note TEXT, status TEXT, server TEXT, channel TEXT)',
    'CREATE TABLE IF NOT EXISTS back (id INTEGER PRIMARY KEY, nickname TEXT,\
     start_time TEXT, back_time TEXT, server TEXT, channel TEXT)'
]

for table in TABLES:
    cmd_database.execute(table)


class ActiveCommands(threading.Thread):
    """
    Class which keeps track of all the commands that gets
    executed by specific commands.

    A privat method (_ prepended) cannot be launched and
    is filtered away, only public methods are available.

    The docstring of the method gets printed when
    using self.help().

    """

    def __init__(self):
        """Sets initial values"""
        threading.Thread.__init__(self)
        self.users_in_room = {}
        self.sock = None
        self.readdata = None
        self.channels = None
        self.server = None

    def _data(self, socket, data, server, channels):
        """Saves the given data and socket to the instance"""
        self.sock = socket
        self.readdata = data
        self.channels = channels
        self.server = server

    def _user_join(self, nick, chan):
        """Add joined user to instance variable"""
        try:
            self.users_in_room[chan]
        except KeyError:
            self.users_in_room[chan] = []
        self.users_in_room[chan].append(nick)

    def _user_left(self, nick, chan):
        """Add joined user to instance variable"""
        try:
            self.users_in_room[chan].remove(nick)
        except KeyError:
            self.users_in_room[chan] = []

    def _users(self, action, users=None):
        """Sets or gets the instance variable"""
        if action == "get":
            return self.users_in_room
        if action == "set":
            self.users_in_room = users

    def users(self):
        """Prints out all users in the room"""
        nickname = get_nickname(self.readdata)
        chan = get_channel(self.readdata, self.channels)
        try:
            self.users_in_room[chan]
        except KeyError:
            self.users_in_room[chan] = []
        users = " ".join(self.users_in_room[chan])
        if len(self.users_in_room[chan]) > 0:
            self._message(users, nickname)
        else:
            self._message("Could not find any users :| !", nickname)

    def help(self):
        """Prints out the docstring of all the public methods"""
        nickname = get_nickname(self.readdata)
        self._message("Displaying command list:", nickname)
        docstrings = get_docstring(quantity='all')
        for cmd, docstring in list(docstrings.items()):
            if cmd != 'help':
                self._message("%s :: %s" % (cmd, docstring,), nickname)
                time.sleep(0.2)

    def _message(self, message, reciever=None, reply_type="NOTICE"):
        """Construct and send a message"""
        if reciever is not None:
            text = "%s %s :[*] %s\r\n" % (reply_type, reciever, message,)
            self.sock.send(to_bytes(text))

    def _raw_message(self, text):
        """Construct an IRC message and send it"""
        text = "%s\r\n" % (text,)
        self.sock.send(to_bytes(text))

    def _extract_note(self):
        """Extract the note from the data"""
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

    def derp(self):
        """Send some herp :D ! lol ^_^"""
        chan = get_channel(self.readdata, self.channels)
        self._message('Herrrrpppp..!', chan, "PRIVMSG")

    def zen(self):
        """Send some random python zen"""
        python_zen = [
            "Beautiful is better than ugly.",
            "Explicit is better than implicit.",
            "Simple is better than complex.",
            "Complex is better than complicated.",
            "Flat is better than nested.",
            "Sparse is better than dense.",
            "Readability counts.",
            "Special cases aren't special enough to break the rules.",
            "Although practicality beats purity.",
            "Errors should never pass silently.",
            "Unless explicitly silenced.",
            "In the face of ambiguity, refuse the temptation to guess.",
            "There should be one-- and preferably only one --obvious way to do it.",
            "Although that way may not be obvious at first unless you're Dutch.",
            "Now is better than never.",
            "Although never is often better than *right* now.",
            "If the implementation is hard to explain, it's a bad idea.",
            "If the implementation is easy to explain, it may be a good idea.",
            "Namespaces are one honking great idea -- let's do more of those!"
        ]
        random.shuffle(python_zen)
        chan = get_channel(self.readdata, self.channels)
        try:
            self._message('%s' % (python_zen[0],), chan, "PRIVMSG")
        except KeyError:
            pass

    def joke(self):
        """Send some random python jokes"""
        python_joke = [
            [
                "Cute Wabbit",
                "A little girl goes into a pet show and asks for a wabbit. The shop keeper looks down at her, smiles and says:",
                "'Would you like a lovely fluffy little white rabbit, or a cutesy wootesly little brown rabbit?'",
                "'Actually', says the little girl, 'I don't think my python would notice.'",
                "—Nick Leaton, Wed, 04 Dec 1996"
            ],
            [
                "Shooting Yourself in the Foot",
                "Python: You create a gun module, a gun class, a foot module and a foot class. After realising you can't point the gun at the foot, you pass a reference to the gun to a foot object. After the foot is blown up, the gun object remains alive for eternity, ready to shoot all future feet that may happen to appear.",
                "Java: You find that Microsoft and Sun have released incompatible class libraries both implementing Gun objects. You then find that although there are plenty of feet objects implemented in the past in many other languages, you cannot get access to one. But seeing as Java is so cool, you dont care and go around shooting anything else you can find.",
                "—Mark Hammond"
            ],
            [
                "Tasty Slices",
                "Timo asked:",
                "> how do i pass a copy of a list of a function?",
                "Use the Paranoia emoticon.",
                "list = ['blah', 'blah']",
                "f(list[:])",
                "This passes the \"here's my desert, where's everyone elses?\" slice."
            ],
            [
                "This has been percolating in the back of my mind for a while. It's a scene from _The Empire Strikes Back_ reinterpreted to serve a valuable moral lesson for aspiring programmers.",
                "--",
                "EXTERIOR: DAGOBAH -- DAY With Yoda strapped to his back, Luke climbs up one of the many thick vines that grow in the swamp until he reaches the Dagobah statistics lab. Panting heavily, he continues his exercises -- grepping, installing new packages, logging in as root, and writing replacements for two-year-old shell scripts in Python.",
                "YODA: Code!  Yes.  A programmer's strength flows from code maintainability.  But beware of Perl.  Terse syntax... more than one way to do it...  default variables.  The dark side of code maintainability are they.  Easily they flow, quick to join you when code you write.  If once you start down the dark path, forever will it dominate your destiny, consume you it will.",
                "LUKE: Is Perl better than Python?",
                "YODA: No... no... no.  Quicker, easier, more seductive.",
                "LUKE: But how will I know why Python is better than Perl?",
                "YODA: You will know.  When your code you try to read six months from now."
            ],
            [
                "There are 10 types of people in this world.",
                "Those who understand binary, and those who don't."
            ],
            [
                "\"C makes it easy to shoot yourself in the foot. C++ makes it",
                "harder, but when you do, it blows away your whole leg.\"",
                "- Bjarne Stroustrup"
            ],
            [
                "An int, a char and a string walk into a bar and order some drinks.",
                "A short while later, the int and char start hitting on the waitress who gets very uncomfortable and walks away.",
                "The string walks up to the waitress and says \"You’ll have to forgive them, they’re primitive types.\""
            ],
            [
                "A SQL query walks up to two tables in a restaurant and asks: \"Mind if I join you?\"",
                "Eight bytes walk into a bar and say to the bartender: \"Make us a double.\"",
                "Two strings walk into a bar. One says to the bartender: \"I’ll have a beer*7jd@jh.\" The other says: \"Excuse my friend, he’s not null terminated.\""
            ],
            [
                "A programmer goes out with a chick. Next day he tells his friend how ",
                "the date went: \"It was raining, we were soaked. We went to her place where she started to undress before me… ",
                "Then she threw the wet clothes on the computer\" – \"Wow… what kind of computer?\" – the other says."
            ],
            [
                "Q: How many programmers does it take to change a lightbulb?",
                "A: None. They won’t touch it because it’s a hardware problem."
            ],
            [
                "Q: What do cats and programmers have in common?",
                "A: When either one is unusually happy and excited, an appropriate question would be, \"did you find a bug?\""
            ],
            [
                "Q: What is the most used language in programming?",
                "A: Profanity."
            ],
            [
                "Q: Why do programmers confuse Halloween and Christmas?",
                "A: Because Oct 31 == Dec 25"
            ],
            [
                "Q: How did the programmer die in the shower?",
                "A: He read the shampoo bottle instructions: Lather. Rinse. Repeat."
            ],
            [
                "Q: Why did the programmer quit his job?",
                "A: Because he didn’t get arrays."
            ],
            [
                "Q: How do developers create shaman spells?",
                "A: Using a hex editor."
            ]
        ]
        chan = get_channel(self.readdata, self.channels)
        random.shuffle(python_joke)
        try:
            for joke in python_joke[0]:
                self._message('%s' % (joke,), chan, "PRIVMSG")
                time.sleep(0.3)
        except KeyError:
            pass

    def note(self, recipient=None, *note):
        """$note : Usage: note <to nickname> <note>. Stores a note for the given nickname."""
        nickname = get_nickname(self.readdata)
        note = self._extract_note()
        if recipient is not None and note != "":
            date_time = time.strftime("%b %d - %H:%M", time.localtime())
            prepend_note = "[%s - %s] :: " % (date_time, nickname,)
            note = prepend_note + note
            cmd_database.insert(
                'notes',
                {
                    'recipient': recipient,
                    'sender': nickname,
                    'note': note,
                    'status': '0',
                    'channel': get_channel(self.readdata, self.channels),
                    'server': self.server
                },
                out='none'
            )
            self._message('Saving note: %s' % (note,), nickname)
            write('Saving note: %s' % (note,))
        elif recipient is None:
            self._message(
                "For whom may I save this, sir?",
                nickname
            )
        elif note == "":
            self._message(
                "The note was empty, sooo not gonna store that, sorry ;)...",
                nickname
            )
        else:
            self._message(
                "Can I take your message sir?...",
                nickname
            )

    def unread(self, note_id=None):
        """ $unread : Usage: unread <id>. Without <id>, list all notes marked as unread. With <i>, gives a note the status of 'unread', so it doesn't show in $read."""
        nickname = get_nickname(self.readdata)
        if note_id is not None:
            cmd_database.update('notes',
                      {'status': '0'},
                      {'recipient': nickname, 'id': note_id})
            write("Note with id %s is now marked as unread" % (note_id,))
            self._message(
                "Note with id %s is now marked as unread" % (note_id,),
                nickname
            )
        else:
            notes = cmd_database.fetchall(
                'notes',
                {
                    'recipient': nickname,
                    'status': '0',
                    'channel': get_channel(self.readdata, self.channels),
                    'server': self.server
                }
            )
            if len(notes) > 0:
                for note in notes:
                    write('%s' % (note,))
                    self._message('[%s]%s' % (note[0], note[3],), nickname)
            else:
                self._message(
                    "No unread messages today sir, sorry :(...",
                    nickname
                )

    def read(self, note_id=None):
        """ $read : Usage: read <id>. Without <id>, list all notes marked as read. With <i>, gives a note the status of 'read', so it doesn't show in $unread."""
        nickname = get_nickname(self.readdata)
        if note_id is not None:
            cmd_database.update('notes',
                      {'status': '1'},
                      {'recipient': nickname, 'id': note_id})
            write("Note with id %s is now marked as read" % (note_id,))
            self._message(
                "Note with id %s is now marked as read" % (note_id,),
                nickname
            )
        else:
            notes = cmd_database.fetchall(
                'notes',
                {
                    'recipient': nickname,
                    'status': '1',
                    'channel': get_channel(self.readdata, self.channels),
                    'server': self.server
                }
            )
            if len(notes) > 0:
                for note in notes:
                    write('%s' % (note,))
                    self._message('[%s]%s' % (note[0], note[3],), nickname)
            else:
                self._message(
                    "No read messages so far sir, sorry :(...",
                    nickname
                )

    def backin(self, back_in=None):
        """Usage: backin <time>"""
        nickname = get_nickname(self.readdata)
        if back_in is not None:
            start_time = int(time.time())
            cmd_database.delete('back', {'nickname': nickname})
            cmd_database.insert(
                'back',
                {
                    'nickname': nickname,
                    'start_time': start_time,
                    'back_time': back_in,
                    'channel': get_channel(self.readdata, self.channels),
                    'server': self.server
                },
                out='none'
            )
            write("Saved: See you in %s" % (back_in,))
            self._message("Saved: See you in %s" % (back_in,), nickname)
        else:
            write("Please specify a time")
            self._message("Please specify a time", nickname)

    def back(self, nickname=None):
        """Usage: back <nickname>"""
        sender_nickname = get_nickname(self.readdata)
        if nickname is not None:
            backin = cmd_database.fetchone('back', {'nickname': nickname})
            if backin is not None:
                backin = back_in_time(backin[3], backin[2])
                write("%s will be back at %s" % (nickname, backin,))
                self._message(
                    "%s will be back at %s" % (nickname, backin,),
                    sender_nickname
                )
            else:
                write(
                    "Sorry, but I don't know when %s will be back :("
                    % (nickname,)
                )
                self._message(
                    "Sorry, but I don't know when %s will be back :(" %
                    (nickname,),
                    sender_nickname
                )
        else:
            cmd_database.delete('back', {'nickname': sender_nickname})
            self._message("Welcome back sir!", sender_nickname)


def write(text):
    """Write output to stdout"""
    text = to_unicode(text)
    text = "[*] %s\n" % (text,)
    sys.stdout.write(text)
    sys.stdout.flush()


def to_bytes(text):
    """Convert string to bytes"""
    if type(text) != bytes:
        try:
            text = bytes(text, 'UTF-8')
        except TypeError:
            print("\n[WARNING] : Failed to encode from unicode to bytes\n")
            print(type(text))
            print(text)
            text = b''
    return text


def to_unicode(text):
    """Converts bytes to unicode"""
    if type(text) != str:
        try:
            text = str(text, encoding='UTF-8')
        except UnicodeDecodeError:
            text = "\n[WARNING] : Failed to decode from bytes to unicode\n"
    return text


def get_nickname(data):
    """Search through the IRC output for the nickname"""
    try:
        return data.split("!")[0][1:]
    except IndexError:
        return False


def get_channel(data, channels):
    """Search through the IRC output for the channel name"""
    chan = False
    try:
        for channel in channels:
            if channel == data.split()[2]:
                chan = data.split()[2]
                # data.split()[3][1:]
        if chan is False:
            for channel in channels:
                if channel == data.split()[2]:
                    chan = data.split()[3][1:]
    except IndexError:
        pass
    return chan.replace(' ', '')


def get_docstring(cmd=None, quantity='one'):
    """
    Fetches the docstring of the given method

    Arg [quantity] specifies how many to fetch:
        one - fetches the given cmd
        all - fetches all cmds in Commands class

    """
    docstring = {}
    if quantity == 'one' and cmd is not None:
        command_doc = inspect.getdoc(getattr(ActiveCommands, cmd))
        docstring[cmd] = inspect.cleandoc(command_doc)
    elif quantity == 'all':
        for cmd in command_list():
            command_doc = inspect.getdoc(getattr(ActiveCommands, cmd))
            docstring[cmd] = inspect.cleandoc(command_doc)
    return docstring


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
    for i in range(len(inspect.getmembers(ActiveCommands))):
        if (inspect.getmembers(ActiveCommands)[i][0].startswith("_") or
            inspect.getmembers(ActiveCommands)[i][0] in cmd_list_ignores):
            pass
        else:
            cmd_list.append(inspect.getmembers(ActiveCommands)[i][0])
    # Sort the command list alphabetically
    cmd_list.sort(key=lambda x: x.lower())
    return cmd_list


def back_in_time(backin, start_time):
    """Converts string given to a usable time"""
    # NOTE return the time in amount of time left
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
