# -*- coding: utf-8 -*-
__author__ = 'Admin'

from PyQt4 import QtGui, QtCore
import pickle, my_gui
import result_client, os

class ClientWidget(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent

        # создание объектов
        self.label_text = QtGui.QLabel(u'Таблица:')
        self.button_work_folder = QtGui.QPushButton(u'Рабочая папка')
        self.button_read_task = QtGui.QPushButton(u'Загрузить задание')
        self.button_expert_group = QtGui.QPushButton(u'Загрузить группу')
        self.button_send = QtGui.QPushButton(u'Отправить', self)
        self.button_result = QtGui.QPushButton(u'Результат', self)

        self.dir = ''
        self.username = ''
        self.subjects = ''
        self.table_comp = None
        self.change_ranzh_var = {'index': -1, 'isClick': False}
        self.ranzh_list_buttons = []
        self.ranzh_list_labels = []
        self.way_file_result = ''
        self.was_normalization = False
        self.result_nepo = []

        # создание и настройка контейнеров
        self.mainbox = QtGui.QVBoxLayout()  # корневой layout
        self.tab = QtGui.QTabWidget()
        self.frame_parn = QtGui.QFrame()
        self.frame_nepo = QtGui.QFrame()
        self.frame_ranzh = QtGui.QFrame()
        self.frame_comp = QtGui.QFrame()
        self.table_box = QtGui.QHBoxLayout()
        self.nepo_box = QtGui.QVBoxLayout()
        self.ranzh_box = QtGui.QHBoxLayout()
        self.buttons_box = QtGui.QHBoxLayout()
        self.comp_box = QtGui.QHBoxLayout()
        self.grid_ranzh = QtGui.QGridLayout()
        self.group_buttons_ranzh = QtGui.QButtonGroup()  # группа для объединения кнопок на вкладке ранжирования

        #  нижние кнопки
        self.buttons_box.addWidget(self.button_work_folder)
        self.buttons_box.addWidget(self.button_read_task)
        self.buttons_box.addWidget(self.button_expert_group)
        self.buttons_box.addStretch()
        self.buttons_box.addWidget(self.button_result)
        self.buttons_box.addWidget(self.button_send)

        self.mainbox.addWidget(self.tab, stretch=0)
        self.mainbox.addLayout(self.buttons_box)

        self.frame_parn.setLayout(self.table_box)
        self.frame_nepo.setLayout(self.nepo_box)
        self.frame_ranzh.setLayout(self.ranzh_box)
        self.ranzh_box.addLayout(self.grid_ranzh)
        self.frame_comp.setLayout(self.comp_box)
        self.tab.addTab(self.frame_parn, u'Парное сравнение')
        self.tab.addTab(self.frame_nepo, u'Непосредственная оценка')
        self.tab.addTab(self.frame_ranzh, u'Ранжирование')
        self.tab.addTab(self.frame_comp, u'Компетентность')
        self.setLayout(self.mainbox)

        self.button_work_folder.clicked.connect(self.select_work_folder)
        self.button_result.clicked.connect(self.click_result)
        self.button_read_task.clicked.connect(self.click_read_task)
        self.button_send.clicked.connect(self.click_send)
        self.button_expert_group.clicked.connect(self.click_expert_group)

        self.connect(self.group_buttons_ranzh, QtCore.SIGNAL('buttonClicked(int)'), self.change_ranzh)  # привязываем

    def set_user_name(self, name):
        self.username = name
        print('Имя пользователя ', self.username)

    def click_expert_group(self):
        if self.dir == '':
            self.select_work_folder()
        if self.dir != '':
            self.file = open(self.dir + '\\' + 'client.ea', 'rb')
            self.list_client = pickle.load(self.file)  # list_client - список с именами
            self.file.close()
        self.compet_tab()

    def compet_tab(self):
        if self.list_client != []:
            self.clearLayout(self.comp_box)
        self.table_comp = my_gui.TableExpert(self.list_client)
        self.comp_box.addWidget(self.table_comp)

    def click_read_task(self):
        if self.dir == '':
            self.select_work_folder()
        if self.dir != '':
            file_task = open(self.dir + '\\' + 'task.ea', 'rb')
            result = pickle.load(file_task)
            print(result)
            self.set_subjects(result)
            file_task.close()
            # при выборе нового задания результат предыдущего стирается из сетевого файла
            file = open(self.dir + '\\' + self.username + '.rea', 'wb')
            pickle.dump(False, file)
            file.close()

    def select_work_folder(self):
        self.dir = QtGui.QFileDialog.getExistingDirectory(parent=self,
                                                          directory=QtCore.QDir.currentPath()+'\\Expert\\')
        if self.dir != '':
            self.way_file_result = self.dir + '\\' + self.username + '.rea'
            self.file_result = open(self.way_file_result, 'wb')
            pickle.dump(False, self.file_result)
            self.file_result.close()

        self.click_read_task()
        print(self.way_file_result)

    def click_result(self):
        if self.dir != '':
            if os.path.isfile(self.dir + '//' + 'result.aea'):
                file = open(self.dir + '//' + 'result.aea', 'rb')
                data = pickle.load(file)
                file.close()
                self.result_client = result_client.ResultWindowClient(data)
                self.result_client.show()

    def click_send(self):

        if not self.table_comp:
            self.show_tip('Не оценена компетентность группы!')
        result = QtGui.QMessageBox.question(self,
                                            u'Подтвердите отправку',
                                            u'Отправить результаты на сервер?',
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                            QtGui.QMessageBox.No)
        if result == QtGui.QMessageBox.Yes:

            print('Формирование результата...')
            # self.result = ''  # общий результат

            # результаты из таблицы
            self.result_table = self.table.get_list_buttons()

            # результаты из НЕПОСРЕДСТВЕННОГО ОЦЕНИВАНИЯ??? после нормализации???
            if not self.was_normalization:
                self.normalization()

            # результаты из РАНЖИРОВАНИЯ
            self.result_ranzh = {}  # словарь "номер поля из self.subjects - ранг"
            self.sum = 0
            self.count = 0
            self.var1 = []
            for i in range(len(self.ranzh_list_labels)):
                self.var1.append(self.ranzh_list_labels[i].text())
            self.ranzh_list_labels_text = self.var1
            print(self.ranzh_list_labels_text)

            # если все символы в label это '>', то
            if self.ranzh_list_labels_text.count('~') == 0:
                for i in range(len(self.ranzh_list_buttons)):
                    self.result_ranzh[self.subjects['fields'].index(self.ranzh_list_buttons[i].text())] = i + 1
            else:  # если встречаются '~', то большие вычисления:
                for i in range(len(self.ranzh_list_buttons)):

                    if i == 0:  # если первый элемент

                        if self.ranzh_list_labels_text[i] == '>':  # это не связанный ранг
                            self.result_ranzh[self.subjects['fields'].index(self.ranzh_list_buttons[i].text())] = i + 1
                            print(self.ranzh_list_buttons[i].text(), i + 1)
                        else:  # тогда это начало связанного ранга
                            self.index_svyaz_rang = i
                            self.nach_svyaz_rang = i + 1
                            self.sum += self.nach_svyaz_rang
                            self.count += 1

                    elif i + 1 == len(self.ranzh_list_buttons):  # если последний элемент

                        if self.ranzh_list_labels_text[i - 1] == '>':  # это не связанный ранг
                            self.result_ranzh[self.subjects['fields'].index(self.ranzh_list_buttons[i].text())] = i + 1
                            print(self.ranzh_list_buttons[i].text(), i + 1)
                        else:  # тогда это конец связанного ранга
                            self.sum += i + 1
                            self.count += 1
                            self.svyz_rang = self.sum / self.count
                            for j in range(self.count):
                                self.result_ranzh[self.subjects['fields'].index(
                                    self.ranzh_list_buttons[self.index_svyaz_rang].text())] = self.svyz_rang
                                print(self.ranzh_list_buttons[self.index_svyaz_rang].text(), self.svyz_rang)
                                self.nach_svyaz_rang += 1
                                self.index_svyaz_rang += 1
                            self.sum = 0
                            self.count = 0
                            self.svyz_rang = 0

                    else:  # это объект по середине

                        if self.ranzh_list_labels_text[i - 1] == '>' and self.ranzh_list_labels_text[
                            i] == '>':  # это не связанный ранг посередине
                            self.result_ranzh[self.subjects['fields'].index(self.ranzh_list_buttons[i].text())] = i + 1
                            print(self.ranzh_list_buttons[i].text(), i + 1)
                        elif self.ranzh_list_labels_text[i - 1] == '>' and self.ranzh_list_labels_text[
                            i] == '~':  # это начало связанного ранга
                            self.index_svyaz_rang = i
                            self.nach_svyaz_rang = i + 1
                            self.sum += self.nach_svyaz_rang
                            self.count += 1
                        elif self.ranzh_list_labels_text[i - 1] == '~' and self.ranzh_list_labels_text[
                            i] == '~':  # связанный ранг посередине
                            self.sum += i + 1
                            self.count += 1
                        elif self.ranzh_list_labels_text[i - 1] == '~' and self.ranzh_list_labels_text[
                            i] == '>':  # это конец связанного ранга
                            self.sum += i + 1
                            self.count += 1
                            self.svyz_rang = self.sum / self.count
                            print('Sum ', self.sum, ', count ', self.count, ', svyz_rang', self.svyz_rang)
                            for j in range(self.count):
                                self.result_ranzh[self.subjects['fields'].index(
                                    self.ranzh_list_buttons[self.index_svyaz_rang].text())] = self.svyz_rang
                                print(self.ranzh_list_buttons[self.index_svyaz_rang].text(), self.svyz_rang)
                                self.nach_svyaz_rang += 1
                                self.index_svyaz_rang += 1
                            self.sum = 0
                            self.count = 0
                            self.svyz_rang = 0

            # доработка ранжирования
            self.result_ranzh_all = []
            self.result_ranzh_all.append(self.result_ranzh)
            self.buferA = []
            for i in range(len(self.ranzh_list_buttons)):
                self.buferA.append(self.ranzh_list_buttons[i].text())
            self.result_ranzh_all.append(self.buferA)
            self.result_ranzh_all.append(self.ranzh_list_labels_text)

            # результаты из КОМПЕТЕНТНОСТИ
            self.result_comp = self.table_comp.get_list_buttons()

            print('Результат парного сравнения:  ', self.result_table)
            print('Результат непоср. оценивания: ', self.result_nepo)
            print('Результат ранжирования:       ', self.result_ranzh_all)
            print('Результат компетентности:     ', self.result_comp)

            # отправка результатов на сервер
            self.very_result = []
            self.very_result.append(self.result_table)
            self.very_result.append(self.result_nepo)
            self.very_result.append(self.result_ranzh_all)
            self.very_result.append(self.result_comp)
            self.file_result = open(self.way_file_result, 'wb')
            pickle.dump(self.very_result, self.file_result)
            self.file_result.close()

            # отключение кнопки "Отправить"
            self.button_send.setDisabled(True)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())

    def set_subjects(self, a):

        self.button_send.setDisabled(False)
        self.was_normalization = False

        self.subjects = a
        self.subjects = my_gui.few_line(self.subjects)

        self.parent.setWindowTitle(u'Клиент' + u' - ' + self.subjects[u'theme'])

        # НАСТРОЙКА 1-ОЙ ВКЛАДКИ (ТАБЛИЦЫ)
        self.clearLayout(self.table_box)  # функция очистки контейнера от предыдущего задания
        self.table = my_gui.MyTable(len(self.subjects[u'fields']),
                                   len(self.subjects[u'fields']),
                                   self.subjects)
        self.table_box.addWidget(self.table)

        # НАСТРОЙКА 2-ОЙ ВКЛАДКИ (НЕПОСРЕДСТВЕННОГО ОЦЕНИВАНИЯ)
        self.clearLayout(self.nepo_box)  # очистка layout
        self.nepo_list = []  # список с группами label-slider-label
        for i in self.subjects[u'fields']:
            self.nepo_list.append(my_gui.MyGroupSlider(i))
            self.connect(self.nepo_list[len(self.nepo_list) - 1], QtCore.SIGNAL('valuechange'), self.change_sum_nepo)
            self.nepo_box.addLayout(self.nepo_list[len(self.nepo_list) - 1])

        self.label_sum = QtGui.QLabel(u'0')
        self.nepo_box.addWidget(self.label_sum, alignment=QtCore.Qt.AlignRight)
        self.label_sum.setFixedWidth(30)
        self.button_norma = QtGui.QPushButton(u'Нормализовать')
        self.nepo_box.addWidget(self.button_norma, alignment=QtCore.Qt.AlignRight)
        self.connect(self.button_norma, QtCore.SIGNAL('clicked()'), self.normalization)

        # НАСТРОЙКА 3-ЕЙ ВКЛАДКИ (РАНЖИРОВАНИЕ)
        self.clearLayout(self.grid_ranzh)
        self.ranzh_list_buttons = []
        self.ranzh_list_labels = []
        self.count_widgets = 0
        for i in range(len(self.subjects[u'fields'])):  # в i у нас индексы по количеству полей 'fields'
            self.ranzh_list_buttons.append(my_gui.MyButton(self.subjects[u'fields'][i]))
            self.group_buttons_ranzh.addButton(self.ranzh_list_buttons[i], i)  # добавляем кнопку в группу кнопок
            self.grid_ranzh.addWidget(self.ranzh_list_buttons[i], 0, self.count_widgets)
            self.count_widgets += 1
            if i != len(self.subjects[u'fields']) - 1:  # если элемент не последний, то после него нужен label
                self.ranzh_list_labels.append(my_gui.MyLabel(u'>'))
                self.grid_ranzh.addWidget(self.ranzh_list_labels[i], 0, self.count_widgets)
                self.count_widgets += 1
        print(self.grid_ranzh.columnCount())

    def change_ranzh(self, index):
        print('Нажата кнопка ', index)
        if not self.change_ranzh_var['isClick']:  # если ранее клика не было, включаем клик
            self.font = QtGui.QFont()
            self.font.setBold(True)
            self.ranzh_list_buttons[index].setFont(self.font)
            self.change_ranzh_var.update({'index': index})
            self.change_ranzh_var.update({'isClick': True})
        elif self.change_ranzh_var['isClick'] & (
            index == self.change_ranzh_var['index']):  # если клик был по той же кнопке, то отключаем клик
            self.font = QtGui.QFont()
            self.font.setBold(False)
            self.ranzh_list_buttons[index].setFont(self.font)
            self.change_ranzh_var.update({'index': -1})
            self.change_ranzh_var.update({'isClick': False})
        elif self.change_ranzh_var['isClick'] & (
            index != self.change_ranzh_var['index']):  # если был клик по другой кнопке, то
            # формирование нового списка ranzh_list_buttons
            self.temp_var = []
            self.temp_var.extend(self.ranzh_list_buttons[:min(index, self.change_ranzh_var[
                'index'])])  # в новый копируется начало списка до первого упоминаемого индекса
            if index < self.change_ranzh_var['index']:  # если элемент перемещается справа налево <-
                self.temp_var.append(self.ranzh_list_buttons[self.change_ranzh_var['index']])
                self.temp_var.extend(self.ranzh_list_buttons[index:self.change_ranzh_var['index']])
            elif index > self.change_ranzh_var['index']:  # если элемент перемещается слева направо ->
                self.temp_var.extend(self.ranzh_list_buttons[self.change_ranzh_var['index'] + 1:index + 1])
                self.temp_var.append(self.ranzh_list_buttons[self.change_ranzh_var['index']])
            self.temp_var.extend(self.ranzh_list_buttons[max(index + 1, self.change_ranzh_var['index'] + 1):])

            # self.ranzh_list_buttons = []
            self.ranzh_list_buttons = self.temp_var

            # формирование нового списка ranzh_list_label ???
            if index - 1 != -1:
                self.ranzh_list_labels[index - 1].set_value()  # предыдущий индекс
            if index != len(self.ranzh_list_labels):
                self.ranzh_list_labels[index].set_value()  # следующий индекс
            if self.change_ranzh_var['index'] - 1 != -1:
                self.ranzh_list_labels[self.change_ranzh_var['index'] - 1].set_value()
            if self.change_ranzh_var['index'] != len(self.ranzh_list_labels):
                self.ranzh_list_labels[self.change_ranzh_var['index']].set_value()

            self.font = QtGui.QFont()
            self.font.setBold(False)
            self.ranzh_list_buttons[index].setFont(self.font)
            self.change_ranzh_var.update({'index': -1})
            self.change_ranzh_var.update({'isClick': False})

            print(len(self.ranzh_list_buttons))
            for i in self.ranzh_list_buttons:
                print(i.text())

            self.update_grid_ranzh()

    def update_grid_ranzh(self):
        count_w = 0
        for i in range(len(self.ranzh_list_buttons)):  # в i у нас индексы по количеству полей 'fields'
            self.group_buttons_ranzh.setId(self.ranzh_list_buttons[i], i)  # присваем кнопке id, равное id по списку
            self.grid_ranzh.addWidget(self.ranzh_list_buttons[i], 0, count_w)
            count_w += 1
            if i != len(self.ranzh_list_buttons) - 1:  # если элемент не последний, то после него нужен label
                self.grid_ranzh.addWidget(self.ranzh_list_labels[i], 0, count_w)
                count_w += 1

    def change_sum_nepo(self):  # изменяет label (сумма) на вкладке непосредственного оценивания
        self.sum = 0
        for i in self.nepo_list:
            self.sum += i.get_value() / 100
        self.label_sum.setText(str(round(self.sum, 2)))

    def normalization(self):
        print('Нормализация:')
        sum = 0

        local_list = []

        for i in self.nepo_list:
            local_list.append(i.get_value())
            sum += i.get_value() / 100  # возвращает значения всех слайдеров / 100
        print('Сумма ', sum)  # просто сумма всех чисел

        self.result_nepo = []
        self.result_nepo.append(local_list)
        self.result_nepo.append([])
        if sum != 0:
            for i in self.nepo_list:
                j = i.get_value() / 100 / sum
                i.set_label(round(j, 3))  # в label мы его округляем
                self.result_nepo[1].append(j)  # в переменной хранится длинное число
        else:
            for i in self.nepo_list:
                self.result_nepo[1].append(0.0)
        print(self.result_nepo)

        self.label_sum.setText('1')

        self.was_normalization = True

class ClientWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.window = ClientWidget(parent=self)
        self.setCentralWidget(self.window)
        self.setWindowTitle(u'Клиент')
        self.resize(700, 415)
        self.statusBar()
        self.statusBar().setMinimumWidth(550)
        self.name, self.ok = QtGui.QInputDialog.getText(self, u'Имя',
                                                     u'Введите ваше имя:')
        if self.ok:
            self.statusBar().showMessage(self.name)

        self.window.set_user_name(self.name)

    def closeEvent(self, e):
        result = QtGui.QMessageBox.question(self,
                                            u'Подтверждение',
                                            u'Вы действительно хотите закрыть программу?',
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                            QtGui.QMessageBox.No)
        if result == QtGui.QMessageBox.Yes:
            e.accept()
            quit()
        else:
            e.ignore()
