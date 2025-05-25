#PROJETO RAD PYTHON

##COMO INSTALAR
-Instale a versão mais recente do python
https://www.python.org/downloads/

-Utilize a funcionalidade do pip para instalar essas duas bibliotecas
pip install customtkinter(Biblioteca customizada do tkinter)
pip install pillow(Biblioteca capaz de carregar imagens no python)

##Descrição do projeto 
Desenvolvemos uma aplicação para o controle de aulas particulares 
agendadas, na qual o professor cadastrado no sistema possui a visão das
aulas pendentes em um determinado período.

##Funcionalidades

Possuímos uma tela de login, cadastro e edição de usuário, vinculada a um 
banco de dados SQLite, que utiliza criptografia MD5 por meio da biblioteca 
hashlib, armazenando apenas a senha criptografada no banco de dados.

<img src="./ReadmeImages/loginScreen.png"><\img>
<img src="./ReadmeImages/signup_screen.png"><\img>

Possuímos, em nossa tela principal, uma tabela na qual o banco de dados retorna as
aulas que o professor possui marcadas, exibindo o nome, o dia, o horário e, inclusive,
o endereço do aluno.

Logo acima, pode-se visualizar também um pequeno formulário para o cadastro de 
novos alunos.
A tela recebe o professor com uma mensagem de boas-vindas e, à direita, apresenta a 
opção de editar algum dado da conta do professor.

<img src="./ReadmeImages/main_screen.png"><\img>