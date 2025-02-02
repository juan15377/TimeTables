import sys
import flet as ft
import time as tm

from src.Logic.database import Professor, Classroom, Group
from src.GUI.Professors_classrooms_groups_pages.new_career_semestre_subgroup import NewGroup
from src.GUI.Professors_classrooms_groups_pages.new_professor_classroom import NewProfessor, NewClassroom

class PCGListItem(ft.Container):

    def __init__(self, DB, pga, listviewpga, enrouter_page):
        self.DB = DB 
        self.pga = pga
        self.listviewpga = listviewpga
        if type(pga)== Group:
            pga_name = pga.career.name + " " + pga.semester.name + " " + pga.subgroup.name
        else:
            pga_name = pga.name
        self.name = pga_name

        pb = ft.ProgressBar(width=400, bgcolor= ft.colors.RED, color = "green")
        pb.value = pga.methods.completion_rate()

        self.pb = pb 
        def delete_pga(pga):

            if type(pga) == Professor:
                self.DB.professors.remove(pga)
            elif type(pga) == Classroom:
                self.DB.classrooms.remove(pga)
            else:
                self.DB.groups.remove(pga)
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
            on_click=lambda e: enrouter_page.pcg.change_page(pga),
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

    def __init__(self, reference_pcgs, db, enrouter_page):
        self.db = db
        self.reference_pcgs = reference_pcgs # to get pcgs 
        self.items = []
        self.enrouter_page = enrouter_page
        
        def search(e):
            coincidence = search_textfield.value
            new_items = self.filter(coincidence)
            self.items = new_items
            ft.ListView(expand=1, spacing=10, item_extent=50, on_scroll= lambda e: print("Hola Mundo"))
            self.controls[1].content = ft.ListView(expand=1, spacing=10, item_extent=1,
                                                   controls = new_items)
            self.controls[1].update()
        
        all_items = self.get_all()
        
        column_pcgs = ft.Column(
            controls = all_items,
            scroll=ft.ScrollMode.AUTO, 
        )
        
        content_column = ft.Container(
            content = column_pcgs,
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
        new_expansions = []
        all_expansions = self.get_all()
        for expansion in all_expansions:
            if coincidence.lower() in expansion.data.lower():  # Data stores the name of the PGA
                new_expansions.append(expansion)
        return new_expansions
        pass    
        
        
    def get_all(self):
        all_items = []
        
        for pcg in self.reference_pcgs():
            item = PCGListItem(self.db, pcg, self, self.enrouter_page )
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

        
class NavigatorBarBack(ft.Container):
    
    def __init__(self, enrouter_page):
        
        def funct_to_back():
            enrouter_page.change_page("/")

        pagelet = ft.Pagelet(
            appbar=ft.AppBar(
                leading=ft.IconButton(icon = ft.icons.ARROW_BACK, 
                                    on_click = lambda x: funct_to_back()),
                leading_width=50,
                title=ft.Text(""),
                center_title=False,
                bgcolor=ft.colors.SURFACE_VARIANT,
                actions=[
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="Item 1"),
                            ft.PopupMenuItem(),  # divider
                            ft.PopupMenuItem(
                                text="Checked item",
                                checked=False,
                            ),
                        ]
                    ),
                ],
            ),
            content=ft.Container(
                expand=False),
            height=50,
            
        )
            
        
        super().__init__(
            content = pagelet,
            expand=True
        )

         
class ProfessorsPage(ft.Container):
    
    def __init__(self, bd, enrouter_page):
        self.bd = bd  # Database connection
        

        listviewprofessor =  ListViewPCG(bd.professors.get, bd, enrouter_page)
        self.listviewprofessor = listviewprofessor
        navigatorbar = NavigatorBarBack(enrouter_page)
        
        button_new_subject = ft.FloatingActionButton(
            text="add subject",
            on_click=lambda e: reference_to_add_subject(),
            width=200,
            height=60,
            icon = ft.icons.DELETE
        )
        
        super().__init__(
            content= ft.Column(
                controls = [
                    
                    ft.Row(
                        controls = [
                            navigatorbar,
                        ],
                    ),
                    
                    ft.Row(
                        controls = [NewProfessor(self.bd, listviewprofessor),
                                   button_new_subject
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

    
    def __init__(self, bd, enrouter_page):
        self.bd = bd  # Database connection
        
        def navigate_to_main_page():
            enrouter_page.change_page("/")
        
        listviewclassrooms =  ListViewPCG(bd.classrooms.get, bd, enrouter_page)
        self.listviewclassrooms = listviewclassrooms
        navigatorbar = NavigatorBarBack(enrouter_page)
        
        button_new_subject = ft.FloatingActionButton(
            text="add subject",
            on_click=lambda e: reference_to_add_subject(),
            width=200,
            height=60,
            icon = ft.icons.DELETE
        )
        
        super().__init__(
            content= ft.Column(
                controls = [
                    ft.Row(
                        controls = [
                            navigatorbar,
                        ],
                    ),
                    
                    ft.Row(
                        controls = [NewClassroom(self.bd, listviewclassrooms),
                                     button_new_subject,],
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

    
    def __init__(self, bd, enrouter_page):
        self.bd = bd  # Database connection
        
        listviewgroups =  ListViewPCG(bd.groups.get, bd, enrouter_page)
        
        def navigate_to_main_page():
            enrouter_page.change_page("/")
    
        navigatorbar = NavigatorBarBack(enrouter_page)
        
        button_new_subject = ft.FloatingActionButton(
            text="add subject",
            on_click=lambda e: reference_to_add_subject(),
            width=200,
            height=60,
            icon = ft.icons.DELETE
        )

        self.listviewgroups = listviewgroups
        super().__init__(
            content= ft.Column(
                controls = [
                    ft.Row(
                        controls = [
                            navigatorbar,
                        ],
                    ),
                    
                    button_new_subject,
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


