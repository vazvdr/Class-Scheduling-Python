from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk


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
                from screens.tela_agendamento import tela_agendamento
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
                from screens.tela_login import tela_login
                tela_login()
            else:
                messagebox.showerror("Erro", "Erro ao excluir a conta.")

    def voltar():
        janela.destroy()
        from screens.tela_agendamento import tela_agendamento
        tela_agendamento(usuario_id, nome_usuario)

    janela = tk.Tk()
    janela.title("Editar Usuário")
    janela.geometry("600x600")
    janela.configure(bg="black")
    janela.resizable(False, False)

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