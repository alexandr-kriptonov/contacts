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

    def connect_main_slots(self):
        self.connect(
            self.b_edit_db,
            SIGNAL("clicked()"),
            self.b_edit_db_on_click)

        self.connect(
            self.b_edit_contact,
            SIGNAL("clicked()"),
            self.b_edit_contact_on_click)

        self.connect(
            self.b_quit,
            SIGNAL("clicked()"),
            self.close)

        self.connect(
            self.le_search,
            SIGNAL("returnPressed()"),
            self.search_query)
        self.connect(
            self.lV_main,
            SIGNAL("clicked(QModelIndex)"),
            self.lV_main_on_click)

        self.connect(
            self.b_submit,
            SIGNAL("clicked()"),
            self.b_submit_on_click)

        # self.connect(
        #     self.b_revert,
        #     SIGNAL("clicked("),
        #     self.edit_contact_model.revertAll)

        self.search_query()

        self.comboB_search.addItem(u"with the any letter")
        self.comboB_search.addItem(u"with the first letter")
        self.comboB_search.addItem(u"with the last letter")

        self.connect(
            self.comboB_search,
            SIGNAL("currentIndexChanged(QString)"),
            self.comboB_search_currentIndexChanged)

        self.le_search.setText("")

        self.comboB_search_currentIndexChanged()

    def connect_google_thread_slots(self):
        self.connect(
            self.b_get_from_google,
            SIGNAL("clicked()"),
            self.b_get_from_google_on_click)

        self.connect(
            self.google_thread,
            SIGNAL("started()"),
            self.google_thread_on_started)

        self.connect(
            self.google_thread,
            SIGNAL("finished()"),
            self.google_thread_on_finished)

        self.connect(
            self.google_thread,
            SIGNAL("set_status_bar"),
            self.set_StatusBar,
            QtCore.Qt.QueuedConnection)

        self.connect(
            self.google_thread,
            SIGNAL("thread_error"),
            self.google_thread_error,
            QtCore.Qt.QueuedConnection)

        self.connect(
            self.google_thread,
            SIGNAL("set_my_status"),
            self.set_google_status,
            QtCore.Qt.QueuedConnection)

    def connect_add_db_thread_slots(self):

        self.connect(
            self.add_to_db_thread,
            SIGNAL("set_my_status"),
            self.set_db_status,
            QtCore.Qt.QueuedConnection)

        self.connect(
            self.google_thread,
            SIGNAL("set_progress_bar"),
            self.set_progress_bar,
            QtCore.Qt.QueuedConnection)

        self.connect(
            self.add_to_db_thread,
            SIGNAL("set_status_bar"),
            self.set_StatusBar,
            QtCore.Qt.QueuedConnection)

        self.connect(
            self.add_to_db_thread,
            SIGNAL("set_progress_bar"),
            self.set_progress_bar,
            QtCore.Qt.QueuedConnection)

        self.connect(
            self.add_to_db_thread,
            SIGNAL("finished()"),
            self.add_to_db_thread_on_finished)
