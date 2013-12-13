# -*- coding: utf-8 -*-
from PySide import QtGui


class MainDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)

    def show(self, type_window=False, TITLE="TITLE", MESSAGE="MESSAGE!"):

        if not type_window:
            return False
        else:
            type_window = type_window.lower()
            if type_window in ("information", "inf"):
                result = self.informationMessage(TITLE, MESSAGE)
                return result
            elif type_window in ("error", "err", "critical", "crit"):
                result = self.criticalMessage(TITLE, MESSAGE)
                return result
            elif type_window in ("question", "qst"):
                result = self.questionMessage(TITLE, MESSAGE)
                return result
            elif type_window in ("warning", "warn"):
                result = self.warningMessage(TITLE, MESSAGE)
                return result
            else:
                return False

    def informationMessage(self, TITLE, MESSAGE):
        reply = QtGui.QMessageBox.information(
            self,
            TITLE,
            MESSAGE)
        if reply == QtGui.QMessageBox.Ok:
            return "ok"
        else:
            return "escape"

    def criticalMessage(self, TITLE, MESSAGE):
        reply = QtGui.QMessageBox.critical(
            self,
            TITLE,
            MESSAGE,
            QtGui.QMessageBox.Abort | QtGui.QMessageBox.Retry | QtGui.QMessageBox.Ignore)
        if reply == QtGui.QMessageBox.Abort:
            return "abort"
        elif reply == QtGui.QMessageBox.Retry:
            return "retry"
        else:
            return "ignore"

    def questionMessage(self, TITLE, MESSAGE):
        reply = QtGui.QMessageBox.question(
            self,
            TITLE,
            MESSAGE,
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel)
        if reply == QtGui.QMessageBox.Yes:
            return "yes"
        elif reply == QtGui.QMessageBox.No:
            return "no"
        else:
            return "cancel"

    def warningMessage(self, TITLE, MESSAGE):
        msgBox = QtGui.QMessageBox(
            QtGui.QMessageBox.Warning,
            TITLE,
            MESSAGE,
            QtGui.QMessageBox.NoButton,
            self)
        msgBox.addButton(QtGui.QMessageBox.Cancel)
        msgBox.addButton("&Continue", QtGui.QMessageBox.RejectRole)
        if msgBox.exec_() == QtGui.QMessageBox.Cancel:
            return "cancel"
        else:
            return "continue"
