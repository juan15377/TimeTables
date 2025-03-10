import sys
import flet as ft
from src.UI.database import database
from src.UI.components.search_bar_items import SearchBarItems

import flet as ft

import flet as ft

import flet as ft

class TableGroups(ft.UserControl):  # Heredamos de UserControl para usarlo como componente personalizado
    def __init__(self):
        super().__init__()
        self.groups = []  # Almacena los grupos localmente

        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Carrera", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Semestre", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("SubGrupo", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Eliminar", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            border=ft.border.all(1, ft.colors.GREY_700),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_700),
            horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_700),
            heading_row_color=ft.colors.BLUE_800,
            heading_row_height=40,
            data_row_color={"hovered": ft.colors.GREY_800},
            show_checkbox_column=False,
            divider_thickness=0,
        )

    def build(self):
        return ft.Container(
            content=ft.ListView(controls=[self.table], expand=True),
            expand=True,
            border=ft.border.all(2, ft.colors.BLUE_200)
        )

    def add_group(self, group):
        # Agrega un grupo a la tabla y actualiza la lista local
        if group in self.groups:
            return None
        self.groups.append(group)
        button_delete = ft.IconButton(
            icon=ft.icons.DELETE,
            on_click=lambda e, group=group: self.remove_group(group)
        )
        self.table.rows.append(
            ft.DataRow(
                cells=[
                    # Ajustar el ancho del texto dentro de la celda
                    ft.DataCell(ft.Text(group.career.name, width=200)),  # Ancho máximo para el texto
                    ft.DataCell(ft.Text(group.semester.name)),
                    ft.DataCell(ft.Text(str(group.subgroup.name), )),
                    ft.DataCell(button_delete),
                ]
            )
        )
        self.table.update()

    def remove_group(self, group):
        # Elimina un grupo de la lista local y actualiza las filas
        if group in self.groups:
            self.groups.remove(group)
            self.table.rows = [
                row for row in self.table.rows
                if row.cells[0].content.value != group.career.name or
                row.cells[1].content.value != group.semester.name or
                row.cells[2].content.value != str(group.subgroup.name)
            ]
            self.table.update()

    def get_groups(self):
        # Devuelve la lista de grupos
        return self.groups

class GroupSelector(ft.Container):
    
    
    def __init__(self):
        tablegroups = TableGroups()
        button_add_group_to_table = ft.FloatingActionButton(
            icon = ft.icons.ADD,
            text = ""
        )
                
        self.table_groups = tablegroups
        
        
        def get_actual_groups():
            return {group.career.name + " " + group.semester.name + " " +  group.subgroup.name : group for group in database.groups.get()}
        
        search_values_textfield = SearchBarItems(
            {group.career.name + " " + group.semester.name + " " +  group.subgroup.name : group for group in database.groups.get()},
            get_actual_groups,  # setear los valores de la búsqueda
        )
        #search_values_textfield.height = 400
        #search_values_textfield.width = 600
        
        self.search_values_textfield = search_values_textfield
        
        button_add_group_to_table.on_click = lambda e : self.add_group_to_table() 
        
        super().__init__(
            content = ft.Column(

                controls=[
                    ft.Row(
                        controls = [
                            search_values_textfield,
                            button_add_group_to_table
                        ],
                        expand = False
                    ),
                    tablegroups,
                ],
                spacing=50,
                expand = False
            ),
            expand = False,
                        border = ft.border.all(2, ft.colors.BLUE_200)

        )
        
        
    def add_group_to_table(self):
        # Agrega un grupo seleccionado a la tabla
        group = self.search_values_textfield.get_value()
        if group:
            self.table_groups.add_group(group)
        self.update()
        
    def get_groups(self):
        # Devuelve la lista de grupos seleccionados
        return self.table_groups.get_groups()
        
        
        

# def main(page: ft.Page):
#     page.title = "Gestión de Grupos"
#     selector_grupos = GroupSelector(Bd)
    
#     page.add(selector_grupos)
    



# ft.app(target=main)
