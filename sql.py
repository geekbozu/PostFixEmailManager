#!/bin/python
# -*- coding: utf-8 -*-
from pony.orm import *


db = Database()
class Virtual_domains(db.Entity):
   id = PrimaryKey(int, auto=True)
   name = Required(str)

class Virtual_aliases(db.Entity):
    id = PrimaryKey(int, auto=True)
    domain_id = Required(int)
    source = Required(str)
    destination = Required(str)


class Virtual_users(db.Entity):
    id = PrimaryKey(int, auto=True)
    domain_id = Required(int)
    password = Required(str)
    email = Required(str)

