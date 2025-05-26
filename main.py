import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime, timedelta
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
import sqlite3

def conectar():
    return sqlite3.connect("usuarios.db")

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
    janela.geometry("600x600")
    janela.configure(bg="black")
    janela.resizable(True, True)

    frame = tk.Frame(janela, bg="black")
    frame.pack(expand=True)

    tk.Label(frame, text="Cadastro", font=("Helvetica", 16, "bold"), bg="black", fg="white").grid(row=0, column=0, columnspan=2, pady=7)

    tk.Label(frame, text="Nome", bg="black", fg="white").grid(row=1, column=0, pady=5, sticky="w")
    entry_nome = tk.Entry(frame, width=30, bg="gray20", fg="white", insertbackground="white")
    entry_nome.grid(row=1, column=1, pady=5)

    tk.Label(frame, text="Email", bg="black", fg="white").grid(row=2, column=0, pady=5, sticky="w")
    entry_email = tk.Entry(frame, width=30, bg="gray20", fg="white", insertbackground="white")
    entry_email.grid(row=2, column=1, pady=5)

    tk.Label(frame, text="Senha", bg="black", fg="white").grid(row=3, column=0, pady=5, sticky="w")
    entry_senha = tk.Entry(frame, show="*", width=30, bg="gray20", fg="white", insertbackground="white")
    entry_senha.grid(row=3, column=1, pady=5)

    tk.Button(frame, text="Cadastrar", command=fazer_cadastro, bg="green", fg="white").grid(row=5, column=1, pady=10, sticky="e")
    tk.Button(frame, text="Voltar", command=voltar, bg="gray30", fg="white").grid(row=5, column=0, pady=10, sticky="w")

    janela.mainloop()

