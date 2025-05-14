import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from database import (
    criar_tabela,
    criar_tabela_agendamentos,
    cadastrar_usuario,
    verificar_login,
    salvar_agendamento,
    listar_agendamentos_por_usuario
)

criar_tabela()

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

    janela = tk.Tk()
    janela.title("Login")
    janela.geometry("400x300")
    janela.resizable(True, True)

    frame = tk.Frame(janela)
    frame.pack(expand=True)

    tk.Label(frame, text="Email").grid(row=0, column=0, pady=5, sticky="w")
    entry_email = tk.Entry(frame, width=30)
    entry_email.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Senha").grid(row=1, column=0, pady=5, sticky="w")
    entry_senha = tk.Entry(frame, show="*", width=30)
    entry_senha.grid(row=1, column=1, pady=5)

    tk.Button(frame, text="Entrar", command=fazer_login).grid(row=2, column=1, pady=10, sticky="e")
    tk.Button(frame, text="Cadastrar", command=ir_para_cadastro).grid(row=2, column=0, pady=10)

    janela.mainloop()

def tela_cadastro():
    def fazer_cadastro():
        nome = entry_nome.get()
        email = entry_email.get()
        senha = entry_senha.get()
        sucesso = cadastrar_usuario(nome, email, senha)
        if sucesso:
            messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
            janela.destroy()
            tela_login()
        else:
            messagebox.showerror("Erro", "Email já cadastrado.")

    janela = tk.Tk()
    janela.title("Cadastro")
    janela.geometry("400x350")
    janela.resizable(True, True)

    frame = tk.Frame(janela)
    frame.pack(expand=True)

    tk.Label(frame, text="Nome").grid(row=0, column=0, pady=5, sticky="w")
    entry_nome = tk.Entry(frame, width=30)
    entry_nome.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Email").grid(row=1, column=0, pady=5, sticky="w")
    entry_email = tk.Entry(frame, width=30)
    entry_email.grid(row=1, column=1, pady=5)

    tk.Label(frame, text="Senha").grid(row=2, column=0, pady=5, sticky="w")
    entry_senha = tk.Entry(frame, show="*", width=30)
    entry_senha.grid(row=2, column=1, pady=5)

    tk.Button(frame, text="Cadastrar", command=fazer_cadastro).grid(row=3, column=1, pady=10, sticky="e")

    janela.mainloop()

def tela_agendamento(usuario_id, nome_usuario):
    def salvar():
        data = entry_data.get()
        horario = entry_horario.get()
        profissional = entry_profissional.get()

        if data and horario and profissional:
            salvar_agendamento(usuario_id, data, horario, profissional)
            messagebox.showinfo("Sucesso", "Agendamento realizado com sucesso!")
            entry_data.delete(0, tk.END)
            entry_horario.delete(0, tk.END)
            entry_profissional.delete(0, tk.END)
            atualizar_lista()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos.")

    def atualizar_lista():
        for item in tree.get_children():
            tree.delete(item)
        agendamentos = listar_agendamentos_por_usuario(usuario_id)
        for agendamento in agendamentos:
            tree.insert("", "end", values=agendamento)

    janela = tk.Tk()
    janela.title("Agendar Aula")
    janela.geometry("700x500")
    janela.resizable(True, True)

    frame = tk.Frame(janela, padx=10, pady=10)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text=f"Agendamentos - {nome_usuario}", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame, text="Data (dd/mm/aaaa):").grid(row=1, column=0, sticky="w")
    entry_data = tk.Entry(frame, width=30)
    entry_data.grid(row=1, column=1, pady=5)

    tk.Label(frame, text="Horário (ex: 14:00):").grid(row=2, column=0, sticky="w")
    entry_horario = tk.Entry(frame, width=30)
    entry_horario.grid(row=2, column=1, pady=5)

    tk.Label(frame, text="Profissional:").grid(row=3, column=0, sticky="w")
    entry_profissional = tk.Entry(frame, width=30)
    entry_profissional.grid(row=3, column=1, pady=5)

    tk.Button(frame, text="Agendar", command=salvar).grid(row=4, column=1, pady=10, sticky="e")

    # Tabela de agendamentos
    tree = ttk.Treeview(frame, columns=("data", "horario", "profissional"), show="headings")
    tree.heading("data", text="Data")
    tree.heading("horario", text="Horário")
    tree.heading("profissional", text="Profissional")
    tree.grid(row=5, column=0, columnspan=2, pady=10, sticky="nsew")

    # Responsividade
    frame.rowconfigure(5, weight=1)
    frame.columnconfigure(1, weight=1)

    atualizar_lista()
    janela.mainloop()


# Iniciar com a tela de login
tela_login()
