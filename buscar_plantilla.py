import tkinter as tk
from bs4 import BeautifulSoup

class BuscarPlantilla():
    ventana:tk.Toplevel
    filename:str
    entry_collection_handle:tk.Entry
    text_resultado:tk.Text

    def __init__(self):
        pass


    def inicializar_ventana(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Pantalla1")
        self.ventana.geometry("500x500")
        tk.Label(self.ventana, text="Introduce el handle de la colección de la que quieras saber su plantilla").pack()
        self.entry_collection_handle = tk.Entry(self.ventana)
        self.entry_collection_handle.pack()
        boton_buscar = tk.Button(self.ventana, text="Buscar", command=self.buscar_plantilla)
        boton_buscar.pack()
        self.text_resultado = tk.Text(self.ventana, height=10, width=50)
        self.text_resultado.pack()

    def buscar_plantilla(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            content = file.read()

        collection_handle = self.entry_collection_handle.get()
        print(collection_handle)

        soup = BeautifulSoup(content, 'lxml-xml')
        name_map = soup.find('name-map', {'collection-handle': collection_handle})

        if name_map:
            self.text_resultado.delete('1.0', tk.END)
            self.text_resultado.insert(tk.END, name_map.get('form-name'))
        else:
            self.text_resultado.delete('1.0', tk.END)
            self.text_resultado.insert(tk.END, "No se encontró ninguna plantilla con el 'collection-handle' especificado.")
