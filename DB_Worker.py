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

    def request_combobox(self, t_name, data):   # Запрос в базу данных из groupbox
        reqin = "INSERT INTO [%s] (" % t_name
        reqval = "VALUES ("
        for row in list(data.items())[:len(data) - 1]:
            if row[1] != "":
                reqin = reqin + " [" + row[0] + "],"
                reqval = reqval + " '" + row[1] + "',"
        if list(data.items())[len(data) - 1][1] != "":
            reqin = reqin + " [" + list(data.items())[len(data) - 1][0] + "]"
            reqval = reqval + " '" + list(data.items())[len(data) - 1][1] + "'"
        else:
            reqin = reqin[:len(reqin) - 1]
            reqval = reqval[:len(reqval) - 1]
        reqin = reqin + ")"
        reqval = reqval + ")"
        print(reqin + " " + reqval)
        self.cursor.execute(reqin + " " + reqval)
        self.db.commit()

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