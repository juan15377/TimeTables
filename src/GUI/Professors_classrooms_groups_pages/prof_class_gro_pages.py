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

        pb = ft.ProgressBar(width=400)
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

        button_remove_pga = ft.Container(
                            content=ft.Text("Delete"),
                            on_click=lambda e, pga=pga: delete_pga(pga),
                            bgcolor=ft.colors.RED,
                            width=70,
                            height=30,
                            alignment=ft.alignment.center
                            )

        Title = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(self.name),
                        pb,
                        ft.Container(
                            content=ft.Text("Delete"),
                            on_click=lambda e, pga=pga: delete_pga(pga),
                            bgcolor=ft.colors.RED,
                            width=70,
                            height=30,
                            alignment=ft.alignment.center
                            ),
                        ft.Container(
                            content=ft.Text("Edit"),
                            on_click=lambda e: self.listviewpga.edit(pga),
                            bgcolor=ft.colors.YELLOW,
                            width=70,
                            height=30,
                            alignment=ft.alignment.center
                        )           
                    ],
                    spacing=50
                ),
                height=50,
                width=1600,
                border_radius=10,
            )
        
        super().__init__(
            content=Title,
            width=1600,
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
        
        
        button_new_subject = ft.FloatingActionButton(
            text="Add Subject",
            on_click=lambda e: self.add_subject(),
            width=1600,
            height=60,
            icon = ft.icons.ADD
        )
        
        subjects = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("name Subject")),
                ft.DataColumn(ft.Text("progress")),
                ft.DataColumn(ft.Text("professor")),
                ft.DataColumn(ft.Text("Classroom")),
                ft.DataColumn(ft.Text("total hours")),
                ft.DataColumn(ft.Text("delete")),
            ]
            )

        for subject in self.pga.get_subjects():
            
            def delete_subject_from_bd(subject):
                self.DB.subjects.remove(subject)
                self.update()
                
            name = subject.name 
            progress = ft.ProgressBar(width=400)
            progress.value = 1 - subject.remaining() / subject.total() if subject.total() != 0 else 1 
            
            subjects.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(name)),
                        ft.DataCell(progress),
                        ft.DataCell(ft.Text(subject.professor.name)),
                        ft.DataCell(ft.Text(subject.classroom.name)),
                        ft.DataCell(ft.Text(str(subject.hours_distribution.total()))),
                        ft.DataCell(ft.Container(content=ft.IconButton(icon = ft.icons.DELETE,
                                                                       on_click=lambda e, s=subject: delete_subject_from_bd(s)),
                                                 
                                                 ), 
                        ),
                    ],
                )
            )
        
            
        super().__init__(
            controls=[subjects],  # Add button for adding new subjects
            alignment=ft.alignment.top_left,
            scroll=ft.ScrollMode.ALWAYS,  # Enable scrolling in the column
            width=1600,
            height=1800,
        )
        
        self.button_new_subject = button_new_subject
    
    def edit_subject(self, s):
        # This should open a new window to edit subject information
        pass 

    def add_subject(self):
        self.reference_to_add_subject()
        pass
    
    def update(self):
        # tambie se tiene que actualizar el header
        

        button_new_subject = ft.FloatingActionButton(
            text="Add Subject",
            on_click=lambda e: self.add_subject(),
            width=1600,
            height=60,
            icon = ft.icons.DELETE
        )
        
        subjects = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("name Subject")),
                ft.DataColumn(ft.Text("progress")),
                ft.DataColumn(ft.Text("professor")),
                ft.DataColumn(ft.Text("Classroom")),
                ft.DataColumn(ft.Text("total hours")),
                ft.DataColumn(ft.Text("delete")),
            ]
        )

        for subject in self.pga.get_subjects():
            
            def delete_subject_from_bd(subject):
                self.DB.subjects.remove(subject)
                self.update()
                
            name = subject.name 
            progress = ft.ProgressBar(width=400)
            progress.value = 1 - subject.remaining() / subject.total() if subject.total() != 0 else 1 
            
            subjects.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(name)),
                        ft.DataCell(progress),
                        ft.DataCell(ft.Text(subject.professor.name)),
                        ft.DataCell(ft.Text(subject.classroom.name)),
                        ft.DataCell(ft.Text(str(subject.hours_distribution.total()))),
                        ft.DataCell(ft.Container(content=ft.Text("Delete"),
                                                 on_click=lambda e, s=subject: delete_subject_from_bd(s)), 
                        ),
                    ],
                )
            )
        
        self.controls = [subjects]
        self.header_subject.update()
        super().update()


def filter_expansions(expansions, coincidence):
    # This should filter expansions that match the coincidence
    new_expansions = []
    print("Ejecutando filtro de expansiones")
    for expansion in expansions:
        if coincidence.lower() in expansion.data.lower():  # Data stores the name of the PGA
            new_expansions.append(expansion)
            print(len(new_expansions))
    return new_expansions

