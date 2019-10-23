import sqlite3

conn = sqlite3.connect('user.db')
cursor = conn.cursor()

#criando a tabela de usuarios
cursor.execute("""
CREATE TABLE user(	
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENET,
	login VARCHAR(32) NOT NULL,
	passwd VARCHAR(32) NOT NULL
	);
	""")
print('Tabela criada com sucesso')