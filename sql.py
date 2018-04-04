#!/bin/python
# -*- coding: utf-8 -*-
from pony.orm import *
import hashlib
import base64
import os
import ConfigParser
db = Database()
class userConfig(object):
    '''Define use case specfic stuff here'''
    def __init__(self, config):
        conf = self.configParse(config)
        db.bind(provider = conf['provider'], host = conf['host'],
                user = conf['user'], passwd = conf['passwd'], db = conf['database'])
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
    def saveUser(self,email = None,password = None, domain = None):
        new = self.getUser(email)
        try:
            domain_id = self.getDomainByName(domain = domain)
            if new:
                new.set(email = email,password = password, domain_id = domain_id)
            else:
                Virtual_users(email = email,password = password, domain_id = domain_id)
            return True
        except:
            return False


    @db_session
    def removeUser(self,id=None):
        Virtual_users.get(id=id).delete()

    @db_session
    def getUser(self,email=None):
        try:
            return Virtual_users.get(email=email)
        except:
            return False


    @db_session
    def removeUser(self,email=None):
        Virtual_users.get(email=email).delete()

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
    def getDomainByName(self,domain = None):
        try:
            return Virtual_domains.get(name = domain).id
        except:
            return False

    @db_session
    def getDomainById(self,id = None):
        try:
            return Virtual_domains.get(id = id).name
        except:
            return False

    @db_session
    def getUsers(self):
        return select(e for e in Virtual_users)[:]

    @db_session
    def getAliases(self):
        return select(e for e in Virtual_aliases)[:]

    def configParse(self,config):
        conf = ConfigParser.ConfigParser()
        conf.read(os.path.expanduser(config))
#        database = config.get(mysql,database)
#        user = config.get(mysql,user)
#        passwd = config.get(mysql,passwd)
#        table = config.get(mysql,table)
#        host = config.get(mysql,host)
        return dict((j,k) for j,k in conf.items('mysql'))

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


