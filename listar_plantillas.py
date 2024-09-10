import tkinter as tk
from bs4 import BeautifulSoup
from tkinter import messagebox


class ListarPlantillas():
    ventana: tk.Toplevel
    filename: str

    def __init__(self):
        pass

    def inicializar_ventana(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Listar plantillas")
        self.ventana.geometry("500x500")

        listbox = tk.Listbox(self.ventana)
        for item in self.listar():
            listbox.insert(tk.END, item)

        listbox.pack(fill=tk.BOTH, expand=True)

    def listar(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'lxml-xml')
        forms = soup.find_all('form')

        # Get attribute name from form tag
        form_names = [name_map.get('name') for name_map in forms]

        return form_names
