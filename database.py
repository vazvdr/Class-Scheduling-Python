import sqlite3

def conectar():
    return sqlite3.connect("usuarios.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def cadastrar_usuario(nome, email, senha):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def atualizar_usuario(usuario_id, email, senha):
    try:
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM usuarios WHERE email = ? AND id != ?", (email, usuario_id))
        if cursor.fetchone():
            conn.close()
            return False

        cursor.execute(
            "UPDATE usuarios SET email = ?, senha = ? WHERE id = ?",
            (email, senha, usuario_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Erro ao atualizar usuário:", e)
        return False

def deletar_usuario(usuario_id):
    try:
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM agendamentos WHERE usuario_id = ?", (usuario_id,))
        
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Erro ao deletar usuário:", e)
        return False


def verificar_login(email, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
    user = cursor.fetchone()
    conn.close()
    return user

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

def criar_tabela_profissionais():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profissionais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def listar_profissionais():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM profissionais")
    resultados = [row[0] for row in cursor.fetchall()]
    conn.close()
    return resultados

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

def listar_agendamentos_por_data(data):
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, data, horario, profissional
        FROM agendamentos
        WHERE data = ?
    """, (data,))

    agendamentos = cursor.fetchall()
    conexao.close()
    return agendamentos

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
