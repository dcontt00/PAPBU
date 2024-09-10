import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET
import buscar_plantilla
import asignar_plantilla
import crear_plantilla
import listar_plantillas
from tkinter import ttk

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
        entry.config(state=tk.NORMAL)
        entry.delete(0, tk.END)
        entry.insert(0, filename)
        entry.config(state="readonly")

        # Mostrar los botones de opciones
        buscar_plantilla.pack()
        asignar_plantilla.pack()
        crear_plantilla.pack()
        modificar_plantilla.pack()
        listar_plantillas.pack()
        buscar_plantilla_ventana.filename = filename
        asignar_plantilla_ventana.filename = filename
        crear_plantilla_ventana.filename = filename
        listar_plantillas_ventana.filename = filename


# Ventanas
ventana = tk.Tk()
buscar_plantilla_ventana = buscar_plantilla.BuscarPlantilla()
asignar_plantilla_ventana = asignar_plantilla.AsignarPlantilla()
crear_plantilla_ventana = crear_plantilla.CrearPlantilla()
listar_plantillas_ventana = listar_plantillas.ListarPlantillas()

ventana.title("Abrir Archivo")
ventana.geometry("600x600")

tk.Label(ventana, text="Seleccione el archivo input-forms.xml para abrirlo:").pack()

# Filename entry
entry = tk.Entry(ventana)
entry.config(state="readonly")
entry.pack(fill="x")

# Crear un botón para abrir el archivo
boton_abrir = tk.Button(ventana, text="Abrir Archivo", command=abrir_archivo)
boton_abrir.pack(pady=20)

# Crear tres botones adicionales y ocultarlos inicialmente
buscar_plantilla = tk.Button(ventana, text="Buscar Plantilla", command=buscar_plantilla_ventana.inicializar_ventana)
asignar_plantilla = tk.Button(ventana, text="Añadir plantilla a colección",
                              command=asignar_plantilla_ventana.inicializar_ventana)
crear_plantilla = tk.Button(ventana, text="Crear plantilla", command=crear_plantilla_ventana.inicializar_ventana)
modificar_plantilla = tk.Button(ventana, text="Modificar plantilla")

listar_plantillas = tk.Button(ventana, text="Listar plantillas", command=listar_plantillas_ventana.inicializar_ventana)

# Iniciar el bucle de la aplicación
ventana.mainloop()
