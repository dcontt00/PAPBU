import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET
import buscar_plantilla
import asignar_plantilla
import crear_plantilla
import listar_plantillas
import modificar_plantilla
import os

root_element = None


def obtener_form_name_por_collection_handle(filename, collection_handle):
    # Parsear el archivo XML
    tree = ET.parse(filename)
    root = tree.getroot()

    # Buscar todas las etiquetas 'name-map'
    name_maps = root.findall('name-map')

    # Iterar sobre las etiquetas para encontrar el 'collection-handle' especificado
    for name_map in name_maps:
        if name_map.get('collection-handle') == collection_handle:
            return name_map.get('form-name')

    return None


def abrir_archivos():
    filenames = filedialog.askopenfilenames(filetypes=[("XML files", "*.xml")])
    required_files = {'input-forms.xml', 'input-forms-integraciones.xml', 'item-submission.xml'}
    selected_files = {os.path.basename(file) for file in filenames}
    print(filenames)

    if required_files.issubset(selected_files):

        # Asignar archivos a funciones
        input_forms_file = None
        input_forms_integraciones_file = None
        item_submission_file = None

        for file in filenames:
            if os.path.basename(file) == 'input-forms.xml':
                input_forms_file = file
            elif os.path.basename(file) == 'input-forms-integraciones.xml':
                input_forms_integraciones_file = file
            elif os.path.basename(file) == 'item-submission.xml':
                item_submission_file = file

        files = [input_forms_file, input_forms_integraciones_file, item_submission_file]

        entry.config(state=tk.NORMAL)
        entry.delete(0, tk.END)
        entry.insert(0, filenames)
        entry.config(state="readonly")

        # Mostrar los botones de opciones
        buscar_plantilla.pack()
        asignar_plantilla.pack()
        crear_plantilla.pack()
        modificar_plantilla.pack()
        listar_plantillas.pack()

        # Asignar archivos a las ventanas
        buscar_plantilla_ventana.files = files
        asignar_plantilla_ventana.files = files
        crear_plantilla_ventana.files = files
        listar_plantillas_ventana.files = files
        modificar_plantilla_ventana.files = files


# Ventanas
ventana = tk.Tk()
buscar_plantilla_ventana = buscar_plantilla.BuscarPlantilla()
asignar_plantilla_ventana = asignar_plantilla.AsignarPlantilla()
crear_plantilla_ventana = crear_plantilla.CrearPlantilla()
listar_plantillas_ventana = listar_plantillas.ListarPlantillas()
modificar_plantilla_ventana = modificar_plantilla.ModificarPlantilla()

ventana.title("Abrir Archivo")
ventana.geometry("600x600")

tk.Label(ventana,
         text="Seleccione los archivos input-forms.xml, input-forms-integraciones.xml y item-submission.xml para abrirlos:").pack()

# Filename entry
entry = tk.Entry(ventana)
entry.config(state="readonly")
entry.pack(fill="x")

# Crear un botón para abrir el archivo
boton_abrir = tk.Button(ventana, text="Abrir Archivos", command=abrir_archivos)
boton_abrir.pack(pady=20)

# Crear tres botones adicionales y ocultarlos inicialmente
buscar_plantilla = tk.Button(ventana, text="Buscar Plantilla", command=buscar_plantilla_ventana.inicializar_ventana)
asignar_plantilla = tk.Button(ventana, text="Asignar plantilla a colección",
                              command=asignar_plantilla_ventana.inicializar_ventana)
crear_plantilla = tk.Button(ventana, text="Crear plantilla", command=crear_plantilla_ventana.inicializar_ventana)
modificar_plantilla = tk.Button(ventana, text="Modificar plantilla")

listar_plantillas = tk.Button(ventana, text="Listar plantillas", command=listar_plantillas_ventana.inicializar_ventana)
modificar_plantilla = tk.Button(ventana, text="Modificar plantilla",
                                command=modificar_plantilla_ventana.inicializar_ventana)

# Iniciar el bucle de la aplicación
ventana.mainloop()
