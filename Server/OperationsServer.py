# -*- coding: UTF-8 -*-
import os

def login_validator(request):

	file = open('users.txt', 'r')
	content_request = request.split()

	for line in file:

		values = line.split(' ')

		if str(content_request[1]) == str(values[0]):
			if str(content_request[2]) == str(values[1][:str(values[1]).find('\n')]):
				return True

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
		print('here')
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