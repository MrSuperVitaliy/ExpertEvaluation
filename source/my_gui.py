# coding: utf-8
__author__ = 'Admin'

from PyQt4 import QtGui, QtCore
from functools import partial
from my_functions import *


class Combo(QtGui.QComboBox):
    def __init__(self):
        QtGui.QComboBox.__init__(self)
        self.addItem(u'0')  # было 0
        self.addItem(u'0.5')  # было 1
        self.addItem(u'1')  # было 2
        self.setCurrentIndex(1)


class SimpleTable(QtGui.QTableWidget):
    def __init__(self, data_vote, result):
        QtGui.QTableWidget.__init__(self, len(data_vote), len(data_vote))
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setSortingEnabled(False)  # отключение возможности сортировки
        self.setCornerButtonEnabled(False)  # отлючить выделение таблицы в левом верхнем углу
        self.setWordWrap(True)  # текст в ячейке может быть перенесен
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.setHorizontalHeaderLabels(data_vote)
        self.setVerticalHeaderLabels(data_vote)

        self.a = 0
        self.b = 0

        for self.a in range(len(data_vote)):
            for self.b in range(len(data_vote)):
                if self.a != self.b:
                    self.buferZ = QtGui.QLabel(str(result[self.a][self.b]))
                    self.buferZ.setAlignment(QtCore.Qt.AlignCenter)
                    if result[self.a][self.b] == 0:
                        self.buferZ.setStyleSheet('background-color: #E67575')
                    elif result[self.a][self.b] == 0.5:
                        self.buferZ.setStyleSheet('background-color: #C4C4C4')
                    elif result[self.a][self.b] == 1:
                        self.buferZ.setStyleSheet('background-color: #7FD4A8')
                    self.setCellWidget(self.a, self.b, self.buferZ)
                else:
                    self.setCellWidget(self.a, self.b, QtGui.QLabel(''))


class MyTable(QtGui.QTableWidget):
    def __init__(self, a, b, data_vote):
        QtGui.QTableWidget.__init__(self, a, b)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setSortingEnabled(False)  # отключение возможности сортировки
        self.setCornerButtonEnabled(False)  # отлючить выделение таблицы в левом верхнем углу
        self.setWordWrap(True)  # текст в ячейке может быть перенесен
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.setHorizontalHeaderLabels(data_vote[u'fields'])
        self.setVerticalHeaderLabels(data_vote[u'fields'])
        self.count_a = 0
        self.count_b = 0

        # Эксперимент с кнопками
        self.list_buttons = []
        for self.count_a in range(a):
            self.list_buttons.append([])
            for self.count_b in range(b):
                self.list_buttons[self.count_a].append(QtGui.QPushButton(u'0.5'))
                self.list_buttons[self.count_a][self.count_b].clicked.connect(partial(self.clicked, self.list_buttons, self.count_a, self.count_b))
                self.list_buttons[self.count_a][self.count_b].setStyleSheet('background-color: #C4C4C4;border: 2px')
                if self.count_a != self.count_b:
                    self.setCellWidget(self.count_a, self.count_b, self.list_buttons[self.count_a][self.count_b])
                elif self.count_a == self.count_b:
                    self.setCellWidget(self.count_a, self.count_b, QtGui.QLabel(u''))

    def clicked(self, list_button, a, b):
        if list_button[a][b].text() == u'0':
            list_button[a][b].setText(u'0.5')
            list_button[a][b].setStyleSheet('background-color: #C4C4C4;border: 1px')  # серый
            # list_button[a][b].setStyleSheet("font-size:40px;background-color:#333333;border: 2px solid #222222")
            list_button[b][a].setText(u'0.5')
            list_button[b][a].setStyleSheet('background-color: #C4C4C4;border: 1px')

        elif list_button[a][b].text() == u'0.5':
            list_button[a][b].setText(u'1')
            list_button[a][b].setStyleSheet('background-color: #7FD4A8;border: 1px')  # зеленый
            list_button[b][a].setText(u'0')
            list_button[b][a].setStyleSheet('background-color: #E67575;border: 1px')  # красный

        elif list_button[a][b].text() == u'1':
            list_button[a][b].setText(u'0')
            list_button[a][b].setStyleSheet('background-color: #E67575;border: 1px')  # красный
            list_button[b][a].setText(u'1')
            list_button[b][a].setStyleSheet('background-color: #7FD4A8;border: 1px')  # зеленый

    def get_list_buttons(self):
        self.result_table = []
        for i in self.list_buttons:
            self.bufer = []
            for j in i:
                self.bufer.append(float(j.text()))
            self.result_table.append(self.bufer)
        return self.result_table


