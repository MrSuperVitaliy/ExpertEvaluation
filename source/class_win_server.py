# coding: utf-8
__author__ = 'Admin'

from PyQt4 import QtGui, QtCore
import class_win_select_data, class_win_client, class_win_enter_data, class_win_result, MyGui
import pickle, os
import class_win_result_client

class ServerWidget(QtGui.QWidget):
    def __init__(self, parent):
        self.parent = parent
        QtGui.QWidget.__init__(self, parent)

        self.button_open_data = QtGui.QPushButton(u'Открыть данные с носителя', self)
        self.button_enter_data = QtGui.QPushButton(u'Ввести данные')
        self.button_work_folder = QtGui.QPushButton(u'Рабочая папка')
        self.button_phone = QtGui.QPushButton(u'Телефон')
        self.button_operator = QtGui.QPushButton(u'Оператор')
        self.button_cuisine = QtGui.QPushButton(u'Кухня')  # кухня
        self.button_sform_group = QtGui.QPushButton(u'Сформировать группу')
        self.button_check_result = QtGui.QPushButton(u'Обработать результаты')
        self.button_open_dump = QtGui.QPushButton(u'Открыть архив')
        self.label_text = QtGui.QLabel(u'Таблица:')
        self.button_send = QtGui.QPushButton(u'Отправить')
        self.button_result = QtGui.QPushButton(u'Результат', self)

        self.dir = ''  # пустой путь к рабочей папке
        self.data_vote = ''
        self.change_ranzh_var = {'index': -1, 'isClick': False}
        self.ranzh_list_buttons = []
        self.ranzh_list_labels = []
        self.name = []
        self.group = []
        self.way_file_result = ''
        self.was_normalization = False
        self.result_nepo = []
        self.list_client = []  # список всех клиентов

        # настройка компоновщиков
        #   объявление:
        self.mainhbox = QtGui.QHBoxLayout()
        self.left_vbox = QtGui.QVBoxLayout()
        self.right_vbox = QtGui.QVBoxLayout()
        self.tab = QtGui.QTabWidget()
        self.frame_parn = QtGui.QFrame()  # фрейм на tab для парного оценивания
        self.frame_nepo = QtGui.QFrame()  # фрейм на tab для непосредственного оценивания
        self.frame_ranzh = QtGui.QFrame()  # фрейм на tab для ранжирования
        self.frame_comp = QtGui.QFrame()  # фрейм на tab для компетентности
        self.btn_hbox = QtGui.QHBoxLayout()
        self.table_box = QtGui.QHBoxLayout()
        self.nepo_box = QtGui.QVBoxLayout()
        self.ranzh_box = QtGui.QHBoxLayout()
        self.comp_box = QtGui.QHBoxLayout()
        self.grid_ranzh = QtGui.QGridLayout()  # сетка для ранжирования
        self.group_box_default = QtGui.QGroupBox(u'Тема:')  # панель с предустановленными вариантами
        self.vbox_default = QtGui.QVBoxLayout()  # сетка для кнопками заданий по умолчанию
        self.group_buttons_ranzh = QtGui.QButtonGroup()  # группа для объединения кнопок на вкладке ранжирования

        #   инициализация:
        # нижний hbox с кнопками
        self.btn_hbox.addStretch()
        self.btn_hbox.addWidget(self.button_result)
        self.btn_hbox.addWidget(self.button_send)

        # кнопки по умолчанию
        self.vbox_default.addWidget(self.button_phone)
        self.vbox_default.addWidget(self.button_operator)
        self.vbox_default.addWidget(self.button_cuisine)
        self.group_box_default.setLayout(self.vbox_default)

        # правый hbox: tab, на табе фреймы, панель с кнопками
        self.right_vbox.addWidget(self.tab)
        self.frame_parn.setLayout(self.table_box) # добавить Layout с qframe
        self.frame_nepo.setLayout(self.nepo_box)
        self.frame_ranzh.setLayout(self.ranzh_box)
        self.frame_comp.setLayout(self.comp_box)
        self.ranzh_box.addLayout(self.grid_ranzh)
        self.tab.addTab(self.frame_parn, u'Парное сравнение')
        self.tab.addTab(self.frame_nepo, u'Непосредственная оценка')
        self.tab.addTab(self.frame_ranzh, u'Ранжирование')
        self.tab.addTab(self.frame_comp, u'Компетентность')
        self.right_vbox.addLayout(self.btn_hbox)

        self.left_vbox.addWidget(self.group_box_default)
        # self.left_vbox.addWidget(self.button_select_data)
        self.left_vbox.addWidget(self.button_open_data)
        self.left_vbox.addWidget(self.button_enter_data)
        self.left_vbox.addWidget(self.button_work_folder)
        self.left_vbox.addWidget(self.button_sform_group)
        self.left_vbox.addWidget(self.button_check_result)
        self.left_vbox.addStretch()
        self.left_vbox.addWidget(self.button_open_dump)

        self.mainhbox.addLayout(self.left_vbox)
        self.mainhbox.addLayout(self.right_vbox)
        self.setLayout(self.mainhbox)

        # self.connect(self.button_select_data, QtCore.SIGNAL('clicked()'), self.click_select_data)
        self.connect(self.button_phone, QtCore.SIGNAL('clicked()'), self.click_phone)
        self.connect(self.button_operator, QtCore.SIGNAL('clicked()'), self.click_operator)
        self.connect(self.button_cuisine, QtCore.SIGNAL('clicked()'), self.click_cuisine)

        self.connect(self.button_open_data, QtCore.SIGNAL('clicked()'), self.click_open_data)
        self.connect(self.button_result, QtCore.SIGNAL('clicked()'), self.click_result)
        self.connect(self.button_send, QtCore.SIGNAL('clicked()'), self.click_send)
        self.connect(self.button_enter_data, QtCore.SIGNAL('clicked()'), self.click_enter_data)
        self.connect(self.button_work_folder, QtCore.SIGNAL('clicked()'), self.click_work_folder)

        self.connect(self.group_buttons_ranzh, QtCore.SIGNAL('buttonClicked(int)'), self.change_ranzh)  # привязываем

        self.connect(self.button_sform_group, QtCore.SIGNAL('clicked()'), self.sform_file_client)
        self.connect(self.button_check_result, QtCore.SIGNAL('clicked()'), self.click_check_result)
        self.connect(self.button_open_dump, QtCore.SIGNAL('clicked()'), self.open_dump)

        self.enter_name = MyGui.InputDialog()
        self.connect(self.enter_name, QtCore.SIGNAL('mysignal2'), self.init_names)
        self.enter_name.show()

    def init_names(self, data):
        self.name = data[0]
        self.group = data[1]
        self.ok = data[2]
        self.parent.statusBar().showMessage(self.name)

    def click_check_result(self):
        # парсит папку, открывает файл с расширением .rea
        # смотрит на первый элемент списка, True или False

        # БЛОК ОТКЛЮЧЕН ДЛЯ ТЕСТОВ
        flag1 = True
        for i in os.listdir(self.dir):  # получаем список файлов
            if flag1:
                if i.count('.rea') > 0:
                    self.file = open(self.dir + '\\' + i, 'rb')
                    self.file2 = pickle.load(self.file)
                    self.file.close()
                    flag1 = flag1 and self.file2
        if flag1:
            self.parent.statusBar().showMessage('Расчет результата...')
            self.click_result()
        else:
            self.parent.statusBar().showMessage('Нет всех результатов')
            print('Нет всех результатов')

    def sform_file_client(self):
        # функция должна парсить рабочий каталог на наличие файлов с именами, а затем составлять один файл client.ea
        self.list_files = os.listdir(self.dir)
        self.list_client = []
        for i in self.list_files:
            if i.count('.rea') > 0:
                self.list_client.append(i[:len(i)-4])
                print(i)
        self.file = open(self.dir + '\\' + 'client.ea', 'wb')
        # записываем в файл полученный список
        pickle.dump(self.list_client, self.file)  # list_client - файл со списком имен
        self.file.close()
        self.compet_tab()  # формирует интерфейс компетентности

    def open_dump(self):
        # функция должна загружать прошлые результаты оценок из файла
        filename = QtGui.QFileDialog.getOpenFileName(parent=self,
                                                     caption='Выберите файл',
                                                     filter='Result (*.aea)')
        if filename != '':
            file = open(filename, 'rb')
            data = pickle.load(file)
            file.close()
            self.class_win_result_client = class_win_result_client.ResultWindowClient(data)
            self.class_win_result_client.show()

    def compet_tab(self):
        # формируем таблицу экспертов на основе файла list_client
        if self.list_client == []:
            self.sform_file_client()
        if self.list_client != []:
            self.clearLayout(self.comp_box)
            self.table_comp = MyGui.TableExpert(self.list_client)
            self.comp_box.addWidget(self.table_comp)

    def click_open_data(self):
        self.filename = QtGui.QFileDialog.getOpenFileName(parent=self,
                                                          caption=u'Выберите файл',
                                                          filter=u'Text (*.txt)')
        if self.filename != u'':
            self.bufer = {u'name': u'',
                          u'fields': []}
            print(self.filename)
            self.file = open(self.filename, 'r')
            self.data = self.file.read()
            self.data = self.data.split('\n')
            self.bufer[u'name'] = self.data[0]
            self.bufer[u'fields'] = self.data[1:len(self.data)]
            self.on_mysignal(self.bufer)

    def click_enter_data(self):
        self.enter_data_window = class_win_enter_data.EnterDataWindow()
        self.connect(self.enter_data_window, QtCore.SIGNAL('enterdata'), self.on_mysignal)
        self.enter_data_window.show()

    def click_work_folder(self):
        print('Текущая папка ', QtCore.QDir.currentPath() + '\\Expert\\')
        self.dir = QtGui.QFileDialog.getExistingDirectory(parent=self,
                                                          directory=QtCore.QDir.currentPath()+'\\Expert\\')
        if self.dir != '':
            # сначала очищаем эту папку от возможных прошлых результатов
            for i in os.listdir(self.dir):
                if i.count('.rea') > 0 or i.count('.ea') > 0:
                    os.remove(self.dir + '\\' + i)

            # формируем файл клиента
            self.way_file_result = self.dir + '\\' + self.name + '.rea'  # формируем путь для результата
            self.file_result = open(self.way_file_result, 'wb')
            pickle.dump(False, self.file_result)
            self.file_result.close()
        self.parent.dir = self.dir
        print(self.dir)

    def click_phone(self):
        self.data_vote_1 = {u'name': u'Телефон',
                            u'fields': [u'Apple',
                                        u'YotaPhone',
                                        u'Samsung',
                                        u'Sony',
                                        u'Fly']}
        self.on_mysignal(self.data_vote_1)

    def click_operator(self):
        self.data_vote_2 = {u'name': u'Мобильный оператор',
                            u'fields': [u'Tele2',
                                        u'МТС',
                                        u'Билайн',
                                        u'Мегафон',
                                        u'Yota']}
        self.on_mysignal(self.data_vote_2)

    def click_cuisine(self):
        self.data_vote_3 = {u'name': u'Кухня',
                            u'fields': [u'Русская',
                                        u'Китайская',
                                        u'Французская',
                                        u'Тайская',
                                        u'Японская']}
        self.on_mysignal(self.data_vote_3)

    def click_send(self):
        result = QtGui.QMessageBox.question(self,
                                            u'Подтвердите отправку',
                                            u'Отправить результаты на сервер?',
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                            QtGui.QMessageBox.No)
        if result == QtGui.QMessageBox.Yes:

            print('Формирование результата...')
            # self.result = ''  # общий результат

            # результаты из ТАБЛИЦЫ
            self.result_table = self.table.get_list_buttons()

            # результаты из НЕПОСРЕДСТВЕННОГО ОЦЕНИВАНИЯ??? после нормализации???
            if not self.was_normalization:
                self.normalization()

            # результаты из РАНЖИРОВАНИЯ
            self.result_ranzh = {} # словарь "номер поля из self.data_vote - ранг"
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
                    self.result_ranzh[self.data_vote['fields'].index(self.ranzh_list_buttons[i].text())] = i+1
            else:  # если встречаются '~', то большие вычисления:
                for i in range(len(self.ranzh_list_buttons)):

                    if i == 0:  # если первый элемент

                        if self.ranzh_list_labels_text[i] == '>':  # это не связанный ранг
                            self.result_ranzh[self.data_vote['fields'].index(self.ranzh_list_buttons[i].text())] = i+1
                            print(self.ranzh_list_buttons[i].text(), i+1)
                        else:  # тогда это начало связанного ранга
                            self.index_svyaz_rang = i
                            self.nach_svyaz_rang = i+1
                            self.sum += self.nach_svyaz_rang
                            self.count += 1

                    elif i+1 == len(self.ranzh_list_buttons):  # если последний элемент

                        if self.ranzh_list_labels_text[i-1] == '>':  # это не связанный ранг
                            self.result_ranzh[self.data_vote['fields'].index(self.ranzh_list_buttons[i].text())] = i + 1
                            print(self.ranzh_list_buttons[i].text(), i + 1)
                        else:  # тогда это конец связанного ранга
                            self.sum += i+1
                            self.count += 1
                            self.svyz_rang = self.sum / self.count
                            for j in range(self.count):
                                self.result_ranzh[self.data_vote['fields'].index(self.ranzh_list_buttons[self.index_svyaz_rang].text())] = self.svyz_rang
                                print(self.ranzh_list_buttons[self.index_svyaz_rang].text(), self.svyz_rang)
                                self.nach_svyaz_rang += 1
                                self.index_svyaz_rang += 1
                            self.sum = 0
                            self.count = 0
                            self.svyz_rang = 0

                    else:  # это объект по середине

                        if self.ranzh_list_labels_text[i-1] == '>' and self.ranzh_list_labels_text[i] == '>':  # это не связанный ранг посередине
                            self.result_ranzh[self.data_vote['fields'].index(self.ranzh_list_buttons[i].text())] = i + 1
                            print(self.ranzh_list_buttons[i].text(), i + 1)
                        elif self.ranzh_list_labels_text[i-1] == '>' and self.ranzh_list_labels_text[i] == '~':  # это начало связанного ранга
                            self.index_svyaz_rang = i
                            self.nach_svyaz_rang = i + 1
                            self.sum += self.nach_svyaz_rang
                            self.count += 1
                        elif self.ranzh_list_labels_text[i-1] == '~' and self.ranzh_list_labels_text[i] == '~':  # связанный ранг посередине
                            self.sum += i+1
                            self.count += 1
                        elif self.ranzh_list_labels_text[i-1] == '~' and self.ranzh_list_labels_text[i] == '>':  # это конец связанного ранга
                            self.sum += i+1
                            self.count += 1
                            self.svyz_rang = self.sum / self.count
                            print('Sum ', self.sum, ', count ', self.count, ', svyz_rang', self.svyz_rang)
                            for j in range(self.count):
                                self.result_ranzh[self.data_vote['fields'].index(
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
            # self.very_result.append(True)
            self.very_result.append(self.result_table)
            self.very_result.append(self.result_nepo)
            self.very_result.append(self.result_ranzh_all)
            self.very_result.append(self.result_comp)
            self.file_result = open(self.way_file_result, 'wb')
            pickle.dump(self.very_result, self.file_result)
            self.file_result.close()

            # отключение кнопки "Отправить"
            self.button_send.setDisabled(True)

    def on_mysignal(self, a):

        self.button_send.setDisabled(False)
        self.was_normalization = False

        # при выборе нового задания результат предыдущего стирается из сетевого файла
        file = open(self.dir + '\\' + self.name + '.rea', 'wb')
        pickle.dump(False, file)
        file.close()

        self.data_vote = a
        self.data_vote = MyGui.few_line(self.data_vote)

        # self.label_text.setText(u'Таблица \'%s\':' % self.data_vote[u'name'])
        self.parent.setWindowTitle(u'Сервер' + u' - ' + self.data_vote[u'name'])

        # НАСТРОЙКА 1-ОЙ ВКЛАДКИ (ТАБЛИЦЫ)
        self.clearLayout(self.table_box)  # функция очистки контейнера от предыдущего задания
        self.table = MyGui.MyTable(len(self.data_vote[u'fields']),
                                   len(self.data_vote[u'fields']),
                                   self.data_vote)
        self.table_box.addWidget(self.table)


        # НАСТРОЙКА 2-ОЙ ВКЛАДКИ (НЕПОСРЕДСТВЕННОГО ОЦЕНИВАНИЯ)
        self.clearLayout(self.nepo_box)  # очистка layout
        self.nepo_list = []  # список с группами label-slider-label
        for i in self.data_vote[u'fields']:
            self.nepo_list.append(MyGui.MyGroupSlider(i))
            self.connect(self.nepo_list[len(self.nepo_list) - 1], QtCore.SIGNAL('valuechange'), self.change_sum_nepo)
            self.nepo_box.addLayout(self.nepo_list[len(self.nepo_list)-1])

        self.label_sum = QtGui.QLabel(u'0')
        self.nepo_box.addWidget(self.label_sum, alignment=QtCore.Qt.AlignRight)
        self.label_sum.setFixedWidth(40)
        self.button_norma = QtGui.QPushButton(u'Нормализовать')
        self.nepo_box.addWidget(self.button_norma, alignment=QtCore.Qt.AlignRight)
        self.connect(self.button_norma, QtCore.SIGNAL('clicked()'), self.normalization)


        # НАСТРОЙКА 3-ЕЙ ВКЛАДКИ (РАНЖИРОВАНИЕ)
        self.clearLayout(self.grid_ranzh)
        self.ranzh_list_buttons = []
        self.ranzh_list_labels = []
        self.count_widgets = 0
        for i in range(len(self.data_vote[u'fields'])):  # в i у нас индексы по количеству полей 'fields'
            self.ranzh_list_buttons.append(MyGui.MyButton(self.data_vote[u'fields'][i]))
            self.group_buttons_ranzh.addButton(self.ranzh_list_buttons[i], i)  # добавляем кнопку в группу кнопок
            self.grid_ranzh.addWidget(self.ranzh_list_buttons[i], 0, self.count_widgets)
            self.count_widgets += 1
            if i != len(self.data_vote[u'fields']) - 1:  # если элемент не последний, то после него нужен label
                self.ranzh_list_labels.append(MyGui.MyLabel(u'>'))
                self.grid_ranzh.addWidget(self.ranzh_list_labels[i], 0, self.count_widgets)
                self.count_widgets += 1
        print(self.grid_ranzh.columnCount())

        # посылка задания на сетевую папку
        if self.dir == '':
            self.click_work_folder()
        if self.dir != '':
            self.file_task = open(self.dir + '\\' + 'task.ea', 'wb')
            print(self.dir + '\\' + 'task.ea')
            pickle.dump(self.data_vote, self.file_task)
            self.file_task.close()

    def change_sum_nepo(self):  # изменяет label (сумма) на вкладке непосредственного оценивания
        self.sum = 0
        for i in self.nepo_list:
            self.sum += i.get_value() / 100
        self.label_sum.setText(str(round(self.sum,2)))

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

    def change_ranzh(self, index):
        print('Нажата кнопка ', index)
        if not self.change_ranzh_var['isClick']:  # если ранее клика не было, включаем клик
            self.font = QtGui.QFont()
            self.font.setBold(True)
            self.ranzh_list_buttons[index].setFont(self.font)
            self.change_ranzh_var.update({'index': index})
            self.change_ranzh_var.update({'isClick': True})
        elif self.change_ranzh_var['isClick'] & (index == self.change_ranzh_var['index']):  # если клик был по той же кнопке, то отключаем клик
            self.font = QtGui.QFont()
            self.font.setBold(False)
            self.ranzh_list_buttons[index].setFont(self.font)
            self.change_ranzh_var.update({'index': -1})
            self.change_ranzh_var.update({'isClick': False})
        elif self.change_ranzh_var['isClick'] & (index != self.change_ranzh_var['index']):  # если был клик по другой кнопке, то
            # формирование нового списка ranzh_list_buttons
            self.temp_var = []
            self.temp_var.extend(self.ranzh_list_buttons[:min(index, self.change_ranzh_var['index'])])  # в новый копируется начало списка до первого упоминаемого индекса
            if index < self.change_ranzh_var['index']:  # если элемент перемещается справа налево <-
                self.temp_var.append(self.ranzh_list_buttons[self.change_ranzh_var['index']])
                self.temp_var.extend(self.ranzh_list_buttons[index:self.change_ranzh_var['index']])
            elif index > self.change_ranzh_var['index']:  # если элемент перемещается слева направо ->
                self.temp_var.extend(self.ranzh_list_buttons[self.change_ranzh_var['index'] + 1:index + 1])
                self.temp_var.append(self.ranzh_list_buttons[self.change_ranzh_var['index']])
            self.temp_var.extend(self.ranzh_list_buttons[max(index+1, self.change_ranzh_var['index']+1):])


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

    def click_result(self):
        # эта процедура запуститься из процедуры click_check_result
        # в том случае, если во всех файлах стоит True
        self.window_result = class_win_result.ResultWindow(self.dir, self.group, self.data_vote['fields'])
        self.window_result.show()

    def update_grid_ranzh(self):
        # self.clearLayout(self.grid_ranzh)
        count_w = 0
        for i in range(len(self.ranzh_list_buttons)):  # в i у нас индексы по количеству полей 'fields'
            self.group_buttons_ranzh.setId(self.ranzh_list_buttons[i], i)  # присваем кнопке id, равное id по списку
            self.grid_ranzh.addWidget(self.ranzh_list_buttons[i], 0, count_w)
            count_w += 1
            if i != len(self.ranzh_list_buttons) - 1:  # если элемент не последний, то после него нужен label
                self.grid_ranzh.addWidget(self.ranzh_list_labels[i], 0, count_w)
                count_w += 1

    def clearLayout(self, layout):  # очистка контейнера с таблицей:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())

class ServerWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.window = ServerWidget(parent=self)
        self.setCentralWidget(self.window)
        self.setWindowTitle(u'Сервер')
        self.resize(900, 415)
        self.statusBar()
        self.statusBar().setMinimumWidth(700)
        self.dir = ''

    # Подтверждение закрытия окна
    def closeEvent(self, e):
        result = QtGui.QMessageBox.question(self,
                                            u'Подтверждение',
                                            u'Вы действительно хотите закрыть программу?',
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                            QtGui.QMessageBox.No)
        if result == QtGui.QMessageBox.Yes:
            if self.dir != '':
                for i in os.listdir(self.dir):
                    if i.count('.rea') > 0 or i.count('.ea') > 0:
                        os.remove(self.dir + '\\' + i)
            e.accept()
            QtGui.QWidget.closeEvent(self, e)
        else:
            e.ignore()