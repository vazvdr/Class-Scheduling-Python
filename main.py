import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from database import (
    criar_tabela,
    criar_tabela_agendamentos,
    cadastrar_usuario,
    verificar_login,
    salvar_agendamento,
    listar_agendamentos_por_usuario,
    atualizar_agendamento,
    deletar_agendamento
)

criar_tabela()
criar_tabela_agendamentos()

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
    janela.configure(bg="black")
    janela.resizable(True, True)

    frame = tk.Frame(janela, bg="black")
    frame.pack(expand=True)

    # Título centralizado
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

    def voltar():
        janela.destroy()
        tela_login()

    janela = tk.Tk()
    janela.title("Cadastro")
    janela.geometry("400x350")
    janela.configure(bg="black")
    janela.resizable(True, True)

    frame = tk.Frame(janela, bg="black")
    frame.pack(expand=True)

    # Título centralizado
    tk.Label(frame, text="Cadastro", font=("Helvetica", 16, "bold"), bg="black", fg="white").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame, text="Nome", bg="black", fg="white").grid(row=1, column=0, pady=5, sticky="w")
    entry_nome = tk.Entry(frame, width=30, bg="gray20", fg="white", insertbackground="white")
    entry_nome.grid(row=1, column=1, pady=5)

    tk.Label(frame, text="Email", bg="black", fg="white").grid(row=2, column=0, pady=5, sticky="w")
    entry_email = tk.Entry(frame, width=30, bg="gray20", fg="white", insertbackground="white")
    entry_email.grid(row=2, column=1, pady=5)

    tk.Label(frame, text="Senha", bg="black", fg="white").grid(row=3, column=0, pady=5, sticky="w")
    entry_senha = tk.Entry(frame, show="*", width=30, bg="gray20", fg="white", insertbackground="white")
    entry_senha.grid(row=3, column=1, pady=5)

    tk.Button(frame, text="Cadastrar", command=fazer_cadastro, bg="green", fg="white").grid(row=4, column=1, pady=10, sticky="e")
    tk.Button(frame, text="Voltar", command=voltar, bg="gray30", fg="white").grid(row=4, column=0, pady=10, sticky="w")

    janela.mainloop()

