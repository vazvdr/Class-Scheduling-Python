import customtkinter as ctk
from tkinter import messagebox
from Model.Usuario import User
from database.db import atualizar_usuario
from Screens.Login_Screen import login as logi
import re
import hashlib

def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

def criptografar_senha(senha):
    return hashlib.md5(senha.encode()).hexdigest()

def edit_user_screen(usuario_existente):
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()
    app.geometry("300x400")
    app.title("Editar Usuário")
    app.resizable(width=False, height=False)
    app.eval('tk::PlaceWindow . center')

    def kill_screen():
        app.destroy()

    label_title1 = ctk.CTkLabel(app, text="Editar Usuário", font=ctk.CTkFont(size=20, weight="bold"))
    label_title1.pack(pady=30)

    entry_name = ctk.CTkEntry(app, placeholder_text="Nome", width=172)
    entry_name.insert(0, usuario_existente[1])
    entry_name.pack(pady=10)

    entry_email = ctk.CTkEntry(app, placeholder_text="Email", width=172)
    entry_email.insert(0, usuario_existente[2])
    entry_email.pack(pady=10)

    entry_password = ctk.CTkEntry(app, placeholder_text="Nova Senha (opcional)", show="*", width=172)
    entry_password.pack(pady=10)

    entry_password_confirm = ctk.CTkEntry(app, placeholder_text="Confirme a Nova Senha", show="*", width=172)
    entry_password_confirm.pack(pady=10)

    def submit_update():
        name = entry_name.get()
        email = entry_email.get()
        password = entry_password.get()
        confirm_password = entry_password_confirm.get()

        if not name or not email:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios!")
            return

        if not validar_email(email):
            messagebox.showerror("Erro", "Email inválido! Por favor, insira um email válido.")
            return

        if password and password != confirm_password:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return

        senha_criptografada = criptografar_senha(password) if password else usuario_existente[3]

        usuario_atualizado = User(name, email, senha_criptografada)

        if atualizar_usuario(usuario_existente[0], usuario_atualizado):
            messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
            app.destroy()
            logi.login_screen()
        else:
            messagebox.showerror("Erro", "Não foi possível atualizar o usuário. Verifique se o email já não está em uso.")

    button_submit = ctk.CTkButton(app, text="Salvar Alterações", command=submit_update, width=172, fg_color="#023020")
    button_submit.pack(pady=10)

    button_back = ctk.CTkButton(app, text="Voltar", command=lambda: (kill_screen(), logi.login_screen()), width=172, fg_color="#333333")
    button_back.pack()

    app.mainloop()

   
def login_screen():
    logi.login_screen()
