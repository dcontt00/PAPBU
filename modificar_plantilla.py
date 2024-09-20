import tkinter as tk
from bs4 import BeautifulSoup
from tkinter import ttk, messagebox
from common import get_form_names

input_types_dict = {
    "Campo de texto": "onebox",
    "Nombre": "name",
    "Desplegable": "dropdown",
    "Área de Texto": "textarea",
    "Fecha": "date",
}


class ModificarPlantilla():
    ventana: tk.Toplevel
    nombre_plantilla: tk.Entry
    files: list[str]
    campos: list

    def inicializar_ventana(self):
        self.campos = []
        self.ventana = tk.Toplevel()
        self.ventana.title("Modificar Plantilla")
        self.ventana.geometry("500x500")

        # Dropdown para elegir la plantilla a modificar
        tk.Label(self.ventana, text="Selecciona la plantilla a modificar").pack()
        form_names = get_form_names(self.files[0])
        self.selected_form_name = tk.StringVar(self.ventana)
        self.selected_form_name.set(form_names[0])
        dropdown = tk.OptionMenu(self.ventana, self.selected_form_name, *form_names)
        dropdown.pack()

        boton_modificar = tk.Button(self.ventana, text="Modificar", command=self.añadir_campo)
        boton_modificar.pack()

        boton_guardar = tk.Button(self.ventana, text="Guardar", command=self.guardar)
        boton_guardar.pack()

    def añadir_campo(self):

        with open(self.files[0], 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'lxml-xml')
        form_definitions = soup.find('form-definitions')
        form = form_definitions.find('form', {'name': self.selected_form_name.get()})
        fields = form.find_all('field')

        for field in fields:
            # Crear un frame para cada campo
            frame = tk.Frame(self.ventana)
            frame.pack(fill='x', padx=5, pady=5)

            # Nombre del campo
            nombre_var = tk.StringVar(value=field.find('label').string)
            tk.Label(frame, text="Nombre:").pack(side='left')
            nombre_entry = tk.Entry(frame, textvariable=nombre_var)
            nombre_entry.pack(side='left')

            # Texto del campo
            texto_var = tk.StringVar(value=field.find('hint').string)
            tk.Label(frame, text="Texto:").pack(side='left')
            texto_entry = tk.Entry(frame, textvariable=texto_var)
            texto_entry.pack(side='left')

            # Metadato
            metadato_var = tk.StringVar(value=f"{field.find('dc-schema').string}.{field.find('dc-element').string}")
            tk.Label(frame, text="Metadato:").pack(side='left')
            metadato_entry = tk.Entry(frame, textvariable=metadato_var)
            metadato_entry.pack(side='left')

            # Tipo de campo
            tipo_campo_var = tk.StringVar(
                value=[k for k, v in input_types_dict.items() if v == field.find('input-type').string][0])
            tk.Label(frame, text="Tipo de campo:").pack(side='left')
            tipo_campo_dropdown = tk.OptionMenu(frame, tipo_campo_var, *input_types_dict.keys(),
                                                command=lambda value: self.on_tipo_campo_change(value, frame))
            tipo_campo_dropdown.pack(side='left')

            # Obligatorio
            obligatorio_var = tk.BooleanVar(value=(field.find('required').string == 'True'))
            obligatorio_check = tk.Checkbutton(frame, text="Obligatorio", variable=obligatorio_var)
            obligatorio_check.pack(side='left')

            # Repetible
            repetible_var = tk.BooleanVar(value=(field.find('repeatable').string == 'True'))
            repetible_check = tk.Checkbutton(frame, text="Repetible", variable=repetible_var)
            repetible_check.pack(side='left')

            # Guardar las variables en self.campos para usarlas más tarde
            self.campos.append({
                "nombre": nombre_var,
                "texto": texto_var,
                "metadato": metadato_var,
                "tipo_campo": tipo_campo_var,
                "obligatorio": obligatorio_var,
                "repetible": repetible_var,
                "field": field
            })

            # Vincular cambios en los elementos de UI a los valores de los fields
            nombre_var.trace_add('write',
                                 lambda *args, f=field, v=nombre_var: f.find('label').string.replace_with(v.get()))
            texto_var.trace_add('write',
                                lambda *args, f=field, v=texto_var: f.find('hint').string.replace_with(v.get()))
            obligatorio_var.trace_add('write',
                                      lambda *args, f=field, v=obligatorio_var: f.find('required').string.replace_with(
                                          str(v.get())))
            repetible_var.trace_add('write',
                                    lambda *args, f=field, v=repetible_var: f.find('repeatable').string.replace_with(
                                        str(v.get())))

            metadato_var.trace_add('write',
                                   lambda *args, f=field, v=metadato_var: f.find('dc-schema').string.replace_with(
                                       v.get().split('.')[0]))
            metadato_var.trace_add('write',
                                   lambda *args, f=field, v=metadato_var: f.find('dc-element').string.replace_with(
                                       v.get().split('.')[1]))
            metadato_var.trace_add('write',
                                   lambda *args, f=field, v=metadato_var: f.find('dc-qualifier').string.replace_with(
                                       v.get().split('.')[2]) if len(v.get().split('.')) == 3 else f.find(
                                       'dc-qualifier').string.replace_with(''))

            # Vincular cambios en el tipo de campo
            tipo_campo_var.trace_add('write',
                                     lambda *args, f=field, v=tipo_campo_var: f.find('input-type').string.replace_with(
                                         input_types_dict[v.get()]))
            if tipo_campo_var.get() == "Desplegable":
                self.campos[-1]["label_value_pairs"].grid()
                self.campos[-1]["dropdown_value_pairs"].grid()
            else:
                self.campos[-1]["label_value_pairs"].grid_remove()
                self.campos[-1]["dropdown_value_pairs"].grid_remove()

            # Dropdown values
            value_pairs_names = self.get_value_pairs_name_map()
            label_value_pairs = tk.Label(frame, text="Valores del desplegable")
            label_value_pairs.pack(side='left')
            value_pairs_name = tk.StringVar(value=field.find('input-type').get('value-pairs-name'))
            dropdown_value_pairs = tk.OptionMenu(frame, value_pairs_name, *value_pairs_names)
            dropdown_value_pairs.pack(side='left')

            self.campos[-1]["value_pairs_name"] = value_pairs_name
            self.campos[-1]["label_value_pairs"] = label_value_pairs
            self.campos[-1]["dropdown_value_pairs"] = dropdown_value_pairs

        self.ventana.update()

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

        print(datos)
        return

        with open(self.files[0], 'r', encoding='utf-8') as file:
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
            else:  # Añadir tag vacío
                dc_qualifier = soup.new_tag('dc-qualifier')
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

        with open(self.files[0], 'w', encoding='utf-8') as file:
            file.write(formatted_xml)

        messagebox.showinfo("Plantilla creada", f"Se ha creado la plantilla {self.nombre_plantilla.get()}")

    def get_value_pairs_name_map(self):
        with open(self.files[0], 'r', encoding='utf-8') as file:
            content = file.read()
        soup = BeautifulSoup(content, 'lxml-xml')
        input_types = soup.find_all('input-type', {'value-pairs-name': True})
        value_pairs_names = [name_map.get('value-pairs-name') for name_map in input_types]

        print(value_pairs_names)
        # Eliminar duplicados
        value_pairs_names = list(set(value_pairs_names))
        value_pairs_names.sort()

        return value_pairs_names
