import flet as ft
import sys

sys.path.append("src/Logic/")
sys.path.append("tests/Logic/")

from tests_3 import Bd
from seleccionar_aula_profesor import SearchValue

groups = Bd.groups


class TableGroups(ft.Container):  # Heredamos de UserControl para usarlo como componente personalizado
    
    def __init__(self):
        self.groups = []  # Almacena los grupos localmente
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Carrera")),
                ft.DataColumn(ft.Text("Semestre")),
                ft.DataColumn(ft.Text("SubGrupo"), numeric=True),
                ft.DataColumn(ft.Text("Eliminar")),
            ],
            rows=[]  # Inicialmente vacío
        )
        
        super().__init__(
            content = self.table)  # Inicialización de UserControl


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


class GroupSelector(SearchValue, ft.Container):
    
    
    def __init__(self, tablegroups : TableGroups, BD, button_add_group_to_table):
        self.table_groups = tablegroups
        
        super().__init__(
            {group.career.name + " " + group.semester.name + " " +  group.subgroup.name : group for group in BD.groups.get()}
        )
        
        button_add_group_to_table.on_click = lambda e : self.add_group_to_table() 
        
        
        
    def add_group_to_table(self):
        # Agrega un grupo seleccionado a la tabla
        group = self.get_value()
        if group:
            self.table_groups.add_group(group)
        self.update()
        
        
        

def main(page: ft.Page):
    page.title = "Gestión de Grupos"
    table = TableGroups()
    button_add_group_to_table = ft.IconButton(
        icon = ft.icons.ADD
    )
    
    selector = GroupSelector(table, Bd, button_add_group_to_table)

    page.add(selector, table, button_add_group_to_table)
    



ft.app(target=main)
