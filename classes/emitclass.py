# -*- coding: utf-8 -*-
from PyQt4.QtCore import SIGNAL


class EmitClass(object):
    """docstring for  EmitClass"""
    def __init__(self):
        super(EmitClass, self).__init__()

    def set_status_bar(self, MESSAGE="None"):
        MESSAGE = unicode(MESSAGE)
        self.emit(SIGNAL("set_status_bar"), MESSAGE)

    def set_progress_bar(self, value=100):
        value = int(value)
        self.emit(SIGNAL("set_progress_bar"), value)

    def set_my_status(self, status=False):
        self.emit(SIGNAL("set_my_status"), status)

    def show_last_message(self):
        self.emit(
            SIGNAL(
                "thread_error"),
            self.last_logger["type_message"],
            self.last_logger["title"],
            self.last_logger["message"])