def tela_agendamento(usuario_id, nome_usuario):
    janela = tk.Tk()
    janela.title("Agendamentos")
    janela.geometry("600x600")
    janela.resizable(True, True)
    janela.configure(bg="black")

    def sair():
        janela.destroy()
        tela_login()

    btn_editar = tk.Button(janela, text="Editar perfil", bg="blue", fg="white", command=lambda: [janela.destroy(), tela_editar_usuario(usuario_id, nome_usuario)])
    btn_editar.place(relx=1.0, x=-45, y=10, anchor="ne")

    btn_sair = tk.Button(janela, text="Sair", command=sair, bg="red", fg="white")
    btn_sair.place(relx=1.0, x=-10, y=10, anchor="ne")

    tk.Label(janela, text=f"Bem-vindo, {nome_usuario}!", bg="black", fg="white").pack(pady=10)

    frame = tk.Frame(janela, bg="black")
    frame.pack(fill="both", expand=True)

    def gerar_horarios():
        return [f"{hora:02d}:00" for hora in range(8, 21) if hora < 12 or hora >= 14]

    def horarios_disponiveis(data, profissional):
        todos = gerar_horarios()
        agendados = [h[0] for h in listar_horarios_agendados(data, profissional)]
        return [h for h in todos if h not in agendados]

    def datas_disponiveis(profissional):
        datas = []
        hoje = datetime.today()
        dia = hoje + timedelta(days=1)
        while len(datas) < 30:
            if dia.weekday() < 5:
                data_str = dia.strftime("%d-%m-%Y")
                if horarios_disponiveis(data_str, profissional):
                    datas.append(data_str)
            dia += timedelta(days=1)
        return datas

    def listar_horarios_agendados(data, profissional):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT horario FROM agendamentos
            WHERE data = ? AND profissional = ?
        """, (data, profissional))
        resultado = cursor.fetchall()
        conn.close()
        return resultado

    style = ttk.Style()
    style.theme_use("default")
    style.configure("TCombobox", fieldbackground="black", background="black", foreground="white")
    style.map("TCombobox", fieldbackground=[("readonly", "black")], background=[("readonly", "black")], foreground=[("readonly", "white")])
    style.configure("Treeview", background="black", foreground="white", fieldbackground="black")
    style.configure("Treeview.Heading", background="gray20", foreground="white")

    agendamento_selecionado = tk.StringVar()

    centro_frame = tk.Frame(frame, bg="black")
    centro_frame.grid(row=0, column=0, pady=10)
    
    campo_frame = tk.Frame(centro_frame, bg="black")
    campo_frame.grid(row=0, column=0, padx=20)

    tk.Label(campo_frame, text="Profissional:", bg="black", fg="white", width=10, anchor="e").grid(row=0, column=0, sticky="e", pady=5)
    combo_profissional = ttk.Combobox(campo_frame, values=["Joao"], state="readonly", width=20)
    combo_profissional.grid(row=0, column=1, pady=5)
    combo_profissional.set("Joao")

    tk.Label(campo_frame, text="Data:", bg="black", fg="white", width=10, anchor="e").grid(row=1, column=0, sticky="e", pady=5)
    combo_data = ttk.Combobox(campo_frame, state="readonly", width=20)
    combo_data.grid(row=1, column=1, pady=5)

    tk.Label(campo_frame, text="Horário:", bg="black", fg="white", width=10, anchor="e").grid(row=2, column=0, sticky="e", pady=5)
    combo_horario = ttk.Combobox(campo_frame, state="readonly", width=20)
    combo_horario.grid(row=2, column=1, pady=5)

    botoes_frame = tk.Frame(centro_frame, bg="black")
    botoes_frame.grid(row=0, column=1, padx=20)

    btn_salvar = tk.Button(botoes_frame, text="Salvar", bg="blue", fg="white", command=lambda: salvar(), width=12)
    btn_salvar.pack(pady=4)

    btn_atualizar = tk.Button(botoes_frame, text="Atualizar", bg="yellow", fg="black", command=lambda: atualizar(), state="disabled", width=12)
    btn_atualizar.pack(pady=4)

    btn_deletar = tk.Button(botoes_frame, text="Deletar", bg="red", fg="white", command=lambda: deletar(), state="disabled", width=12)
    btn_deletar.pack(pady=4)

    tree = ttk.Treeview(frame, columns=("id", "data", "horario", "profissional"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("data", text="Data")
    tree.heading("horario", text="Horário")
    tree.heading("profissional", text="Profissional")
    tree.column("id", width=40, anchor="center")
    tree.column("data", width=100, anchor="center")
    tree.column("horario", width=80, anchor="center")
    tree.column("profissional", width=120, anchor="center")
    tree.grid(row=1, column=0, columnspan=2, sticky="nsew")

    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)

    def salvar():
        data = combo_data.get()
        horario = combo_horario.get()
        profissional = combo_profissional.get()
        if data and horario and profissional:
            if salvar_agendamento(usuario_id, data, horario, profissional):
                atualizar_lista()
                atualizar_comboboxes()
                combo_data.set("")
                combo_horario.set("")
                combo_profissional.set("Joao")

    def atualizar():
        ag_id = agendamento_selecionado.get()
        if ag_id:
            if atualizar_agendamento(ag_id, combo_data.get(), combo_horario.get(), combo_profissional.get()):
                atualizar_lista()
                atualizar_comboboxes()
                agendamento_selecionado.set("")
                combo_data.set("")
                combo_horario.set("")
                combo_profissional.set("Joao")
                btn_atualizar.config(state="disabled")
                btn_deletar.config(state="disabled")

    def deletar():
        ag_id = agendamento_selecionado.get()
        if ag_id:
            deletar_agendamento(ag_id)
            atualizar_lista()
            atualizar_comboboxes()
            agendamento_selecionado.set("")
            combo_data.set("")
            combo_horario.set("")
            combo_profissional.set("Joao")
            btn_atualizar.config(state="disabled")
            btn_deletar.config(state="disabled")

    def atualizar_lista():
        for item in tree.get_children():
            tree.delete(item)
        agendamentos = listar_agendamentos_por_usuario(usuario_id)
        for ag in agendamentos:
            tree.insert("", "end", values=ag)

    def atualizar_comboboxes(event=None):
        profissional = combo_profissional.get()
        combo_data["values"] = datas_disponiveis(profissional)
        combo_data.set("")
        combo_horario.set("")
        combo_horario["values"] = []

    def on_select_data(event):
        data = combo_data.get()
        profissional = combo_profissional.get()
        combo_horario["values"] = horarios_disponiveis(data, profissional)
        combo_horario.set("")

    def on_select(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected)["values"]
            if values:
                agendamento_selecionado.set(values[0])
                combo_data.set(values[1])
                combo_horario.set(values[2])
                combo_profissional.set(values[3])
                btn_atualizar.config(state="normal")
                btn_deletar.config(state="normal")

    tree.bind("<<TreeviewSelect>>", on_select)
    combo_profissional.bind("<<ComboboxSelected>>", atualizar_comboboxes)
    combo_data.bind("<<ComboboxSelected>>", on_select_data)

    atualizar_lista()
    atualizar_comboboxes()
    janela.mainloop()


def existe_agendamento(profissional, data, horario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM agendamentos
        WHERE profissional = ? AND data = ? AND horario = ?
    """, (profissional, data, horario))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] > 0

