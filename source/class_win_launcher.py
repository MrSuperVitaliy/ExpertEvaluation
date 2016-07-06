# coding: utf-8
__author__ = 'Admin'

from PyQt4 import QtGui, QtCore
import class_win_client, class_win_server, MyGui

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setFixedSize(350, 130)
        self.setWindowTitle(u'Методы экспертное оценивания')

        # кнопка "Клиентская часть"
        self.button_client = QtGui.QPushButton(u'Запустить как клиент', self)
        self.button_client.setGeometry(30, 20, 290, 40)
        # кнопка "Серверная часть"
        self.button_server = QtGui.QPushButton(u'Запустить как сервер', self)
        self.button_server.setGeometry(30, 70, 290, 40)
        # кнопка "О программе"
        # self.button_about = QtGui.QPushButton(u'О программе', self)
        # self.button_about.setGeometry(30, 120, 290, 40)

        self.connect(self.button_client, QtCore.SIGNAL('clicked()'), self.click_client)
        self.connect(self.button_server, QtCore.SIGNAL('clicked()'), self.click_server)
        # self.connect(self.button_about, QtCore.SIGNAL('clicked()'), self.click_about)

    def click_client(self):
        self.hide()
        self.client_window = class_win_client.ClientWindow()
        self.client_window.show()

    def click_server(self):
        self.hide()
        self.server_window = class_win_server.ServerWindow()
        self.server_window.show()

    def click_about(self):
        pass
        # self.hide()
        # self.about_window = about.AboutWindow()
        # self.about_window.show()