
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(808, 648)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMaximumSize(QtCore.QSize(16777215, 556))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.listWidget = QtWidgets.QListWidget(self.tab)
        self.listWidget.setGeometry(QtCore.QRect(80, 110, 256, 200))
        self.listWidget.setObjectName("listWidget")
        self.tabWidget.addTab(self.tab, "")

        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.ComboBox = QtWidgets.QComboBox(self.tab_2)
        self.ComboBox.setGeometry(QtCore.QRect(40, 70, 86, 25))
        self.ComboBox.setObjectName("ComboBox")
        self.ButtonComboBox = QtWidgets.QPushButton(self.tab_2)
        self.ButtonComboBox.setGeometry(QtCore.QRect(40, 130, 89, 25))
        self.ButtonComboBox.setObjectName("ButtonComboBox")
        self.groupBox = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox.setGeometry(QtCore.QRect(320, 20, 441, 461))
        self.groupBox.setObjectName("groupBox")
        self.tabWidget.addTab(self.tab_2, "")


        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.pushButton_SQB = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_SQB.setGeometry(QtCore.QRect(20, 30, 211, 81))
        self.pushButton_SQB.setObjectName("SelectQueryButton")
        self.radioButN = QtWidgets.QRadioButton(self.tab_3)
        self.radioButN.setGeometry(QtCore.QRect(250, 40, 100, 15))
        self.radioButN.setObjectName("radioButN")
        self.radioButB = QtWidgets.QRadioButton(self.tab_3)
        self.radioButB.setGeometry(QtCore.QRect(250, 60, 150, 15))
        self.radioButB.setObjectName("radioButB")
        self.radioButM = QtWidgets.QRadioButton(self.tab_3)
        self.radioButM.setGeometry(QtCore.QRect(250, 80, 150, 15))
        self.radioButM.setObjectName("radioButM")
        self.tabWidget.addTab(self.tab_3, "")


        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 808, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RGZ_DB"))
        self.pushButton_SQB.setText(_translate("MainWindow", "Query"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Просмотр Таблиц"))
        self.ButtonComboBox.setText(_translate("MainWindow", "Select DB"))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Добавление Данных"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Выборка"))
        self.radioButN.setText(_translate("MainWindow", "Defolt"))
        self.radioButB.setText(_translate("MainWindow", "Цена >= 1000"))
        self.radioButM.setText(_translate("MainWindow", "Цена < 1000"))
