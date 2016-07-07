# coding: utf-8
__author__ = 'Admin'

from PyQt4 import QtGui, QtCore
from functools import partial


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
        # self.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
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
        # шрифт
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.mouseReleaseEvent = self.change_value

    def change_value(self, event):
        if self.text() == '>':
            self.setText('~')
            print(u'Изменено на \'~\'')
        else:
            self.setText('>')
            print(u'Изменено на \'>\'')

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
        print(self.line_group.text())
        self.data = [self.line_name.text(), self.line_group.text()]
        if (self.label_name.text() != '') & (self.label_group.text() != ''):
            self.data.append(True)
        else:
            self.data.append(False)
        self.emit(QtCore.SIGNAL('mysignal2'), self.data)
        self.close()


class MainTab(QtGui.QWidget):
    def __init__(self):
        QtGui.QTabWidget.__init__(self)



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