class TableExpert(QtGui.QTableWidget):
    def __init__(self, list):
        QtGui.QTableWidget.__init__(self, len(list), 1)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setSortingEnabled(False)  # отключение возможности сортировки
        self.setCornerButtonEnabled(False)  # отлючить выделение таблицы в левом верхнем углу
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.horizontalHeader().hide()

        self.setVerticalHeaderLabels(list)
        self.list_buttons_expert = []
        self.count = 0
        for self.count in range(len(list)):
            self.list_buttons_expert.append(QtGui.QPushButton(u'0'))
            self.list_buttons_expert[self.count].clicked.connect(partial(self.clicked, self.list_buttons_expert, self.count))
            self.list_buttons_expert[self.count].setFixedWidth(80)
            self.list_buttons_expert[self.count].setStyleSheet('background-color: #E67575;border: 1px')  # красный
            self.setCellWidget(self.count, 0, self.list_buttons_expert[self.count])

    def clicked(self, list_button, i):
        if list_button[i].text() == '0':
            list_button[i].setText('1')
            list_button[i].setStyleSheet('background-color: #7FD4A8;border: 1px')  # зеленый

        elif list_button[i].text() == '1':
            list_button[i].setText('0')
            list_button[i].setStyleSheet('background-color: #E67575;border: 1px')  # красный

    def get_list_buttons(self):
        self.result_table = []
        for i in self.list_buttons_expert:
            self.result_table.append(int(i.text()))
        return self.result_table


class SimpleTableExpert(QtGui.QTableWidget):
    def __init__(self, clients, result):
        QtGui.QTableWidget.__init__(self, len(result), 1)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setSortingEnabled(False)  # отключение возможности сортировки
        self.setCornerButtonEnabled(False)  # отлючить выделение таблицы в левом верхнем углу
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.horizontalHeader().hide()

        self.setVerticalHeaderLabels(clients)

        for i in range(len(clients)):
            label = QtGui.QLabel(str(result[i]))
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setFixedWidth(80)
            if result[i] == 0:
                label.setStyleSheet('background-color: #E67575')
            else:
                label.setStyleSheet('background-color: #7FD4A8')
            self.setCellWidget(i, 0, label)


class ResultTable(QtGui.QTableWidget):
    def __init__(self, data, name_a, name_b, a, b):
        QtGui.QTableWidget.__init__(self, a, b)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setSortingEnabled(False)  # отключение возможности сортировки
        self.setCornerButtonEnabled(False)  # отлючить выделение таблицы в левом верхнем углу
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.setHorizontalHeaderLabels(name_a)
        self.setVerticalHeaderLabels(name_b)

        for i in range(len(data)):
            for j in range(len(data[i])):
                label = QtGui.QLabel(str(round(data[i][j], 3)))
                label.setAlignment(QtCore.Qt.AlignCenter)
                self.setCellWidget(i, j, label)


class ResultTableComp(QtGui.QTableWidget):
    def __init__(self, data, name_a, name_b, a, b):
        QtGui.QTableWidget.__init__(self, a, b)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setSortingEnabled(False)  # отключение возможности сортировки
        self.setCornerButtonEnabled(False)  # отлючить выделение таблицы в левом верхнем углу
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.setHorizontalHeaderLabels(name_a)
        self.setVerticalHeaderLabels(name_b)

        for i in range(len(data)):
            for j in range(len(data[i])):
                label = QtGui.QLabel(str(round(data[j][i], 3)))
                label.setAlignment(QtCore.Qt.AlignCenter)
                self.setCellWidget(i, j, label)


