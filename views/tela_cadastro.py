import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from controllers.usuario_controller import cadastrar_usuario

def tela_cadastro():
    def fazer_cadastro():
        nome = entry_nome.get()
        email = entry_email.get()
        senha = entry_senha.get()
        sucesso = cadastrar_usuario(nome, email, senha)
        if sucesso:
            messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
            janela.destroy()
            from views.tela_login import tela_login  # importação atrasada
            tela_login()
        else:
            messagebox.showerror("Erro", "Email já cadastrado.")

    def voltar():
        janela.destroy()
        from views.tela_login import tela_login 
        tela_login()

    janela = tk.Tk()  
    janela.title("Cadastro")
    janela.geometry("600x600")
    janela.configure(bg="black")
    janela.resizable(False, False)

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
