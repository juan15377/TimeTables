import sys
import flet as ft
import time as tm

from src.models.database import Professor, Classroom, Group, PCG
from src.UI.database import database
from .components import *

PAGE_MAP = {
    Professor : "/PROFESSOR",
    Classroom : "/CLASSROOM",
    Group : "/GROUP",
}


class PCGListItem(ft.Container):

    def __init__(self, value : PCG , listviewpcg, page):
        self.value = value
        self.listviewpga = listviewpga
        
        if type(value)== Group:
            value_name = value.career.name + " " + value.semester.name + " " + value.subgroup.name
        else:
            value_name = value.name
        self.name = value_name

        pb = ft.ProgressBar(width=400, bgcolor= ft.colors.RED, color = "green")
        pb.value = value.methods.completion_rate()

        self.pb = pb 
        def delete_value_in_database(value : PCG):

            if type(value) == Professor:
                database.professors.remove(pga)
            elif type(value) == Classroom:
                database.classrooms.remove(pga)
            else:
                database.groups.remove(pga)
            self.listviewpga.update_()
            
        column_Title = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("progress")),
                ft.DataColumn(ft.Text("Delete")),
                ft.DataColumn(ft.Text("Edit")),
            ],
            checkbox_horizontal_margin= 30,
            animate_offset= 10,
            
            )
        
        button_delete = ft.IconButton(
            on_click=lambda e, pga=pga: delete_pga(pga),
            icon = ft.icons.DELETE_SHARP
        )
        
        button_edit = ft.IconButton(
            on_click=lambda e: page.go(F"{PAGE_MAP[type(value)]}?{value.key.key}"),
            icon = ft.icons.EDIT
        )
        
        column_Title.rows.append(
            ft.DataRow(
                cells=[
                        ft.DataCell(ft.Text(self.name, expand=True)),
                        ft.DataCell(pb),
                        ft.DataCell(button_delete),
                        ft.DataCell(button_edit),
                        ]
            )
        )

    
        
        super().__init__(
            content=column_Title,
            width=1600,
            expand=True,
            theme_mode= ft.colors.AMBER_ACCENT,
            data = pga.name if type(pga) in [Professor, Classroom] else pga.career.name + " " + pga.semester.name + " " + pga.subgroup.name
            )
        
    def edit_availability_matrix(self):
        
        pass 
    
    def delete(self):
        
        pass
    
    def update(self):
        self.pb.value = self.pga.methods.completion_rate()
        self.pb.update()
        pass  
    
# simplemente es una lista de los grupo, aulas, y profesores, simplemente tiene un buscador arriba
# solo actualizar la columas de expansiones


# methods: update
class ListViewPCG(ft.Column):

    def __init__(self, call_refresh_items, page):
        
        self.call_refresh_items = call_refresh_items
        self.items = []
        self.page = page
        
        def search(e):
            coincidence = search_textfield.value
            new_items = self.filter(coincidence)
            self.items = new_items
            self.controls[1].content = ft.ListView(expand=1, spacing=10, item_extent=1,
                                                   controls = new_items)
            self.controls[1].update()
        
        all_items = self.get_all()
        
        column_items = ft.Column(
            controls = all_items,
            scroll=ft.ScrollMode.AUTO, 
        )
        
        content_column = ft.Container(
            content = column_items,
            expand = True
        )
        
        search_textfield = ft.TextField(
                        label="Search now",
                        on_change=search,
                        )
        
        super().__init__(
            controls = [search_textfield] + [content_column],
            expand=True
        )
        
        
    def filter(self, coincidence):
        if coincidence == "":
            return self.get_all()
        new_items = []
        all_items = self.get_all()
        for item in all_items:
            if coincidence.lower() in item.data.lower():  # Data stores the name of the PGA
                new_items.append(expansion)
        return new_items
        pass    
        
        
    def get_all(self):
        all_items = []
        
        for pcg in self.call_refresh_items():
            item = PCGListItem(pcg, self, self.page )
            all_items.append(item)
        return all_items


    def update_(self, update = True):
        all_items = self.get_all()
        self.items = all_items

        self.controls[1].content  = ft.ListView(expand=1, spacing=10, item_extent=50,
                                                   controls = all_items)
        if update:
            self.controls[1].update()
    
    def update(self):
        for item in self.items:
            item.update()



         
class ProfessorsPage(ft.Container):
    
    def __init__(self, page, query):
        self.page = page # Database connection
        

        listviewprofessor =  ListViewPCG(database.professors.get, page)
        self.listviewprofessor = listviewprofessor
    
        
        super().__init__(
            content= ft.Column(
                controls = [
                    
                    ft.Row(
                        controls = [NewProfessor(listviewprofessor),
                        ],
                    ),
                    
                    listviewprofessor,
                ],
                #expand = True
            ),
            expand = True,
            theme_mode=ft.ThemeMode.DARK,
        )
    
    def update(self, update = True):
        self.listviewprofessor.update_(update)


class ClassroomsPage(ft.Container):

    
    def __init__(self, page, query):
        self.page = page  # Database connection
        
        
        listviewclassrooms =  ListViewPCG(database.classrooms.get, page)
        self.listviewclassrooms = listviewclassrooms

        
        super().__init__(
            content= ft.Column(
                controls = [

                    ft.Row(
                        controls = [NewClassroom(listviewclassrooms),
                                     ],
                    ),
                    listviewclassrooms
                ],
                expand=True
            ),
            expand = True
        )
        pass
    
    def update(self, update = True):
        self.listviewclassrooms.update_(update)
        



class GroupsPage(ft.Container):

    
    def __init__(self, page, query):
        self.page = page  # Database connection
        
        listviewgroups =  ListViewPCG(database.groups.get, page)
        

        self.listviewgroups = listviewgroups
        
        super().__init__(
            content= ft.Column(
                controls = [
                    ft.Row(
                        controls = [NewGroup(self.bd, listviewgroups),
                                    ],
                    ),
                    listviewgroups
                ],
                spacing=30
            ),
            expand = True
        )
        pass
    
    def update(self, update = True):
        self.listviewgroups.update_(update)


