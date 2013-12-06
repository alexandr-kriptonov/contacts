# -*- coding: utf-8 -*-

import gdata.data
import gdata.gauth
import gdata.contacts.client
import gdata.contacts.data
# import atom
from PyQt4.QtCore import *

def get_all_contacts(gd_client):
    query = gdata.contacts.client.ContactsQuery()
    query.max_results = 1000
    feed = gd_client.GetContacts(q=query)
    return feed.entry

def google_contact_to_obj(g_contact):
    db_contact = {}
    db_contact["id_google"] = unicode(g_contact.id.text)
    db_contact["full_name"] = unicode(g_contact.name.full_name.text)
    if g_contact.birthday:
        db_contact["birthday"] = unicode(g_contact.birthday.when)
    else:
        db_contact["birthday"] = ""
    if g_contact.email:
        db_contact["email"] = unicode(g_contact.email[0].address)
    else:
        db_contact["email"] = ""
    if g_contact.phone_number:
        db_contact["phone"] = unicode(g_contact.phone_number[0].text)
    else:
        db_contact["phone"] = ""
    return db_contact

class GoogleThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.db_contacts = {}
    def run(self):
        self.email = 'example@gmail.com'
        self.password = '****'
        # connect to Google Contacts
        self.emit(SIGNAL("google_signal(QString)"), "CONNECT TO GOOGLE CONTACTS!")
        self.msleep(100)
        self.gd_client = gdata.contacts.client.ContactsClient()
        self.gd_client.ClientLogin(self.email, self.password,self.gd_client.source)
        self.emit(SIGNAL("set_google_status"), True)
        self.Google_Contacts = get_all_contacts(self.gd_client)
        self.db_contacts = {}
        count = 0
        for i in self.Google_Contacts:
            count += 1

        round_percent = int(round(100/count))
        for i,g_contact in enumerate(self.Google_Contacts):
            self.db_contacts[i] = google_contact_to_obj(g_contact)
            self.emit(SIGNAL("google_signal(QString)"), "contact(%s) processed" % self.db_contacts[i]["full_name"])
            self.emit(SIGNAL("set_progress_bar"), i*round_percent)
            self.msleep(1)
        self.emit(SIGNAL("set_progress_bar"), 100)
        self.emit(SIGNAL("google_signal(QString)"), "Disconeccted from Google")
        # print self.db_contacts
        self.emit(SIGNAL("set_google_status"), False)
        self.sleep(1)
        return self.db_contacts