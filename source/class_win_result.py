# -*- coding: utf-8 -*-
__author__ = 'Admin'

from PyQt4 import QtGui, QtCore
import os, pickle
import MyGui

class ResultWindow(QtGui.QWidget):
    def __init__(self, dir, group, data_vote, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.resize(900, 400)

        self.dir = dir
        self.group = group
        self.data_vote = data_vote

        self.setWindowTitle(u'Результат - ' + self.group)

        self.result = []
        self.list_dir = []
        self.list_tab = []
        self.clients = []

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

        self.all_result()

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

    def all_result(self):
        self.result = []

        # формируем список по клиентам
        self.list_dir = os.listdir(self.dir)

        # формирование файла self.result
        # шагаем по количеству файлов в директории
        for i in range(len(self.list_dir)):
            if self.list_dir[i].count('.rea') > 0:
                self.file = open(self.dir + '\\' + self.list_dir[i], 'rb')
                self.unpacked = pickle.load(self.file)
                self.result.append(self.unpacked)
                self.file.close()

        print('Все результаты: ')
        for i in range(len(self.result)):
            print('Результат:')
            for j in range(len(self.result[i])):
                print(self.result[i][j])

        # формируем левые кнопки
        self.id = 0
        for i in range(len(self.list_dir)):
            if self.list_dir[i].count('.rea') > 0:
                self.list_buttons.append(QtGui.QPushButton(self.list_dir[i][:-4]))
                self.left_panel_buttons.addButton(self.list_buttons[self.id], self.id)
                self.left_vbox.addWidget(self.list_buttons[self.id])
                self.id += 1
        self.left_vbox.addStretch()

        # инициализация переменной self.clients
        file = open(self.dir + '\\' + 'client.ea', 'rb')
        self.clients = pickle.load(file)
        file.close()

        # формируем список табов
        self.list_tab = [] # список переменных с табами
        for i in range(len(self.result)):
            self.list_tab.append(MyGui.MyTabWidget(self.clients,
                                                   self.data_vote,
                                                   self.result[i]))

        self.calc_nepo()  # обработка непосредственного оценивания

        # обработка парного сравнения
        print('=============================Парное сравнение=================================')
        table = []
        for i in self.result:
            table.append(i[0])
        self.result_parn = MyGui.calc_parn(table, self.clients, self.data_vote)

        # обработка ранжирования
        self.calc_ranzh()

        self.calc_comp()

        self.init_interface_result()

    def calc_nepo(self):
        print('===============================Непосредственное оценивание=================================')
        # формирование списка-таблицы непосредственного оценивания
        table = []
        for i in range(len(self.clients)):
            table.append(self.result[i][1][1])
            print('Результат эксперта ', i+1, ': ', table[i])

        list_k0 = []  # список коэффициентов компетентности
        for i in range(len(self.clients)):
            list_k0.append(1 / len(self.clients))
        print('Список коэффициентов комп. на 0 шаге: ', list_k0)

        list_x = []  # список средних оценок первого шага
        for i in range(len(self.data_vote)):
            sum_ = 0
            for j in range(len(self.clients)):
                sum_ = sum_ + table[j][i]
            x = sum_ * list_k0[0]
            list_x.append(x)
        print('Список коэффициентов x для первого шага: ', list_x)

        # вычисляем нормировочный коэффициент
        lambda_ = 0
        for i in range(len(self.data_vote)):
            sum_ = 0
            for j in range(len(self.clients)):
                sum_ = sum_ + table[j][i]
            lambda_ = lambda_ + (list_x[i] * sum_)
        print('Коэффициент лямбда:      ', lambda_)

        # вычисляем коэффициенты компетентности первого шага
        list_k = []
        for i in range(len(self.clients) - 1):
            sum_ = 0
            for j in range(len(self.data_vote)):
                print('Коэффициент компететности :', i, table[i][j], list_x[j])
                sum_ = sum_ + (table[i][j] * list_x[j])
            if lambda_ != 0:
                list_k.append(1 / lambda_ * sum_)
            else:
                list_k.append(0)
        list_k.append(1 - sum(list_k))
        print('Коэффициенты компететности первого шага: ', list_k, 'Последний элемент с округлением ', round(list_k[-1:][0], 2))

        self.result_nepo = []
        self.result_nepo.append(list_x)

        # остальные шаги:
        for i in range(4):
            list_x = []
            # итерации по мероприятиям:
            for j in range(len(self.data_vote)):
                sum_ = 0
                for k in range(len(self.clients)):
                    sum_ = sum_ + table[k][j] * list_k[k]
                list_x.append(sum_)
            print('Список x на шаге ', i+1, ': ', list_x)

            # счет лямбды
            lambda_ = 0
            for j in range(len(self.data_vote)):
                sum_ = 0
                for k in range(len(self.clients)):
                    sum_ = sum_ + table[k][j]
                sum_ = sum_ * list_x[j]
                lambda_ = lambda_ + sum_
            print('Лямбда на шаге ', i+1, ': ', lambda_)

            # счет компетентности
            list_k = []
            for j in range(len(self.clients) - 1):
                sum_ = 0
                for k in range(len(self.data_vote)):
                    sum_ = sum_ + (table[j][k] * list_x[k])
                if lambda_ != 0:
                    list_k.append(sum_ / lambda_)
                else:
                    list_k.append(0)
            list_k.append(1 - sum(list_k))
            print('Коэф. комп. на шаге ', i+1, ': ', list_k)
            self.result_nepo.append(list_x)

        # печать всего результата
        print('ИТОГ: ')
        for i in self.result_nepo:
            print(i)

    def calc_ranzh(self):
        print('=============================Ранжирование=================================')

        # формируем список словарей
        list_dict = []
        print('Исходные словари экспертов')
        for i in range(len(self.result)):  # итерация по людям
            list_dict.append(self.result[i][2][0])

        for i in list_dict:
            print(i)

        table = []
        for i in range(len(self.clients)):
            table.append([])
            for a in range(len(self.data_vote)):
                table[i].append([])
                for b in range(len(self.data_vote)):
                    if list_dict[i][a] == list_dict[i][b]:
                        table[i][a].append(0.5)
                    elif list_dict[i][a] > list_dict[i][b]:
                        table[i][a].append(0.0)
                    elif list_dict[i][a] < list_dict[i][b]:
                        table[i][a].append(1.0)

        print('Созданные матрицы парных сравнений: ')
        for i in range(len(self.clients)):
            print(table[i])

        self.result_ranzh = MyGui.calc_parn(table, self.clients, self.data_vote)

    def calc_comp(self):
        print('===================Компетентность===================')
        table = []
        self.result_comp = []
        for i in self.result:
            table.append(i[3])
        print('Коэффициенты компетентности: ', table)
        self.result_comp.append(table)

        list_k0 = []
        self.result_comp.append([])
        for i in range(len(table)):
            list_k0.append(1.0)
        print('Список k0: ', list_k0)
        self.result_comp[1].append(list_k0)

        y = 0
        for i in range(len(table)):
            for j in range(len(table)):
                y = y + table[i][j]
        print('Y: ',y)

        list_k = []
        for i in range(len(table)):
            sum_ = 0
            for j in range(len(table)):
                sum_ = sum_ + table[j][i] * list_k0[j]
            if y != 0:
                list_k.append(sum_ / y)
            else:
                list_k.append(0.0)
        print('list_k: ', list_k)
        self.result_comp[1].append(list_k)

        # итерация по шагам
        for k in range(3):
            print('Шаг ', k + 1)
            y = 0
            for i in range(len(table)):
                for j in range(len(table)):
                    y = y + table[j][i] * list_k[j]
            print('y: ', y)

            list_k_next = []
            for i in range(len(table)):
                sum_ = 0
                for j in range(len(table)):
                    sum_ = sum_ + table[j][i] * list_k[j]
                if y != 0:
                    list_k_next.append(sum_ / y)
                else:
                    list_k_next.append(0.0)
            list_k = list_k_next
            self.result_comp[1].append(list_k)
            print('k: ', list_k)

            print('Все результаты: ')
            for i in self.result_comp:
                print(i)

    def init_interface_result(self):
        self.tab_all_result = MyGui.MyTabWidgetResult(self.result_nepo,
                                                      self.result_parn,
                                                      self.result_ranzh,
                                                      self.result_comp,
                                                      self.clients,
                                                      self.data_vote)
        file = open(self.dir + '//' + 'result.aea', 'wb')
        bufer = []
        bufer.append(self.group)
        bufer.append(self.clients)
        bufer.append(self.data_vote)
        bufer.append(self.result)
        bufer.append(self.result_nepo)
        bufer.append(self.result_parn)
        bufer.append(self.result_ranzh)
        bufer.append(self.result_comp)
        pickle.dump(bufer, file)
        file.close()
        self.right_vbox.addWidget(self.tab_all_result)