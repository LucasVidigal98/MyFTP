# -*- coding: UTF-8 -*-
import os
import sqlite3

def login_validator(request):

	conn = sqlite3.connect('usuario.db')
	cursor = conn.cursor()

	content_request = request.split()
	login = str(content_request[1])
	passwd = str(content_request[2])
	cursor.execute("""
		SELECT * FROM users
		""")

	for it in cursor.fetchall():
		if it[1] == login:
			if it[2] == passwd:
				conn.close()
				return True

	conn.close()
	return False

def list_dir(user):

	str_file = ''
	found_files = False
	try:
		for name_file in os.listdir(r'Users_dir/'+user):
			found_files = True
			str_file += str(name_file) + '\n'
	except:
		str_file = 'O diretório do servidor está vazio'

	if found_files == False:
		return 'O diretório do servidor está vazio'

	return str_file

def is_file(name_file, user):
	
	try:
		with open('Users_dir/' + user + '/' + str(name_file), 'rb') as file:
			return True
	except:
		return False

def read_file(name_file, user):

	try:
		with open('Users_dir/' + user + '/' + str(name_file), 'rb') as file:
			msg = file.read()
			file.close()
	except:
		return False

	return msg

def upload_file(name_file, content_file, user):

	try:
		with open('Users_dir/' + user + '/' + str(name_file), 'wb') as file:
			file.write(content_file)
			file.close()
	except:
		return False #Não conssegui fazer o upload
	
	return True

def add_user(user):

	conn = sqlite3.connect('usuario.db')
	cursor = conn.cursor()

	#Verfica se usuário já está cadastrado no servidor
	cursor.execute("""
		SELECT * FROM users
		WHERE login = ?
		""", (user,))

	if len(cursor.fetchall()) > 0:	#Encontrou usuário no servidor
		return False

	#Tenta adicionar o user no banco. "pingacomlimao" = senha default para um usuario cadastrado
	tuple_user = (user, 'pingacomlimao')
	try:
		cursor.execute("""
				INSERT INTO users (login, passwd) VALUES (?, ?)
				""", tuple_user)

		conn.commit()
		conn.close()

		return True

	except:
		conn.close()
		return False

def remove_user(user):

	conn = sqlite3.connect('usuario.db')
	cursor = conn.cursor()

	cursor.execute("""
		SELECT * FROM users
		WHERE login = ?
		""", (user,))

	if len(cursor.fetchall()) > 0: #Encontrou usuário no servidor

		#Tenta remover usuário do servidor
		try:
			cursor.execute("""
				DELETE FROM users
				WHERE login = ?
				""", (user,))
			
			conn.commit()
			conn.close()

			return True

		except:
			conn.close()
			return False
	else:
		conn.close()
		return False

def passwd_r(passwd, user):

	conn = sqlite3.connect('usuario.db')
	cursor = conn.cursor()

	cursor.execute("""
		SELECT * FROM users
		WHERE login = ?
		""", (user,))

	if len(cursor.fetchall()) > 0: #Encontrou usuário no servidor
		
		#Redefine a senha
		cursor.execute("""
			UPDATE users
			SET passwd = ?
			WHERE login = ?
			""", (passwd, user))

		conn.commit()
		conn.close()
		return True

	else:
		conn.close()
		return False