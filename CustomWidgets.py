#!/bin/python
import npyscreen
import curses

class InfoForm(npyscreen.fmForm._FormBase):
    def __init__(self, info=None, *args, **keywords):
        super(InfoForm,self).__init__(*args, **keywords)
        self.info=info

    def display_menu_advert_at(self):
            return self.lines-1, 1

    def draw_form(self):
        super(InfoForm, self).draw_form()
        if self.info:
            self.info = self.info.decode('utf-8', 'replace')
            y, x = self.display_menu_advert_at()
            self.add_line(y, x,
              self.info,
              self.make_attributes_list(self.info, curses.A_NORMAL),
              self.columns - x - 1
              )

class mainMenu(npyscreen.MultiLineAction):
    def actionHighlighted(self, act_on_this, key_press):
        if act_on_this == 'Manage Domains':
            self.parent.parentApp.switchForm("DOMAIN")
        elif act_on_this == 'Manage Users':
            self.parent.parentApp.switchForm("USER")
        else:
            self.parent.parentApp.switchForm(None)
        pass


