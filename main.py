# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui  # подключает основные модули PyQt
from ui import mainform  # подключает модуль описания формы
from ui.informform import MainDialog


def main():
    app = QtGui.QApplication(sys.argv)  # создаёт основной объект программы
    try:
        form = mainform.MainForm()  # создаёт объект формы
        form.show()  # даёт команду на отображение объекта формы и содержимого
    except Exception, e:
        error = MainDialog()
        error.show("error", "MAIN ERROR!", u"%s" % e.message)
    app.exec_()  # запускает приложение

if __name__ == "__main__":
    sys.exit(main())
