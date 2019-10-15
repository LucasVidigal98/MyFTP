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
	print(user)
	try:
		for name_file in os.listdir(r'Users_dir/'+user):
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

def read_file(name_file, user):

	try:
		with open('Users_dir/' + user + '/' + str(name_file), 'rb') as file:
			print('aqui')
			msg = file.read()
	except:
		print('zorua')
		return False

	return msg

def upload_flie(name_file, content_file, user):

	try:
		with open('Users_dir/' + user + '/' + str(name_file), 'wb') as file:
			file.write(content_file)
	except:
		return False #Não conssegui fazer o upload
	
	return True