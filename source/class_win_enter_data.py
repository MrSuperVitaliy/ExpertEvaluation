# -*- coding: utf-8 -*-
__author__ = 'Admin'

from PyQt4 import QtGui, QtCore

class EnterDataWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setWindowTitle(u'Ввод данных')
        self.setWindowModality(2)

        title = QtGui.QLabel(u'Введите данные:')
        self.edit = QtGui.QTextEdit()
        button = QtGui.QPushButton(u'Ввести')

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 0, 0)
        grid.addWidget(self.edit, 1, 0)
        grid.addWidget(button, 2, 0)
        self.setLayout(grid)
        self.resize(250, 200)

        self.connect(button,
                     QtCore.SIGNAL('clicked()'),
                     self.click_button)

    def click_button(self):
        self.bufer = self.edit.toPlainText()
        self.data_vote = {u'name': u'',
                          u'fields': []}
        data = self.bufer.split('\n')
        self.data_vote[u'name'] = data[0]
        self.data_vote[u'fields'] = data[1:]
        print(self.data_vote)
        self.emit(QtCore.SIGNAL('enterdata'), self.data_vote)
        self.close()