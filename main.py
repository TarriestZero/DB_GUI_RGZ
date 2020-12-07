import DB_Worker
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
import design
import dialog
import table
import json
import sys


def printf(item):
    print('vibor:' + str(item.text()))


def error_dialog(text):
    DialogWindow = QtWidgets.QDialog()
    setupwin = dialog.Ui_Dialog()
    setupwin.setupUi(DialogWindow)
    setupwin.retranslateUi(DialogWindow, text)
    DialogWindow.setWindowModality(QtCore.Qt.ApplicationModal)
    DialogWindow.exec_()


def table_dialog(item):  # Создание диалогового окна с таблицей
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
        self.req_ComboBox = list()  # комбобоксы для заполнения при запросе

        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        db = DB_Worker.DBWorker()
        tables = db.get_name_all_tables()
        for row in tables:
            self.listWidget.addItem(str(row[0]))


        # -- Кнопки
        self.ButtonComboBox.clicked.connect(lambda: self.create_item_request())
        # -- Лист таблиц
        self.listWidget.itemClicked.connect(table_dialog)

        self.init_combobox()

        with open("package.json", "r") as read_file:
            self.conf = json.load(read_file)

    def init_combobox(self):
        db = DB_Worker.DBWorker()
        tables = db.get_name_all_tables()
        for row in tables:
            self.ComboBox.addItem(str(row[0]))



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
            if list(self.conf[t_name][0]["Drop-down_list"][0].keys()).count(head[i]):
                ComboBox = QtWidgets.QComboBox(self.groupBox)
                ComboBox.setGeometry(QtCore.QRect(200, y, 150, 40))
                ComboBox.setObjectName("ComboBoxForReq")
                lines = db.get_only_one_table(self.conf[t_name][0]["Drop-down_list"][0][head[i]][0],
                                              self.conf[t_name][0]["Drop-down_list"][0][head[i]][1])
                for row in lines:
                    ComboBox.addItem(row[0])

                ComboBox.show()
                self.req_ComboBox.append(ComboBox)
            else:
                line_in_group = QtWidgets.QLineEdit(self.groupBox)
                line_in_group.setGeometry(QtCore.QRect(200, y, 150, 40))
                line_in_group.setObjectName("LineForReq")
                line_in_group.show()
                self.req_LineEdit.append(line_in_group)

            label_in_group = QtWidgets.QLabel(self.groupBox)
            label_in_group.setGeometry(QtCore.QRect(100, y, 150, 40))
            label_in_group.setObjectName("LabelForReq")
            label_in_group.setText(head[i])
            label_in_group.show()
            self.req_label.append(label_in_group)
            y += 45
        self.req_button.setGeometry(QtCore.QRect(150, y + 50, 150, 40))
        self.req_button.setText("Request")
        self.req_button.setObjectName("ReqButton")
        self.req_button.show()

    def request(self, t_name):
        req = dict()
        i = 0
        db = DB_Worker.DBWorker()
        for row in self.req_LineEdit:
            req[self.req_label[i].text()] = row.text()
            row.clear()
            i += 1
        for row in self.req_ComboBox:
            req[self.req_label[i].text()] = db.get_id(
                    self.conf[t_name][0]["Drop-down_list"][0][self.req_label[i].text()][0],
                    self.req_label[i].text(),
                    self.conf[t_name][0]["Drop-down_list"][0][self.req_label[i].text()][1],
                    row.currentText())
            i += 1

        tf, info = db.check_not_null(t_name, req, self.conf[t_name][0]["AEncrem"])
        if not tf:
            error_dialog(info)
            return

        for row in list(req.items()):
            if row[1] == "":
                req.pop(row[0])
                try:    # пытаемся удалить пустые строки из исключения
                    self.conf[t_name][0]["Punisher"].remove(row[0])
                except:
                    pass

        tf, info = db.check_type(t_name, req)
        if tf:
            ttf = db.check_repeat(t_name, req, self.conf[t_name][0]["Punisher"])
            if ttf == True:
                db.request_combobox(t_name, req)
            else:
                error_dialog(ttf)
        else:
            error_dialog("error in %(d)s need %(i)s" % {'d': str(info[1]), 'i': str(info[2])})



    def __del_last_but__(self):
        try:
            for row in self.req_LineEdit:
                row.deleteLater()
            for row in self.req_label:
                row.setText("")
                row.deleteLater()
            for row in self.req_ComboBox:
                row.deleteLater()

            self.req_label.clear()
            self.req_LineEdit.clear()
            self.req_ComboBox.clear()
            self.req_button.deleteLater()
        except:
            pass

    # ---------------



def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()
