from database import conectar

class Agendamento:
    def __init__(self, id=None, usuario_id=None, data=None, horario=None, profissional=None):
        self.id = id
        self.usuario_id = usuario_id
        self.data = data
        self.horario = horario
        self.profissional = profissional

    @staticmethod
    def criar_tabela():
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

    @staticmethod
    def existe(profissional, data, horario):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM agendamentos
            WHERE profissional = ? AND data = ? AND horario = ?
        """, (profissional, data, horario))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] > 0

    def salvar(self):
        if Agendamento.existe(self.profissional, self.data, self.horario):
            return False
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO agendamentos (usuario_id, data, horario, profissional)
            VALUES (?, ?, ?, ?)
        """, (self.usuario_id, self.data, self.horario, self.profissional))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def listar_por_usuario(usuario_id):
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

    def atualizar(self):
        conn = conectar()
        cursor = conn.cursor()

        # Evita conflito com outro agendamento no mesmo horário
        cursor.execute("""
            SELECT id FROM agendamentos
            WHERE profissional = ? AND data = ? AND horario = ?
        """, (self.profissional, self.data, self.horario))
        resultado = cursor.fetchone()
        if resultado and resultado[0] != self.id:
            conn.close()
            return False

        cursor.execute("""
            UPDATE agendamentos
            SET data = ?, horario = ?, profissional = ?
            WHERE id = ?
        """, (self.data, self.horario, self.profissional, self.id))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def deletar(agendamento_id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM agendamentos WHERE id = ?", (agendamento_id,))
        conn.commit()
        conn.close()
