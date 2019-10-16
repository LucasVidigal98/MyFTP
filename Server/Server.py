# -*- coding: UTF-8 -*-
import socket
from OperationsServer import *
import random
import os

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
FAIL_UPLOAD = 'FAIL_UPLOAD'					#Erro ao recber um upload de um arquivo
SUCESS_UPLOAD = 'SUCESS_UPLOAD'				#Upload de arquivo feito com sucsesso

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
		
		if validation == True:	#Login existe
			try:
				#Se for o primeiro login desse usuário no servidor criar um diretório para ele	
				os.mkdir('Users_dir/' + request[1])
			except:
				pass
			conex.send(bytes(LOGIN_EXISTS, 'utf-8'))
		else:					#Login não existe
			conex.send(bytes(LOGIN_NOT_FOUND, 'utf-8'))

	elif request[0] == 'ls':  #Lista diretório

		str_list = list_dir(request[1])

		conex.send(bytes(str_list, 'utf-8')) #Envia a listagem do diretorio

	elif request[0] == 'get':	#Verifica se o arquivo existe
		
		if len(request) > 2: #Concatena os espaços da requisição
			for i in range(2, len(request)-1):
				request[1] += ' ' + request[i]
				print(request[1])
				
		try:
			file_validation = is_file(request[1], request[len(request)-1])

			if file_validation == True:		#Arquivo existe
				conex.send(bytes(FILE_EXISTS, 'utf-8'))
			else:							#Arquivo não existe
				conex.send(bytes(FILE_NOT_FOUND, 'utf-8'))
		except:
			conex.send(bytes(FILE_NOT_FOUND, 'utf-8'))

	elif request[0] == 'get_':	#Força dowload se arquivo existir

		if len(request) > 2: #Concatena os espaços da requisição
			for i in range(2, len(request)-1):
				request[1] += ' ' + request[i]

		content_file = read_file(request[1], request[len(request)-1])	#Recece o conteúdo do arquivo

		if content_file == False:				#Falso = Não foi possível baixar o conteúdo
			conex.send(bytes(CONTENT_NOT_AVAILBE, 'utf-8'))
		else:
			conex.send(bytes(content_file))

	elif request[0] == 'put':

		print('Aguardando conexao ... put')
		conex, client = s.accept()
		print('Conectado ... put')
		print('Aguardando Requisição ... put')
		#Espera requisição
		
		full_msg = bytes('', 'utf-8')
		while True:		#Recebe os bytes do arquivo de upload
			
			msg = conex.recv(1000000)
			full_msg += msg

			if len(msg) < 1000000:
				break

		success = upload_file(request[1], full_msg, request[len(request)-1])	#Salva o arquivo no diretório do cliente

		if success == True:
			conex.send(bytes(SUCESS_UPLOAD, 'utf-8'))
		else:
			conex.send(bytes(FAIL_UPLOAD, 'utf-8'))