class MyTabWidgetResult(QtGui.QTabWidget):
    def __init__(self, nepo, parn, ranzh, comp, clients, data_vote):
        QtGui.QTabWidget.__init__(self)

        # вкладка парного сравнения
        self.frame_parn = QtGui.QFrame()
        self.box_parn = QtGui.QVBoxLayout()
        self.frame_parn.setLayout(self.box_parn)

        self.mat_ozh = ResultTable(parn[0], data_vote, data_vote, len(data_vote), len(data_vote))

        list = []
        for i in range(5):
            list.append(str(i))
        self.koef_otn = ResultTable(parn[1], data_vote, list, len(list), len(data_vote))

        self.button_change_parn = QtGui.QPushButton('Матрица математического ожидания')
        self.connect(self.button_change_parn, QtCore.SIGNAL('clicked()'), self.click_parn)
        self.flag_parn = 0

        self.box_parn.addWidget(self.mat_ozh)
        self.box_parn.addWidget(self.koef_otn)
        self.koef_otn.hide()
        self.box_parn.addWidget(self.button_change_parn)
        self.addTab(self.frame_parn, 'Групповая парная оценка')

        # вкладка непосредственного оценивания
        self.frame_nepo = QtGui.QFrame()
        self.box_nepo = QtGui.QHBoxLayout()
        self.frame_nepo.setLayout(self.box_nepo)

        self.nepo = ResultTable(nepo, data_vote, list, len(list), len(data_vote))
        self.box_nepo.addWidget(self.nepo)
        self.addTab(self.frame_nepo, 'Групповая непосредственная оценка')

        # вкладка ранжирования
        self.frame_ranzh = QtGui.QFrame()
        self.box_ranzh = QtGui.QVBoxLayout()
        self.frame_ranzh.setLayout(self.box_ranzh)
        self.ranzh_mat_ozh = ResultTable(ranzh[0], data_vote, data_vote, len(data_vote), len(data_vote))
        self.ranzh_koef_otn = ResultTable(ranzh[1], data_vote, list, len(list), len(data_vote))
        self.button_change_ranzh = QtGui.QPushButton('Матрица математического ожидания')
        self.connect(self.button_change_ranzh, QtCore.SIGNAL('clicked()'), self.click_ranzh)
        self.box_ranzh.addWidget(self.ranzh_mat_ozh)
        self.box_ranzh.addWidget(self.ranzh_koef_otn)
        self.ranzh_koef_otn.hide()
        self.box_ranzh.addWidget(self.button_change_ranzh)
        self.flag_ranzh = 0
        self.addTab(self.frame_ranzh, 'Обобщенная ранжировка')

        # вкладка компетентность
        self.frame_comp = QtGui.QFrame()
        self.box_comp = QtGui.QVBoxLayout()
        self.frame_comp.setLayout(self.box_comp)
        self.comp_tabl = ResultTableComp(comp[0], clients, clients, len(clients), len(clients))
        self.comp_koef = ResultTable(comp[1], clients, list, len(list), len(clients))
        self.button_change_comp = QtGui.QPushButton('Сводная таблица')
        self.connect(self.button_change_comp, QtCore.SIGNAL('clicked()'), self.click_comp)
        self.box_comp.addWidget(self.comp_tabl)
        self.box_comp.addWidget(self.comp_koef)
        self.comp_koef.hide()
        self.box_comp.addWidget(self.button_change_comp)
        self.flag_comp = 0
        self.addTab(self.frame_comp, 'Относительная компетентность')

    def click_parn(self):
        if self.flag_parn == 0:

            self.mat_ozh.hide()
            self.koef_otn.show()
            self.button_change_parn.setText('Матрица векторов относительной важности')
            self.flag_parn = 1
        elif self.flag_parn == 1:

            self.koef_otn.hide()
            self.mat_ozh.show()
            self.button_change_parn.setText('Матрица математических ожиданий')
            self.flag_parn = 0

    def click_ranzh(self):
        if self.flag_ranzh == 0:

            self.ranzh_mat_ozh.hide()
            self.ranzh_koef_otn.show()
            self.button_change_ranzh.setText('Матрица векторов относительной важности')
            self.flag_ranzh = 1
        elif self.flag_ranzh == 1:

            self.ranzh_koef_otn.hide()
            self.ranzh_mat_ozh.show()
            self.button_change_ranzh.setText('Матрица математических ожиданий')
            self.flag_ranzh = 0

    def click_comp(self):
        if self.flag_comp == 0:
            self.comp_tabl.hide()
            self.comp_koef.show()
            self.button_change_comp.setText('Коэффициенты компетентности')
            self.flag_comp = 1
        elif self.flag_comp == 1:
            self.comp_koef.hide()
            self.comp_tabl.show()
            self.button_change_comp.setText('Сводная таблица')
            self.flag_comp = 0


