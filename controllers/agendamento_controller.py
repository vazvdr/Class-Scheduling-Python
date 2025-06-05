from models.agendamento_model import Agendamento

def criar_tabela_agendamentos():
    Agendamento.criar_tabela()

def salvar_agendamento(usuario_id, data, horario, profissional):
    agendamento = Agendamento(
        usuario_id=usuario_id,
        data=data,
        horario=horario,
        profissional=profissional
    )
    return agendamento.salvar()

def listar_agendamentos_por_usuario(usuario_id):
    return Agendamento.listar_por_usuario(usuario_id)

def atualizar_agendamento(agendamento_id, data, horario, profissional):
    agendamento = Agendamento(
        id=agendamento_id,
        data=data,
        horario=horario,
        profissional=profissional
    )
    return agendamento.atualizar()

def deletar_agendamento(agendamento_id):
    return Agendamento.deletar(agendamento_id)
