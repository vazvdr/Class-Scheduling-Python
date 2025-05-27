import customtkinter as ctk
from Screens.Login_Screen import login as logi
from database import db

if __name__ == "__main__":
    print("IT WORKS!!!")
    db.create_table()
    print("Tabela usuário criado")
    db.create_agendamento_table()
    print("Tabela agendamento criado")
    logi.login_screen()