def tela_agendamento(usuario_id, nome_usuario):
    janela = tk.Tk()
    janela.title("Agendamentos")
    janela.geometry("600x500")
    janela.resizable(True, True)
    janela.configure(bg="black")

    def sair():
        janela.destroy()
        tela_login()

    def editar():
        janela.destroy()
        tela_editar()

    btn_editar = tk.Button(janela, text="Editar", bg="blue", fg="white", command=editar)
    btn_editar.place(relx=1.0, x=-45, y=10, anchor="ne")

    btn_sair = tk.Button(janela, text="Sair", command=sair, bg="red", fg="white")
    btn_sair.place(relx=1.0, x=-10, y=10, anchor="ne")

    tk.Label(janela, text=f"Bem-vindo, {nome_usuario}!", bg="black", fg="white").pack(pady=10)

    frame = tk.Frame(janela, bg="black")
    frame.pack(fill="both", expand=True)

    # Campos de entrada
    tk.Label(frame, text="Data (DD-MM-YYYY)", bg="black", fg="white").grid(row=0, column=0)
    entry_data = tk.Entry(frame, bg="gray15", fg="white", insertbackground="white")
    entry_data.grid(row=0, column=1, sticky="ew")

    tk.Label(frame, text="Horário (HH:MM)", bg="black", fg="white").grid(row=1, column=0)
    entry_horario = tk.Entry(frame, bg="gray15", fg="white", insertbackground="white")
    entry_horario.grid(row=1, column=1, sticky="ew")

    tk.Label(frame, text="Profissional", bg="black", fg="white").grid(row=2, column=0)
    entry_profissional = tk.Entry(frame, bg="gray15", fg="white", insertbackground="white")
    entry_profissional.grid(row=2, column=1, sticky="ew")

    agendamento_selecionado = tk.StringVar()

    def salvar():
        data = entry_data.get()
        horario = entry_horario.get()
        profissional = entry_profissional.get()
        if data and horario and profissional:
            salvar_agendamento(usuario_id, data, horario, profissional)
            atualizar_lista()
            entry_data.delete(0, tk.END)
            entry_horario.delete(0, tk.END)
            entry_profissional.delete(0, tk.END)

    def atualizar():
        ag_id = agendamento_selecionado.get()
        if ag_id:
            atualizar_agendamento(
                ag_id,
                entry_data.get(),
                entry_horario.get(),
                entry_profissional.get()
            )
            atualizar_lista()
            agendamento_selecionado.set("")
            entry_data.delete(0, tk.END)
            entry_horario.delete(0, tk.END)
            entry_profissional.delete(0, tk.END)
            btn_atualizar.config(state="disabled")
            btn_deletar.config(state="disabled")

    def deletar():
        ag_id = agendamento_selecionado.get()
        if ag_id:
            deletar_agendamento(ag_id)
            atualizar_lista()
            agendamento_selecionado.set("")
            entry_data.delete(0, tk.END)
            entry_horario.delete(0, tk.END)
            entry_profissional.delete(0, tk.END)
            btn_atualizar.config(state="disabled")
            btn_deletar.config(state="disabled")

    frame_botoes = tk.Frame(frame, bg="black")
    frame_botoes.grid(row=3, column=1, sticky="e", pady=10)

    btn_salvar = tk.Button(frame_botoes, text="Salvar", bg="blue", fg="white", command=salvar)
    btn_salvar.pack(side=tk.LEFT, padx=5)

    btn_atualizar = tk.Button(frame_botoes, text="Atualizar", bg="yellow", fg="black", command=atualizar, state="disabled")
    btn_atualizar.pack(side=tk.LEFT, padx=5)

    btn_deletar = tk.Button(frame_botoes, text="Deletar", bg="red", fg="white", command=deletar, state="disabled")
    btn_deletar.pack(side=tk.LEFT, padx=5)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="black", foreground="white", fieldbackground="black")
    style.configure("Treeview.Heading", background="gray20", foreground="white")

    tree = ttk.Treeview(frame, columns=("data", "horario", "profissional"), show="headings")
    tree.heading("data", text="Data")
    tree.heading("horario", text="Horário")
    tree.heading("profissional", text="Profissional")
    tree.grid(row=4, column=0, columnspan=2, sticky="nsew")

    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(4, weight=1)

    def atualizar_lista():
        for item in tree.get_children():
            tree.delete(item)
        agendamentos = listar_agendamentos_por_usuario(usuario_id)
        for ag in agendamentos:
            tree.insert("", "end", values=ag)

    def on_select(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected)["values"]
            agendamento_selecionado.set(values[0])
            entry_data.delete(0, tk.END)
            entry_data.insert(0, values[0])
            entry_horario.delete(0, tk.END)
            entry_horario.insert(0, values[1])
            entry_profissional.delete(0, tk.END)
            entry_profissional.insert(0, values[2])
            btn_atualizar.config(state="normal")
            btn_deletar.config(state="normal")

    tree.bind("<<TreeviewSelect>>", on_select)

    atualizar_lista()
    janela.mainloop()

def tela_editar():
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
            
    def voltar():
        janela.destroy()
        tela_agendamento()

    janela = tk.Tk()
    janela.title("Editar Usuário")
    janela.geometry("400x350")
    janela.configure(bg="black")
    janela.resizable(True, True)

    frame = tk.Frame(janela, bg="black")
    frame.pack(expand=True)

    # Título centralizado
    tk.Label(frame, text="Editar Usuário", font=("Helvetica", 16, "bold"), bg="black", fg="white").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame, text="Nome", bg="black", fg="white").grid(row=1, column=0, pady=5, sticky="w")
    entry_nome = tk.Entry(frame, width=30, bg="gray20", fg="white", insertbackground="white")
    entry_nome.grid(row=1, column=1, pady=5)

    tk.Label(frame, text="Email", bg="black", fg="white").grid(row=2, column=0, pady=5, sticky="w")
    entry_email = tk.Entry(frame, width=30, bg="gray20", fg="white", insertbackground="white")
    entry_email.grid(row=2, column=1, pady=5)

    tk.Label(frame, text="Senha", bg="black", fg="white").grid(row=3, column=0, pady=5, sticky="w")
    entry_senha = tk.Entry(frame, show="*", width=30, bg="gray20", fg="white", insertbackground="white")
    entry_senha.grid(row=3, column=1, pady=5)

    tk.Button(frame, text="Voltar", command=voltar, bg="gray30", fg="white").grid(row=4, column=0, pady=10, sticky="w")
    tk.Button(frame, text="Atualizar", command=fazer_cadastro, bg="blue", fg="white").grid(row=4, column=1, pady=10, sticky="e")

    janela.mainloop()

# Iniciar com a tela de login
tela_login()
