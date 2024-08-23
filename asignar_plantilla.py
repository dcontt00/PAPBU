import tkinter as tk
from bs4 import BeautifulSoup


class AsignarPlantilla():
    ventana: tk.Toplevel
    entry_collection_handle: tk.Entry
    text_resultado: tk.Text
    filename: str
    selected_form_name: tk.StringVar

    def inicializar_ventana(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Pantalla2")
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
        self.text_resultado = tk.Text(self.ventana, height=10, width=50)
        self.text_resultado.pack()

    def get_form_names(self):
        # Parsear el archivo XML
        with open(self.filename, 'r', encoding='utf-8') as file:
            content = file.read()
        soup = BeautifulSoup(content, 'lxml-xml')
        name_maps = soup.find_all('name-map')
        form_names = [name_map.get('form-name') for name_map in name_maps]

        # Eliminar duplicados
        form_names = list(set(form_names))
        form_names.sort()

        return form_names

    def asignar_plantilla(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            content = file.read()

        collection_handle = self.entry_collection_handle.get()
        print(collection_handle)
        soup = BeautifulSoup(content, 'lxml-xml')
        form_map = soup.find('form-map')

        # Añadir un nuevo 'name-map' con el 'collection-handle' y 'form-name' especificados
        new_name_map = soup.new_tag('name-map')
        new_name_map['collection-handle'] = collection_handle
        new_name_map['form-name'] = self.selected_form_name.get()
        # Añadir al principio
        form_map.insert(0, new_name_map)

        # Formatear el contenido del archivo XML
        formatte_content = soup.prettify()

        # Guardar los cambios en el archivo XML
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write(formatte_content)
        self.text_resultado.delete('1.0', tk.END)
        self.text_resultado.insert(tk.END, "Plantilla asignada correctamente.")
