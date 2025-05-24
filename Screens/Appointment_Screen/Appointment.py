import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image
from Screens.Edit_User.edit import edit_user_screen as edit
from Screens.Login_Screen import login as logi
import os

def appointment_screen():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()
    app.geometry("700x500")
    app.title("Agenda")
    app.resizable(width=False, height=False)
    app.eval('tk::PlaceWindow . center')
    
    def kill_screen():
        app.destroy()

    # Top Frame
    top_frame = ctk.CTkFrame(app)
    top_frame.pack(fill="x", pady=10)

    label_welcome = ctk.CTkLabel(top_frame, text="Bem-vindo, ming!", font=ctk.CTkFont(size=14, weight="bold"))
    label_welcome.pack(side="left", padx=10)

    # Caminho absoluto para a imagem, relativo ao script atual
    base_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_path, "exit.png")

    # Debug: mostra o caminho final
    print(f"Base path: {base_path}")
    print(f"Image path: {image_path}")

    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {image_path}")

        image = Image.open(image_path)
        exit_icon = ctk.CTkImage(light_image=image, dark_image=image, size=(20, 20))
    except Exception as e:
        messagebox.showerror("Erro", f"Imagem não encontrada: {image_path}\n{e}")
        exit_icon = None

    btn_exit = ctk.CTkButton(
        top_frame,
        text="",
        command=lambda: (kill_screen(), login_screen()),
        image=exit_icon if exit_icon else None,
        fg_color="white",  # fundo escuro para garantir contraste
        width=5,
        height=20,
        compound="left"  # mostra a imagem à esquerda do texto
    )

    if exit_icon:
      btn_exit.image = exit_icon
    btn_exit.pack(side="right", padx=5)

    btn_edit = ctk.CTkButton(top_frame, text="Editar Perfil",command=edit_screen, fg_color="#1B03A3")
    btn_edit.pack(side="right")

    # Container principal
    container_frame = ctk.CTkFrame(app)
    container_frame.pack(pady=10)

    # Form Frame
    form_frame = ctk.CTkFrame(container_frame)
    form_frame.grid(row=0, column=0, padx=10)

    # Data
    label_data = ctk.CTkLabel(form_frame, text="Data (DD-MM-YYYY):")
    label_data.grid(row=0, column=0, sticky="w", pady=5, padx=5)
    entry_data = ctk.CTkEntry(form_frame, width=200)
    entry_data.grid(row=0, column=1, pady=5, padx=5)

    # Horário
    label_horario = ctk.CTkLabel(form_frame, text="Horário (HH:MM):")
    label_horario.grid(row=1, column=0, sticky="w", pady=5, padx=5)
    entry_horario = ctk.CTkEntry(form_frame, width=200)
    entry_horario.grid(row=1, column=1, pady=5, padx=5)

    # Aluno
    label_prof = ctk.CTkLabel(form_frame, text="Nome do Aluno:")
    label_prof.grid(row=2, column=0, sticky="w", pady=5, padx=5)
    entry_prof = ctk.CTkEntry(form_frame, width=200)
    entry_prof.grid(row=2, column=1, pady=5, padx=5)
     # Endereco
    label_prof = ctk.CTkLabel(form_frame, text="Endereço:")
    label_prof.grid(row=3, column=0, sticky="w", pady=5, padx=5)
    entry_prof = ctk.CTkEntry(form_frame, width=200)
    entry_prof.grid(row=3, column=1, pady=5, padx=5)


    # Buttons Frame
    btn_frame = ctk.CTkFrame(container_frame)
    btn_frame.grid(row=0, column=1, padx=10)

    btn_salvar = ctk.CTkButton(btn_frame, text="Salvar", fg_color="green")
    btn_salvar.pack(pady=5)

    btn_atualizar = ctk.CTkButton(btn_frame, text="Atualizar", fg_color="yellow", text_color="black")
    btn_atualizar.pack(pady=5)

    btn_deletar = ctk.CTkButton(btn_frame, text="Deletar", fg_color="red")
    btn_deletar.pack(pady=5)

   # Tabela
    table_frame = ctk.CTkFrame(app)
    table_frame.pack(pady=10, fill="both", expand=True)

    # >>> Estilo aqui <<<
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                background="#1a1a1a",
                foreground="white",
                rowheight=25,
                fieldbackground="#1a1a1a")
    style.map('Treeview', background=[('selected', '#333333')])

    columns = ("Data", "Horário", "Aluno", "Endereco")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
      tree.heading(col, text=col)
      tree.column(col, anchor="center")

    tree.pack(fill="both", expand=True)

    app.mainloop()

def edit_screen():
    edit()

def login_screen():
    logi.login_screen()