def salvar_agendamento(usuario_id, data, horario, profissional):
    if existe_agendamento(profissional, data, horario):
        return False
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO agendamentos (usuario_id, data, horario, profissional)
        VALUES (?, ?, ?, ?)
    """, (usuario_id, data, horario, profissional))
    conn.commit()
    conn.close()
    return True

def listar_agendamentos_por_usuario(usuario_id):
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

def atualizar_agendamento(agendamento_id, data, horario, profissional):
    if existe_agendamento(profissional, data, horario):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM agendamentos
            WHERE profissional = ? AND data = ? AND horario = ?
        """, (profissional, data, horario))
        resultado = cursor.fetchone()
        if resultado and resultado[0] != agendamento_id:
            conn.close()
            return False
        conn.close()

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE agendamentos
        SET data = ?, horario = ?, profissional = ?
        WHERE id = ?
    """, (data, horario, profissional, agendamento_id))
    conn.commit()
    conn.close()
    return True

def deletar_agendamento(agendamento_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM agendamentos WHERE id = ?", (agendamento_id,))
    conn.commit()
    conn.close()

def tela_editar_usuario(usuario_id, nome_usuario):
    def salvar_alteracoes():
        novo_email = entry_email.get()
        nova_senha = entry_senha.get()

        if novo_email and nova_senha:
            from database import atualizar_usuario
            sucesso = atualizar_usuario(usuario_id, novo_email, nova_senha)
            if sucesso:
                messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
                janela.destroy()
                tela_agendamento(usuario_id, nome_usuario)
            else:
                messagebox.showerror("Erro", "Email já cadastrado por outro usuário.")
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")

    def excluir_conta():
        resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir sua conta?")
        if resposta:
            from database import deletar_usuario
            sucesso = deletar_usuario(usuario_id)
            if sucesso:
                messagebox.showinfo("Conta excluída", "Sua conta foi excluída com sucesso.")
                janela.destroy()
                tela_login()  # Redireciona ao login após exclusão
            else:
                messagebox.showerror("Erro", "Erro ao excluir a conta.")

    def voltar():
        janela.destroy()
        tela_agendamento(usuario_id, nome_usuario)

    janela = tk.Tk()
    janela.title("Editar Usuário")
    janela.geometry("600x600")
    janela.configure(bg="black")
    janela.resizable(True, True)

    frame = tk.Frame(janela, bg="black")
    frame.pack(expand=True)

    tk.Label(frame, text="Editar Perfil", font=("Helvetica", 16, "bold"), bg="black", fg="white").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame, text="Nome", bg="black", fg="white").grid(row=1, column=0, pady=5, sticky="w")
    entry_nome = tk.Entry(frame, width=30, bg="gray30", fg="white", insertbackground="white")
    entry_nome.insert(0, nome_usuario)
    entry_nome.config(state="disabled")
    entry_nome.grid(row=1, column=1, pady=5)

    tk.Label(frame, text="Novo Email", bg="black", fg="white").grid(row=2, column=0, pady=5, sticky="w")
    entry_email = tk.Entry(frame, width=30, bg="gray20", fg="white", insertbackground="white")
    entry_email.grid(row=2, column=1, pady=5)

    tk.Label(frame, text="Nova Senha", bg="black", fg="white").grid(row=3, column=0, pady=5, sticky="w")
    entry_senha = tk.Entry(frame, show="*", width=30, bg="gray20", fg="white", insertbackground="white")
    entry_senha.grid(row=3, column=1, pady=5)

    tk.Button(frame, text="Salvar", command=salvar_alteracoes, bg="green", fg="white").grid(row=5, column=1, pady=10, sticky="e")
    tk.Button(frame, text="Voltar", command=voltar, bg="gray30", fg="white").grid(row=5, column=0, pady=10, sticky="w")
    tk.Button(frame, text="Excluir Conta", command=excluir_conta, bg="red", fg="white").grid(row=6, column=0, columnspan=2, pady=10)


    janela.mainloop()

# Iniciar com a tela de login
tela_login()
