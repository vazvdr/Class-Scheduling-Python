
import sqlite3
from database import conectar


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