class MyTabWidget(QtGui.QTabWidget):
    def __init__(self, clients, data_vote, result):
        QtGui.QTabWidget.__init__(self)

        # вкладка парного сравнения
        self.frame_parn = QtGui.QFrame()
        self.box_parn = QtGui.QHBoxLayout()
        self.frame_parn.setLayout(self.box_parn)
        self.box_parn.addWidget(SimpleTable(data_vote, result[0]))  # [[0, 0, 0], [0, 1, 0], [1, 0, 0]]

        # вкладка непосредственного оценивания
        self.frame_nepo = QtGui.QFrame()
        self.box_nepo = QtGui.QVBoxLayout()
        self.frame_nepo.setLayout(self.box_nepo)
        for i in range(len(data_vote)):
            self.box_nepo.addLayout(SimpleGroupSlider(data_vote[i], result[1][0][i], result[1][1][i]))

        # вкладка ранжирования
        self.frame_ranzh = QtGui.QFrame()
        self.box_ranzh = QtGui.QGridLayout()
        self.frame_ranzh.setLayout(self.box_ranzh)
        self.count_widgets = 0
        for i in range(len(data_vote)):
            self.box_ranzh.addWidget(QtGui.QPushButton(result[2][1][i]), 0, self.count_widgets)
            self.count_widgets += 1
            if i != len(data_vote) - 1:
                x = QtGui.QLabel(result[2][2][i])

                font = QtGui.QFont()
                font.setPointSize(15)
                x.setFont(font)
                # шрифт
                x.setAlignment(QtCore.Qt.AlignCenter)

                self.box_ranzh.addWidget(x, 0, self.count_widgets)
                self.count_widgets += 1

        # вкладка компетентности
        self.frame_comp = QtGui.QFrame()
        self.box_comp = QtGui.QVBoxLayout()
        self.frame_comp.setLayout(self.box_comp)
        # при создании передаем clients и result[3]
        self.box_comp.addWidget(SimpleTableExpert(clients, result[3]))

        self.addTab(self.frame_parn, u'Парное сравнение')
        self.addTab(self.frame_nepo, u'Непосредственное оценивание')
        self.addTab(self.frame_ranzh, u'Ранжирование')
        self.addTab(self.frame_comp, u'Компетентность')


class SimpleGroupSlider(QtGui.QHBoxLayout):
    def __init__(self, data, source_value, calc_value):  # data - название одного поля; value
        QtGui.QHBoxLayout.__init__(self)
        self.name_label = QtGui.QLabel(data + ':')  # label с названием варианта выбора
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label.setFixedWidth(100)

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setSingleStep(5)
        self.slider.setTickPosition(QtGui.QSlider.TicksAbove)  # слайдер
        self.slider.setSliderPosition(source_value)

        self.value_label = QtGui.QLabel(str(round(calc_value, 3)))
        self.value_label.setAlignment(QtCore.Qt.AlignCenter)
        self.value_label.setFixedWidth(70)

        self.addWidget(self.name_label)
        self.addWidget(self.slider)
        self.addWidget(self.value_label)


class MyGroupSlider(QtGui.QHBoxLayout):
    def __init__(self, data):
        QtGui.QHBoxLayout.__init__(self)
        self.name_label = QtGui.QLabel(data + ':')  # label с названием варианта выбора
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label.setFixedWidth(100)

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setSingleStep(5)
        self.slider.setTickPosition(QtGui.QSlider.TicksAbove)  # слайдер

        self.value_label = QtGui.QLabel(u'0.0')
        self.value_label.setAlignment(QtCore.Qt.AlignCenter)
        self.value_label.setFixedWidth(70)

        self.addWidget(self.name_label)
        self.addWidget(self.slider)
        self.addWidget(self.value_label)

        self.slider.valueChanged.connect(self.set_value)

    def set_value(self):
        self.value_label.setText(str(self.slider.value() / 100))
        self.emit(QtCore.SIGNAL('valuechange'))

    # возможно нигде не используется
    def simple_set_value(self, value):
        self.value_label.setText(str(value))
        self.slider.setSliderPosition(value * 100)

    def get_value(self):
        return self.slider.value()

    def set_label(self, num):
        self.value_label.setText(str(num))


