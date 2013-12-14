# -*- coding: utf-8 -*-
from PyQt4.QtCore import SIGNAL
from PyQt4 import QtCore


class AllSlots(object):
    """Action & his action"""
    def __init__(self):
        super(AllSlots, self).__init__()

    def connect_all_slots(self):
        self.connect_main_slots()
        self.connect_google_thread_slots()
        self.connect_add_db_thread_slots()

    def connect_google_thread_slots(self):
        self.connect(
            self.b_get_from_google,
            SIGNAL(
                "clicked()"),
            self.b_get_from_google_on_click)

        self.connect(
            self.google_thread,
            SIGNAL(
                "started()"),
            self.google_thread_on_started)

        self.connect(
            self.google_thread,
            SIGNAL(
                "finished()"),
            self.google_thread_on_finished)

        self.connect(
            self.google_thread,
            SIGNAL(
                "set_status_bar"),
            self.set_StatusBar,
            QtCore.Qt.QueuedConnection)

        self.connect(
            self.google_thread,
            SIGNAL(
                "thread_error"),
            self.google_thread_error,
            QtCore.Qt.QueuedConnection)

        self.connect(
            self.google_thread,
            SIGNAL(
                "set_my_status"),
            self.set_google_status,
            QtCore.Qt.QueuedConnection)

    def connect_add_db_thread_slots(self):

        self.connect(
            self.add_to_db_thread,
            SIGNAL(
                "set_my_status"),
            self.set_db_status,
            QtCore.Qt.QueuedConnection)

        self.connect(
            self.google_thread,
            SIGNAL(
                "set_progress_bar"),
            self.set_progress_bar,
            QtCore.Qt.QueuedConnection)

        self.connect(
            self.add_to_db_thread,
            SIGNAL(
                "set_status_bar"),
            self.set_StatusBar,
            QtCore.Qt.QueuedConnection)

        self.connect(
            self.add_to_db_thread,
            SIGNAL(
                "set_progress_bar"),
            self.set_progress_bar,
            QtCore.Qt.QueuedConnection)

    def connect_main_slots(self):
        pass

    def b_get_from_google_on_click(self):
        self.b_get_from_google.setDisabled(True)
        self.google_thread.db_contacts = self.google_thread.start()

    def google_thread_on_started(self):
        # Вызывается при запуске потока
        self.set_StatusBar("Вызван метод google_thread_on_started()")

    def google_thread_on_finished(self):
        # Вызывается при завершении потока
        self.b_get_from_google.setDisabled(False)  # Делаем кнопку активной
        # print self.google_thread.db_contacts
        # import pdb; pdb.set_trace()
        if self.google_thread.db_contacts:
            self.add_to_db_thread.db_contacts = self.google_thread.db_contacts
            self.add_to_db_thread.start()

    def google_thread_error(self, TYPE_ERROR, TITLE, MESSAGE):
        self.show_error(TYPE_ERROR, TITLE, MESSAGE)

    def set_db_status(self, value=False):
        if value:
            self.l_db_status.setText("<font color = green>CONNECTED!<\\font>")
        else:
            self.l_db_status.setText("<font color = red>DISCONNECTED!<\\font>")

    def set_google_status(self, value=False):
        if value:
            self.l_google_status.setText("\
                <font color = green>CONNECTED!<\\font>")
        else:
            self.l_google_status.setText("\
                <font color = red>DISCONNECTED!<\\font>")

    def set_progress_bar(self, value):
        value = int(value)
        if(0 <= value <= 100):
            self.pBar.setValue(value)
        elif(value > 100):
            while(value > 100):
                value = value - 100
            self.pBar.setValue(value)

    def set_StatusBar(self, MESSAGE="None"):
        self.statusBar().showMessage(MESSAGE)
