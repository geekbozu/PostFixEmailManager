#!/bin/python
import npyscreen

class emailUserForm(npyscreen.ActionForm):
    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
       self.myTitle        = self.add(npyscreen.TitleText, name='User Email:', editable=False)
       self.myDomain       = self.add(npyscreen.TitleText, name='Domain:', color= 'CAUTIONHL',
			     labelColor='CAUTION', value='test', editable=False)
       self.myEmail        = self.add(npyscreen.TitleMultiLine, scroll_exit=True, max_height=3, 
			     name='Configure:', values = ['Edit Aliases', 'Change Password', 'Delete User'],
		  	     rely=5)


class MyApplication(npyscreen.NPSAppManaged):
   def onStart(self):
       self.addForm('MAIN', emailUserForm, name='User Email')
       # A real application might define more forms here.......

if __name__ == '__main__':
   TestApp = MyApplication().run()
