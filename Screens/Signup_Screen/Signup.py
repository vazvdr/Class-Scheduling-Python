import customtkinter as ctk
from tkinter import messagebox
from Model.Usuario import User
from database.db import inserir_usuario
from Screens.Login_Screen import login as logi
import re
import hashlib

def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

def criptografar_senha(senha):
    return hashlib.md5(senha.encode()).hexdigest()

def signup_screen():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()
    app.geometry("300x400")
    app.title("Cadastro")
    app.resizable(width=False, height=False)
    app.eval('tk::PlaceWindow . center')

    def kill_screen():
        app.destroy()

    label_title1 = ctk.CTkLabel(app, text="Cadastro", font=ctk.CTkFont(size=20, weight="bold"))
    label_title1.pack(pady=30)

    entry_name = ctk.CTkEntry(app, placeholder_text="Por Favor, Insira seu Nome", width=172)
    entry_name.pack(pady=10)

    entry_email = ctk.CTkEntry(app, placeholder_text="Por Favor, Insira seu Email", width=172)
    entry_email.pack(pady=10)

    entry_password = ctk.CTkEntry(app, placeholder_text="Por Favor, Insira sua Senha", show="*", width=172)
    entry_password.pack(pady=10)

    entry_password_confirm = ctk.CTkEntry(app, placeholder_text="Por Favor, Confirme sua Senha", show="*", width=172)
    entry_password_confirm.pack(pady=10)

    def submit():
        name = entry_name.get()
        email = entry_email.get()
        password = entry_password.get()
        confirm_password = entry_password_confirm.get()

        if not name or not email or not password:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos!")
            return

        if not validar_email(email):
            messagebox.showerror("Erro", "Email inválido! Por favor, insira um email válido.")
            return

        if password != confirm_password:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return

        senha_criptografada = criptografar_senha(password)
        novo_usuario = User(name, email, senha_criptografada)

        if inserir_usuario(novo_usuario):
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            app.destroy()
            logi.login_screen()
        else:
            messagebox.showerror("Erro", "Email já cadastrado!")

    button_submit = ctk.CTkButton(app, text="Cadastrar", command=submit, width=172, fg_color="#023020")
    button_submit.pack(pady=10)

    button_back = ctk.CTkButton(app, text="Voltar", command=lambda: (kill_screen(), logi.login_screen()), width=172, fg_color="#333333")
    button_back.pack()

    app.mainloop()
   
# Functions
def submit(entry_name,entry_email,entry_password):
    name = entry_name.get()
    email = entry_email.get()
    password = entry_password.get()
    messagebox.showinfo("Form Submitted", f"Name:{name}\n Email: {email}\nPassword: {'*' * len(password)}")

def login_screen():
    logi.login_screen()
