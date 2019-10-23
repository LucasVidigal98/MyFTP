# -*- coding: UTF-8 -*-
import socket
from OperationsServer import *
import random
import os
from thread_server import ThreadServer

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

	#Inicia a thread do server
	t = ThreadServer(0, request, conex)
	t.start()