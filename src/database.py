#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Database abstraction layer. Simplyfies database
handling a bit.

An example of common usecase could be as such:

# Import the module
from databaselayer import database

# Create the database
myDB = database.Database('SQLite', 'database.sql')
# Create a table
myDB.execute(
    'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)'
)
# Insert a few people in the users table
myDB.insert('users', {'username': 'John'})
myDB.insert('users', {'username': 'Tom'})


"""

import threading
import sys
try:
    import sqlite3
    SQLITE = True
except ImportError:
    # Fallback for sqlite3 (custom install)
    try:
        from pysqlite2 import dbapi2 as sqlite3
        SQLITE = True
    except ImportError:
        SQLITE = False
try:
    import MySQLdb
    MYSQL = True
except ImportError:
    MYSQL = False


class Database(threading.Thread):
    """
    Higher level database abstraction layer.
    
    Provides a database abstraction layer, for easy use with
    multiple different database types, without the need to
    think about SQL differences. If you want to execute raw SQL, 
    you can use the execute method.
    
    Throughout the class, a lot of methods take in a filter argument. 
    The filter is in the format of {'field': 'value'}. The data
    argument follows the same syntax.
    
    The add argument is to add additional raw SQL to a constructed 
    query (e.g. add="ORDER BY time").
    
    """
    
    def __init__(self, dbtype=None, dbname=None, dbserver=None, creden=None):
        """Sets the values for the database instance"""
        threading.Thread.__init__(self)
        try:
            self.dbtype = dbtype
            self.dbname = dbname
        except NameError:
            raise NameError('No database type or name specified!')
        if dbserver is not None:
            self.dbserver = dbserver
        if creden is not None:
            try:
                self.user = creden['username']
            except KeyError:
                self.user = None
            try:
                self.passwd = creden['password']
            except KeyError:
                self.passwd = None
        else:
            self.user = None
            self.passwd = None
        self.temp_values = None
        self.temp_insert_values = None
        self.last_insert_id = None
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Make the connection based on the type of database.
        
        Types allowed:
            SQLite
            MySQL
        
        """
        if SQLITE and self.dbtype == 'SQLite':
            self.conn = sqlite3.connect(self.dbname)
            self.cursor = self.conn.cursor()
        elif MYSQL and self.dbtype == 'MySQL':
            self.conn = MySQLdb.connect(host=self.dbserver, db=self.dbname,
                                        user=self.user, passwd=self.passwd)
            self.cursor = self.conn.cursor()
        else:
            raise NameError('No database available!')

    def _keys_to_sql(self, keys=None, sep='AND '):
        """Construct the SQL filter from a dict"""
        if keys is None:
            keys = {}
        filters = []
        self.temp_values = ()
        for field, value in list(keys.items()):
            filters.append("%s = ? " % field)
            self.temp_values = self.temp_values + (value,)
        return sep.join(filters)
    
    def _keys_to_insert_sql(self, keys=None, sep=', '):
        """Convert a dict into an SQL field value pair"""
        if keys is None:
            keys = {}
        fields = []
        values = []
        self.temp_insert_values = ()
        for field, value in list(keys.items()):
            fields.append(field)
            values.append('?')
            self.temp_insert_values = self.temp_insert_values + (value,)
        fields = '(' + sep.join(fields) + ') '
        values = 'VALUES(' + sep.join(values) + ') '
        return fields + values
    
    def execute(self, sql=None):
        """Simply execute the given SQL"""
        if sql is not None:
            self.connect()
            try:
                self.cursor.execute(sql)
            except sqlite3.OperationalError as error:
                self.conn.rollback()
                return 'SQL Error: %s' % error
            else:
                self.conn.commit()
                self.cursor.close()
        else:
            raise NameError('There was no SQL to be parsed')
    
    def rawfetch(self, sql=None, data=None, fetchall=True, out='none'):
        """Fetches all rows from the given SQL.
        
        Arg [out] specifies what the output should be:
            none   : do nothing here (simply return)
            output : send output to stdout

        """
        if sql is not None:
            self.connect()
            try:
                if data is None:
                    self.cursor.execute(sql)
                else:
                    self.cursor.execute(sql, tuple(data))
            except sqlite3.OperationalError as error:
                self.conn.rollback()
                if out == 'output':
                    write("Error running SQL: %s" % (sql,))
                return 'SQL Error: %s' % error
            else:
                if out == 'output':
                    write("Successfully ran: %s" % (sql,))
                # Cleanup and return
                if fetchall:
                    result = self.cursor.fetchall()
                else:
                    result = self.cursor.fetchone()
                self.cursor.close()
                return result
        else:
            raise NameError('There was no SQL to be parsed')

    def fetchall(self, table=None, filters=None, add='', out='none'):
        """Fetches all rows from database based on the filters applied.
        
        Arg [out] specifies what the output should be:
            none   : do nothing here (simply return)
            output : send output to stdout
        
        """
        append = ' WHERE '
        if filters is None:
            filters = {}
            append = ''
        if table is not None:
            # Construct the SQL
            sql = 'SELECT * FROM ' + table + append +\
                  self._keys_to_sql(filters)
            self.connect()
            try:
                self.cursor.execute(sql + add, self.temp_values)
            except sqlite3.OperationalError as error:
                self.conn.rollback()
                del self.temp_values
                if out == 'output':
                    write("Error running SQL: %s" % (sql,))
                return 'SQL Error: %s' % error
            else:
                if out == 'output':
                    write("Successfully ran: %s" % (sql,))
                # Cleanup and return
                del self.temp_values
                result = self.cursor.fetchall()
                self.cursor.close()
                return result
        else:
            raise NameError('Table not specified!')
    
    def fetchone(self, table=None, filters=None, out='none'):
        """Fetches the first row from database based on the filters applied.
        
        Arg [out] specifies what the output should be:
            none   : do nothing here (simply return)
            output : send output to stdout
        
        """
        if filters is None:
            filters = {}
        if table is not None:
            # Construct the SQL
            sql = 'SELECT * FROM ' + table + ' WHERE ' +\
                  self._keys_to_sql(filters)
            self.connect()
            try:
                self.cursor.execute(sql, self.temp_values)
            except sqlite3.OperationalError as error:
                del self.temp_values
                self.conn.rollback()
                if out == 'output':
                    write("Error running SQL: %s" % (sql,))
                return 'SQL Error: %s' % error
            else:
                if out == 'output':
                    write("Successfully ran: %s" % (sql,))
                # Cleanup and return
                del self.temp_values
                result = self.cursor.fetchone()
                self.cursor.close()
                return result
        else:
            raise NameError('Table not specified!')
    
    def insert(self, table=None, data=None, out=None):
        """
        Inserts specified data into the database
        
        Arg [out] specifies what the output should be:
            none   : do nothing here (simply return)
            output : send output to stdout
        
        """
        if data is None:
            data = {}
        if table is not None:
            sql = 'INSERT INTO ' + table + self._keys_to_insert_sql(data)
            self.connect()
            try:
                self.cursor.execute(sql, self.temp_insert_values)
            except sqlite3.OperationalError as error:
                self.conn.rollback()
                del self.temp_insert_values
                if out == 'output':
                    write("Error running SQL: %s" % (sql,))
                return 'SQL Error: %s' % error
            else:
                if out == 'output':
                    write("Successfully ran: %s" % (sql,))
                    write("With data       : %s" % (self.temp_insert_values,))
                del self.temp_insert_values
                # TODO Fix the last insert id
                # self.last_insert_id = self.cursor.lastrowid()
                self.conn.commit()
                self.cursor.close()
                return True
        else:
            raise NameError('Table not specified!')
    
    def update(self, table=None, data=None, filters=None, out=None):
        """
        Updates rows where filters apply with, given data
        
        Arg [out] specifies what the output should be:
            none   : do nothing here (simply return)
            output : send output to stdout
        
        """
        if data is None:
            data = {}
        if filters is None:
            filters = {}
        if table is not None:
            values = []
            data = self._keys_to_sql(data, sep=', ')
            values = self.temp_values
            if filters:
                filters = ' WHERE ' + str(self._keys_to_sql(filters))
                values = values + self.temp_values
            else:
                filters = ''
            sql = 'UPDATE ' + table + ' SET ' + data + filters
            self.connect()
            try:
                self.cursor.execute(sql, values)
            except sqlite3.OperationalError as error:
                self.conn.rollback()
                del self.temp_values
                if out == 'output':
                    write("Error running SQL: %s" % (sql,))
                return 'SQL Error: %s' % error
            else:
                if out == 'output':
                    write("Successfully ran: %s" % (sql,))
                del self.temp_values
                # TODO Fix the last insert id
                # self.last_insert_id = self.cursor.lastrowid()
                self.conn.commit()
                self.cursor.close()
                return True
        else:
            raise NameError('Table not specified!')
    
    def delete(self, table=None, filters=None):
        """Deletes rows where given filters apply"""
        if filters is None:
            filters = {}
        if table is not None:
            filters = self._keys_to_sql(filters)
            sql = 'DELETE FROM ' + table + ' WHERE ' + filters
            self.connect()
            try:
                self.cursor.execute(sql, self.temp_values)
            except sqlite3.OperationalError as error:
                self.conn.rollback()
                del self.temp_values
                return 'SQL Error: %s' % error
            else:
                del self.temp_values
                self.conn.commit()
                self.cursor.close()
                return True
        else:
            raise NameError('Table not specified!')
    
    def count(self, table=None, filters=None):
        """Counts the rows based on the given filters"""
        if table is not None:
            # Construct the SQL
            sql = 'SELECT * FROM ' + table + ' WHERE ' 
            sql += self._keys_to_sql(filters)
            self.connect()
            try:
                self.cursor.execute(sql, self.temp_values)
            except sqlite3.OperationalError as error:
                self.conn.rollback()
                del self.temp_values
                return 'SQL Error: %s' % error
            else:
                # Cleanup and return
                del self.temp_values
                count = self.cursor.rowcount()
                self.cursor.close()
                if count < 0 or count is None:
                    count = 0
                return count
        else:
            raise NameError('Table not specified!')

def write(text):
    """Handle the output from the IRC bot"""
    text = str(text) + "\n"
    sys.stdout.write(text)
    sys.stdout.flush()
