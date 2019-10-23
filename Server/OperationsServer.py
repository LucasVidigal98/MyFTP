# -*- coding: UTF-8 -*-
import os
import MySQLdb

host = "localhost"
user = "root"
password = ""
db = "users"
port = 3306

conex = MySQLdb.connect(host, user, password, db, port)
c = conex.cursor(MySQLdb.cursors.DictCursor)

def login_validator(request):

	global c

	content_request = request.split()
	query = 'SELECT ' + 'passwd' + ' FROM ' + 'user' + ' WHERE login =  ' + content_request[1]
	c.excecute(query)
	print(c.fetchall()) 

	return False

def list_dir(user):

	str_file = ''
	found_files = False
	try:
		for name_file in os.listdir(r'Users_dir/'+user):
			found_files = True
			str_file += str(name_file) + '\n'
	except:
		str_file = 'O diretório do servidor está vazio'

	if found_files == False:
		return 'O diretório do servidor está vazio'

	return str_file

def is_file(name_file, user):
	
	try:
		with open('Users_dir/' + user + '/' + str(name_file), 'rb') as file:
			return True
	except:
		return False

def read_file(name_file, user):

	try:
		with open('Users_dir/' + user + '/' + str(name_file), 'rb') as file:
			msg = file.read()
			file.close()
	except:
		return False

	return msg

def upload_file(name_file, content_file, user):

	try:
		with open('Users_dir/' + user + '/' + str(name_file), 'wb') as file:
			file.write(content_file)
			file.close()
	except:
		return False #Não conssegui fazer o upload
	
	return True