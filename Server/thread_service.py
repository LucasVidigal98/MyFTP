# -*- coding: UTF-8 -*-
import socket
from OperationsServer import *
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

class ThreadService(threading.Thread):

	def __init__(self, id_thread, request, conex, s):
		super(ThreadService, self).__init__()
		self.id_thread = id_thread
		self.request = request						#Requisição
		self.conex = conex 							#Conexao com o cliente
		self.s = s 									#Socket da conexão


	def run(self):

		if self.id_thread == 0:	#Thread get

			if len(self.request) > 2: #Concatena os espaços da requisição
				for i in range(2, len(self.request)-1):
					self.request[1] += ' ' + self.request[i]

			content_file = read_file(self.request[1], self.request[len(self.request)-1])	#Recece o conteúdo do arquivo

			if content_file == False:				#Falso = Não foi possível baixar o conteúdo
				self.conex.send(bytes(CONTENT_NOT_AVAILBE, 'utf-8'))
			else:
				self.conex.send(bytes(content_file))

		else:		#Thread put	

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

			success = upload_file(self.request[1], full_msg, self.request[len(self.request)-1])	#Salva o arquivo no diretório do cliente

			if success == True:
				self.conex.send(bytes(SUCESS_UPLOAD, 'utf-8'))
			else:
				self.conex.send(bytes(FAIL_UPLOAD, 'utf-8'))