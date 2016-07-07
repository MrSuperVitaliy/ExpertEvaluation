def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clear_layout(child.layout())


def few_line(data):  # функция для обрезки длинных строк
    for i in range(len(data[u'fields'])):
        if len(data[u'fields'][i]) > 13:  # если строка длинная
            index = data[u'fields'][i].find(' ', 4, 16)
            if index != -1:  # и если есть пробелы
                data[u'fields'][i] = data[u'fields'][i][0:index] + '\n' + data[u'fields'][i][index + 1:]
    return data