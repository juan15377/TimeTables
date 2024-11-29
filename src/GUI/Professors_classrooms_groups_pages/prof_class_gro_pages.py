import flet as ft
import sys  
import time as tm 
sys.path.append("tests/Logic/")
sys.path.append("src/Logic/")
# Object responsible for creating a list
from tests_3 import Bd
from Professor_Classroom_Group import Professor, Classroom, Group
from new_career_semestre_subgroup import NewGroup
from new_professor_classroom import NewProfessor, NewClassroom


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
        


class SubjectListView(ft.Column):

    def __init__(self, DB, pga, listviewpga, reference_to_add_subject):
        self.DB = DB 
        self.listviewpga = listviewpga
        self.pga = pga
        self.reference_to_add_subject = reference_to_add_subject

        subjects = []

        button_new_subject = ft.TextButton(
            text="Add Subject",
            on_click=lambda e: self.add_subject(),
            width=1600,
            height=60,
        )

        for subject in self.pga.get_subjects():
            
            def delete_subject_from_bd(subject):
                self.DB.subjects.remove(subject)
                self.update()
                
            name = subject.name 
            progress = ft.ProgressBar(width=400)
            progress.value = 1 - subject.remaining() / subject.total() if subject.total() != 0 else 1 
            subject_view = ft.Row(
                controls=[
                    ft.Text(name),
                    progress,
                    ft.Container(content=ft.Text("Delete"), 
                                 on_click=lambda e, s=subject: delete_subject_from_bd(s)),
                ],
                spacing=150,
                width = 1200,
            )
            print(1 - subject.remaining() / subject.total() if subject.total() != 0 else 1 )
            subjects.append(subject_view)
            
        super().__init__(
            controls=[button_new_subject] + subjects,  # Add button for adding new subjects
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
        subjects = []
        for subject in self.pga.get_subjects():
 
            def delete_subject_from_bd(subject):
                self.DB.subjects.remove(subject)
                self.update()
                
            name = subject.name 
            progress = ft.ProgressBar(width=400)
            progress.value = 1 - subject.remaining() / subject.total() if subject.total() != 0 else 1 
            subject_view = ft.Row(
                controls=[
                    ft.Text(name),
                    progress,
                    ft.Container(content=ft.Text("Delete"), 
                                 on_click=lambda e, s=subject: delete_subject_from_bd(s)),
                ],
                spacing=150,
                width = 1200,
            )
            subjects.append(subject_view)
        self.controls = [self.button_new_subject] + subjects
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
    subject_list = SubjectListView(DB, pcg, listviewpcg, reference_to_add_subject)
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
            height=500,
            
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
            width=1000
        )

         
class ProfessorsPage(ft.Container):
    
    def __init__(self, bd, navigate_to_main_page, reference_to_add_subject):
        self.bd = bd  # Database connection
        

        listviewprofessor =  ListViewPCG(Bd.professors.get, Bd, reference_to_add_subject)
        self.listviewprofessor = listviewprofessor
        navigatorbar = NavigatorBarBack(navigate_to_main_page)
        
        super().__init__(
            content= ft.Column(
                controls = [
                    navigatorbar,
                    NewProfessor(self.bd, listviewprofessor),
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
        
        listviewclassrooms =  ListViewPCG(Bd.classrooms.get, Bd, reference_to_add_subject)
        self.listviewclassrooms = listviewclassrooms
        navigatorbar = NavigatorBarBack(navigate_to_main_page)
        
        super().__init__(
            content= ft.Column(
                controls = [
                    navigatorbar,
                    NewClassroom(self.bd, listviewclassrooms),
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
        
        listviewgroups =  ListViewPCG(Bd.groups.get, Bd, reference_to_add_subject)
        navigatorbar = NavigatorBarBack(navigate_to_main_page)

        self.listviewgroups = listviewgroups
        super().__init__(
            content= ft.Column(
                controls = [
                    navigatorbar,
                    NewGroup(self.bd, listviewgroups),
                    listviewgroups
                ],
                spacing=20,
                height=1000,
                width=1600
            )
        )
        pass
    
    def update(self, update = True):
        self.listviewgroups.update_(update)


