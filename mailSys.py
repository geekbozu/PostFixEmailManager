#!/bin/python
# -*- coding: utf-8 -*-
import npyscreen
import CustomWidgets
from pony.orm import *
import pony.orm.dbproviders.mysql
from sql import *
import curses
import hashlib
import base64
import os,sys
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

class emailUser(CustomWidgets.goodForm):
    def beforeEditing(self):
        self.myList.values = self.update_users()

    def afterEditing(self):
        #self.parentApp.setNextFormPrevious()
        pass

    def update_users(self):
        return self.parentApp.database.getUsers()

    def create(self):
        self.info = u" ^A: Add ── ^D: Delete "
        self.myList = self.add(CustomWidgets.UserList, scroll_edit = True)
        self.add_handlers({
           "^A": self.when_add_record,
           "^D": self.when_delete_record})
        super(emailUser,self).create()

    def when_add_record(self, *args, **keywords):
        self.parentApp.switchForm('USERFORM')

    def when_delete_record(self,*args, **keywords):
        if npyscreen.notify_yes_no("Do you want to delete [%s]" %
                self.myList.values[self.myList.cursor_line].email, title="Warning!",
                form_color="DANGER"):
            self.parentApp.database.removeUser(email=self.myList.values[self.myList.cursor_line].email)
            self.myList.values=self.update_users()


class emailUserForm(CustomWidgets.InfoForm,npyscreen.ActionPopup):
    user = None
    oldHash = None
    changed = False
    def afterEditing(self):
        pass
        #self.parentApp.setNextFormPrevious()
    def beforeEditing(self):
       if self.changed:
           return
       if self.user is not None:
            self.myLocalPart.value, self.myDomain.value = self.user.email.split('@')
            self.oldHash = self.user.password
            self.changed = True
       else:
            self.value = None
            self.oldHash = None
            self.myLocalPart.value = None
            self.myDomain.value = None
            self.myPassword.value = None


    def create(self):
       self.info = u''
       self.myLocalPart    = self.add(npyscreen.TitleText, name = u'Local-Part:')
       self.myDomain       = self.add(npyscreen.TitleText, name = 'Domain:', color = 'CAUTIONHL',
               labelColor='CAUTION')
       self.myPassword     = self.add(npyscreen.TitleText, name = 'Password:', value = None)
       self.myDomain.add_handlers({
           curses.ascii.NL: self.h_key_handle,
           " ":             self.h_key_handle})
       self.myEmail        = self.add(npyscreen.TitleMultiLine,
               scroll_exit = True, max_height=3, name='Configure:', rely=6)

    def on_cancel(self):
        self.myLocalPart.value = None
        self.myDomain.value = None
        self.myPassword.value  = None
        self.oldHash = None
        self.user = None
        self.changed = False
	self.parentApp.setNextFormPrevious()

    def on_ok(self):
        if (self.myLocalPart.value != None and
            self.myDomain.value != None and
            self.myPassword.value != None):
            #Define Email
            email = self.myLocalPart.value + '@' + self.myDomain.value

            #Define Password
            if self.myPassword.value != None:
                password = self.parentApp.database.genPassword(self.myPassword.value)
            else:
                password = self.oldHash

            if password == None:
                npyscreen.notify_wait("Password Required!", "Super Witty Title")
                return

            #Define Domain_id
            if not self.parentApp.database.getDomainByName(domain = self.myDomain.value):
                npyscreen.notify_wait("Invalid Domain: {}".format(self.myDomain.value),"ERROR")
                return

            if self.parentApp.database.getUser(email):
                if npyscreen.notify_yes_no("Do you want to overwrite {}?".format(email), title= "Warning",
                        form_color="DANGER") == False:
                    return

            if self.parentApp.database.saveUser(email = email, password = password,
                    domain = self.myDomain.value):
                npyscreen.notify_wait("User Saved!", "WITTY TITLE", form_color = "WARNING")
            else:
                npyscreen.notify_wait("Failed to save user!", "IDK WHY YOU CAN SEE THIS",
                        form_color="WARNING")
            self.changed = False
            self.parentApp.switchFormPrevious()

    def h_key_handle(self, *args, **keywords):
        self.parentApp.switchForm('DOMAINSELECT')


class addDomainPopup(npyscreen.ActionPopup):
    def create(self):
        self.myDomain = self.add(npyscreen.TitleText,name="New Domain")

    def on_ok(self):
        if self.myDomain.value != '':
             self.parentApp.database.addDomain(domain=self.myDomain.value)
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

    def update_domains(self):
        return self.parentApp.database.getDomains()

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

    def update_domains(self):
        return self.parentApp.database.getDomains()

    def buttonpress(self):
        if self.myList.value != None:
            self.parentApp.getForm("USERFORM").myDomain.value=self.myList.values[self.myList.value].name
            #import pdb; pdb.set_trace()
        self.parentApp.switchFormPrevious()

class EmailManager(npyscreen.NPSAppManaged):
    def onStart(self):
        self.database = userConfig(config)
        self.addForm('MAIN', emailMain, name='Email Manager')
        self.addForm('DOMAIN', emailDomain, name='Domain Manager')
        self.addForm('ADDDOMAIN', addDomainPopup, name='Add Domain')
        self.addForm('DOMAINSELECT', emailDomainPopup, name='Domain List')
        self.addForm("ALIASES", emailAliasPopup, name='Alias manager')
        self.addForm("USER", emailUser, name = 'User Manager')
        self.addForm("USERFORM", emailUserForm, name = 'Edit User')
        # A real application might define more forms here.......

if __name__ == '__main__':
    try:
        config = sys.argv[1]
    except:
        config = '/usr/local/etc/mailSys/mailSys.conf'
    if not os.path.isfile(config):
       print "{} not found!".format(config)
       sys.exit()
    TestApp = EmailManager().run()
