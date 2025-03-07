import sys
import flet as ft
from src.UI.database import database
from src.UI.components.search_bar_items import SearchBarItems

class TableGroups(ft.Container):  # Heredamos de UserControl para usarlo como componente personalizado
    
    def __init__(self):
        self.groups = []  # Almacena los grupos localmente
        
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Carrera")),
                ft.DataColumn(ft.Text("Semestre")),
                ft.DataColumn(ft.Text("SubGrupo")),
                ft.DataColumn(ft.Text("Eliminar")),
            ],
            rows=[],
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
            horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
            heading_row_color=ft.colors.BLUE_200,
            heading_row_height=40,
            data_row_color={"hovered": ft.colors.GREY_200},
            show_checkbox_column=False,
            divider_thickness=0,
        )
        
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Carrera")),
                ft.DataColumn(ft.Text("Semestre")),
                ft.DataColumn(ft.Text("SubGrupo")),
                ft.DataColumn(ft.Text("Eliminar")),
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
        
        super().__init__(
            content = ft.ListView(controls = [self.table]),
            #
            expand = True
            )  # Inicialización de UserControl


    def add_group(self, group):
        # Agrega un grupo a la tabla y actualiza la lista local
        if group in self.groups:
            return None
        self.groups.append(group)
        button_delete = ft.IconButton(
            icon = ft.icons.DELETE,
            on_click=lambda e,group = group: self.remove_group(group)
        )
        self.table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(group.career.name)),
                    ft.DataCell(ft.Text(group.semester.name)),
                    ft.DataCell(ft.Text(str(group.subgroup.name))),
                    ft.DataCell(button_delete),
                ]
            )
        )
        self.table.update()

    def remove_group(self, group):
        # Elimina un grupo de la lista local y actualiza las filas
        self.table.rows.clear()
        self.groups.remove(group)
        for g in self.groups:
            self.groups.remove(g)
            self.add_group(g)
            
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
            expand = False
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
