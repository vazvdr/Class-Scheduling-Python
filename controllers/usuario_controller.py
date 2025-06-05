from models.usuario_model import Usuario

def criar_tabela():
    Usuario.criar_tabela()

def cadastrar_usuario(nome, email, senha):
    usuario = Usuario(nome=nome, email=email, senha=senha)
    return usuario.salvar()

def atualizar_usuario(usuario_id, email, senha):
    usuario = Usuario(id=usuario_id, email=email, senha=senha)
    return usuario.atualizar()

def deletar_usuario(usuario_id):
    return Usuario.deletar(usuario_id)

def verificar_login(email, senha):
    return Usuario.verificar_login(email, senha)
