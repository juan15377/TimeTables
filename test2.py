import flet as ft

def main(page: ft.Page):
    selected_items = { "Profesor": set(), "Aula": set(), "Grupo": set() }
    
    # Datos
    all_professors = [f"Profesor {i}" for i in range(1, 21)]
    all_rooms = [f"Aula {i}" for i in range(1, 11)]
    all_groups = [f"Grupo {i}" for i in range(1, 6)]

    # Contenedores para los componentes de la interfaz
    professors_column = ft.ListView(expand = True)
    rooms_column = ft.ListView(expand = True)
    groups_column = ft.ListView(expand = True)

    # Función para manejar la selección de checkboxes
    def toggle_checkbox(tipo, e):
        if e.control.value:
            selected_items[tipo].add(e.control.label)
        else:
            selected_items[tipo].discard(e.control.label)
        print(f"Seleccionados {tipo}: {selected_items[tipo]}")

    # Función para actualizar la lista de items
    def update_list(tipo, search_text=""):
        search_text = search_text.lower()
        items = []
        if tipo == "Profesor":
            items = all_professors
        elif tipo == "Aula":
            items = all_rooms
        elif tipo == "Grupo":
            items = all_groups

        items_with_score = []

        for item in items:
            lower_item = item.lower()
            score = 0

            if search_text in lower_item:
                score = len(search_text) / len(lower_item)  # Más coincidencia, mayor score
                if lower_item.startswith(search_text):
                    score += 1  # Coincidencia al inicio tiene más prioridad

            items_with_score.append((score, item))

        sorted_items = [item for _, item in sorted(items_with_score, key=lambda x: (-x[0], x[1]))]

        if tipo == "Profesor":
            professors_column.controls.clear()
        elif tipo == "Aula":
            rooms_column.controls.clear()
        elif tipo == "Grupo":
            groups_column.controls.clear()

        for item in sorted_items:
            cb = ft.Checkbox(label=item, value=item in selected_items[tipo], on_change=lambda e, tipo=tipo: toggle_checkbox(tipo, e))
            container = ft.Container(content=cb)
            if tipo == "Profesor":
                professors_column.controls.append(container)
            elif tipo == "Aula":
                rooms_column.controls.append(container)
            elif tipo == "Grupo":
                groups_column.controls.append(container)

        page.update()

    # Funciones de selección/deselección masiva
    def select_all(tipo, e):
        if tipo == "Profesor":
            for item in all_professors:
                selected_items[tipo].add(item)
            for cb in professors_column.controls:
                cb.content.value = True
        elif tipo == "Aula":
            for item in all_rooms:
                selected_items[tipo].add(item)
            for cb in rooms_column.controls:
                cb.content.value = True
        elif tipo == "Grupo":
            for item in all_groups:
                selected_items[tipo].add(item)
            for cb in groups_column.controls:
                cb.content.value = True
        page.update()

    def deselect_all(tipo, e):
        selected_items[tipo].clear()
        if tipo == "Profesor":
            for cb in professors_column.controls:
                cb.content.value = False
        elif tipo == "Aula":
            for cb in rooms_column.controls:
                cb.content.value = False
        elif tipo == "Grupo":
            for cb in groups_column.controls:
                cb.content.value = False
        page.update()

    # Funciones de búsqueda
    def on_search_professors(e):
        update_list("Profesor", professors_search_box.value)

    def on_search_rooms(e):
        update_list("Aula", rooms_search_box.value)

    def on_search_groups(e):
        update_list("Grupo", groups_search_box.value)

    # Campos de búsqueda
    professors_search_box = ft.TextField(label="Buscar profesor...", on_change=on_search_professors,)
    rooms_search_box = ft.TextField(label="Buscar aula...", on_change=on_search_rooms,)
    groups_search_box = ft.TextField(label="Buscar grupo...", on_change=on_search_groups,)

    # Inicializar las listas
    update_list("Profesor")
    update_list("Aula")
    update_list("Grupo")

    # Crear los botones
    professors_buttons = ft.Row([
        ft.ElevatedButton("Seleccionar todos", on_click=lambda e: select_all("Profesor", e)),
        ft.ElevatedButton("Deseleccionar todos", on_click=lambda e: deselect_all("Profesor", e)),
    ],)

    rooms_buttons = ft.Row([
        ft.ElevatedButton("Seleccionar todos", on_click=lambda e: select_all("Aula", e)),
        ft.ElevatedButton("Deseleccionar todos", on_click=lambda e: deselect_all("Aula", e)),
    ])

    groups_buttons = ft.Row([
        ft.ElevatedButton("Seleccionar todos", on_click=lambda e: select_all("Grupo", e)),
        ft.ElevatedButton("Deseleccionar todos", on_click=lambda e: deselect_all("Grupo", e)),
    ])

    # Agregar los componentes a la página
    page.add(
        ft.Row([
            ft.Column([professors_search_box, professors_buttons, professors_column], expand=True),
            ft.Column([rooms_search_box, rooms_buttons, rooms_column], expand=True),
            ft.Column([groups_search_box, groups_buttons, groups_column], expand=True),
        ],
        expand = True)
    )

ft.app(target=main)
