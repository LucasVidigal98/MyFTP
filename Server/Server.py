# -*- coding: UTF-8 -*-
import socket
from OperationsServer import *
import random

successful = False	#Vefica se encontrou uma porta válida

while successful == False:

	#Tenta encontrar uma porta válida	
	HOST = ''
	PORT = random.randint(60000, 65000) #Tenta encontrar uma porta livre entre 60000 e 65000
	addr = (HOST, PORT)

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(addr)
		s.listen(10)
		successful = True

	except:
		continue

#RESPONSE MESSAGE#
FILE_EXISTS = 'FILE_EXISTS';            	#Arquivo existe
FILE_NOT_FOUND = 'FILE_NOT_FOUND';         	#Arquivo não existe
CONTENT_AVAILBE = 'CONTENT_AVAILBE';        #Contéudo disponível
CONTENT_NOT_AVAILBE = 'CONTENT_NOT_AVAILBE' #Conteúdo não disponível
EOF = 'EOF';                    			#Fim do arquivo
LOGIN_EXISTS = 'LOGIN_EXISTS';           	#Login encontrado
LOGIN_NOT_FOUND = 'LOGIN_NOT_FOUND';        #Login não encontrado

print('Server Started PORT: '+ str(PORT))

while True:
	
	print('Aguardando conexao')
	conex, client = s.accept()
	print('Conectado')
	print('Aguardando Requisição')
	#Espera requisição
	req = conex.recv(1024)
	request = str(req.decode('utf-8')).split(' ')
	
	if request[0] == 'login':	#Validação de login

		validation = login_validator(str(req.decode('utf-8')))
		print(validation)
		if validation == True:	#Login existe
			conex.send(bytes(LOGIN_EXISTS, 'utf-8'))
		else:					#Login não existe
			conex.send(bytes(LOGIN_NOT_FOUND, 'utf-8'))

	elif request[0] == 'ls':  #Lista diretório

		str_list = list_dir()

		conex.send(bytes(str_list, 'utf-8')) #Envia a listagem do diretorio

	elif request[0] == 'get':	#Verifica se o arquivo existe

		if len(request) > 2: #Concatena os espaços da requisição
			for i in range(2, len(request)):
				request[1] += ' ' + request[i]

		try:
			file_validation = is_file(request[1])

			if file_validation == True:		#Arquivo existe
				conex.send(bytes(FILE_EXISTS, 'utf-8'))
			else:							#Arquivo não existe
				conex.send(bytes(FILE_NOT_FOUND, 'utf-8'))
		except:
			conex.send(bytes(FILE_NOT_FOUND, 'utf-8'))

	elif request[0] == 'get_':	#Força dowload se arquivo existir

		if len(request) > 2: #Concatena os espaços da requisição
			for i in range(2, len(request)):
				request[1] += ' ' + request[i]

		content_file = read_file(request[1])	#Recece o conteúdo do arquivo

		if content_file == False:				#Falso = Não foi possível baixar o conteúdo
			conex.send(bytes(CONTENT_NOT_AVAILBE, 'utf-8'))
		else:
			conex.send(bytes(content_file))