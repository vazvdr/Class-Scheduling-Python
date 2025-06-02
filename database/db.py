import sqlite3
from Model import Usuario
from Model import Agendamento
import hashlib

def create_table():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    # Criação da tabela (executar uma vez)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def inserir_usuario(usuario: Usuario):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO User (name, email, password) VALUES (?, ?, ?)
        ''', (usuario.name, usuario.email, usuario.password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    
def authenticate_user(email, password):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    senha_criptografada = criptografar_senha(password)
    cursor.execute("SELECT * FROM User WHERE email=? AND password=?", (email, senha_criptografada))
    user = cursor.fetchone()
    conn.close()

    return user  # Agora retorna a tupla completa ou None

def criptografar_senha(senha):
    return hashlib.md5(senha.encode()).hexdigest()

def atualizar_usuario(id_usuario, usuario: Usuario):
    try:
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        sql = '''UPDATE User 
                 SET name = ?, email = ?, password = ?
                 WHERE id = ?'''
        cursor.execute(sql, (usuario.name, usuario.email, usuario.password, id_usuario))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao atualizar usuário: {e}")
        return False


#Agendamento
def create_agendamento_table():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Agendamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            endereco TEXT NOT NULL,
            professor TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def inserir_agendamento(agendamento: Agendamento):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO Agendamento (nome, data, horario, endereco,professor) 
            VALUES (?, ?, ?, ?, ?)
        ''', (agendamento.nome, agendamento.data, agendamento.horario, agendamento.endereco,agendamento.professor))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao inserir agendamento: {e}")
        return False
    finally:
        conn.close()


def listar_agendamentos_por_professor(professor):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id,nome, data, horario, endereco, professor FROM Agendamento WHERE professor = ?", 
        (professor,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def deletar_agendamento(agendamento_id: int):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    sql = "DELETE FROM Agendamento WHERE id = ?"
    cursor.execute(sql, (agendamento_id,))
    conn.commit()

def atualizar_agendamento(id_agendamento, agendamento: Agendamento):
    try:
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        sql = '''UPDATE Agendamento 
                 SET nome = ?, data = ?, horario = ?, endereco = ?, professor = ?
                 WHERE id = ?'''
        cursor.execute(sql, (agendamento.nome, agendamento.data, agendamento.horario, agendamento.endereco, agendamento.professor, id_agendamento))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao atualizar agendamento: {e}")