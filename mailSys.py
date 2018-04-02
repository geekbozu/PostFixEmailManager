#!/bin/python
# -*- coding: utf-8 -*-
import npyscreen
import CustomWidgets
from pony.orm import *
from sql import *
import curses
import hashlib
import base64
import os
import crypt
class emailMain(npyscreen.FormBaseNew):
    def afterEditing(self):
	pass
	#self.parentApp.setNextForm(None)

    def create(self):
	self.Title          = self.add(npyscreen.Textfield, value = "Select an Option:", name='Option')
	self.myActions      = self.add(CustomWidgets.mainMenu, scoll_edit=True, name='Options:',
                values = ['Manage Domains', 'Manage Users', 'Quit'],
                relx = 6)

class emailUserForm(CustomWidgets.InfoForm,npyscreen.ActionPopup):
    user = None
    def afterEditing(self):
        pass
        #self.parentApp.setNextFormPrevious()

    def create(self):
       self.info = u''
       if self.__class__.user:
           pass
           #sql shennangins here
       else:
           self.value = None

       self.myLocalPart        = self.add(npyscreen.TitleText, name = u'Local-Part:', value = '')
       self.myDomain       = self.add(npyscreen.TitleText, name = 'Domain:', color = 'CAUTIONHL',
               labelColor='CAUTION')
       self.myPassword     = self.add(npyscreen.TitleText, name = 'Password:', value = '')
       self.myDomain.add_handlers({
           curses.ascii.NL: self.h_key_handle,
           " ":             self.h_key_handle})
       self.myEmail        = self.add(npyscreen.TitleMultiLine,
               scroll_exit = True, max_height=3, name='Configure:',
               values = self.value, rely=6)

    def on_cancel(self):
        self.myLocalPart.value = None
        self.myDomain.value = None
        self.myPassword.value  = None
	self.parentApp.setNextFormPrevious()

    @db_session
    def on_ok(self):
        if (self.myLocalPart.value != None) and (self.myDomain.value != None) and (self.myPassword.value != None):
            email = self.myLocalPart.value + '@' + self.myDomain.value
            password = self.myPassword.value #need to salt+hash this
            sha = hashlib.sha512()
            sha.update(password)
            salt = base64.b64encode(os.urandom(12))
            sha.update('$6$')
            sha.update(salt)
            #salt = base64.b64encode(salt)
            password = base64.b64encode(sha.digest())
            password = '$6${}${}'.format(salt,password)
            try:
                did = Virtual_domains.get(name=self.myDomain.value).id
            except:
                npyscreen.notify_wait("Invalid Domain","ERROR")
                return
            Virtual_users(email=email,password = password, domain_id = did)
            commit()
            self.parentApp.switchFormPrevious()
    def h_key_handle(self, *args, **keywords):
        self.parentApp.switchForm('DOMAINSELECT')


class addDomainPopup(npyscreen.ActionPopup):
    def create(self):
        self.myDomain = self.add(npyscreen.TitleText,name="New Domain")

    @db_session
    def on_ok(self):
        if self.myDomain.value != '':
             Virtual_domains(name=self.myDomain.value)
             commit()
        self.parentApp.setNextFormPrevious()
    def on_cancel(self):
        self.myDomain.value = ''
        self.parentApp.setNextFormPrevious()

class emailAliasPopup(npyscreen.ActionPopup):
    def beforeEditing(self):
        pass
    #load Aliases for selected user here

    def afterEditing(self):
	self.parentApp.setNextFormPrevious()
    def create(self):
	self.myActions = self.add(npyscreen.TitleMultiLine, scroll_edit=True, Name='Options',
                values = ['Add Alias', 'Delete alias'])

class emailDomain(CustomWidgets.goodForm):
    def beforeEditing(self):
        self.myList.values = self.update_domains()

    @db_session
    def update_domains(self):
        return select(e for e in Virtual_domains)[:]

    def create(self):
        self.info = u" ^A: Add ── ^D: Delete "
        self.myList = self.add(CustomWidgets.DomainList, scroll_edit = True)
        super(emailDomain,self).create()

    def buttonpress(self):
        self.parentApp.switchForm('MAIN')

class emailDomainPopup(emailDomain):
    #def create(self):
    #    self.info = u" ^A: Add ── ^D: Delete "
    #    self.myDomainList = self.add(CustomWidgets.DomainList,scroll_edit=True, name = 'Domains:')

    def beforeEditing(self):
        self.myList.values = self.update_domains()

    @db_session
    def update_domains(self):
        return select(e for e in Virtual_domains)[:]

    @db_session
    def buttonpress(self):
        if self.myList.value != None:
            self.parentApp.getForm("USERFORM").myDomain.value=self.myList.values[self.myList.value].name
            #import pdb; pdb.set_trace()
        self.parentApp.switchFormPrevious()

class emailUser(CustomWidgets.goodForm):
    @db_session
    def beforeEditing(self):
        self.myList.values = select(e for e in Virtual_users)[:]

    def afterEditing(self):
        #self.parentApp.setNextFormPrevious()
        pass

    def create(self):
        self.info = u" ^A: Add ── ^D: Delete "
        self.myList = self.add(CustomWidgets.UserList, scroll_edit = True)
        super(emailUser,self).create()

class EmailManager(npyscreen.NPSAppManaged):
   def onStart(self):
       self.database = db
       self.database.bind(provider='mysql', host='localhost', user='rodger',passwd='changeme', db='rodger')
       self.database.generate_mapping()
       self.addForm('MAIN', emailMain, name='Email Manager')
       self.addForm('DOMAIN', emailDomain, name='Domain Manager')
       self.addForm('ADDDOMAIN', addDomainPopup, name='Add Domain')
       self.addForm('DOMAINSELECT', emailDomainPopup, name='Domain List')
       self.addForm("ALIASES", emailAliasPopup, name='Alias manager')
       self.addForm("USER", emailUser, name = 'User Manager')
       self.addForm("USERFORM", emailUserForm, name = 'Edit User')
       # A real application might define more forms here.......

if __name__ == '__main__':
   TestApp = EmailManager().run()