def generate_expansion_view(pcg, DB, listviewpcg, reference_to_add_subject):
    header = Header(DB, pcg, listviewpcg)
    subject_list = SubjectListView(DB, pcg, listviewpcg, reference_to_add_subject, header)
    expansion = ft.ExpansionTile(
                    title=header,
                    subtitle=ft.Text("Subjects"),
                    affinity=ft.TileAffinity.LEADING,
                    controls=[
                            ft.Container(
                                    content=subject_list,
                                    height=200,  # Set height to allow scrolling
                                )
                            ],
                            data=header.name
                        )
    return expansion
# simplemente es una lista de los grupo, aulas, y profesores, simplemente tiene un buscador arriba
# solo actualizar la columas de expansiones

class ListViewPCG(ft.Container):

    def __init__(self, reference_pcgs, DB, reference_to_add_subject):
        self.reference_to_add_subject = reference_to_add_subject
        self.DB = DB  
        self.reference_pcgs = reference_pcgs
        self.expansions = []

        def search(e):
            coincidence = search_textfield.value
            if coincidence == "":
                all_expansions = self.get_all_expansions()
                expansions_column = ft.Column(
                    controls = all_expansions,
                    scroll=ft.ScrollMode.AUTO,  # Enable scrolling in the column
                    width=1300,
                    height=500,
                )
                self.content.controls[1] = expansions_column
                self.content.update()
                return None
            self.search(coincidence)
            


        search_textfield = ft.TextField(
                        label="Search now",
                        on_change=search,
                        width=500,
                        height=70,
                    )
        
        self.search_textfield = search_textfield
                
        all_expansions = self.get_all_expansions()
        
        self.expansions = all_expansions
        
        self.expansions_column = ft.Column(
            controls = self.expansions,
            scroll=ft.ScrollMode.AUTO,  # Enable scrolling in the column
            width=1300,
            height=500,
            )
                
        self.charges_expansions(all_expansions, update = False)

        super().__init__(
            content=ft.Column(
                controls=[search_textfield] + [self.expansions_column],
            ),
            width=1300,
            height=600,
            
            )        
        
    def charges_expansions(self, expansions, update = True):
        self.expansions = expansions
        if update:
            expansions_column = ft.Column(
                controls = expansions,
                scroll=ft.ScrollMode.ALWAYS,  # Enable scrolling in the column
                width=1300,
                height=500,
            )
            self.content=ft.Column(
                    controls=[self.search_textfield] + [expansions_column],
                )
            self.update()   #self.content.controls= [self.search_textfield] + [self.expansions_column],
            
            
        
    def get_all_expansions(self):
        expansions = []
        
        for pcg in self.reference_pcgs():
            expansion = generate_expansion_view(pcg, self.DB, self, self.reference_to_add_subject)
            expansions.append(expansion)
        print("Ingresando ala funcion de obtener todas las expanciones")
        print("Tamaño_de_expansiones :", len(expansions))
        return expansions
    
    def search(self, coincidence):
        all_expansions =  self.get_all_expansions()
        expansions_filter = filter_expansions(all_expansions, coincidence)
        expansions_column = ft.Column(
                controls = expansions_filter,
                scroll=ft.ScrollMode.ALWAYS,  # Enable scrolling in the column
                width=1300,
                height=500,
            )
        self.content.controls[1] = expansions_column
        self.content.update()

    def update_(self, update = True):
        all_expansions = self.get_all_expansions()
        expansions_column = ft.Column(
                controls = all_expansions,
                    scroll=ft.ScrollMode.ALWAYS,  # Enable scrolling in the column
                    width=1300,
                    height=500,
                )
        print("Tamaño_de_expansiones :", len(all_expansions))
        self.content.controls[1].controls.clear()
        self.content.controls[1] = expansions_column
        if update:
            self.content.update()       
        
        
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
            content=ft.Container(),
        )
            
        
        super().__init__(
            content = pagelet,
            height=50,
            width=1450
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
                    navigatorbar,
                    ft.Row(
                        controls = [NewProfessor(self.bd, listviewprofessor),
                                   button_new_subject],
                        spacing= 400
                    ),
                    listviewprofessor
                ],
                height=1000,
                width=1600
            )
        )
        
        def update(self):
            self.listviewprofessor.update_()
            
        pass
    
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
                    navigatorbar,
                    button_new_subject,
                    ft.Row(
                        controls = [NewClassroom(self.bd, listviewclassrooms),
                                    ],
                    ),
                    listviewclassrooms
                ],
                spacing=20,
                height=1000,
                width=1600
            )
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
            icon = ft.icons.DELETE
        )

        self.listviewgroups = listviewgroups
        super().__init__(
            content= ft.Column(
                controls = [
                    navigatorbar,
                    button_new_subject,
                    ft.Row(
                        controls = [NewGroup(self.bd, listviewgroups),
                                    ]
                    ),
                    listviewgroups
                ],
                height=1400,
                width=1600
            )
        )
        pass
    
    def update(self, update = True):
        self.listviewgroups.update_(update)


