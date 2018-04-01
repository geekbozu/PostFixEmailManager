#!/bin/python
# -*- coding: utf-8 -*-
import npyscreen
import CustomWidgets
from pony.orm import *
from sql import *
import curses

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
        self.parentApp.setNextFormPrevious()

    def create(self):
       self.info = u''
       if self.__class__.user:
           pass
           #sql shennangins here
       else:
           self.value = None

       self.myTitle        = self.add(npyscreen.TitleText, name = u'Local-Part:')
       self.myDomain       = self.add(npyscreen.TitleText, name = 'Domain:', color = 'CAUTIONHL',
               labelColor='CAUTION')
       self.myPassword     = self.add(npyscreen.TitleText, name = 'Password:')
       self.myDomain.add_handlers({
           curses.ascii.NL: self.test,
           " ": self.test})
       self.myEmail        = self.add(npyscreen.TitleMultiLine,
               scroll_exit = True, max_height=3, name='Configure:',
               values = self.value, rely=6)

    def on_cancel(self):
	self.parentApp.setNextFormPrevious()
    def test(self, *args, **keywords):
        raise Exception("We did it")
class addDomainPopup(npyscreen.ActionPopup):
    def create(self):
        self.myDomain = self.add(npyscreen.TitleText,name="New Domain")

    @db_session
    def on_ok(self):
        if self.myDomain.value != '':
             Virtual_domains(name=self.myDomain.value)
             commit()
        self.parentApp.setNextForm('DOMAIN')
    def on_cancel(self):
        self.myDomain.value = ''
        self.parentApp.setNextForm('DOMAIN')

class emailAliasPopup(npyscreen.ActionPopup):
    def beforeEditing(self):
        pass
    #load Aliases for selected user here

    def afterEditing(self):
	self.parentApp.setNextFormPrevious()
    def create(self):
	self.myActions     = self.add(npyscreen.TitleMultiLine, scroll_edit=True, Name='Options',
                values = ['Add Alias', 'Delete alias'])

class emailDomain(CustomWidgets.InfoForm,npyscreen.FormBaseNew):
    def beforeEditing(self):
        self.myDomainList.values = self.update_domains()
    @db_session
    def update_domains(self):
        return select(e for e in Virtual_domains)[:]
    def create(self):
        self.info = u" ^A: Add ── ^D: Delete "
        y,x= self.curses_pad.getmaxyx()
        y-=5
        self.myDomainList = self.add(CustomWidgets.DomainList, scroll_edit = True,height=y)
        self.button =       self.add(npyscreen.MiniButtonPress, use_max_space=True,
                when_pressed_function=self.buttonpress, name='OK', rely=-3, relx=-10,
                cursor_color='CURSOR_INVERSE')
    def buttonpress(self):
        self.parentApp.switchForm('MAIN')

class emailUser(CustomWidgets.InfoForm,npyscreen.Form):
    @db_session
    def beforeEditing(self):
        self.myUserList.values = select(e for e in Virtual_users)[:]

    def afterEditing(self):
        self.parentApp.setNextFormPrevious()

    def create(self):
        self.info = u" ^A: Add ── ^D: Delete "
        self.myUserList = self.add(CustomWidgets.UserList, scroll_edit = True)

class EmailManager(npyscreen.NPSAppManaged):
   def onStart(self):
       self.database = db
       self.database.bind(provider='mysql', host='localhost', user='rodger',passwd='changeme', db='rodger')
       self.database.generate_mapping()
       self.addForm('MAIN', emailMain, name='Email Manager')
       self.addForm('DOMAIN', emailDomain, name='Domain Manager')
       self.addForm('ADDDOMAIN', addDomainPopup, name='Add Domain')
       self.addForm("ALIASES", emailAliasPopup, name='Alias manager')
       self.addForm("USER", emailUser, name = 'User Manager')
       self.addForm("USERFORM", emailUserForm, name = 'Edit User')
       # A real application might define more forms here.......

if __name__ == '__main__':
   TestApp = EmailManager().run()
