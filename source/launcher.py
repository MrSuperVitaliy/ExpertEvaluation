import client, server
from PyQt4 import QtGui, QtCore


class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setFixedSize(350, 140)
        self.setWindowTitle(u'Методы экспертное оценивания')

        self.button_client = QtGui.QPushButton(u'Запустить как клиент', self)
        self.button_client.setGeometry(30, 20, 290, 40)

        self.button_server = QtGui.QPushButton(u'Запустить как сервер', self)
        self.button_server.setGeometry(30, 70, 290, 40)

        self.label_about = QtGui.QLabel(u'Автор: Притула Виталий, ИСиТ-12 (2016 г.)', self)
        self.label_about.setGeometry(30, 120, 290, 20)

        self.connect(self.button_client, QtCore.SIGNAL('clicked()'), self.click_client)
        self.connect(self.button_server, QtCore.SIGNAL('clicked()'), self.click_server)

    def click_client(self):
        self.hide()
        client_ = client.ClientWindow()
        client_.show()

    def click_server(self):
        self.hide()
        server_ = server.ServerWindow()
        server_.show()
