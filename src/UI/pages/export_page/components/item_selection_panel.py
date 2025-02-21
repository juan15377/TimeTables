import flet as ft  
from src.tests.database_example import database_example 

class ItemSelectionPanel(ft.Container):
    
    def __init__(self, professors, classrooms, groups):
        
        selected_items = { "Professor": set(), "Classroom": set(), "Group": set() }
        
        # Datos
        all_professors = professors
        all_rooms = classrooms
        all_groups = groups
        
        self.selected_items = selected_items

        # Contenedores para los componentes de la interfaz
        professors_column = ft.ListView(expand = True)
        rooms_column = ft.ListView(expand = True)
        groups_column = ft.ListView(expand = True)

        # Función para manejar la selección de checkboxes
        def toggle_checkbox(tipo, e):
            if e.control.value:
                selected_items[tipo].add(e.control.data)
            else:
                selected_items[tipo].discard(e.control.data)
            print(f"Seleccionados {tipo}: {selected_items[tipo]}")

        # Función para actualizar la lista de items
        def update_list(tipo, search_text="", init = False):
            search_text = search_text.lower()
            items = []
            if tipo == "Professor":
                items = all_professors
            elif tipo == "Classroom":
                items = all_rooms
            elif tipo == "Group":
                items = all_groups

            items_with_score = []

            for item in items:
                lower_item = item.name.lower()
                score = 0

                if search_text in lower_item:
                    score = len(search_text) / len(lower_item)  # Más coincidencia, mayor score
                    if lower_item.startswith(search_text):
                        score += 1  # Coincidencia al inicio tiene más prioridad

                items_with_score.append((score, item))

            sorted_items = [item for _, item in sorted(items_with_score, key=lambda x: (-x[0], x[1].name))]

            if tipo == "Professor":
                professors_column.controls.clear()
            elif tipo == "Classroom":
                rooms_column.controls.clear()
            elif tipo == "Group":
                groups_column.controls.clear()

            for item in sorted_items:
                cb = ft.Checkbox(label=item.name, value=item in selected_items[tipo], on_change=lambda e, tipo=tipo: toggle_checkbox(tipo, e), data = item)
                container = ft.Container(content=cb, on_long_press = lambda e, name=item.name : print(name), bgcolor="blue")
                if tipo == "Professor":
                    professors_column.controls.append(container)
                elif tipo == "Classroom":
                    rooms_column.controls.append(container)
                elif tipo == "Group":
                    groups_column.controls.append(container)
            
            if not init :
                self.update()

        # Funciones de selección/deselección masiva
        def select_all(tipo, e):
            if tipo == "Professor":
                for item in all_professors:
                    selected_items[tipo].add(item)
                for cb in professors_column.controls:
                    cb.content.value = True
            elif tipo == "Classroom":
                for item in all_rooms:
                    selected_items[tipo].add(item)
                for cb in rooms_column.controls:
                    cb.content.value = True
            elif tipo == "Group":
                for item in all_groups:
                    selected_items[tipo].add(item)
                for cb in groups_column.controls:
                    cb.content.value = True
            self.update()

        def deselect_all(tipo, e):
            selected_items[tipo].clear()
            if tipo == "Professor":
                for cb in professors_column.controls:
                    cb.content.value = False
            elif tipo == "Classroom":
                for cb in rooms_column.controls:
                    cb.content.value = False
            elif tipo == "Group":
                for cb in groups_column.controls:
                    cb.content.value = False
            self.update()

        # Funciones de búsqueda
        def on_search_professors(e):
            update_list("Professor", professors_search_box.value)

        def on_search_rooms(e):
            update_list("Classroom", rooms_search_box.value)

        def on_search_groups(e):
            update_list("Group", groups_search_box.value)

        # Campos de búsqueda
        professors_search_box = ft.TextField(label="Buscar profesor...", on_change=on_search_professors,)
        rooms_search_box = ft.TextField(label="Buscar aula...", on_change=on_search_rooms,)
        groups_search_box = ft.TextField(label="Buscar grupo...", on_change=on_search_groups,)

        # Inicializar las listas
        update_list("Professor", init=True)
        update_list("Classroom", init=True)
        update_list("Group", init = True)

        # Crear los botones
        professors_buttons = ft.Row([
            ft.ElevatedButton("Seleccionar todos", on_click=lambda e: select_all("Professor", e), expand = True),
            ft.ElevatedButton("Deseleccionar todos", on_click=lambda e: deselect_all("Professor", e), expand = True),
        ],)

        rooms_buttons = ft.Row([
            ft.ElevatedButton("Seleccionar todos", on_click=lambda e: select_all("Classroom", e), expand = True),
            ft.ElevatedButton("Deseleccionar todos", on_click=lambda e: deselect_all("Classroom", e), expand = True),
        ])

        groups_buttons = ft.Row([
            ft.ElevatedButton("Seleccionar todos", on_click=lambda e: select_all("Group", e), expand = True),
            ft.ElevatedButton("Deseleccionar todos", on_click=lambda e: deselect_all("Group", e), expand = True),
        ])

        # Agregar los componentes a la página
        super().__init__(
            content = ft.Row([
                ft.Column([professors_search_box, professors_buttons, professors_column], expand=True),
                ft.Column([rooms_search_box, rooms_buttons, rooms_column], expand=True),
                ft.Column([groups_search_box, groups_buttons, groups_column], expand=True),
            ],
            expand = True),
            expand = True
        )
    
    def get_selected_items(self):
        return self.selected_items

