import DB_Worker
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
import design
import table
import sys


def printf():
    print('sdfs')


def show_table():  # Создание диалогового окна с таблицей
    DialogWindow = QtWidgets.QDialog()
    DialogWindow.resize(1000, 1000)
    DialogWindow.setWindowTitle("Dialog")
    table = QtWidgets.QTableWidget(DialogWindow)
    db = DB_Worker.DBWorker()
    buf, head = db.show_all_table("Buyers")
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
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(lambda: show_table())


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()
