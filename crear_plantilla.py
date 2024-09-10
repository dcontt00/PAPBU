import tkinter as tk
from bs4 import BeautifulSoup
from tkinter import ttk, messagebox

input_types_dict = {
    "Campo de texto": "onebox",
    "Nombre": "name",
    "Desplegable": "dropdown",
    "Área de Texto": "textarea",
    "Fecha": "date",
}


class CrearPlantilla():
    ventana: tk.Toplevel
    nombre_plantilla: tk.Entry
    filename: str
    campos: list

    def inicializar_ventana(self):
        self.campos = []
        self.ventana = tk.Toplevel()
        self.ventana.title("Crear Plantilla")
        self.ventana.geometry("500x500")
        tk.Label(self.ventana, text="Nombre").pack()
        self.nombre_plantilla = tk.Entry(self.ventana)
        self.nombre_plantilla.pack()

        boton_añadir_campo = tk.Button(self.ventana, text="Añadir Campo", command=self.añadir_campo)
        boton_añadir_campo.pack()

        boton_guardar = tk.Button(self.ventana, text="Guardar", command=self.guardar)
        boton_guardar.pack()

    def añadir_campo(self):
        # Añadir separador
        separator = ttk.Separator(self.ventana, orient='horizontal')
        separator.pack(fill='x')

        top = tk.Frame(self.ventana)

        tk.Label(top, text="Nombre").grid(row=0, column=0)
        nombre = tk.Entry(top)
        nombre.grid(row=0, column=1)

        tk.Label(top, text="Texto descriptivo").grid(row=1, column=0)
        texto = tk.Entry(top)
        texto.grid(row=1, column=1)

        tk.Label(top, text="Metadato").grid(row=2, column=0)
        metadato = tk.Entry(top)
        metadato.grid(row=2, column=1)

        # Dropdown tipo de campo
        tk.Label(top, text="Tipo de campo").grid(row=3, column=0)
        tipo_campo = tk.StringVar(top)
        tipo_campo.set(list(input_types_dict.keys())[0])
        dropdown = tk.OptionMenu(top, tipo_campo, *input_types_dict.keys(),
                                 command=lambda value: self.on_tipo_campo_change(value, top))
        dropdown.grid(row=3, column=1)

        # Dropdown values
        value_pairs_names = self.get_value_pairs_name_map()
        print(value_pairs_names)
        label_value_pairs = tk.Label(top, text="Valores del desplegable")
        label_value_pairs.grid(row=3, column=2)
        value_pairs_name = tk.StringVar(top)
        value_pairs_name.set(value_pairs_names[0])
        dropdown_value_pairs = tk.OptionMenu(top, value_pairs_name, *value_pairs_names)
        dropdown_value_pairs.grid(row=3, column=3)
        label_value_pairs.grid_remove()  # Ocultar inicialmente
        dropdown_value_pairs.grid_remove()  # Ocultar inicialmente

        tk.Label(top, text="Obligatorio").grid(row=4, column=0)
        obligatorio = tk.BooleanVar(top)
        obligatorio.set(False)
        checkbox_obligatorio = tk.Checkbutton(top, variable=obligatorio)
        checkbox_obligatorio.grid(row=4, column=1)

        tk.Label(top, text="Repetible").grid(row=5, column=0)
        repetible = tk.BooleanVar(top)
        repetible.set(False)
        checkbox_repetible = tk.Checkbutton(top, variable=repetible)
        checkbox_repetible.grid(row=5, column=1)

        top.pack()
        self.campos.append({
            "nombre": nombre,
            "texto": texto,
            "metadato": metadato,
            "tipo_campo": tipo_campo,
            "value_pairs_name": value_pairs_name,
            "label_value_pairs": label_value_pairs,
            "dropdown_value_pairs": dropdown_value_pairs,
            "obligatorio": obligatorio,
            "repetible": repetible
        })

    def on_tipo_campo_change(self, value: str, top: tk.Frame):
        for campo in self.campos:
            if campo["tipo_campo"].get() == value:
                if value == "Desplegable":
                    campo["label_value_pairs"].grid()
                    campo["dropdown_value_pairs"].grid()
                else:
                    campo["label_value_pairs"].grid_remove()
                    campo["dropdown_value_pairs"].grid_remove()

    def guardar(self):
        datos = []
        for campo in self.campos:
            tipo_campo_clave = input_types_dict[campo["tipo_campo"].get()]
            datos.append({
                "nombre": campo["nombre"].get(),
                "texto": campo["texto"].get(),
                "metadato": campo["metadato"].get(),
                "tipo_campo": tipo_campo_clave,
                "obligatorio": campo["obligatorio"].get(),
                "value_pairs_name": campo["value_pairs_name"].get(),
                "repetible": campo["repetible"].get()
            })

        with open(self.filename, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'lxml-xml')
        form_definitions = soup.find('form-definitions')

        # Crear tag form
        form = soup.new_tag('form')
        form['name'] = self.nombre_plantilla.get()

        # Añadir tag page a form
        page = soup.new_tag('page')
        page["number"] = "1"
        form.append(page)

        # Añadir campos a page
        for x in datos:
            field = soup.new_tag('field')
            metadato_partes = x["metadato"].split(".")

            # Añadir metadato
            dc_schema = soup.new_tag('dc-schema')
            dc_schema.string = metadato_partes[0]
            field.append(dc_schema)
            dc_element = soup.new_tag('dc-element')
            dc_element.string = metadato_partes[1]
            field.append(dc_element)

            # Añadir dc-qualifier si existe
            if len(metadato_partes) == 3:
                dc_qualifier = soup.new_tag('dc-qualifier')
                dc_qualifier.string = metadato_partes[2]
                field.append(dc_qualifier)

            repeatable = soup.new_tag('repeatable')
            repeatable.string = str(x['repetible'])
            field.append(repeatable)

            label = soup.new_tag('label')
            label.string = x['nombre']
            field.append(label)

            input_type = soup.new_tag('input-type')
            input_type.string = x['tipo_campo']
            if x['tipo_campo'] == 'dropdown':
                input_type['value-pairs-name'] = x['value_pairs_name']
            field.append(input_type)

            hint = soup.new_tag('hint')
            hint.string = x['texto']
            field.append(hint)

            required = soup.new_tag('required')
            required.string = str(x['obligatorio'])
            field.append(required)

            page.append(field)

        form_definitions.insert(0, form)
        formatted_xml = soup.prettify()

        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write(formatted_xml)

        messagebox.showinfo("Plantilla creada", f"Se ha creado la plantilla {self.nombre_plantilla.get()}")

    def get_value_pairs_name_map(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            content = file.read()
        soup = BeautifulSoup(content, 'lxml-xml')
        input_types = soup.find_all('input-type', {'value-pairs-name': True})
        value_pairs_names = [name_map.get('value-pairs-name') for name_map in input_types]

        print(value_pairs_names)
        # Eliminar duplicados
        value_pairs_names = list(set(value_pairs_names))
        value_pairs_names.sort()

        return value_pairs_names
