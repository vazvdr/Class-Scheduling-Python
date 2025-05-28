import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from screens.tela_agendamento import tela_agendamento
from screens.tela_cadastro import tela_cadastro
from controllers.usuario_controller import verificar_login

def tela_login():
    def fazer_login():
        email = entry_email.get()
        senha = entry_senha.get()
        user = verificar_login(email, senha)
        if user:
            messagebox.showinfo("Sucesso", f"Bem-vindo, {user[1]}!")
            janela.destroy()
            tela_agendamento(user[0], user[1])
        else:
            messagebox.showerror("Erro", "Email ou senha inválidos.")

    def ir_para_cadastro():
        janela.destroy()
        tela_cadastro()

    janela = tk.Tk() # type: ignore
    janela.title("Login")
    janela.geometry("600x600")
    janela.configure(bg="black")
    janela.resizable(True, True)

    frame = tk.Frame(janela, bg="black")
    frame.pack(expand=True)

    tk.Label(frame, text="Login", font=("Helvetica", 16, "bold"), bg="black", fg="white").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame, text="Email", bg="black", fg="white").grid(row=1, column=0, pady=5, sticky="w")
    entry_email = tk.Entry(frame, width=30, bg="gray20", fg="white", insertbackground="white")
    entry_email.grid(row=1, column=1, pady=5)

    tk.Label(frame, text="Senha", bg="black", fg="white").grid(row=2, column=0, pady=5, sticky="w")
    entry_senha = tk.Entry(frame, show="*", width=30, bg="gray20", fg="white", insertbackground="white")
    entry_senha.grid(row=2, column=1, pady=5)

    tk.Button(frame, text="Entrar", command=fazer_login, bg="blue", fg="white").grid(row=3, column=1, pady=10, sticky="e")
    tk.Button(frame, text="Cadastrar", command=ir_para_cadastro, bg="green", fg="white").grid(row=3, column=0, pady=10)

    janela.mainloop()