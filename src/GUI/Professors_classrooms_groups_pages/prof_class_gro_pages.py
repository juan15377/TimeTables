import sys
import flet as ft
import time as tm


from src.Logic.Professor_Classroom_Group import Professor, Classroom, Group
from src.GUI.Professors_classrooms_groups_pages.new_career_semestre_subgroup import NewGroup
from src.GUI.Professors_classrooms_groups_pages.new_professor_classroom import NewProfessor, NewClassroom

class Header(ft.Container):

    def __init__(self, DB, pga, listviewpga):
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
            on_click=lambda e: self.listviewpga.edit(pga),
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
            theme_mode= ft.colors.AMBER_ACCENT
            )
        
    def edit_availability_matrix(self):
        
        pass 
    
    def delete(self):
        
        pass
    
    def update(self):
        self.pb.value = self.pga.methods.completion_rate()
        self.pb.update()
        pass  

class SubjectListView(ft.Column):

    def __init__(self, DB, pga, listviewpga, reference_to_add_subject, header_subject):
        self.DB = DB 
        self.listviewpga = listviewpga
        self.pga = pga
        self.reference_to_add_subject = reference_to_add_subject
        self.header_subject = header_subject
            
        super().__init__(
            controls=[],  # Add button for adding new subjects
            scroll=ft.ScrollMode.AUTO,  # Enable scrolling in the column
            expand = True,
            alignment = ft.alignment.top_left,
        )
        
        self.update(update = False)

            
    def edit_subject(self, s):
        # This should open a new window to edit subject information
        pass 

    def add_subject(self):
        self.reference_to_add_subject()
        pass
    
    def update(self, update = True):
        # tambie se tiene que actualizar el header
        
        
        subjects_list = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("name Subject")),
                ft.DataColumn(ft.Text("progress")),
                ft.DataColumn(ft.Text("professor")),
                ft.DataColumn(ft.Text("Classroom")),
                ft.DataColumn(ft.Text("total hours")),
                ft.DataColumn(ft.Text("delete")),
                ft.DataColumn(ft.Text("edit")),
            ],
            width = 1200
        )

        for subject in self.pga.get_subjects():
            
            def delete_subject_from_bd(subject):
                self.DB.subjects.remove(subject)
                self.listviewpga.update()
                self.update()
                
            def edit_subject_from_bd(subject):
                self.edit_subject(subject)
                self.update()
                
            name = subject.name 
            progress = ft.ProgressBar(expand=True)
            progress.value = 1 - subject.remaining() / subject.total() if subject.total() != 0 else 1 
            
            subjects_list.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(name)),
                        ft.DataCell(progress),
                        ft.DataCell(ft.Text(subject.professor.name, expand = True)),
                        ft.DataCell(ft.Text(subject.classroom.name, expand = True)),
                        ft.DataCell(ft.Text(str(subject.hours_distribution.total()))),
                        ft.DataCell(ft.Container(content=ft.IconButton(icon = ft.icons.DELETE,
                                                                       on_click=lambda e, s=subject: delete_subject_from_bd(s)),
                                                 
                                                 ), 
                        ),
                        ft.DataCell(ft.Container(content=ft.IconButton(icon = ft.icons.EDIT,
                                                                       on_click=lambda e, s=subject: edit_subject_from_bd(s)),
                                                 
                                                 )
                        ),
                    ],
                ),

            )
        
        self.controls = [subjects_list]
        if update:
            self.header_subject.update()
            super().update()


class ExpansionPCG(ft.ExpansionTile):
    
    def __init__(self, pcg, DB, listviewpcg, reference_to_add_subject):
        header = Header(DB, pcg, listviewpcg)
        subject_list = SubjectListView(DB, pcg, listviewpcg, reference_to_add_subject, header)
        
        self.subject_list = subject_list
        self.header = header
        
        super().__init__(
                        title=header,
                        affinity=ft.TileAffinity.LEADING,
                        controls=[
                                ft.Container(
                                        content=self.subject_list,
                                        height=400,  # Set height to allow scrolling
                                        alignment= ft.alignment.top_left
                                    )
                                ],
                                data=header.name,
                                on_change = lambda e : subject_list.update(update = True),
                            )

    def update(self):
        self.header.update()
        #self.subject_list.update()
        super().update()
        

def generate_expansion_view(pcg, DB, listviewpcg, reference_to_add_subject):
    
    expansion_pcg = ExpansionPCG(pcg, DB, listviewpcg, reference_to_add_subject)

    return expansion_pcg
# simplemente es una lista de los grupo, aulas, y profesores, simplemente tiene un buscador arriba
# solo actualizar la columas de expansiones


# methods: update
class ListViewPCG(ft.Column):

    def __init__(self, reference_pcgs, DB, reference_to_add_subject):
        self.reference_to_add_subject = reference_to_add_subject
        self.DB = DB  
        self.reference_pcgs = reference_pcgs # to get pcgs 
        self.expansions = []
        
        def search(e):
            coincidence = search_textfield.value
            new_expansions = self.filter_expansions(coincidence)
            self.expansions = new_expansions
            ft.ListView(expand=1, spacing=10, item_extent=50, on_scroll= lambda e: print("Hola Mundo"))
            self.controls[1].content = ft.ListView(expand=1, spacing=10, item_extent=1,
                                                   controls = new_expansions)
            self.controls[1].update()
        
        all_expansions = self.get_all_expansions()
        
        column_pcgs = ft.Column(
            controls = all_expansions,
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
        
        
    def filter_expansions(self, coincidence):
        if coincidence == "":
            return self.get_all_expansions()
        new_expansions = []
        all_expansions = self.get_all_expansions()
        for expansion in all_expansions:
            if coincidence.lower() in expansion.data.lower():  # Data stores the name of the PGA
                new_expansions.append(expansion)
        return new_expansions
        pass    
        
        
    def get_all_expansions(self):
        expansions = []
        
        for pcg in self.reference_pcgs():
            expansion = generate_expansion_view(pcg, self.DB, self, self.reference_to_add_subject)
            expansions.append(expansion)
        return expansions
    

    def update_(self, update = True):
        all_expansions = self.get_all_expansions()
        self.expansions = all_expansions

        self.controls[1].content  = ft.ListView(expand=1, spacing=10, item_extent=50,
                                                   controls = all_expansions)
        if update:
            self.controls[1].update()
    
    def update(self):
        for expansion in self.expansions:
            expansion.update()
        
   
       
        
class NavigatorBarBack(ft.Container):
    
    def __init__(self, funct_to_back):

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
    
    def __init__(self, bd, navigate_to_main_page, reference_to_add_subject):
        self.bd = bd  # Database connection
        

        listviewprofessor =  ListViewPCG(bd.professors.get, bd, reference_to_add_subject)
        self.listviewprofessor = listviewprofessor
        navigatorbar = NavigatorBarBack(navigate_to_main_page)
        
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

    
    def __init__(self, bd, navigate_to_main_page, reference_to_add_subject):
        self.bd = bd  # Database connection
        
        listviewclassrooms =  ListViewPCG(bd.classrooms.get, bd, reference_to_add_subject)
        self.listviewclassrooms = listviewclassrooms
        navigatorbar = NavigatorBarBack(navigate_to_main_page)
        
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

    
    def __init__(self, bd, navigate_to_main_page, reference_to_add_subject):
        self.bd = bd  # Database connection
        
        listviewgroups =  ListViewPCG(bd.groups.get, bd, reference_to_add_subject)
        navigatorbar = NavigatorBarBack(navigate_to_main_page)
        
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


