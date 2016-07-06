# coding: utf-8
__author__ = 'Admin'

from PyQt4 import QtGui
import sys, class_win_launcher

app = QtGui.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('icon.png'))

launcher = class_win_launcher.MainWindow()
launcher.show()

(sys.exit(app.exec_()))