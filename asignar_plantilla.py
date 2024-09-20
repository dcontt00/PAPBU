import tkinter as tk
from bs4 import BeautifulSoup
from tkinter import messagebox


class AsignarPlantilla():
    ventana: tk.Toplevel
    entry_collection_handle: tk.Entry
    files: list[str]
    selected_form_name: tk.StringVar

    def inicializar_ventana(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Asignar Plantilla")
        self.ventana.geometry("500x500")
        tk.Label(self.ventana, text="Introduce el handle de la colección a la que quieras asignar la plantilla").pack()
        self.entry_collection_handle = tk.Entry(self.ventana)
        self.entry_collection_handle.pack()
        tk.Label(self.ventana, text="Selecciona la plantilla a asignar").pack()

        # Añadir un menú desplegable con las plantillas disponibles
        form_names = self.get_form_names()
        self.selected_form_name = tk.StringVar(self.ventana)
        self.selected_form_name.set(form_names[0])
        dropdown = tk.OptionMenu(self.ventana, self.selected_form_name, *form_names)
        dropdown.pack()

        boton_asignar = tk.Button(self.ventana, text="Asignar", command=self.asignar_plantilla)
        boton_asignar.pack()

    def get_form_names(self):
        # Parsear el archivo XML
        with open(self.files[0], 'r', encoding='utf-8') as file:
            content = file.read()
        soup = BeautifulSoup(content, 'lxml-xml')
        name_maps = soup.find_all('form')
        form_names = [name_map.get('name') for name_map in name_maps]

        print(form_names)
        # Eliminar duplicados
        form_names = list(set(form_names))
        form_names.sort()
        return form_names

    def asignar_plantilla(self):
        with open(self.files[0], 'r', encoding='utf-8') as file:
            content = file.read()

        collection_handle = self.entry_collection_handle.get()
        print(collection_handle)
        soup = BeautifulSoup(content, 'lxml-xml')
        form_map = soup.find('form-map')

        # Comprobar si existe un 'name-map' con el 'collection-handle' especificado
        name_map = soup.find('name-map', {'collection-handle': collection_handle})
        if name_map:
            print("existe")
            name_map['form-name'] = self.selected_form_name.get()
            with open(self.files[0], 'w', encoding='utf-8') as file:
                file.write(soup.prettify())

        else:

            # Añadir un nuevo 'name-map' con el 'collection-handle' y 'form-name' especificados
            new_name_map = soup.new_tag('name-map')
            new_name_map['collection-handle'] = collection_handle
            new_name_map['form-name'] = self.selected_form_name.get()
            # Añadir al principio
            form_map.insert(0, new_name_map)

            # Formatear el contenido del archivo XML
            formatte_content = soup.prettify()

            # Guardar los cambios en el archivo XML
            with open(self.files[0], 'w', encoding='utf-8') as file:
                file.write(formatte_content)
        messagebox.showinfo("Plantilla asignada",
                            f"Se ha asignado la plantilla {self.selected_form_name.get()} al 'collection-handle' {collection_handle}")
