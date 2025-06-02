import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image
from tkcalendar import DateEntry
from Screens.Edit_User.edit import edit_user_screen as edit
from Screens.Login_Screen import login as logi
from Model.Agendamento import Agendamento as appoint
from database import db as datac
import os


def appointment_screen(name_user: str):
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()
    app.geometry("800x600")
    app.title("Agenda")
    app.resizable(width=False, height=False)
    app.eval('tk::PlaceWindow . center')

    def kill_screen():
        app.destroy()

    def popular_tree():
        for item in tree.get_children():
            tree.delete(item)
        agendamentos = datac.listar_agendamentos_por_professor(name_user)
        for agendamento in agendamentos:
            agendamento_id, nome, data, horario, endereco, professor = agendamento
            tree.insert("", "end", iid=str(agendamento_id), values=(data, horario, nome, endereco))

    def submit():
        agend_data = entry_data.get_date().strftime("%d-%m-%Y")
        agend_hora = combo_hora.get()
        agend_minuto = combo_minuto.get()
        agend_horario = f"{agend_hora}:{agend_minuto}"
        agend_nome = entry_name.get()
        agend_endereco = entry_end.get()

        novo_appoint = appoint(agend_nome, agend_data, agend_horario, agend_endereco, name_user)
        datac.inserir_agendamento(novo_appoint)

        messagebox.showinfo("Sucesso", "Agendamento salvo com sucesso!")
        popular_tree()

    def deletar():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um agendamento para deletar.")
            return
        agendamento_id = selected[0]
        confirmar = messagebox.askyesno("Confirmar", "Tem certeza que deseja deletar o agendamento selecionado?")
        if confirmar:
            try:
                datac.deletar_agendamento(int(agendamento_id))
                messagebox.showinfo("Sucesso", "Agendamento deletado com sucesso!")
                popular_tree()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao deletar agendamento: {e}")

    def atualizar():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um agendamento para atualizar.")
            return

        agendamento_id = int(selected[0])
        agend_data = entry_data.get_date().strftime("%d-%m-%Y")
        agend_hora = combo_hora.get()
        agend_minuto = combo_minuto.get()
        agend_horario = f"{agend_hora}:{agend_minuto}"
        agend_nome = entry_name.get()
        agend_endereco = entry_end.get()

        novo_appoint = appoint(agend_nome, agend_data, agend_horario, agend_endereco, name_user)

        try:
            datac.atualizar_agendamento(agendamento_id, novo_appoint)
            messagebox.showinfo("Sucesso", "Agendamento atualizado com sucesso!")
            popular_tree()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar agendamento: {e}")

    def preencher_campos(event):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            data, horario, nome, endereco = item['values']
            entry_data.set_date(data)
            hora, minuto = horario.split(":")
            combo_hora.set(hora)
            combo_minuto.set(minuto)
            entry_name.delete(0, "end")
            entry_name.insert(0, nome)
            entry_end.delete(0, "end")
            entry_end.insert(0, endereco)

    def edit_screen():
        edit()

    def login_screen():
        logi.login_screen()

    # --- UI ---

    top_frame = ctk.CTkFrame(app)
    top_frame.pack(fill="x", pady=10)

    label_welcome = ctk.CTkLabel(top_frame, text=f"Bem-vindo, {name_user}", font=ctk.CTkFont(size=14, weight="bold"))
    label_welcome.pack(side="left", padx=10)

    base_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_path, "exit.png")

    try:
        image = Image.open(image_path)
        exit_icon = ctk.CTkImage(light_image=image, dark_image=image, size=(20, 20))
    except Exception:
        exit_icon = None

    btn_exit = ctk.CTkButton(
        top_frame,
        text="",
        command=lambda: (kill_screen(), login_screen()),
        image=exit_icon if exit_icon else None,
        fg_color="white",
        width=5,
        height=20,
        compound="left"
    )
    btn_exit.pack(side="right", padx=5)

    container_frame = ctk.CTkFrame(app)
    container_frame.pack(pady=10)

    form_frame = ctk.CTkFrame(container_frame)
    form_frame.grid(row=0, column=0, padx=10)

    # Data com DateEntry
    label_data = ctk.CTkLabel(form_frame, text="Data (DD-MM-YYYY):")
    label_data.grid(row=0, column=0, sticky="w", pady=5, padx=5)
    entry_data = DateEntry(form_frame, width=18, date_pattern="dd-mm-yyyy", background='darkblue', foreground='white')
    entry_data.grid(row=0, column=1, pady=5, padx=5)

    # Horário
    label_horario = ctk.CTkLabel(form_frame, text="Horário (HH:MM):")
    label_horario.grid(row=1, column=0, sticky="w", pady=5, padx=5)

    horario_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    horario_frame.grid(row=1, column=1, pady=5, padx=5)

    horas = [f"{h:02d}" for h in range(0, 24)]
    combo_hora = ttk.Combobox(horario_frame, values=horas, width=5)
    combo_hora.pack(side="left", padx=(0, 5))
    combo_hora.set("00")

    minutos = [f"{m:02d}" for m in range(0, 60, 5)]
    combo_minuto = ttk.Combobox(horario_frame, values=minutos, width=5)
    combo_minuto.pack(side="left")
    combo_minuto.set("00")

    label_name = ctk.CTkLabel(form_frame, text="Nome do Aluno:")
    label_name.grid(row=2, column=0, sticky="w", pady=5, padx=5)
    entry_name = ctk.CTkEntry(form_frame, width=200)
    entry_name.grid(row=2, column=1, pady=5, padx=5)

    label_end = ctk.CTkLabel(form_frame, text="Endereço:")
    label_end.grid(row=3, column=0, sticky="w", pady=5, padx=5)
    entry_end = ctk.CTkEntry(form_frame, width=200)
    entry_end.grid(row=3, column=1, pady=5, padx=5)

    btn_frame = ctk.CTkFrame(container_frame)
    btn_frame.grid(row=0, column=1, padx=10)

    btn_salvar = ctk.CTkButton(btn_frame, text="Salvar", command=submit, fg_color="green")
    btn_salvar.pack(pady=5)

    btn_atualizar = ctk.CTkButton(btn_frame, text="Atualizar", command=atualizar, fg_color="yellow", text_color="black")
    btn_atualizar.pack(pady=5)

    btn_deletar = ctk.CTkButton(btn_frame, text="Deletar", command=deletar, fg_color="red")
    btn_deletar.pack(pady=5)

    table_frame = ctk.CTkFrame(app)
    table_frame.pack(pady=10, fill="both", expand=True)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="#1a1a1a", foreground="white", rowheight=25, fieldbackground="#1a1a1a")
    style.map('Treeview', background=[('selected', '#333333')])

    columns = ("Data", "Horário", "Aluno", "Endereço")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(fill="both", expand=True)
    tree.bind("<<TreeviewSelect>>", preencher_campos)

    popular_tree()
    app.mainloop()


def edit_screen():
    edit()


def login_screen():
    logi.login_screen()
