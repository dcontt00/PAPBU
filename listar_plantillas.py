import tkinter as tk
from bs4 import BeautifulSoup
from tkinter import messagebox
from common import get_form_names


class ListarPlantillas():
    ventana: tk.Toplevel
    files: list[str]

    def __init__(self):
        pass

    def inicializar_ventana(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Listar plantillas")
        self.ventana.geometry("500x500")

        listbox = tk.Listbox(self.ventana)
        for item in get_form_names(self.files[0]):
            listbox.insert(tk.END, item)

        listbox.pack(fill=tk.BOTH, expand=True)
