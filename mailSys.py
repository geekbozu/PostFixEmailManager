#!/bin/python
import npyscreen
import CustomWidgets
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

    def create(self):
       self.myTitle        = self.add(npyscreen.TitleText, name='User Email:', editable=False)
       self.myDomain       = self.add(npyscreen.TitleText, name='Domain:', color= 'CAUTIONHL',
               labelColor='CAUTION', value='test', editable=False)
       self.myEmail        = self.add(npyscreen.TitleMultiLine,
               scroll_exit=True, max_height=3, name='Configure:',
               values = ['Edit Aliases', 'Change Password', 'Delete User'],rely=5)
    def on_cancel(self):
	self.parentApp.setNextFormPrevious()

class emailAliasPopup(npyscreen.ActionPopup):
    def afterEditing(self):
	self.parentApp.setNextFormPrevious()
    def create(self):
	self.myActions     = self.add(npyscreen.TitleMultiLine, scroll_edit=True, Name='Options',
                values = ['Add Alias', 'Delete alias'])

class emailDomain(CustomWidgets.InfoForm,npyscreen.Form):
    def afterEditing(self):
        self.parentApp.setNextFormPrevious()
    def create(self):
        self.info = "^A: Add | ^D: Delete"
        self.myDomainList = self.add(npyscreen.MultiLineAction, scroll_edit = True,
                values = [chr(i) for i in range(21,81)])

class EmailManager(npyscreen.NPSAppManaged):
   def onStart(self):
       self.addForm('MAIN', emailMain, name='Email Manager')
       self.addForm('DOMAIN', emailDomain, name='Domain Manager')
       self.addForm("ALIASES", emailAliasPopup, name='Alias manager')
       self.addForm("USER", emailUserForm, name = 'User Manager')
       # A real application might define more forms here.......

if __name__ == '__main__':
   TestApp = EmailManager().run()
