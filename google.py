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

# def create_contact(gd_client):
#   new_contact = gdata.contacts.data.ContactEntry()
#   # Set the contact's name.
#   new_contact.name = gdata.data.Name(
#       given_name=gdata.data.GivenName(text='Elizabeth'),
#       family_name=gdata.data.FamilyName(text='Bennet'),
#       full_name=gdata.data.FullName(text='Elizabeth Bennet'))
#   new_contact.content = atom.data.Content(text='Notes')
#   # Set the contact's email addresses.
#   new_contact.email.append(gdata.data.Email(address='liz@gmail.com',
#       primary='true', rel=gdata.data.WORK_REL, display_name='E. Bennet'))
#   new_contact.email.append(gdata.data.Email(address='liz@example.com',
#       rel=gdata.data.HOME_REL))
#   # Set the contact's phone numbers.
#   new_contact.phone_number.append(gdata.data.PhoneNumber(text='(206)555-1212',
#       rel=gdata.data.WORK_REL, primay='true'))
#   new_contact.phone_number.append(gdata.data.PhoneNumber(text='(206)555-1213',
#       rel=gdata.data.HOME_REL))
#   # Set the contact's IM address.
#   new_contact.im.append(gdata.data.Im(text='liz@gmail.com',
#       primary='true', rel=gdata.data.HOME_REL, protocol=gdata.data.GOOGLE_TALK_PROTOCOL))
#   # Set the contact's postal address.
#   new_contact.structured_postal_address.append(
#       rel=gdata.data.WORK_REL, primary='true',
#       street=gdata.data.Street(text='1600 Amphitheatre Pkwy'),
#       city=gdata.data.City(text='Mountain View'),
#       region=gdata.data.Region(text='CA'),
#       postcode=gdata.data.PostCode(text='94043'),
#       country=gdata.data.Country(text='United States'))
#   # Send the contact data to the server.
#   contact_entry = gd_client.CreateContact(new_contact)
#   print "Contact's ID: %s" % contact_entry.id.text
#   return contact_entry

# class Google_Contact(gd_client):
#     def __init__(self, fullname, ):


# def google_update_contact(gd_client, contact, friend, vkGroup):

#     #Set the contact's phone numbers.
#     if ('mobile_phone' in friend) and (friend['mobile_phone'] != 0):
#         contact.phone_number.append(gdata.data.PhoneNumber(text=friend['mobile_phone'],
#                                                            rel=gdata.data.WORK_REL, primay='true'))
#     if ('home_phone' in friend) and (friend['home_phone'] != 0):
#         contact.phone_number.append(gdata.data.PhoneNumber(text=friend['home_phone'],
#                                                            rel=gdata.data.HOME_REL))
#     if 'bdate' in friend:
#         contact.birthday = gdata.contacts.data.Birthday(when=friend['bdate'])

#     #Set Group for VK friends
#     contact.group_membership_info.append(gdata.contacts.data.GroupMembershipInfo(href=vkGroup))

#     #Push changes to Google
#     gd_client.Update(contact)

#     #Download photo from vk, add to google, remove from local computer
#     local_image_filename = friend['photo_big'][friend['photo_big'].rfind('/') + 1:]
#     downloadPhoto(friend['photo_big'], local_image_filename)
#     gd_client.ChangePhoto(local_image_filename, contact, content_type='image/jpeg')
#     removeLocalPhoto(local_image_filename)


# def google_create_contact(gd_client, friend, vkGroup):

#     new_contact = gdata.contacts.data.ContactEntry()
#     name = friend['full_name']
#     new_contact = gdata.contacts.data.ContactEntry(name=gdata.data.Name(full_name=gdata.data.FullName(text=name)))
#     contact = gd_client.CreateContact(new_contact)

#     google_update_contact(gd_client, contact, friend, vkGroup)


class GoogleThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.db_contacts = {}

    def run(self):
        self.username = 'alexandr.kriptonov@gmail.com'
        self.password = '08093192S1h2I3p43000'
        # connect to Google Contacts
        self.emit(
            SIGNAL(
                "google_signal"),
            "TRY CONNECT TO GOOGLE CONTACTS!")
        self.msleep(100)
        self.gd_client = gdata.contacts.client.ContactsClient()
        self.gd_client.ClientLogin(
            self.username,
            self.password,
            self.gd_client.source)
        self.emit(SIGNAL("set_google_status"), True)
        self.Google_Contacts = get_all_contacts(self.gd_client)
        self.db_contacts = {}
        count = 0
        for i in self.Google_Contacts:
            count += 1

        round_percent = int(round(100/count))
        for i, g_contact in enumerate(self.Google_Contacts):
            self.db_contacts[i] = google_contact_to_obj(g_contact)
            self.emit(
                SIGNAL("google_signal"),
                "contact(%s) processed" % self.db_contacts[i]["full_name"])
            self.emit(SIGNAL("set_progress_bar"), i*round_percent)
            self.msleep(1)
        self.emit(SIGNAL("set_progress_bar"), 100)
        self.emit(SIGNAL("google_signal(QString)"), "Disconeccted from Google")
        # print self.db_contacts
        self.emit(SIGNAL("set_google_status"), False)
        self.sleep(1)
        return self.db_contacts
