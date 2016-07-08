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
        bufer = self.edit.toPlainText()
        subjects = {u'name': u'',
                          u'fields': []}
        data = bufer.split('\n')
        subjects[u'name'] = data[0]
        subjects[u'fields'] = data[1:]
        self.emit(QtCore.SIGNAL('enterdata'), subjects)
        self.close()
