#!/bin/python
import npyscreen

class emailMain(npyscreen.Form):
    class mainMenu(npyscreen.MultiLineAction):
	def actionHighlighted(self, act_on_this, key_press):
            if act_on_this == 'Manage Domains':
                self.parent.parentApp.switchForm("ALIASES")
            elif act_on_this == 'Manage Users':
                self.parent.parentApp.switchForm("USER")
            else:
	        self.parent.parentApp.switchForm(None)
		pass
	
    def afterEditing(self):
	pass
	#self.parentApp.setNextForm(None)
    def create(self):
	self.Title          = self.add(npyscreen.Textfield, value = "Select an Option:", name='Option') 
	self.myActions      = self.add(self.mainMenu, scoll_edit=True, name='Options:',
			      values = ['Manage Domains', 'Manage Users', 'Quit'],
			      relx = 6)
    
	

class emailUserForm(npyscreen.ActionForm):
    def afterEditing(self):
        self.parentApp.setNextFormPrevious()

    def create(self):
       self.myTitle        = self.add(npyscreen.TitleText, name='User Email:', editable=False)
       self.myDomain       = self.add(npyscreen.TitleText, name='Domain:', color= 'CAUTIONHL',
			     labelColor='CAUTION', value='test', editable=False)
       self.myEmail        = self.add(npyscreen.TitleMultiLine, scroll_exit=True, max_height=3, 
			     name='Configure:', values = ['Edit Aliases', 'Change Password', 'Delete User'],
		  	     rely=5)
    def on_cancel(self):
	self.parentApp.setNextFormPrevious()

class emailAliasForm(npyscreen.ActionPopup):
    def afterEditing(self):
	self.parentApp.setNextFormPrevious()
    def create(self):
	self.myActions     = self.add(npyscreen.TitleMultiLine, scroll_edit=True, Name='Options',
			     values = ['Add Alias', 'Delete alias'])


class EmailManager(npyscreen.NPSAppManaged):
   def onStart(self):
       self.addForm('MAIN', emailMain, name='Email Manager')
       self.addForm("ALIASES", emailAliasForm, name='Alias manager')
       self.addForm("USER", emailUserForm, name = 'User Manager')
       # A real application might define more forms here.......

if __name__ == '__main__':
   TestApp = EmailManager().run()
