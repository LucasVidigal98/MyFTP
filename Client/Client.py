# -*- coding: UTF-8 -*-
import socket
import os

HOST = raw_input('IP Server: ')
PORT = int(input('Port: '))
addr = (HOST, PORT)

#RESPONSES MESSAGES#
FILE_EXISTS = 'FILE_EXISTS';            	#Arquivo existe
FILE_NOT_FOUND = 'FILE_NOT_FOUND';         	#Arquivo não existe
CONTENT_AVAILBE = 'CONTENT_AVAILBE';        #Contéudo disponível
CONTENT_NOT_AVAILBE = 'CONTENT_NOT_AVAILBE' #Conteúdo não disponível
EOF = 'EOF';                    			#Fim do arquivo
LOGIN_EXISTS = 'LOGIN_EXISTS';           	#Login encontrado
LOGIN_NOT_FOUND = 'LOGIN_NOT_FOUND';        #Login não encontrado
FAIL_UPLOAD = 'FAIL_UPLOAD'					#Erro ao recber um upload de um arquivo
SUCESS_UPLOAD = 'SUCESS_UPLOAD'				#Upload de arquivo feito com sucsesso



login = False					 	#Verfica se o usuário está conectado ao servidor
user = ''							#Usuário que está logado no momento da execução

#Tenta fazer conexão com o servidor
try:
	ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ftp_socket.connect(addr)
	print('Conectado com sucesso!!')
except:
	print('Erro ao conetar ao com o servidor')
	exit(1)

while True:

	try:
		ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ftp_socket.connect(addr)
	except:
		print('Erro ao conetar ao com o servidor')
		exit(1)

	request = raw_input('$> ')	#Requisição do cliente

	content_request = str(request).split(' ')

	if content_request[0] == 'login':	#Requisição de login

		if login == True: 				#Usuário já está logado
			print('Você já está Logado')
			continue

		ftp_socket.send(request)		#Envia a requisição
		msg = ftp_socket.recv(1024)		#Recebe a resposta
		id_msg = str(msg.decode('utf-8'))

		if id_msg == LOGIN_EXISTS:	#Login Existe
			print('Login Realizado com sucesso')
			login = True
			user = content_request[1]
			continue
		else:
			print('Login não existente: Usuário ou senha Inválidos')	#Login não existe
			continue

	elif content_request[0] == 'ls':
		
		#Verficar se o cliente está logado
		if login == False:
			print('Você não tem permissao para o comando: ' + content_request[0] + ' - Faça o login $> login <user> <passwd>')
			continue

		request += ' ' + user
		ftp_socket.send(request)		#Eniva a requisição

		full_msg = ''
		while True:						#Recebe os bytes resposta

			msg = ''
			msg = ftp_socket.recv(1024)

			full_msg += msg.decode('utf-8')

			if len(msg) < 1024:
				break

		print('')
		print(full_msg)

	elif content_request[0] == 'get':

		#Verficar se o cliente está logado
		if login == False:
			print('Você não tem permissao para o comando: ' + content_request[0] + ' - Faça o login $> login <user> <passwd>')
			continue

		#Verficar se o arquivo existe
		ftp_socket.send(request)			#Envia a requisição
		msg = ftp_socket.recv(1024)			#Recbe a resposta se o arquivo existe ou não

		if msg.decode('utf-8') == FILE_EXISTS:
			
			print('Arquivo Disponível no servidor - Inicando Download')

			#Renicia a conexão com o servidor para iniciar o download
			try:	
				ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				ftp_socket.connect(addr)
			except:
				print('Erro ao conetar ao com o servidor')
				exit(1)

			#Cria a requisição de dowload
			request = 'get_ ' + content_request[1] + ' ' + user
			ftp_socket.send(request)

			#Recebe os bytes do arquivo
			full_msg = ''
			while True:

				msg_file = ftp_socket.recv(1000000)
				full_msg += msg_file

				if len(msg) < 1000000:
					break

			if full_msg == CONTENT_NOT_AVAILBE:	#Não foi possível fazer download de algum pacote do arquivo
				print('Erro no download do arquivo')
				continue

			#Cria o arquivo no cliente
			try:
				os.mkdir(r'Files')
			except:
				pass

			if len(content_request) > 2: #Concatena os espaços da requisição
				for i in range(2, len(content_request)):
					content_request[1] += ' ' + content_request[i]

			try:	#Escreve no arquivo o conteúdo recebido do servidor
				with open('Files/' + str(content_request[1]), 'wb') as file:
					file.write(full_msg)
			except:
				print('Falha ao fazer download de arquivo: ' + str(content_request[1]))

			print('Download Concluído com sucesso')

		else:
			print('Arquivo não Disponível no servidor')

	elif content_request[0] == 'q' or content_request[0] == 'quit':
		ftp_socket.close()
		exit(0)

	elif content_request[0] == 'put':	#Comando para fazer upload de um arquivo para o servidor

		if len(content_request) > 2: #Concatena os espaços da requisição
			for i in range(2, len(content_request)):
				content_request[1] += ' ' + content_request[i]

		exists = False
		try: #Verificar se o arquivo está local do cliente
			with open('Files/' + content_request[1], 'rb') as file:
				msg_file = file.read()
				exists = True
		except:
			exists = False
			continue

		if exists == True:	#Encontrou o arquivo, avisa o servidor que o client irá realizar um 'PUT'
			ftp_socket.send(content_request[0])
		else:				#Não encontrou o arquivo
			print('Arquivo não encontrado')
			continue

		msg = ftp_socket.recv(1024)

		if msg.decode('utf-8') == 'OK':

			#Renicia a conexão com o servidor para iniciar o upload
			try:	
				ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				ftp_socket.connect(addr)
			except:
				print('Erro ao conetar ao com o servidor')
				exit(1)

			print('Relaziando upload do arquivo ' + content_request[1])

			request = 'put_ ' + content_request[1] + ' ' +  msg_file + ' ' + user
			ftp_socket.send(request) 		#Envia a requisição

			ftp_socket.send(msg_file) 		#Envia a menssagem com o conteúdo do arquivo

			success = ftp_socket.recv(1024)	#Rece a resposta do servidor sobre o upload

			if success == 'SUCESS_UPLOAD':
				print('Upload terminado com sucesso!')
			else:
				print('Falha ao fazer Upload do arquivo ' + content_request[1])
				continue

		else:
			print('Falha ao fazer Upload do arquivo ' + content_request[1])
			continue

	else:
		print('Comando não reconhecido: ' + str(content_request[0]))