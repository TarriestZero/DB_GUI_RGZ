import sqlite3


class DBWorker:
    def __init__(self):
        self.db = sqlite3.connect('musicshop.db')
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def get_info_table_search(self, table, column, data):
        head = ["First Name", "Phone Number", "Orders.Date", "ProductName", "Price"]
        sql = """ 
                SELECT Buyers.[First Name], Buyers.[Phone Number], Orders.Date, Product.Name, Product.Price, Orders.OrdId
                FROM Buyers
                JOIN Orders ON Buyers.ClientId = Orders.ClientId
                JOIN Product ON Orders.ProdId = Product.ProdId
                 """
        sql = sql + " WHERE %(t)s.[%(c)s] = '%(f)s'" % {'t': table, 'c': column, 'f': data}
        self.cursor.execute(sql)
        return self.cursor.fetchall(), head

    def set_sale(self, tname, column, search, proc):
        buf, head = self.get_info_table_search(tname, column, search)
        del head
        if len(buf) != 0:
            for tup in buf:
                #sql = "UPDATE Orders SET Sale = " + str(proc / 100) + " WHERE OrdId = " + str(tup[len(tup) - 1:][0])
                sql = "UPDATE Orders SET Sale = %(p)s WHERE OrdId = %(i)s" \
                       % {'p': str(proc/100), 'i': str(tup[len(tup) - 1:][0])}

                self.cursor.execute(sql)
                self.db.commit()
            return "Успех"
        else:
            return "Нет записей, удовлетворяющих поиск"

    def get_info_table(self, B, M, Phone, Date):
        head = ["First Name"]
        select = "SELECT Buyers.[First Name], "
        if Phone:
            head.append("Phone Number")
            select += "Buyers.[Phone Number], "
        if Date:
            head.append("Date")
            select += "Orders.Date, "
        head.append("ProductName")
        head.append("Price")
        select += "Product.Name, Product.Price "
        sql = """
                FROM Buyers
                JOIN Orders ON Buyers.ClientId = Orders.ClientId
                JOIN Product ON Orders.ProdId = Product.ProdId
                 """
        sql = select + sql
        if B:
            sql = sql + " WHERE Product.Price >= 1000"
        if M:
            sql = sql + " WHERE Product.Price < 1000"
        self.cursor.execute(sql)
        return self.cursor.fetchall(), head

    def dell(self):
        pass

    def get_id(self, t_name, id_column, name_column, name):
        sql = ("SELECT [%(ic)s] FROM [%(t)s] WHERE [%(nc)s] = %(n)s" % {'ic': id_column,
                                                                        't': t_name,
                                                                        'nc': name_column,
                                                                        'n': "\"" + name + "\""}
               )
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    def get_only_one_table(self, t_name, data):
        self.cursor.execute("SELECT [%(d)s] FROM [%(t)s]" % {'d': data, 't': t_name})
        buf = list()
        for row in self.cursor.fetchall():
            buf.append(row)
        return buf

    def check_repeat(self, t_name, data, repeaters):  # поиск повторяющихся записей по конкретным полям
        for row in repeaters:
            sql = "SELECT count([%(r)s])>0 FROM [%(t)s] " \
                  "WHERE [%(r)s] = %(d)s" % {'r': row, 't': t_name, 'd': data[row]}
            self.cursor.execute(sql)
            g = self.cursor.fetchone()[0]
            if g == 1:
                return "Совпадает поле %(r)s" % {'r': row}
        return True

    def check_type(self, t_name, data):
        self.cursor.execute("PRAGMA table_info([%s])" % t_name)
        for row in self.cursor.fetchall():
            if row[2] == "INTEGER":
                try:
                    print(data[row[1]])
                    try:
                        int(data[row[1]])
                    except:
                        return False, row
                except:
                    pass
        return True, 0

    def check_not_null(self, t_name, data, encrem):
        self.cursor.execute("PRAGMA table_info([%s])" % t_name)
        for row in self.cursor.fetchall():
            if row[3] == 1 and not (row[1] in encrem):
                if data[row[1]] == "":
                    return False, "Not Null field: %s" % row[1]
        return True, 0

    def request_combobox(self, t_name, data):  # Запрос в базу данных из groupbox
        reqin = "INSERT INTO [%s] (" % t_name
        reqval = "VALUES ("
        for row in list(data.items())[:len(data)]:
            reqin = reqin + " [" + str(row[0]) + "],"
            reqval = reqval + " '" + str(row[1]) + "',"

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
            return buf, head  # [heading[0] for heading in self.cursor.description]
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
