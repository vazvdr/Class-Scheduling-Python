import sqlite3
from Model import Usuario
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

    return user is not None

def criptografar_senha(senha):
    return hashlib.md5(senha.encode()).hexdigest()