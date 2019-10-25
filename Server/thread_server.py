# -*- coding: UTF-8 -*-
import socket
from OperationsServer import *
import os
import threading
from thread_service import ThreadService

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
ADD_SUCCESS = 'ADD_SUCCESS'					#Usuário adicionado com sucesso no servidor
ADD_FAIL = 	'ADD_FAIL'						#Falha ao adicionar o usuário no sistema
RM_SUCCES = 'RM_SUCCES'						#Usuário removido com sucesso
RM_FAIL = 'RM_FAIL'							#Falha ao remover usuário
PASSWD_SUCCESS = 'PASSWD_SUCCESS'			#Sucesso ao redefinir senha
PASSWD_FAIL = 'PASSWD_FAIL'					#Falha ao redefinir senha

class ThreadServer(threading.Thread):

	def __init__(self, conex, s):
		super(ThreadServer, self).__init__()
		self.conex = conex 							#Conexao com o cliente
		self.s = s 									#Socket da conexão


	def run(self):

		print('Aguardando Requisição')
		#Espera requisição
		req = self.conex.recv(1024)
		request = str(req.decode('utf-8')).split(' ')

		if request[0] == 'login':

			str_request = ''
			for item in request:
				str_request += ' ' + str(item) 

			validation = login_validator(str_request)
			
			if validation == True:	#Login existe
				try:
					#Se for o primeiro login desse usuário no servidor criar um diretório para ele	
					os.mkdir('Users_dir/' + request[1])
				except:
					pass
				self.conex.send(bytes(LOGIN_EXISTS, 'utf-8'))
			else:					#Login não existe
				self.conex.send(bytes(LOGIN_NOT_FOUND, 'utf-8'))

		elif request[0] == 'ls':

			str_list = list_dir(request[1])

			self.conex.send(bytes(str_list, 'utf-8')) #Envia a listagem do diretorio

		elif request[0] == 'get':

			if len(request) > 2: #Concatena os espaços da requisição
				for i in range(2, len(request)-1):
					request[1] += ' ' + request[i]
				
			try:
				file_valid_Threadation = is_file(request[1], request[len(request)-1])

				if file_valid_Threadation == True:		#Arquivo existe
					self.conex.send(bytes(FILE_EXISTS, 'utf-8'))
				else:							#Arquivo não existe
					self.conex.send(bytes(FILE_NOT_FOUND, 'utf-8'))
			except:
				self.conex.send(bytes(FILE_NOT_FOUND, 'utf-8'))

		elif request[0] == 'get_':
			
			t = ThreadService(0, request, self.conex, self.s)	#Aciona a thread de download
			t.start()

			'''
			if len(request) > 2: #Concatena os espaços da requisição
				for i in range(2, len(request)-1):
					request[1] += ' ' + request[i]

			content_file = read_file(request[1], request[len(request)-1])	#Recece o conteúdo do arquivo

			if content_file == False:				#Falso = Não foi possível baixar o conteúdo
				self.conex.send(bytes(CONTENT_NOT_AVAILBE, 'utf-8'))
			else:
				self.conex.send(bytes(content_file))
			'''

		elif request[0] == 'put':

			
			t = ThreadService(1, request, self.conex, self.s)	#Aciona a thread de upload
			t.start()
			'''
			print('Aguardando conexao ... put')
			self.conex, client = self.s.accept()
			print('Conectado ... put')
			print('Aguardando Requisição ... put')
			#Espera requisição
				
			full_msg = bytes('', 'utf-8')
			while True:		#Recebe os bytes do arquivo de upload
					
				msg = self.conex.recv(1000000)
				full_msg += msg

				if len(msg) < 1000000:
					break

			success = upload_file(request[1], full_msg, request[len(request)-1])	#Salva o arquivo no diretório do cliente

			if success == True:
				self.conex.send(bytes(SUCESS_UPLOAD, 'utf-8'))
			else:
				self.conex.send(bytes(FAIL_UPLOAD, 'utf-8'))
				'''

		elif request[0] == 'adduser':	#Comando para adicionar um usuário

			if len(request) > 2:
				self.conex.send(bytes(ADD_FAIL, 'utf-8'))

			add = add_user(str(request[1])) #Adiciona o user no banco de dados

			if add == True:
				self.conex.send(bytes(ADD_SUCCESS, 'utf-8'))
			else:
				self.conex.send(bytes(ADD_FAIL, 'utf-8'))

		elif request[0] == 'removeuser':	#Comando para remover um usuário

			if len(request) > 2:
				self.conex.send(bytes(RM_FAIL, 'utf-8'))

			rm = remove_user(str(request[1])) #Remove usuário do banco de dados

			if rm == False:
				self.conex.send(bytes(RM_FAIL, 'utf-8'))
			else:
				#Apaga o diretório do usuário no servidor
				list_files = os.listdir(r'Users_dir/'+request[1]+'/')
				for file in list_files:
					os.remove(r'Users_dir/'+request[1]+'/'+str(file))
				os.rmdir(r'Users_dir/'+request[1]+'/')
				self.conex.send(bytes(RM_SUCCES, 'utf-8'))

		elif request[0] == 'passwd':

			if len(request) > 3:
				self.conex.send(bytes(PASSWD_FAIL, 'utf-8'))

			passwd = passwd_r(str(request[1]), str(request[2]))

			if passwd == False:
				self.conex.send(bytes(PASSWD_FAIL, 'utf-8'))
			else:
				self.conex.send(bytes(PASSWD_SUCCESS, 'utf-8'))