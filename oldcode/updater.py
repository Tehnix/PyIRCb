#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import os
import sys
import urllib
import urllib2
import sqlite3
import signal
import zipfile



class BotUpdate(threading.Thread):
    """Here resides the methods to update the bot, or check if an older bot
    exists, and remove it if so.
    """
    
    
    def __init__(self, botdeployment, botversion, sqldatabase):
        """Sets the environment variables and others."""
        self.deployment = botdeployment
        self.version = botversion
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
            insertquery = [str(BOT_VERSION), str(self.current_location), str(self.cur_pid), "NO", "NO"]
            sqlcursor.execute('INSERT INTO information VALUES (null,?,?,?,?,?)', insertquery)
            sqlcon.commit()
        sqlcursor.close()
        sqlcon.close()
    
    def exportdatabase(self):
        """Exports the SQLite database to an external file."""
        # Export the SQLite DB
        if PROFILING: print "Exporting the SQL to %s" % self.sqldump
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
        if PROFILING: print "Imported the SQL from %s" % self.dumpsql
        os.remove(sys.path[0] + self.slash + self.dumpsql)
        if PROFILING: print "Removed the temporary dump: %s" % self.dumpsql
            
    def checkforoldbot(self):
        """Checks to see if an old bot is present (and removes it) and imports the database if it hasn't been done."""
        # Check if the old DB has been imported or not
        if os.path.isfile(sys.path[0] + self.slash + self.sqldump):
            if PROFILING: print "Importing Database"
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
                    if PROFILING: print "Killing old application !"
                    # Kill the program
                    os.kill(int(old_id), signal.SIGHUP)
                    # Delete the old file
                    if PROFILING: print "Deleting old application at: " + old_filepath
                    os.remove(old_filepath)
                    # Update DB to reflect changes
                    updatequery = [str(BOT_VERSION), str("YES")]
                    sqlcursor.execute('UPDATE information SET version=?,deleted=?', updatequery)
                    sqlcon.commit()
            sqlcursor.close()
            sqlcon.close()
            if PROFILING: print "Application updated successfully !"
        else:
            self.setupdatabase()
            
    def updatebot(self, sock, recipient, reply_type, new_version, url):
        """Checks to see if the bot needs to be updated, and does so if needed."""
        #Make DB connection
        sqlcon = sqlite3.connect(self.sqldatabase)
        sqlcursor = sqlcon.cursor()
        sqlcursor.execute('SELECT * FROM information')
        # Check if NEW_VERSION is newer
        if new_version > BOT_VERSION:
            if PROFILING: print "Updating !"
            # Download new version
            while 1:
                try:
                    f = urllib2.urlopen(urllib2.Request(url))
                    link_working = True
                    if PROFILING: print "Link is working"
                    break
                except:
                    link_working = False
                    if PROFILING: print "Link is not working !"
                    break
            if link_working:
                if PROFILING: print "Downloading file"
                new_file_path = self.base_location + self.slash + url.split("/")[-1:][0]
                urllib.urlretrieve (url, new_file_path)
                # Unzip file
                while zipfile.is_zipfile(new_file_path):
                        try:
                            if PROFILING: print "Unzipping file..."
                            zippedfile = zipfile.ZipFile(new_file_path)
                            if self.deployment == ".app":
                                # Remove trailing / (.app is a folder)
                                new_file = self.base_location + self.slash + zippedfile.namelist()[0][:-1]
                            else:
                                new_file =  self.base_location + self.slash + zippedfile.namelist()[0]
                            zippedfile.extractall(BASE_LOCATION)
                            break
                        except OSError:
                            if PROFILING: print "File already unzipped"
                            break
                # Update DB, and put info about current program
                updatequery = [str(self.current_location), str(self.cur_pid), str("NO")]
                sqlcursor.execute('UPDATE information SET old_filepath=?,old_pid=?,deleted=?', updatequery)
                sqlcon.commit()
                # Export the SQL DB
                if PROFILING: print "Exporting Database"
                exportsqlitedb(irc, SPEC_CHAN)
                # Start program
                if PROFILING: print "Starting Program"
                if self.deployment == ".py":
                    os.system("python %s" % new_file)
                else:
                    os.system("open %s" % new_file)
        else:
            if PROFILING: print "Already updated !"   
        # Close the DB connection
        sqlcursor.close()
        sqlcon.close()


