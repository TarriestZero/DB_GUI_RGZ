import sqlite3
import os


class DBWorker:
    def __init__(self):
        self.db = sqlite3.connect('musicshop.db')
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def add(self):
        pass

    def dell(self):
        pass

    def sample_request(self):
        pass

    def show_all_table(self, t_name):
        request = "SELECT "
        head = self.get_column_name(t_name)
        for row in head[:len(head) - 1]:
            request = request + "[%s], " % row
        request = request + "[%s] " % head[len(head) - 1] + "FROM " + t_name
        self.cursor.execute(request)
        try:
            buf = self.cursor.fetchall()
            return buf, head    #[heading[0] for heading in self.cursor.description]
        except:
            print("Нет записей")

    def get_column_name(self, t_name):
        self.cursor.execute("SELECT * FROM %(n)s" % {'n': t_name})
        return [heading[0] for heading in self.cursor.description]

    def get_name_all_tables(self):
        buf = ''
        self.cursor.execute("""SELECT name FROM sqlite_master
                                WHERE type='table' AND name != 'sqlite_sequence' 
                                """)
        return self.cursor.fetchall()