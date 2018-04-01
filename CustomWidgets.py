#!/bin/python
# -*- coding: utf-8 -*-
import npyscreen
import curses
from pony.orm import *
from sql import *
class InfoForm(npyscreen.fmForm._FormBase):
    def __init__(self, info=None, *args, **keywords):
        self.info=info
        super(InfoForm,self).__init__(*args, **keywords)

    def display_menu_advert_at(self):
            return self.lines-1, 1

    def draw_form(self):
        super(InfoForm, self).draw_form()
        if self.info:
           # self.info = self.info.decode('utf-8', 'replace')
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

class DomainList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(DomainList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record})
    def display_value(self,v1):
        return "[%s] %s" % (v1.id, v1.name)
    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.switchForm('ADDDOMAIN')
        pass

    @db_session
    def when_delete_record(self, *args, **keywords):
        if npyscreen.notify_yes_no("Do you want to delete [%s]" %
                self.values[self.cursor_line].name, title="Warning!",
                form_color="DANGER"):
            Virtual_domains[self.values[self.cursor_line].id].delete()
            commit()
            self.values = self.parent.update_domains()

    def actionHighlighted(self, act_on_this, keypress):
        pass

class UserList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(UserList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record})
    def display_value(self,v1):
        return "[%s] %s" % (v1.id, v1.email)

    def when_add_record(self, act_on_this, keypress):
        pass
    def when_delete_record(self, act_on_this, keypress):
        npyscreen.notify_yes_no("Do you want to delete [%s]" %
                self.values[self.cursor_line].name, title="Warning!",
                form_color="DANGER")
    def actionHighlighted(self, act_on_this, keypress):
        pass
