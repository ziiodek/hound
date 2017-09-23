import hashlib
import uuid
import os
import re
from .id_generator import IdGenerator
import fileinput
import sys

class Authenticator:
    dir_path = os.path.dirname( os.path.realpath( __file__ ) )
    path = dir_path + '/data/kitty.txt'

    def hashPassword(email,password):
        salt = uuid.uuid4().hex
        hash_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
        if Authenticator.getSalt(email) != None:
            Authenticator.update_record(email,salt)
        else:
            Authenticator.store_salt(salt,email)
        return hash_password


    def update_record(email,salt):
        for line in fileinput.input(Authenticator.path, inplace=1):
            if email in line:
                line = line.replace(line, email + ":" + salt+"\n")
            sys.stdout.write(line)



    def store_salt(salt,email):
        file = open(Authenticator.path,'a')
        file.write(email+':'+salt+'\n')
        file.close()

    def getSalt(email):
        file = open(Authenticator.path,'r')
        data = file.readlines()
        for line in data:
            words = line.split( ':' )
            if words[0] == email:
                salt = words[1].split('\n')
                salt = salt[0]
                file.close( )
                return salt
        file.close()
        return None

    def authenticate(email,password):
        if Authenticator.getSalt(email) != None:
            salt = Authenticator.getSalt(email)
            hash_password =  hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
            return hash_password
        return None

    def validate_password(password):
        error = ''
        if len(password) < 8:
           error += 'password must be have at least 8 characters '
        if not re.search( r'[0-9]', password ):
            error += 'password must contains numbers '

        if not re.search( r'[A-Z]+', password ):
            error += 'password must contains upper case characters '

        if not re.search( r'[a-z]+', password ):
            error += 'password must contains lower case characters '

        return error

    def validate_email(email):
        file = open(Authenticator.path, 'r')
        data = file.readlines()
        for line in data:
            words = line.split(':')
            file.close()
            if words[0] == email:
               print(words[0])
               return True
        return False


    def validate_email_form(email):
        error = ''
        if not re.search( r'[@]', email ):
            error += 'Invalid email address '
        return error