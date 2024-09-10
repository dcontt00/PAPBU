import tkinter as tk
from bs4 import BeautifulSoup
from tkinter import messagebox


class BuscarPlantilla():
    ventana: tk.Toplevel
    filename: str
    entry_collection_handle: tk.Entry

    def __init__(self):
        pass

    def inicializar_ventana(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Buscar plantilla")
        self.ventana.geometry("500x500")
        tk.Label(self.ventana, text="Introduce el handle de la colección de la que quieras saber su plantilla").pack()
        self.entry_collection_handle = tk.Entry(self.ventana)
        self.entry_collection_handle.pack()
        boton_buscar = tk.Button(self.ventana, text="Buscar", command=self.buscar_plantilla)
        boton_buscar.pack()

    def buscar_plantilla(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            content = file.read()

        collection_handle = self.entry_collection_handle.get()
        print(collection_handle)

        soup = BeautifulSoup(content, 'lxml-xml')
        name_map = soup.find('name-map', {'collection-handle': collection_handle})

        if name_map:
            messagebox.showinfo("Plantilla encontrada",
                                f"La plantilla asociada al 'collection-handle' {collection_handle} es "
                                f"{name_map.get('form-name')}")
        else:
            messagebox.showinfo("Plantilla no encontrada",
                                f"No se encontró una plantilla asociada al 'collection-handle' {collection_handle}")
