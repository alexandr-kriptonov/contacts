# -*- coding: utf-8 -*-
from ui.informform import MainDialog


class MainClass(object):

    def to_log(
        self,
        type_message='info',
        MESSAGE='info',
        level=None,
    ):

        sent_to_log = False
        self.last_logger = {}

        if self.logger:
            type_message = type_message.lower()
            if type_message in ("debug", "dbg"):
                self.logger.debug(MESSAGE)
                self.last_logger["type_message"] = "info"
                self.last_logger["title"] = "!DEBUG!"
                self.last_logger["message"] = MESSAGE
                sent_to_log = True
            elif type_message in ("information", "info"):
                self.logger.info(MESSAGE)
                self.last_logger["type_message"] = "info"
                self.last_logger["title"] = "!INFO!"
                self.last_logger["message"] = MESSAGE
                sent_to_log = True
            elif type_message in ("warning", "warn"):
                self.logger.warn(MESSAGE)
                self.last_logger["type_message"] = "warn"
                self.last_logger["title"] = "!WARNING!"
                self.last_logger["message"] = MESSAGE
                sent_to_log = True
            elif type_message in ("error", "err"):
                self.logger.error(MESSAGE)
                self.last_logger["type_message"] = "err"
                self.last_logger["title"] = "!ERROR!"
                self.last_logger["message"] = MESSAGE
                sent_to_log = True
            elif type_message in ("critical", "crit"):
                self.logger.critical(MESSAGE)
                self.last_logger["type_message"] = "err"
                self.last_logger["title"] = "!CRITICAL!"
                self.last_logger["message"] = MESSAGE
                sent_to_log = True
            elif type_message in ("exception", "except", "expt"):
                self.logger.exception(MESSAGE)
                self.last_logger["type_message"] = "warn"
                self.last_logger["title"] = "!WARNING!"
                self.last_logger["message"] = MESSAGE
                sent_to_log = True
            else:
                return False
            if sent_to_log:
                return True

    def show_error(
        self,
        type_message,
        TITLE,
        MESSAGE
    ):
        if type_message and TITLE and MESSAGE:
            try:
                dialog = MainDialog()
                dialog.show(type_message, TITLE, MESSAGE)
            except Exception, e:
                self.logger.exception("%s" % e.message)
            else:
                self.logger.exception("Uncaught exception!")
