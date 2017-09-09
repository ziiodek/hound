import os
import string
import random
import fileinput
import sys


class IdGenerator:
    dir_path = os.path.dirname( os.path.realpath( __file__ ) )
    drivers_file ='drivers.txt'
    vehicles_file = 'vehicles.txt'
    trailers_file = 'trailers.txt'

    def start_files(user_id):
        path_drivers = IdGenerator.dir_path+'/data/'+IdGenerator.drivers_file
        path_vehicles = IdGenerator.dir_path+'/data/' + IdGenerator.vehicles_file
        path_trailers = IdGenerator.dir_path+'/data/' + IdGenerator.trailers_file

        drivers_file = open(path_drivers,'a')
        vehicles_file = open(path_vehicles,'a')
        trailers_file = open(path_trailers,'a')

        drivers_file.write(user_id+':'+'1000000\n')
        vehicles_file.write(user_id+':'+'-1\n')
        trailers_file.write(user_id + ':' + '-1\n')

        drivers_file.close()
        vehicles_file.close()
        trailers_file.close()

    def generate_assigned_id(user_id):
        path = IdGenerator.dir_path+'/data/'+IdGenerator.drivers_file
        file = open(path,'r')
        data = file.readlines()
        for line in data:
            words = line.split(':')
            if words[0] == user_id:
                assigned_id = int(words[1])+1
                file.close()
                return assigned_id
        file.close()
        return -1

    def generate_economic_no(user_id,file_name):
        path = IdGenerator.dir_path+'/data/'+file_name+'.txt'
        file = open(path,'r')
        data = file.readlines()
        for line in data:
            words = line.split(':')
            if words[0] == user_id:
                assigned_id = int(words[1])+1
                file.close()
                return assigned_id
        file.close()
        return -1

    def store_assigned_id(user_id):
        path = IdGenerator.dir_path + '/data/' + IdGenerator.drivers_file
        assigned_id = -1
        for line in fileinput.input(path, inplace=1):
            if user_id in line:
                words = line.split( ':' )
                assigned_id = int( words[1] ) + 1
                line = line.replace(line, str(user_id) + ":" +str(assigned_id) +"\n")
            sys.stdout.write(line)
        return assigned_id




    def store_economic_no(user_id,file_name):
        path = IdGenerator.dir_path+'/data/' + file_name +'.txt'
        economic_no = -1
        for line in fileinput.input(path, inplace=1):
            if user_id in line:
                words = line.split(':')
                economic_no = int(words[1]) + 1
                line = line.replace(line, str(user_id) + ":" +str(economic_no) +"\n")
            sys.stdout.write(line)
        return economic_no


    def generate_user_id(self):
        chars = string.ascii_uppercase + string.digits
        user_id = ''.join( random.choice( chars ) for _ in range(5))
        IdGenerator.start_files(user_id)
        return user_id

    def generate_token_key(self):
        chars = string.ascii_uppercase + string.digits
        key = ''.join(random.choice(chars) for _ in range(8))
        return key