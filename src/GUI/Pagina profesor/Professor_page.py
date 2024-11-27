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
            pga_name = pga.career.name + " " + pga.semester.name + " " + pga.semester.name
        else:
            pga_name = pga.name
        self.name = pga_name

        pb = ft.ProgressBar(width=400)
        pb.value = pga.methods.completion_rate()

        def delete_pga(pga):

            if type(pga) == Professor:
                self.DB.professors.remove(self.name)
            elif type(pga) == Classroom:
                self.DB.classrooms.remove(pga)
            else:
                self.DB.groups.remove(pga)
            self.listviewpga.update_expansions()
            self.listviewpga.update()

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
                width=1200,
                border_radius=10,
            )
        
        super().__init__(
            content=Title)


class SubjectListView(ft.Column):

    def __init__(self, DB, pga, listviewpga):
        self.DB = DB 
        self.listviewpga = listviewpga
        self.pga = pga

        subjects = []

        button_new_subject = ft.TextButton(
            text="Add Subject",
            on_click=lambda e: self.add_subject(),
            width=200,
            height=30,
        )

        for subject in self.pga.get_subjects():
            name = subject.name 
            progress = ft.ProgressBar(width=400)
            progress.value = 1 - subject.remaining() / subject.total() if subject.total != 0 else 1 
            subject_view = ft.Row(
                controls=[
                    ft.Text(name),
                    progress,
                    ft.Container(content=ft.Text("Details"), 
                                 on_click=lambda e, s=subject: self.edit_subject(s)),
                ],
                spacing=70
            )
            subjects.append(subject_view)
            
        super().__init__(
            controls=[button_new_subject] + subjects,  # Add button for adding new subjects
            alignment=ft.alignment.top_left,
            scroll=ft.ScrollMode.ALWAYS,  # Enable scrolling in the column
            width=1200,
            height=300
        )
    
    def edit_subject(self, s):
        # This should open a new window to edit subject information
        pass 

    def add_subject(self):
        pass


def filter_expansions(expansions, coincidence):
    # This should filter expansions that match the coincidence
    new_expansions = []
    print("Ejecutando filtro de expansiones")
    for expansion in expansions:
        if coincidence.lower() in expansion.data.lower():  # Data stores the name of the PGA
            new_expansions.append(expansion)
            print(len(new_expansions))
    return new_expansions

def generate_expansion_view(pcg, DB, listviewpcg):
    header = Header(DB, pcg, listviewpcg)
    subject_list = SubjectListView(DB, pcg, listviewpcg)
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

    def __init__(self, reference_pcgs, DB):
        self.DB = DB  
        self.reference_pcgs = reference_pcgs
        self.expansions = []

        def search(e):
            coincidence = search_textfield.value
            if coincidence == "":
                all_expansions = self.get_all_expansions()
                expansions_column = ft.Column(
                    controls = all_expansions,
                    scroll=ft.ScrollMode.ALWAYS,  # Enable scrolling in the column
                    width=800,
                    height=600,
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
            scroll=ft.ScrollMode.ALWAYS,  # Enable scrolling in the column
            width=800,
            height=600,
            )
                
        self.charges_expansions(all_expansions, update = False)

        super().__init__(
            content=ft.Column(
                controls=[search_textfield] + [self.expansions_column],
            ),
            width=1200,
            height=600,
        )        
        
    def charges_expansions(self, expansions, update = True):
        self.expansions = expansions
        if update:
            expansions_column = ft.Column(
                controls = expansions,
                scroll=ft.ScrollMode.ALWAYS,  # Enable scrolling in the column
                width=800,
                height=600,
            )
            self.content=ft.Column(
                    controls=[self.search_textfield] + [expansions_column],
                )
            self.update()   #self.content.controls= [self.search_textfield] + [self.expansions_column],
            
            
        
    def get_all_expansions(self):
        expansions = []
        
        for pcg in self.reference_pcgs():
            expansion = generate_expansion_view(pcg, self.DB, self)
            expansions.append(expansion)
            expansions.append(expansion)
        
        return expansions
    
    def search(self, coincidence):
        all_expansions =  self.get_all_expansions()
        expansions_filter = filter_expansions(all_expansions, coincidence)
        expansions_column = ft.Column(
                controls = expansions_filter,
                scroll=ft.ScrollMode.ALWAYS,  # Enable scrolling in the column
                width=800,
                height=600,
            )
        self.content.controls[1] = expansions_column
        self.content.update()

        
        
        
        
        
        
         
class ProfessorsPage(ft.Container):
    
    def __init__(self, bd):
        self.bd = bd  # Database connection
        
        listviewprofessor =  ListViewPCG(Bd.professors.get, Bd)
        self.listviewprofessor = listviewprofessor
        super().__init__(
            content=listviewprofessor,
        )
        pass
    
    def update(self):
        self.listviewprofessor.update()

class ClassroomsPage(ft.Container):

    
    def __init__(self, bd):
        self.bd = bd  # Database connection
        
        listviewclassrooms =  ListViewPCG(Bd.classrooms.get, Bd)
        self.listviewclassrooms = listviewclassrooms
        super().__init__(
            content=listviewclassrooms,
        )
        pass
    
    def update(self):
        self.listviewclassrooms.update()
        



class GroupsPage(ft.Container):

    
    def __init__(self, bd):
        self.bd = bd  # Database connection
        
        listviewgroups =  ListViewPCG(Bd.groups.get, Bd)
        self.listviewgroups = listviewgroups
        super().__init__(
            content= ft.Column(
                controls = [
                    #NewGroup(self.bd, listviewgroups),
                    listviewgroups
                ],
                spacing=20
            )
        )
        pass
    
    def update(self):
        self.listviewgroups.update()



professor_page = ProfessorsPage(Bd)
classroom_page = ClassroomsPage(Bd)
group_page = GroupsPage(Bd)



def main(page: ft.Page):
    page.add(group_page) 

ft.app(main)
