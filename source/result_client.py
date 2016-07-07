# -*- coding: utf-8 -*-
__author__ = 'Admin'

from PyQt4 import QtGui, QtCore
import os, pickle
import MyGui

class ResultWindowClient(QtGui.QWidget):
    def __init__(self, data, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.resize(900, 400)

        self.setWindowTitle(u'Результат - ' + data[0])

        self.bold = QtGui.QFont()
        self.bold.setBold(True)

        self.us_bold = QtGui.QFont()
        self.us_bold.setBold(False)

        # главный виджет
        self.mainbox = QtGui.QHBoxLayout()
        self.setLayout(self.mainbox)

        # левый и правый виджет
        self.left_vbox = QtGui.QVBoxLayout()  # виджет с кнопками
        self.right_vbox = QtGui.QVBoxLayout()

        self.left_panel_buttons = QtGui.QButtonGroup()  # группа для объединения кнопок на вкладке ранжирования
        self.connect(self.left_panel_buttons,
                     QtCore.SIGNAL('buttonClicked(int)'),
                     self.click_buttons)  # привязываем

        # кнопка результат
        self.buttons_result = QtGui.QPushButton(u'РЕЗУЛЬТАТ')
        self.buttons_result.setFont(self.bold)
        self.left_vbox.addWidget(self.buttons_result)

        # список объектов кнопок
        self.list_buttons = []

        self.mainbox.addLayout(self.left_vbox)
        self.mainbox.addLayout(self.right_vbox)

        self.group_buttons_ranzh = QtGui.QButtonGroup()  # группа для объединения кнопок на вкладке ранжирования

        self.connect(self.buttons_result, QtCore.SIGNAL('clicked()'), self.click_all_result)

        # формируем левые кнопки
        self.id = 0
        for i in data[1]:
            self.list_buttons.append(QtGui.QPushButton(i))
            self.left_panel_buttons.addButton(self.list_buttons[self.id], self.id)
            self.left_vbox.addWidget(self.list_buttons[self.id])
            self.id += 1
        self.left_vbox.addStretch()

        self.list_tab = []
        for i in range(len(data[3])):
            self.list_tab.append(MyGui.MyTabWidget(data[1],
                                                   data[2],
                                                   data[3][i]))

        self.tab_all_result = MyGui.MyTabWidgetResult(data[4],
                                                      data[5],
                                                      data[6],
                                                      data[7],
                                                      data[1],
                                                      data[2])

        self.right_vbox.addWidget(self.tab_all_result)

    def click_buttons(self, index):
        child = self.right_vbox.takeAt(0)
        child.widget().hide()
        for i in self.list_buttons:
            i.setFont(self.us_bold)
        self.buttons_result.setFont(self.us_bold)
        self.right_vbox.addWidget(self.list_tab[index])
        self.list_tab[index].show()
        self.list_buttons[index].setFont(self.bold)

    def click_all_result(self):
        child = self.right_vbox.takeAt(0)
        child.widget().hide()
        for i in self.list_buttons:
            i.setFont(self.us_bold)
        self.right_vbox.addWidget(self.tab_all_result)
        self.tab_all_result.show()
        self.buttons_result.setFont(self.bold)










