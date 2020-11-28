import DB_Worker
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
import design
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
        self.req_buttons = list()   # Копки создаваемые для запросов
        self.req_label = list()     # Названия полей заполнения для запросов
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        db = DB_Worker.DBWorker()
        tables = db.get_name_all_tables()
        for row in tables:
            self.listWidget.addItem(str(row[0]))


        # -- Кнопки
        self.pushButton_3.clicked.connect(lambda: self.check_text_in_LineEdit())
        self.ButtonComboBox.clicked.connect(lambda: self.create_item_request())
        # -- Лист таблиц
        self.listWidget.itemClicked.connect(show_table)

        self.init_combobox()

    def init_combobox(self):
        db = DB_Worker.DBWorker()
        tables = db.get_name_all_tables()
        for row in tables:
            self.ComboBox.addItem(str(row[0]))

    def check_combo(self):  # Проверяем выбранный текст в ComboBox
        msg = str(self.ComboBox.currentText())
        print(msg)

    def check_text_in_LineEdit(self):
        msg = self.lineEdit.text()
        print(msg)
        self.lineEdit.clear()

    # -------------- Создание и работа с GroupBox запросами в DB

    def create_item_request(self):
        self.__del_last_but__()
        y = 80
        msg = str(self.ComboBox.currentText())
        db = DB_Worker.DBWorker()
        buf, head = db.show_all_table(msg)
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
            self.req_buttons.append(line_in_group)
            self.req_label.append(label_in_group)
            y += 45

    def __del_last_but__(self):
        try:
            for row in self.req_buttons:
                row.deleteLater()
            for row in self.req_label:
                row.setText("")
                row.deleteLater()
            self.req_label.clear()
            self.req_buttons.clear()
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
