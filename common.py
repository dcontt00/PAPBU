from bs4 import BeautifulSoup


def asignar_item_submission(item_submission_file: str, collection_handle: str):
    # Asignar la plantilla al archivo 'item_submission.xml'
    with open(item_submission_file, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'lxml-xml')
    submission_map = soup.find('submission-map')

    # Comprobar si existe un 'name-map' con el 'collection-handle' especificado
    name_map = soup.find('name-map', {'collection-handle': collection_handle})
    if not name_map:
        file_name_map = soup.new_tag('name-map')
        file_name_map['collection-handle'] = collection_handle
        file_name_map['submission-name'] = "integraciones"

        submission_map.insert(0, file_name_map)
        with open(item_submission_file, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())


def asignar_input_forms_integraciones(input_forms_integraciones_file: str, collection_handle: str):
    with open(input_forms_integraciones_file, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'lxml-xml')
    form_map = soup.find('form-map')

    # Comprobar si existe un 'name-map' con el 'collection-handle' especificado
    name_map = soup.find('name-map', {'collection-handle': collection_handle})
    if not name_map:
        new_name_map = soup.new_tag('name-map')
        new_name_map['collection-handle'] = collection_handle
        new_name_map['form-name'] = "crossref"
        form_map.insert(0, new_name_map)

        with open(input_forms_integraciones_file, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())