class MyButton(QtGui.QPushButton):
    def __init__(self, text):
        QtGui.QPushButton.__init__(self)
        self.setText(text)


class MyLabel(QtGui.QLabel):
    def __init__(self, text):
        QtGui.QLabel.__init__(self)
        self.setText(text)
        # шрифт
        self.font = QtGui.QFont()
        self.font.setPointSize(15)
        self.setFont(self.font)

        self.setAlignment(QtCore.Qt.AlignCenter)
        self.mouseReleaseEvent = self.change_value

    def change_value(self, event):
        if self.text() == '>':
            self.setText('~')
        else:
            self.setText('>')

    def set_value(self):
        self.setText('>')


class InputDialog(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setFixedSize(260, 150)
        self.setWindowTitle(u'Введите данные')
        self.setWindowModality(2)

        self.vbox = QtGui.QVBoxLayout()
        self.label_name = QtGui.QLabel(u'Введите имя и фамилию:')
        self.line_name = QtGui.QLineEdit()
        self.label_group = QtGui.QLabel(u'Введите группу:')
        self.line_group = QtGui.QLineEdit()
        # self.buttons_box = QtGui.QVBoxLayout()
        self.button_ok = QtGui.QPushButton(u'ОК')
        # self.button_cancel = QtGui.QPushButton(u'Отмена')

        self.vbox.addWidget(self.label_name)
        self.vbox.addWidget(self.line_name)
        self.vbox.addWidget(self.label_group)
        self.vbox.addWidget(self.line_group)
        self.vbox.addWidget(self.button_ok)
        self.setLayout(self.vbox)

        self.connect(self.button_ok, QtCore.SIGNAL('clicked()'), self.click)

    def click(self):
        print(self.line_name.text())
        data = [self.line_name.text(), self.line_group.text()]
        if (self.label_name.text() != '') & (self.label_group.text() != ''):
            data.append(True)
        else:
            data.append(False)
        self.emit(QtCore.SIGNAL('mysignal2'), data)
        self.close()


class MainTab(QtGui.QTabWidget):
    def __init__(self):
        QtGui.QTabWidget.__init__(self)

        self.frame_pair = QtGui.QFrame()  # фрейм на tab для парного оценивания
        self.frame_direct = QtGui.QFrame()  # фрейм на tab для непосредственного оценивания
        self.frame_ranging = QtGui.QFrame()  # фрейм на tab для ранжирования
        self.frame_competence = QtGui.QFrame()  # фрейм на tab для ранжирования

        self.box_pair = QtGui.QHBoxLayout()  # для таблицы
        self.box_direct = QtGui.QVBoxLayout()  # для непосредственной оценки
        # self.box_ranging = QtGui.QHBoxLayout()  # для ранжирования
        self.box_competence = QtGui.QHBoxLayout()  # для компетентности

        self.box_ranging = QtGui.QGridLayout()  # сетка для ранжирования

        self.group_buttons = QtGui.QButtonGroup()  # группа для кнопок на ранжировании
        self.connect(self.group_buttons, QtCore.SIGNAL('buttonClicked(int)'), self.click_buttons_ranging)

        self.frame_pair.setLayout(self.box_pair)
        self.frame_direct.setLayout(self.box_direct)
        self.frame_ranging.setLayout(self.box_ranging)
        self.frame_competence.setLayout(self.box_competence)

        self.addTab(self.frame_pair, u'Парное сравнение')
        self.addTab(self.frame_direct, u'Непосредственная оценка')
        self.addTab(self.frame_ranging, u'Ранжирование')
        self.addTab(self.frame_competence, u'Компетентность')

        self.direct_list = []  # список с MyGroupSlider
        self.result_direct = []
        self.was_normalization = False
        self.change_ranging = {'index': -1, 'isClick': False}
        self.subjects = []
        self.table_competence = None

    def init_subjects(self, subjects):
        """
        обновляет существующий tabwidget - изменяет поля
        """

        self.subjects = subjects

        # НАСТРОЙКА 1-ОЙ ВКЛАДКИ (ТАБЛИЦЫ)
        clear_layout(self.box_pair)
        self.table_pair = MyTable(len(subjects['fields']),
                             len(subjects['fields']),
                             subjects)
        self.box_pair.addWidget(self.table_pair)

        # НАСТРОЙКА 2-ОЙ ВКЛАДКИ (НЕПОСРЕДСТВЕННОГО ОЦЕНИВАНИЯ)
        clear_layout(self.box_direct)
        self.direct_list = []
        for i in subjects['fields']:
            self.direct_list.append(MyGroupSlider(i))
            self.connect(self.direct_list[len(self.direct_list) - 1],
                         QtCore.SIGNAL('valuechange'),
                         self.change_sum_direct)
            self.box_direct.addLayout(self.direct_list[len(self.direct_list) - 1])

        self.label_sum = QtGui.QLabel(u'0')
        self.box_direct.addWidget(self.label_sum, alignment=QtCore.Qt.AlignRight)
        self.label_sum.setFixedWidth(40)
        self.buttons_normalization = QtGui.QPushButton('Нормализовать')
        self.box_direct.addWidget(self.buttons_normalization, alignment=QtCore.Qt.AlignRight)
        self.connect(self.buttons_normalization,
                     QtCore.SIGNAL('clicked()'),
                     self.click_normalization)

        # НАСТРОЙКА ВКЛАДКИ РАНЖИРОВАНИЕ
        clear_layout(self.box_ranging)
        self.list_buttons_ranging = []
        self.list_labels_ranging = []
        count = 0
        for i in range(len(subjects['fields'])):  # в i у нас индексы по количеству полей 'fields'
            self.list_buttons_ranging.append(MyButton(subjects['fields'][i]))
            self.group_buttons.addButton(self.list_buttons_ranging[i], i)  # добавляем кнопку в группу кнопок
            self.box_ranging.addWidget(self.list_buttons_ranging[i], 0, count)
            count += 1
            if i != len(subjects['fields']) - 1:  # если элемент не последний, то после него нужен label
                self.list_labels_ranging.append(MyLabel('>'))
                self.box_ranging.addWidget(self.list_labels_ranging[i], 0, count)
                count += 1

    def change_sum_direct(self):  # изменяет label (сумма) на вкладке непосредственного оценивания
        sum = 0
        for i in self.direct_list:
            sum += i.get_value() / 100
        self.label_sum.setText(str(round(sum, 2)))

    def click_normalization(self):
        sum_ = 0

        local_list = []  # список исходных значений

        for i in self.direct_list:
            local_list.append(i.get_value())
            sum_ += i.get_value() / 100  # возвращает значения всех слайдеров / 100

        self.result_direct = []
        self.result_direct.append(local_list)
        self.result_direct.append([])
        z = 1
        if sum_ != 0:
            for i in range(len(self.direct_list) - 1):
                j = self.direct_list[i].get_value() / 100 / sum_
                z -= j
                self.direct_list[i].set_label(round(j, 3))  # в label мы его округляем
                self.result_direct[1].append(j)  # в переменной хранится неокругленное число
            self.direct_list[len(self.direct_list) - 1].set_label(round(z, 3))
            self.result_direct[1].append(z)
        else:
            for i in self.direct_list:
                self.result_direct[1].append(0.0)

        if sum_ != 0:
            self.label_sum.setText('1')

        self.was_normalization = True

    def click_buttons_ranging(self, index):
        if not self.change_ranging['isClick']:
            font = QtGui.QFont()
            font.setBold(True)
            self.list_buttons_ranging[index].setFont(font)
            self.change_ranging.update({'index': index})
            self.change_ranging.update({'isClick': True})

        # если клик был по той же кнопке, то отключаем клик
        elif self.change_ranging['isClick'] & index == self.change_ranging['index']:
            font = QtGui.QFont()
            font.setBold(False)
            self.list_buttons_ranging[index].setFont(font)
            self.change_ranging.update({'index': -1})
            self.change_ranging.update({'isClick': False})

        # если был клик по другой кнопке, то
        elif self.change_ranging['isClick'] & index != self.change_ranging['index']:
            temp = []
            # в новый копируется начало списка до первого упоминаемого индекса:
            temp.extend(self.list_buttons_ranging[:min(index, self.change_ranging['index'])])
            if index < self.change_ranging['index']:  # если элемент перемещается справа налево <-
                temp.append(self.list_buttons_ranging[self.change_ranging['index']])
                temp.extend(self.list_buttons_ranging[index:self.change_ranging['index']])
            elif index > self.change_ranging['index']:  # если элемент перемещается слева направо ->
                temp.extend(self.list_buttons_ranging[self.change_ranging['index'] + 1:index + 1])
                temp.append(self.list_buttons_ranging[self.change_ranging['index']])
            temp.extend(self.list_buttons_ranging[max(index + 1, self.change_ranging['index'] + 1):])

            self.list_buttons_ranging = temp

            # формирование нового списка ranzh_list_label ???
            if index - 1 != -1:
                self.list_labels_ranging[index - 1].set_value()  # предыдущий индекс
            if index != len(self.list_labels_ranging):
                self.list_labels_ranging[index].set_value()  # следующий индекс
            if self.change_ranging['index'] - 1 != -1:
                self.list_labels_ranging[self.change_ranging['index'] - 1].set_value()
            if self.change_ranging['index'] != len(self.list_labels_ranging):
                self.list_labels_ranging[self.change_ranging['index']].set_value()

            font = QtGui.QFont()
            font.setBold(False)
            self.list_buttons_ranging[index].setFont(font)
            self.change_ranging.update({'index': -1})
            self.change_ranging.update({'isClick': False})

            self.update_grid_ranging()

    def update_grid_ranging(self):
        count = 0
        for i in range(len(self.list_buttons_ranging)):  # в i у нас индексы по количеству полей 'fields'
            self.group_buttons.setId(self.list_buttons_ranging[i], i)  # присваем кнопке id, равное id по списку
            self.box_ranging.addWidget(self.list_buttons_ranging[i], 0, count)
            count += 1
            if i != len(self.list_buttons_ranging) - 1:  # если элемент не последний, то после него нужен label
                self.box_ranging.addWidget(self.list_labels_ranging[i], 0, count)
                count += 1

    def init_competence(self, clients):
        clear_layout(self.box_competence)
        self.table_competence = TableExpert(clients)
        self.box_competence.addWidget(self.table_competence)

    def formation_all_result(self):
        result = []
        result.append(self.formation_pair_result())
        result.append(self.formation_direct_result())
        result.append(self.formation_ranging_result())
        result.append(self.formation_competence_result())
        return result

    def formation_pair_result(self):
        return self.table_pair.get_list_buttons()

    def formation_direct_result(self):
        if not self.was_normalization:
            self.click_normalization()
        return self.result_direct

    def formation_ranging_result(self):
        result_ranging_extended = []
        result_ranging = {}  # словарь "номер поля из self.subjects - ранг"
        sum_ = 0
        count = 0
        temp = []
        for i in range(len(self.list_labels_ranging)):
            temp.append(self.list_labels_ranging[i].text())
        list_labels_text_ranging = temp

        # если все символы в label это '>', то
        if list_labels_text_ranging.count('~') == 0:

            for i in range(len(self.list_buttons_ranging)):
                result_ranging[self.subjects['fields'].index(self.list_buttons_ranging[i].text())] = i + 1

        else:  # если встречаются '~', то большие вычисления:
            for i in range(len(self.list_buttons_ranging)):

                # если первый элемент
                if i == 0:

                    # это не связанный ранг
                    if list_labels_text_ranging[i] == '>':
                        result_ranging[self.subjects['fields'].index(self.list_buttons_ranging[i].text())] = i + 1
                        print(self.list_buttons_ranging[i].text(), i + 1)

                    # иначе это начало связанного ранга
                    else:
                        index_linked_rank = i
                        start_linked_rank = i + 1
                        sum_ += start_linked_rank
                        count += 1

                elif i + 1 == len(self.list_buttons_ranging):  # если последний элемент

                    # это не связанный ранг
                    if list_labels_text_ranging[i - 1] == '>':
                        result_ranging[self.subjects['fields'].index(self.list_buttons_ranging[i].text())] = i + 1
                        print(self.list_buttons_ranging[i].text(), i + 1)

                    # тогда это конец связанного ранга
                    else:
                        sum_ += i + 1
                        count += 1
                        linked_rank = sum_ / count
                        for j in range(count):
                            result_ranging[self.subjects['fields'].index(self.list_buttons_ranging[index_linked_rank].text())] = linked_rank
                            print(self.list_buttons_ranging[index_linked_rank].text(), linked_rank)
                            start_linked_rank += 1
                            index_linked_rank += 1
                        sum_ = 0
                        self.count = 0
                        linked_rank = 0

                else:  # это объект по середине

                    # это не связанный ранг посередине
                    if (list_labels_text_ranging[i - 1] == '>') and \
                            (list_labels_text_ranging[i] == '>'):
                        result_ranging[self.subjects['fields'].index(self.list_buttons_ranging[i].text())] = i + 1
                        print(self.list_buttons_ranging[i].text(), i + 1)

                    # это начало связанного ранга
                    elif (list_labels_text_ranging[i - 1] == '>') and \
                            (list_labels_text_ranging[i] == '~'):
                        index_linked_rank = i
                        start_linked_rank = i + 1
                        sum_ += start_linked_rank
                        count += 1

                    # связанный ранг посередине
                    elif (list_labels_text_ranging[i - 1] == '~') and \
                            (list_labels_text_ranging[i] == '~'):
                        sum_ += i + 1
                        count += 1

                    # это конец связанного ранга
                    elif list_labels_text_ranging[i - 1] == '~' and \
                            (list_labels_text_ranging[i] == '>'):
                        sum_ += i + 1
                        count += 1
                        linked_rank = sum_ / count
                        for j in range(count):
                            result_ranging[self.subjects['fields'].index(
                                self.list_buttons_ranging[index_linked_rank].text())] = linked_rank
                            print(self.list_buttons_ranging[index_linked_rank].text(), linked_rank)
                            start_linked_rank += 1
                            index_linked_rank += 1
                        sum_ = 0
                        count = 0
                        linked_rank = 0

        # доработка ранжирования
        result_ranging_extended = []
        result_ranging_extended.append(result_ranging)
        temp = []
        for i in range(len(self.list_buttons_ranging)):
            temp.append(self.list_buttons_ranging[i].text())
        result_ranging_extended.append(temp)
        result_ranging_extended.append(list_labels_text_ranging)

        return result_ranging_extended

    def formation_competence_result(self):
        return self.table_competence.get_list_buttons()


def matrix(a, b):
    c = []
    for i in range(len(a)):
        sum_ = 0
        for j in range(len(a[i])):
            sum_ = sum_ + a[i][j] * b[j]
        c.append(sum_)
    return c


def calc_parn(table, clients, data_vote):
    # количество экспертов
    kol_vo_exp = len(clients)
    kol_vo_data = len(data_vote)

    # составляем матрицу мат ожиданий
    mat_ozh = []
    for i in range(kol_vo_data):
        mat_ozh.append([])
        for j in range(kol_vo_data):
            Oi = 0
            Oj = 0
            for k in range(kol_vo_exp):  # проход по количеству экспертов
                if table[k][i][j] == 1:
                    Oi = Oi + 1
                elif table[k][i][j] == 0:
                    Oj = Oj + 1
            mat_ozh[i].append(0.5 + (Oi - Oj) / (2 * kol_vo_exp))
    print('Матрица мат ожиданий: ')
    for i in mat_ozh:
        print(i)

    list_k0 = []
    for i in data_vote:
        list_k0.append(1.0)
    print('Матрица k0: ', list_k0)

    list_y = []
    list_y = matrix(mat_ozh, list_k0)
    print('Матрица Y: ', list_y)

    lambda_ = sum(list_y)
    print('Лямбда: ', lambda_)

    list_k = []
    for i in list_y:
        list_k.append(i / lambda_)
    print('Список коэффициентов k: ', list_k)

    result_parn = []
    result_parn.append(mat_ozh)
    result_parn.append([])
    result_parn[1].append(list_k)

    # остальные шаги
    for i in range(4):
        print('=========ШАГ ', i + 1)
        list_y = matrix(mat_ozh, list_k)
        print('Y: ', list_y)

        lambda_ = sum(list_y)
        print('Лямбда: ', lambda_)

        list_k = []
        for i in list_y:
            list_k.append(i / lambda_)
        print('Список коэф.: ', list_k)

        result_parn[1].append(list_k)

    print('ИТОГ: ')
    print('Матрица математических ожиданий: ', result_parn[0])
    print('Коэффициенты относительной важности: ', result_parn[1])

    return result_parn