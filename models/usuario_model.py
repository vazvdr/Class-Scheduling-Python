import sqlite3
from database import conectar

class Usuario:
    def __init__(self, id=None, nome=None, email=None, senha=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

    @staticmethod
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

    def salvar(self):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                (self.nome, self.email, self.senha)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def atualizar(self):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id FROM usuarios WHERE email = ? AND id != ?",
                (self.email, self.id)
            )
            if cursor.fetchone():
                return False
            cursor.execute(
                "UPDATE usuarios SET email = ?, senha = ? WHERE id = ?",
                (self.email, self.senha, self.id)
            )
            conn.commit()
            return True
        except Exception as e:
            print("Erro ao atualizar usuário:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def deletar(usuario_id):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM agendamentos WHERE usuario_id = ?", (usuario_id,))
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
            conn.commit()
            return True
        except Exception as e:
            print("Erro ao deletar usuário:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def verificar_login(email, senha):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Usuario(id=row[0], nome=row[1], email=row[2], senha=row[3])
        return None
