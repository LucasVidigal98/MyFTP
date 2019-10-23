# Protocolo-FTP
Trabalho de Implementação do protocolo FTP proposto pela disciplina de Redes de Computadores do Curso de Ciência da computação da UFSJ

O objetivo do primeiro trabalho prático é implementar um protocolo FTP simples 
utilizando a biblioteca sockets. O serviço FTP (File Transport Protocol) realiza
 a transferência de arquivos entre computadores clientes e servidores em ambas 
direções.

O protocolo MyFTP implementa os seguintes comandos:

+ login: o usuário digita o login e senha para ter acesso ao serviço. 
  Os usuários e suas respectivas senhas devem estar cadastrados no servidor. 
  O protocolo MyFTP deve tratar e não deixar que usuários não cadastrados no 
  servidor tenham acesso ao sistema. Não é necessário tratar o cadastro do 
  usuário e senha. Eles já existem no servidor. 

+ put: O comando put envia um arquivo que está armazenado no cliente para o 
  servidor. A sintaxe do comando é: put nome_arquivo. 

+ get: O comando get faz com que o cliente receba um arquivo que está armazenado
  no servidor. A sintaxe do comando é: get nome_arquivo.

+ ls: O comando ls busca o nome de todos os arquivos na pasta do servidor e 
  mostra para o cliente.


Todos os comandos devem tratam possíveis erros, tais como: usuário/senha 
incorreta ou nome de arquivo inexistente. Não navega nas pastas. 
Não Suporta múltiplos usuários conectados no servidor. 

Cliente esá rodando na versão 2 do python e, o servidor na versão 3. Ao fazer put ou get de um arquivo utilizar o nome + a extenção do arquivo. Ex: "MyFile.pdf".
