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

print('Server Started PORT: '+ str(PORT))

while True:
	
	print('Aguardando conexao')
	conex, client = s.accept()

	#Inicia a thread do server
	t = ThreadServer(conex, s)
	t.start()