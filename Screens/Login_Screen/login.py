import customtkinter as ctk
from tkinter import messagebox
from Screens.Signup_Screen import Signup as sign
from Screens.Appointment_Screen import Appointment as appo
from database.db import authenticate_user

def login_screen():
    def login_screen_switch():
        app.destroy()

    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()
    app.geometry("300x400")
    app.title("Login")
    app.resizable(width=False, height=False)
    app.eval('tk::PlaceWindow . center')

    label_title = ctk.CTkLabel(app, text="Bem-Vindo", font=ctk.CTkFont(size=20, weight="bold"))
    label_title.pack(pady=40)

    entry_email = ctk.CTkEntry(app, placeholder_text="Por Favor, Insira seu Email", width=172)
    entry_email.pack(pady=10)

    entry_password = ctk.CTkEntry(app, placeholder_text="Por Favor, Insira sua Senha", show="*", width=172)
    entry_password.pack(pady=10)

    button_submit = ctk.CTkButton(
        app, text="Entrar", 
        command=lambda: submit(entry_email, entry_password, app), 
        width=172
    )
    button_submit.pack(pady=10)

    button_clear = ctk.CTkButton(
        app, text="Não possui cadastro?", 
        command=lambda: (login_screen_switch(), signUp_button()), 
        fg_color="#333333", width=172
    )
    button_clear.pack(pady=5)

    app.mainloop()

def submit(entry_email, entry_password, app):
    email = entry_email.get()
    password = entry_password.get()
    
    if email != "" and password != "":
        user = authenticate_user(email, password)
        if user:
            nome = user[1]  # Supondo que o nome é a segunda coluna do SELECT
            messagebox.showinfo("Login realizado", f"Bem-vindo, {nome}!")
            app.destroy()
            appo.appointment_screen(nome)
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos.")
    else:
        messagebox.showwarning("Campos vazios", "Por favor, preencha todos os campos.")

def signUp_button():
    sign.signup_screen()