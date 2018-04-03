#!/bin/python
# -*- coding: utf-8 -*-
from pony.orm import *
import hashlib
import base64
import os

db = Database()
class userConfig(object):
    '''Define use case specfic stuff here'''
    def __init__(self):
        db.bind(provider='mysql', host='localhost',
                user='rodger', passwd='changeme', db='rodger')
        db.generate_mapping(create_tables=True)
        # Maybe init tables here later?

    def genPassword(self,password=None):
        sha = hashlib.sha512()
        sha.update(password)
        salt = base64.b64encode(os.urandom(12)) #arbitrary length salt
        sha.update('$6$')
        sha.update(salt)
        password = base64.b64encode(sha.digest())
        return  '$6${}${}'.format(salt,password)

    @db_session
    def saveUser(self,email,password,domain_id):
        Virtual_users(email = email,password = password, domain_id = domain_id)

    @db_session
    def removeUser(self,id=None,email=None):
        if id:
            Virtual_users.get(id=id).delete()
        elif email:
            Virtual_users.get(email=email).delete()
        else:
            return 0
    @db_session
    def addDomain(self,domain = None):
        Virtual_domains(name = domain)

    @db_session
    def removeDomain(self,did = None):
        Virtual_domains[did].delete()

    @db_session
    def getDomains(self):
        return select(e for e in Virtual_domains)[:]

    @db_session
    def getDomainId(self,name = None):
        try:
            return Virtual_domains.get(name = name).id
        except:
            return 0

    @db_session
    def getUsers(self):
        return select(e for e in Virtual_users)[:]



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
    domain_id = Optional(int)
    password = Optional(str)
    email = Required(str)


