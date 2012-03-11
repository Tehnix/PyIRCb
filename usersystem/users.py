#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading


from databaselayer import database

class BotAdmins(threading.Thread):
    """Creates and manages the admins, plus the loggedin dictionary."""
    
    def __init__(self):
        self.sqldatabase = sqldatabase
        # Predefined admins. The key is the username and the
        # value is a sha224 of the password
        self.admins = {"AdminName":"90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809"}
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
    
