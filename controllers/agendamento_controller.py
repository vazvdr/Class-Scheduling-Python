from database import conectar


def criar_tabela_agendamentos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            profissional TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)
    conn.commit()
    conn.close()

def existe_agendamento(profissional, data, horario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM agendamentos
        WHERE profissional = ? AND data = ? AND horario = ?
    """, (profissional, data, horario))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] > 0

def salvar_agendamento(usuario_id, data, horario, profissional):
    if existe_agendamento(profissional, data, horario):
        return False
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO agendamentos (usuario_id, data, horario, profissional)
        VALUES (?, ?, ?, ?)
    """, (usuario_id, data, horario, profissional))
    conn.commit()
    conn.close()
    return True

def listar_agendamentos_por_usuario(usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, data, horario, profissional FROM agendamentos
        WHERE usuario_id = ?
        ORDER BY data, horario
    """, (usuario_id,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def atualizar_agendamento(agendamento_id, data, horario, profissional):
    if existe_agendamento(profissional, data, horario):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM agendamentos
            WHERE profissional = ? AND data = ? AND horario = ?
        """, (profissional, data, horario))
        resultado = cursor.fetchone()
        if resultado and resultado[0] != agendamento_id:
            conn.close()
            return False
        conn.close()

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE agendamentos
        SET data = ?, horario = ?, profissional = ?
        WHERE id = ?
    """, (data, horario, profissional, agendamento_id))
    conn.commit()
    conn.close()
    return True

def deletar_agendamento(agendamento_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM agendamentos WHERE id = ?", (agendamento_id,))
    conn.commit()
    conn.close()