import sqlite3

conn = sqlite3.connect('usuario.db')
cursor = conn.cursor()

#criando a tabela de usuarios

cursor.execute("""
CREATE TABLE users(	
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	login VARCHAR(32) NOT NULL,
	passwd VARCHAR(32) NOT NULL
	);
	""")
print('Tabela criada com sucesso')

#Adicionando usuário administrador
cursor.execute("""
INSERT INTO users (login, passwd)
VALUES ('admin', 'admin')
""")

conn.commit()
conn.close()