import DB_Worker
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
import design
import dialog
import table
import json
import sys


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
    DialogWindow.setWindowTitle(str(item.text()))
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

        self.req_LineEdit = list()  # Заполняемые строки для запросов
        self.req_label = list()  # Названия полей заполнения для запросов
        self.req_ComboBox = list()  # комбобоксы для заполнения при запросе


        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        db = DB_Worker.DBWorker()
        tables = db.get_name_all_tables()
        for row in tables:
            self.listWidget.addItem(str(row[0]))

        self.ReqLine.setDisabled(True)
        self.ReqLineSale.setDisabled(True)
        self.pushButton_FIND.setDisabled(True)
        # -- Кнопки
        self.pushButton_SQB.clicked.connect(lambda: self.info_table_dialog())
        self.ButtonComboBox.clicked.connect(lambda: self.create_item_request())
        self.ComboBoxT3Tname.activated[str].connect(self.fill_combobox_column)
        self.ComboBoxT3Cname.activated[str].connect(self.activate_find)
        self.pushButton_FIND.clicked.connect(lambda: self.find_table())
        self.radioButSale.clicked.connect(lambda: self.set_name_sale())
        self.radioButSnot.clicked.connect(lambda: self.set_name_find())

        # -- Лист таблиц
        self.listWidget.itemClicked.connect(table_dialog)

        self.radioButSnot.setChecked(True)
        self.radioButN.setChecked(True)
        self.init_combobox()

        with open("package.json", "r") as read_file:
            self.conf = json.load(read_file)

    def init_combobox(self):
        db = DB_Worker.DBWorker()
        tables = db.get_name_all_tables()
        for row in tables:
            self.ComboBox.addItem(str(row[0]))
            self.ComboBoxT3Tname.addItem(str(row[0]))

    def set_name_sale(self):
        self.ReqLineSale.setDisabled(False)
        self.LabelLCinfo.setText("   Добавить скидку всем,\nкто удовлетворяет запросу")
        self.LabelLCinfo.setGeometry(QtCore.QRect(100, 20, 200, 50))
        self.pushButton_FIND.setText("Присвоить скидку")
        self.pushButton_FIND.setGeometry(QtCore.QRect(120, 220, 150, 50))

    def set_name_find(self):
        self.ReqLineSale.setDisabled(True)
        self.LabelLCinfo.setText("Текст для поиска")
        self.LabelLCinfo.setGeometry(QtCore.QRect(130, 20, 200, 50))
        self.pushButton_FIND.setText("Найти")
        self.pushButton_FIND.setGeometry(QtCore.QRect(140, 220, 100, 50))

    def available_id_inputted(self):
        if self.CheckBox.isChecked():
            self.req_LineEdit[0].setDisabled(False)
        else:
            self.req_LineEdit[0].setDisabled(True)

    def find_table(self):
        db = DB_Worker.DBWorker()
        if self.radioButSale.isChecked():
            try:
                int(self.ReqLineSale.text())
            except:
                error_dialog("Введите число в поле 'скидка'")
                return
            if 0 < int(self.ReqLineSale.text()) < 100:
                report = db.set_sale(str(self.ComboBoxT3Tname.currentText()),
                                     str(self.ComboBoxT3Cname.currentText()),
                                     str(self.ReqLine.text()),
                                     int(self.ReqLineSale.text())
                                     )
                error_dialog(report)
            else:
                error_dialog("Введите корректо значение скидка в %")
        else:
            buf, head = db.get_info_table_search(str(self.ComboBoxT3Tname.currentText()),
                                                 str(self.ComboBoxT3Cname.currentText()),
                                                 str(self.ReqLine.text()))
            if len(buf) == 0:
                error_dialog("Нет такой записи")
                return

            DialogWindow = QtWidgets.QDialog()
            DialogWindow.resize(1000, 1000)
            DialogWindow.setWindowTitle("Dialog")
            table = QtWidgets.QTableWidget(DialogWindow)
            table.resize(700, 500)
            table.setColumnCount(len(buf[0]) - 1)
            table.setRowCount(len(buf))
            table.setHorizontalHeaderLabels(head)
            row = 0
            for tup in buf:
                col = 0
                for item in tup[:len(tup) - 1]:
                    cellinfo = QtWidgets.QTableWidgetItem(str(item))
                    table.setItem(row, col, cellinfo)
                    col += 1
                row += 1

            DialogWindow.setWindowModality(QtCore.Qt.ApplicationModal)
            DialogWindow.exec_()

    def fill_combobox_column(self, table_name):
        self.ComboBoxT3Cname.clear()
        db = DB_Worker.DBWorker()
        buf, head = db.show_all_table(table_name)
        for row in head:
            if self.conf[table_name][0]["NotForSearch"].count(row) == 0:
                self.ComboBoxT3Cname.addItem(str(row))

    def activate_find(self):
        self.ReqLine.setDisabled(False)
        self.pushButton_FIND.setDisabled(False)

    def info_table_dialog(self):
        self.check_phone.isChecked()
        db = DB_Worker.DBWorker()
        buf, head = db.get_info_table(self.radioButB.isChecked(), self.radioButM.isChecked(),
                                      self.check_phone.isChecked(), self.check_date.isChecked())
        DialogWindow = QtWidgets.QDialog()
        DialogWindow.resize(1000, 1000)
        DialogWindow.setWindowTitle("Dialog")
        table = QtWidgets.QTableWidget(DialogWindow)
        table.resize(700, 500)
        table.setColumnCount(len(buf[0]))
        table.setRowCount(len(buf))
        table.setHorizontalHeaderLabels(head)
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

    # -------------- Создание и работа с GroupBox запросами в DB



    def create_item_request(self):
        self.__del_last_but__()
        self.req_button = QtWidgets.QPushButton(self.groupBox)  # Кнопка для проведения запроса
        y = 80
        t_name = str(self.ComboBox.currentText())
        self.req_button.clicked.connect(lambda: self.request(t_name))
        db = DB_Worker.DBWorker()
        buf, head = db.show_all_table(t_name)

        self.CheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.CheckBox.setGeometry(QtCore.QRect(380, y, 150, 40))
        self.CheckBox.setObjectName("CheckBoxForReq")
        self.CheckBox.clicked.connect(lambda: self.available_id_inputted())
        self.CheckBox.show()

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
        self.req_LineEdit[0].setDisabled(True)
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
                try:  # пытаемся удалить пустые строки из исключения
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

        error_dialog("Успех")

    def __del_last_but__(self):
        try:
            for row in self.req_LineEdit:
                row.deleteLater()
            for row in self.req_label:
                row.setText("")
                row.deleteLater()
            for row in self.req_ComboBox:
                row.deleteLater()

            self.CheckBox.deleteLater()
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
