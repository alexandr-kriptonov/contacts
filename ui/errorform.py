# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, uic  # подключает основные модули PyQt

class ErrorForm(QtGui.QDialog):
    def __init__(self):
        super(ErrorForm, self).__init__()
        uic.loadUi("ui/errorform.ui", self)

    def set_text_error(self, header=u"ERROR!", message=u"LOL!"):
        self.l_error_header.setText(header)
        self.l_error.setText(message)
        print("good!")

