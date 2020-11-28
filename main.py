import DB_Worker
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
import design
import dialog
import table
import sys


def printf(item):
    print('vibor:' + str(item.text()))


def show_table(item):  # Создание диалогового окна с таблицей
    DialogWindow = QtWidgets.QDialog()
    DialogWindow.resize(1000, 1000)
    DialogWindow.setWindowTitle("Dialog")
    table = QtWidgets.QTableWidget(DialogWindow)
    db = DB_Worker.DBWorker()
    buf, head = db.show_all_table(str(item.text()))
    table.resize(500, 500)
    table.setColumnCount(len(buf[0]))
    table.setRowCount(len(buf))
    table.setHorizontalHeaderLabels(head)
    # --- данные из DB заполняеи в таблицу диалога
    row = 0
    for tup in buf:
        col = 0
        for item in tup:
            cellinfo = QtWidgets.QTableWidgetItem(str(item))
            table.setItem(row, col, cellinfo)
            col += 1
        row += 1

    DialogWindow.setWindowModality(QtCore.Qt.ApplicationModal)
    DialogWindow.exec_()


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()

        self.req_LineEdit = list()   # Заполняемые строки для запросов
        self.req_label = list()     # Названия полей заполнения для запросов


        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        db = DB_Worker.DBWorker()
        tables = db.get_name_all_tables()
        for row in tables:
            self.listWidget.addItem(str(row[0]))


        # -- Кнопки
        self.ButtonComboBox.clicked.connect(lambda: self.create_item_request())
        # -- Лист таблиц
        self.listWidget.itemClicked.connect(show_table)

        self.init_combobox()

    def init_combobox(self):
        db = DB_Worker.DBWorker()
        tables = db.get_name_all_tables()
        for row in tables:
            self.ComboBox.addItem(str(row[0]))

    def check_text_in_LineEdit(self):
        msg = self.lineEdit.text()
        print(msg)
        self.lineEdit.clear()

    # -------------- Создание и работа с GroupBox запросами в DB

    def create_item_request(self):
        self.__del_last_but__()
        self.req_button = QtWidgets.QPushButton(self.groupBox)  # Кнопка для проведения запроса
        y = 80
        t_name = str(self.ComboBox.currentText())
        self.req_button.clicked.connect(lambda: self.request(t_name))
        db = DB_Worker.DBWorker()
        buf, head = db.show_all_table(t_name)
        for i in range(len(head)):
            label_in_group = QtWidgets.QLabel(self.groupBox)
            line_in_group = QtWidgets.QLineEdit(self.groupBox)
            label_in_group.setGeometry(QtCore.QRect(100, y, 150, 40))
            line_in_group.setGeometry(QtCore.QRect(200, y, 150, 40))
            label_in_group.setObjectName("LabelForReq")
            line_in_group.setObjectName("LineForReq")
            label_in_group.setText(head[i])
            line_in_group.show()
            label_in_group.show()
            self.req_LineEdit.append(line_in_group)
            self.req_label.append(label_in_group)
            y += 45
        self.req_button.setGeometry(QtCore.QRect(150, y + 50, 150, 40))
        self.req_button.setText("Request")
        self.req_button.setObjectName("ReqButton")
        self.req_button.show()

    def request(self, t_name):
        req = dict()
        i = 0
        for row in self.req_LineEdit:
            req[self.req_label[i].text()] = row.text()
            row.clear()
            i += 1
        for row in list(req.items()):
            if row[1] == "":
                req.pop(row[0])
        db = DB_Worker.DBWorker()
        tf, info = db.check_type(t_name, req)
        if tf:
            db.request_combobox(t_name, req)
        else:

            DialogWindow = QtWidgets.QDialog()
            setupwin = dialog.Ui_Dialog()
            setupwin.setupUi(DialogWindow)
            setupwin.retranslateUi(DialogWindow, "error in %(d)s need %(i)s" % {'d': str(info[1]), 'i': str(info[2])})
            DialogWindow.setWindowModality(QtCore.Qt.ApplicationModal)
            DialogWindow.exec_()


    def __del_last_but__(self):
        try:
            for row in self.req_LineEdit:
                row.deleteLater()
            for row in self.req_label:
                row.setText("")
                row.deleteLater()
            self.req_label.clear()
            self.req_LineEdit.clear()
            self.req_button.deleteLater()
        except:
            pass

    # ---------------

    def add_in_db(self):
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()
