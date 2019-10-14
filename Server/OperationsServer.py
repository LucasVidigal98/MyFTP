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

def list_dir():

	str_file = ''

	try:
		for name_file in os.listdir(r'Files'):
			str_file += str(name_file) + '\n'
	except:
		str_file = 'O diretório do servidor está vazio'

	return str_file

def is_file(name_file):

	try:
		with open('Files/' + str(name_file), 'r') as file:
			return True
	except:
		return False

def read_file(name_file):

	try:
		with open('Files/' + str(name_file), 'rb') as file:
			msg = file.read()
	except:
		return False

	return msg