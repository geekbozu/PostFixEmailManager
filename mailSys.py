#!/bin/python
# -*- coding: utf-8 -*-
import npyscreen
import CustomWidgets
from pony.orm import *

class virtual_domains(db.entity):
   id = primarykey(int, auto=true)
   name = optional(str)

class virtual_aliases(db.entity):
    id = primarykey(int, auto=true)
    domain_id = optional(int)
    source = optional(str)
    destination = optional(str)


class virtual_users(db.entity):
    id = primarykey(int, auto=true)
    domain_id = optional(int)
    password = optional(str)
    email = optional(str)

class emailMain(npyscreen.FormBaseNew):
    def afterEditing(self):
	pass
	#self.parentApp.setNextForm(None)
    def create(self):
	self.Title          = self.add(npyscreen.Textfield, value = "Select an Option:", name='Option')
	self.myActions      = self.add(CustomWidgets.mainMenu, scoll_edit=True, name='Options:',
                values = ['Manage Domains', 'Manage Users', 'Quit'],
                relx = 6)

class emailUserForm(CustomWidgets.InfoForm,npyscreen.ActionForm):
    def afterEditing(self):
        self.parentApp.setNextFormPrevious()
    def beforeEditing(self):
        pass
    #Need to Pull SQL info here for user

    def create(self):
       self.value=None
       self.myTitle        = self.add(npyscreen.TitleText, name='User Email:', editable=False)
       self.myDomain       = self.add(npyscreen.TitleText, name='Domain:', color= 'CAUTIONHL',
               labelColor='CAUTION', value='test', editable=False)
       self.myEmail        = self.add(npyscreen.TitleMultiLine,
               scroll_exit=True, max_height=3, name='Configure:',
               values = ['Edit Aliases', 'Change Password', 'Delete User'],rely=5)
    def on_cancel(self):
	self.parentApp.setNextFormPrevious()

class emailAliasPopup(npyscreen.ActionPopup):
    def beforeEditing(self):
        pass
    #load Aliases for selected user here

    def afterEditing(self):
	self.parentApp.setNextFormPrevious()
    def create(self):
	self.myActions     = self.add(npyscreen.TitleMultiLine, scroll_edit=True, Name='Options',
                values = ['Add Alias', 'Delete alias'])

class emailDomain(CustomWidgets.InfoForm,npyscreen.Form):
    def beforeEditing(self):
        pass
    #pull Domain List here

    def afterEditing(self):
        self.parentApp.setNextFormPrevious()
    def create(self):
        self.info = u" ^A: Add ── ^D: Delete "
        self.myDomainList = self.add(CustomWidgets.DomainList, scroll_edit = True,
                values = [chr(i) for i in range(21,81)])

class emailUser(CustomWidgets.InfoForm,npyscreen.Form):
    def beforeEditing(self):
        pass
    #pull User list here

    def afterEditing(self):
        self.parentApp.setNextFormPrevious()

    def create(self):
        self.value = None
        self.info = u" ^A: Add ── ^D: Delete "
        self.myUserList = self.add(CustomWidgets.UserList, scroll_edit = True,
                values = self.value)

class EmailManager(npyscreen.NPSAppManaged):
   def onStart(self):
       self.db = database()
       db.generate_mapping()
       self.addForm('MAIN', emailMain, name='Email Manager')
       self.addForm('DOMAIN', emailDomain, name='Domain Manager')
       self.addForm("ALIASES", emailAliasPopup, name='Alias manager')
       self.addForm("USER", emailUser, name = 'User Manager')
       # A real application might define more forms here.......

if __name__ == '__main__':
   TestApp = EmailManager().run()
