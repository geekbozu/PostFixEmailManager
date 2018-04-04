# PostFixEmailManager
npyscreen ui to manage emails on my postfix mail server

compile with pyinstaller
move binary to /usr/local/sbin

Config file stored in /usr/local/etc/mailSys

# example Config
'''
[mysql]
user = user
host = localhost
passwd = password
database = mailuserdatabase
provider = ponyorm provider type


# working with not my database setup
Edit sql.py functions to return matching results from what ever database setup you use. 
