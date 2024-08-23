import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import xml.etree.ElementTree as ET
import buscar_plantilla
import asignar_plantilla
import crear_plantilla

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


def abrir_archivo():
    filename = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if filename:
        # Leer y parsear el contenido del archivo XML.
        tree = ET.parse(filename)
        root = tree.getroot()
        # Mostrar los botones de opciones
        buscar_plantilla.pack()
        asignar_plantilla.pack()
        crear_plantilla.pack()
        modificar_plantilla.pack()
        buscar_plantilla_ventana.filename = filename
        asignar_plantilla_ventana.filename = filename
        crear_plantilla_ventana.filename = filename


# Ventanas
ventana = tk.Tk()
buscar_plantilla_ventana = buscar_plantilla.BuscarPlantilla()
asignar_plantilla_ventana = asignar_plantilla.AsignarPlantilla()
crear_plantilla_ventana = crear_plantilla.CrearPlantilla()

ventana.title("Abrir Archivo")
ventana.geometry("300x200")
tk.Label(ventana, text="Selecciona un archivo para abrirlo:").pack()

# Crear un botón para abrir el archivo
boton_abrir = tk.Button(ventana, text="Abrir Archivo", command=abrir_archivo)
boton_abrir.pack()

# Crear tres botones adicionales y ocultarlos inicialmente
buscar_plantilla = tk.Button(ventana, text="Buscar Plantilla", command=buscar_plantilla_ventana.inicializar_ventana)
asignar_plantilla = tk.Button(ventana, text="Añadir plantilla a colección",
                              command=asignar_plantilla_ventana.inicializar_ventana)
crear_plantilla = tk.Button(ventana, text="Crear plantilla", command=crear_plantilla_ventana.inicializar_ventana)
modificar_plantilla = tk.Button(ventana, text="Modificar plantilla")

# Iniciar el bucle de la aplicación
ventana.mainloop()
