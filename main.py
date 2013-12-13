# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui  # подключает основные модули PyQt
from ui import mainform, errorform  # подключает модуль описания формы


def main():
    app = QtGui.QApplication(sys.argv)  # создаёт основной объект программы
    try:
        form = mainform.MainForm()  # создаёт объект формы
        form.show()  # даёт команду на отображение объекта формы и содержимого
    except Exception, e:
        error_form = errorform.ErrorForm()
        error_form.l_error.setText(u"%s" % e)
        error_form.show()
    app.exec_()  # запускает приложение

if __name__ == "__main__":
    sys.exit(main())
