# -*- coding: UTF-8 -*-
import socket
from OperationsServer import *
import random
import os
import threading

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

class ThreadServer(threading.Thread):

	def __init__(self, id_Thread, request, conex):
		super(ThreadServer, self).__init__()
		self.id_Thread = id_Thread 					#id da thread
		self.request = request						#Requição recebida
		self.conex = conex							#Conexão com o cliente


	def run(self):

		if self.id_Thread == 0: #Thread que abre a conexão com cliente, id_Threadentid_Threadica a requisição e encaminha para a thread específica

			if self.request[0] == 'login':	#Aciona a thread de valid_Threadação de login
				t = ThreadServer(1, self.request, self.conex)
				t.start()

			elif self.request[0] == 'ls':	#Aciona a thread para o comando ls
				t = ThreadServer(2, self.request, self.conex)
				t.start()

			elif self.request[0] == 'get': 	#Aciona a thread para o comando get
				t = ThreadServer(3, self.request, self.conex)
				t.start()

			elif self.request[0] == 'get_': 	#Aciona a thread para o comando get_
				t = ThreadServer(4, self.request, self.conex)
				t.start()

			elif self.request[0] == 'put'	:#Aciona a thread para o comando put
				t = ThreadServer(5, self.request, self.conex)
				t.start()

		elif self.id_Thread == 1:
			
			str_request = ''
			for item in self.request:
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


		elif self.id_Thread == 2:	#Thread ls

			str_list = list_dir(self.request[1])

			self.conex.send(bytes(str_list, 'utf-8')) #Envia a listagem do diretorio

		elif self.id_Thread == 3: #Thread get

			if len(self.request) > 2: #Concatena os espaços da requisição
				for i in range(2, len(self.request)-1):
					self.request[1] += ' ' + self.request[i]
					print(self.request[1])
				
				print(self.request)
			try:
				file_valid_Threadation = is_file(self.request[1], self.request[len(self.request)-1])

				if file_valid_Threadation == True:		#Arquivo existe
					self.conex.send(bytes(FILE_EXISTS, 'utf-8'))
				else:							#Arquivo não existe
					self.conex.send(bytes(FILE_NOT_FOUND, 'utf-8'))
			except:
				self.conex.send(bytes(FILE_NOT_FOUND, 'utf-8'))

		elif self.id_Thread == 4: #Thread get_

			if len(self.request) > 2: #Concatena os espaços da requisição
				for i in range(2, len(self.request)-1):
					self.request[1] += ' ' + self.request[i]

			content_file = read_file(self.request[1], self.request[len(self.request)-1])	#Recece o conteúdo do arquivo

			if content_file == False:				#Falso = Não foi possível baixar o conteúdo
				self.conex.send(bytes(CONTENT_NOT_AVAILBE, 'utf-8'))
			else:
				self.conex.send(bytes(content_file))

		elif self.id_Thread == 5: #Thread put

			print('Aguardando conexao ... put')
			self.conex, client = s.accept()
			print('Conectado ... put')
			print('Aguardando Requisição ... put')
			#Espera requisição
			
			full_msg = bytes('', 'utf-8')
			while True:		#Recebe os bytes do arquivo de upload
				
				msg = self.conex.recv(1000000)
				full_msg += msg

				if len(msg) < 1000000:
					break

			success = upload_file(self.request[1], full_msg, self.request[len(self.request)-1])	#Salva o arquivo no diretório do cliente

			if success == True:
				self.conex.send(bytes(SUCESS_UPLOAD, 'utf-8'))
			else:
				self.conex.send(bytes(FAIL_UPLOAD, 'utf-8'))