# -*- coding: utf-8 -*-
__author__ = 'Admin'

from PyQt4 import QtGui, QtCore

class SelectDataWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.data_vote_1 = {u'name': u'Выбор занятия',
                            u'fields': [u'На пару',
                                        u'В кино',
                                        u'В буфет']}

        self.data_vote_2 = {u'name': u'Объект',
                            u'fields': [u'Автомобильный завод',
                                        u'Завод холодильников',
                                        u'Кондитерская фабрика',
                                        u'Швейная фабрика']}
        self.data_vote_3 = {u'name': u'Проект',
                            u'fields': [u'Бесплатные разговоры',
                                        u'Подарки новым абонентам',
                                        u'Льготы за друзей',
                                        u'Телефоны в рассрочку',
                                        u'Бесплатный пакет звонков']}

        self.setFixedSize(300, 150)
        self.setWindowTitle(u'Выбор данных')
        self.setWindowModality(2)

        self.button1 = QtGui.QRadioButton(u'Набор данных \'Занятия\'')
        self.button2 = QtGui.QRadioButton(u'Набор данных \'Выбор объекта инвестирования\'')
        self.button3 = QtGui.QRadioButton(u'Набор данных \'Акция в мобильной связи\'')
        self.button_select = QtGui.QPushButton(u'Выбрать')

        # группировка радиокнопок
        group = QtGui.QButtonGroup()
        group.addButton(self.button1)
        group.addButton(self.button2)
        group.addButton(self.button3)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button_select)

        self.setLayout(layout)

        self.connect(self.button_select, QtCore.SIGNAL('clicked()'), self.click_select)

    def click_select(self):

        if self.button1.isChecked():
            self.emit(QtCore.SIGNAL('mysignal'), self.data_vote_1)  # было 1
            self.close()
        elif self.button2.isChecked():
            self.emit(QtCore.SIGNAL('mysignal'), self.data_vote_2)
            self.close()
        elif self.button3.isChecked():
            self.emit(QtCore.SIGNAL('mysignal'), self.data_vote_3)
            self.close()
        else:
            pass