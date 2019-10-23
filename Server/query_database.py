import sqlite3

conn = sqlite3.connect('usuario.db')
cursor = conn.cursor()

#criando a tabela de usuarios
'''
cursor.execute("""
CREATE TABLE users(	
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	login VARCHAR(32) NOT NULL,
	passwd VARCHAR(32) NOT NULL
	);
	""")
print('Tabela criada com sucesso')
'''

cursor.execute("""
INSERT INTO users (login, passwd)
VALUES ('admin', 'admin')
""")

cursor.execute("""
INSERT INTO users (login, passwd)
VALUES ('fulano1', '123')
""")

cursor = conn.cursor()
cursor.execute("""
		SELECT * FROM users;
	""")

x = cursor.fetchall()
print(x)

conn.close()