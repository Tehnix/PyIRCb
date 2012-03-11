class BotDatabase(threading.Thread):
    """Handles the database actions of the bot."""
    
    def __init__(self):
        self.sqldatabase = sqldatabase
        self.sqlcon = sqlite3.connect(self.sqldatabase)
        self.sqlcursor = self.sqlcon.cursor()
    
    def setupdatabase(self):
        """Sets up the initial database to be used for the bots information."""
        sqlcon = sqlite3.connect(self.sqldatabase)
        sqlcursor = sqlcon.cursor()
        sqlcursor.execute('CREATE TABLE IF NOT EXISTS admins (id INTEGER PRIMARY KEY, username VARCHAR(250), password VARCHAR(250))')
        sqlcursor.execute('CREATE TABLE IF NOT EXISTS settings (id VARCHAR(250), nickname VARCHAR(250), hostname VARCHAR(250), port VARCHAR(250), channels VARCHAR(250))')
        sqlcursor.execute('CREATE TABLE IF NOT EXISTS bookcase (id INTEGER PRIMARY KEY, nickname VARCHAR(250), book_name VARCHAR(250), book_link VARCHAR(250))')
        sqlcursor.execute('CREATE TABLE IF NOT EXISTS tutorials (id INTEGER PRIMARY KEY, nickname VARCHAR(250), tut_name VARCHAR(250), tut_link VARCHAR(250))')
        sqlcursor.execute('CREATE TABLE IF NOT EXISTS tools (id INTEGER PRIMARY KEY, nickname VARCHAR(250), tool_name VARCHAR(250), tool_link VARCHAR(250))')
        sqlcursor.execute('CREATE TABLE IF NOT EXISTS requests (id INTEGER PRIMARY KEY, nickname VARCHAR(250), req_name VARCHAR(250), req_catagory VARCHAR(250))')
        sqlcon.commit()
        sqlcursor.close()
        sqlcon.close()
    
    def get_db(self,*hilight):
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM settings)')
        if self.sqlcursor.fetchone()[0] == 0:
            print "\n\nNo settings has been saved yet !\n\n"
        else:
            print "\n\n"
            print "     ,----,,----------------------,,---------------------------,,----------,,---------------------------------------,"
            print "     | id ||       Nickname       ||          Hostname         ||   port   ||              channels                 |"
            print "     '----''----------------------''---------------------------''----------''---------------------------------------'"
            self.sqlcursor.execute('SELECT * FROM settings')
            for row in self.sqlcursor:
                x = "     "
                if hilight:
                    if row[0] == hilight[0]:
                        x = "---> "
                print x+"| %s ||    %s    ||      %s     ||  %s  ||         %s          |" % (row[0].center(2), row[1].center(14), row[2].center(16), row[3].center(6), row[4].center(20),)
                print "     '----''----------------------''---------------------------''----------''---------------------------------------'"
            print "\n\n"
        self.sqlcursor.close()
        self.sqlcon.close()
    
    def set_db(self, db_id, nickname, hostname, port, channels):
        search_query = [db_id]
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM settings WHERE id=?)', search_query)
        if self.sqlcursor.fetchone()[0] == 0:
            insertquery = [db_id, nickname, hostname, port, channels]
            self.sqlcursor.execute('INSERT INTO settings VALUES (?,?,?,?,?)', insertquery)
            self.sqlcon.commit()
            print "\n\nSetting has been added."
            self.get_db(db_id)
        else:
            updatequery = [nickname, hostname, port, channels, db_id]
            self.sqlcursor.execute('UPDATE settings SET nickname=?, hostname=?, port=?, channels=? WHERE id=?', updatequery)
            self.sqlcon.commit()
            print "\n\nSetting has been updated !"
            self.get_db(db_id)
    
    def clear_db(self):
        self.sqlcursor.execute('TRUNCATE TABLE settings')
        print "\n\nCleared database !\n\n"
        self.sqlcon.commit()
        self.sqlcursor.close()
        self.sqlcon.close()
    
    def del_id(self, db_id):
        search_query = [db_id]
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM settings WHERE id=?)', search_query)
        if self.sqlcursor.fetchone()[0] == 0:
            print "\n\nNo setting with id: %s !\n\n" % db_id
        else:
            delete_query = [db_id]
            self.sqlcursor.execute('DELETE FROM settings WHERE id=?', delete_query)
            self.sqlcon.commit()
            print "\n\nDeleted setting with id %s.\n\n" % db_id
        self.sqlcursor.close()
        self.sqlcon.close()
    
    def database_addbook(self, sock, recipient, reply_type, nickname, book_name, book_link):
        # Check if the tutorial has already been added (to avoid duplicates)
        search_query = [book_name]
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM bookcase WHERE book_name=?)', search_query)
        if self.sqlcursor.fetchone()[0] == 0:
            insertquery = [nickname, book_name, book_link]
            self.sqlcursor.execute('INSERT INTO bookcase VALUES (null,?,?,?)', insertquery)
            self.sqlcon.commit()
            send_text = "Book %s has been added under the catagory %s with the link %s" % (book_name, book_link,)
        else:
            send_text = "Seems as though this book has already been added"
        sock.send("%s %s :%s\r\n" % (reply_type, recipient, send_text))
        self.sqlcursor.close()
        self.sqlcon.close()
    
    def database_getbooks(self, sock, recipient, reply_type):
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM bookcase)')
        if self.sqlcursor.fetchone()[0] == 0:
            sock.send("%s %s :Nothing here yet !\r\n" % (reply_type, recipient))
        else:
            send_text = []
            # Get list of requests and add them to list object send_text
            self.sqlcursor.execute('SELECT * FROM bookcase')
            for row in self.sqlcursor:
                send_text.append("Book: %s (%s) from %s (id:%s)" % (row[2], row[3], row[1], row[0],))
            # Now for each item in send_text, send with speed depending on how many there are (avoid flooding).
            for text in send_text:
                sock.send("%s %s :%s\r\n" % (reply_type, recipient, text))
                if 10 < len(send_text):
                    time.sleep(1)
                else:
                    time.sleep(0.5)
            self.sqlcursor.close()
            self.sqlcon.close()
    
    def database_addtut(self, sock, recipient, reply_type, nickname, tut_name, tut_link):
        # Check if the tutorial has already been added (to avoid duplicates)
        search_query = [tut_name]
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM tutorials WHERE tut_name=?)', search_query)
        if self.sqlcursor.fetchone()[0] == 0:
            insertquery = [nickname, tut_name, tut_link]
            self.sqlcursor.execute('INSERT INTO tutorials VALUES (null,?,?,?)', insertquery)
            self.sqlcon.commit()
            send_text = "Tutorial %s has been added with the link %s" % (tut_name, tut_link,)
        else:
            send_text = "Seems as though this tutorial has already been added"
        sock.send("%s %s :%s\r\n" % (reply_type, recipient, send_text))
        self.sqlcursor.close()
        self.sqlcon.close()
    
    def database_gettuts(self, sock, recipient, reply_type):
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM tutorials)')
        if self.sqlcursor.fetchone()[0] == 0:
            sock.send("%s %s :Nothing here yet !\r\n" % (reply_type, recipient))
        else:
            send_text = []
            # Get list of requests and add them to list object send_text
            self.sqlcursor.execute('SELECT * FROM tutorials')
            for row in self.sqlcursor:
                send_text.append("Tut: %s (%s) from %s (id:%s)" % (row[2], row[3], row[1], row[0],))
            # Now for each item in send_text, send with speed depending on how many there are (avoid flooding).
            for text in send_text:
                sock.send("%s %s :%s\r\n" % (reply_type, recipient, text))
                if 10 < len(send_text):
                    time.sleep(1)
                else:
                    time.sleep(0.5)
            self.sqlcursor.close()
            self.sqlcon.close()
    
    def database_addtool(self, sock, recipient, reply_type, nickname, tool_name, tool_link):
        # Check if the tutorial has already been added (to avoid duplicates)
        search_query = [tool_name]
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM tools WHERE tool_name=?)', search_query)
        if self.sqlcursor.fetchone()[0] == 0:
            insertquery = [nickname, tool_name, tool_link]
            self.sqlcursor.execute('INSERT INTO tools VALUES (null,?,?,?)', insertquery)
            self.sqlcon.commit()
            send_text = "Tool %s has been added with the link %s" % (tool_name, tool_link,)
        else:
            send_text = "Seems as though this tool has already been added"
        sock.send("%s %s :%s\r\n" % (reply_type, recipient, send_text))
        self.sqlcursor.close()
        self.sqlcon.close()
    
    def database_gettools(self, sock, recipient, reply_type):
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM tools)')
        if self.sqlcursor.fetchone()[0] == 0:
            sock.send("%s %s :Nothing here yet !\r\n" % (reply_type, recipient))
        else:
            send_text = []
            # Get list of requests and add them to list object send_text
            self.sqlcursor.execute('SELECT * FROM tools')
            for row in self.sqlcursor:
                send_text.append("Tool: %s (%s) from %s (id:%s)" % (row[2], row[3], row[1], row[0],))
            # Now for each item in send_text, send with speed depending on how many there are (avoid flooding).
            for text in send_text:
                sock.send("%s %s :%s\r\n" % (reply_type, recipient, text))
                if 10 < len(send_text):
                    time.sleep(1)
                else:
                    time.sleep(0.5)
            self.sqlcursor.close()
            self.sqlcon.close()
    
    def database_addrequest(self, sock, recipient, reply_type, nickname, req_name, req_catagory):
        # Check if the request has already been made (to avoid duplicates)
        search_query = [req_name]
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM requests WHERE req_name=?)', search_query)
        if self.sqlcursor.fetchone()[0] == 0:
            insertquery = [nickname, req_name, req_catagory]
            self.sqlcursor.execute('INSERT INTO requests VALUES (null,?,?,?)', insertquery)
            self.sqlcon.commit()
            send_text = "Request %s has been added under the catagory %s" % (req_name, req_catagory,)
        else:
            send_text = "Sorry, a request has already been made for this tutorial."
        sock.send("%s %s :%s\r\n" % (reply_type, recipient, send_text))
        self.sqlcursor.close()
        self.sqlcon.close()
    
    def database_getrequests(self, sock, recipient, reply_type):
        self.sqlcursor.execute('SELECT count(*) > 0 FROM (SELECT * FROM requests)')
        if self.sqlcursor.fetchone()[0] == 0:
            sock.send("%s %s :Nothing here yet !\r\n" % (reply_type, recipient))
        else:
            send_text = []
            # Get list of requests and add them to list object send_text
            self.sqlcursor.execute('SELECT * FROM requests')
            for row in self.sqlcursor:
                send_text.append("%s requested tutorial about %s under catagory %s (id:%s)" % (row[1], row[2], row[3], row[0],))
            # Now for each item in send_text, send with speed depending on how many there are (avoid flooding).
            for text in send_text:
                sock.send("%s %s :%s\r\n" % (reply_type, recipient, text))
                if 10 < len(send_text):
                    time.sleep(1)
                else:
                    time.sleep(0.5)
            self.sqlcursor.close()
            self.sqlcon.close()
    
    def database_deleteitem(self, sock, recipient, reply_type, table, id):
        delete_query = [id]
        if table == "bookcase":
            self.sqlcursor.execute('DELETE FROM bookcase WHERE id=?', delete_query)
        elif table == "tutorials":
            self.sqlcursor.execute('DELETE FROM tutorials WHERE id=?', delete_query)
        elif table == "tools":
            self.sqlcursor.execute('DELETE FROM tools WHERE id=?', delete_query)
        elif table == "requests":
            self.sqlcursor.execute('DELETE FROM requests WHERE id=?', delete_query)
        self.sqlcon.commit()
        sock.send("%s %s :Deleted item with id %s from %s\r\n" % (reply_type, recipient, id, table))
        self.sqlcursor.close()
        self.sqlcon.close()
