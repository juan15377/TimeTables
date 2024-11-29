import flet as ft 
import sys 

sys.path.append("src/Logic/")
sys.path.append("tests/Logic/")
sys.path.append("src/GUI/Utils/")


from name_and_code import NameCodeSubject # encargado del nombre y codigo de la materia 
from groups_selector import GroupSelector  # para saber en que grupos se dara la materia
from SearchValue import SearchValue # para saber en que aula y que profesor dara la materia 
from hours_distribution import SelectorDistributionHours
import sys 

from Subjects import InfoSubject

from tests_3 import Bd

class NavigatorBarBack(ft.Container):
    
    def __init__(self, funct_to_back):
        print("funct_to_back", funct_to_back)

        pagelet = ft.Pagelet(
            appbar=ft.AppBar(
                leading=ft.IconButton(icon = ft.icons.ARROW_BACK, 
                                    on_click = lambda e: funct_to_back()),
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

# esta clase tiene dos objectivos, que carguen los datos de una materia y desde este se puedan editar estos
# otro es que esta clase tiene es que sea capaz de crear una nueva materia 
class SubjectEditor(ft.Container):
    
    def __init__(self, bd, reference_page_router, subject = False):
        print(reference_page_router)
        self.bd = bd
        
        name_code_subject = NameCodeSubject("", "")
        self.name_code_subject = name_code_subject
        name_code_subject.spacing = 50
        
        groups_selector = GroupSelector(bd)
        self.groups_selector = groups_selector
        
        
        def get_actual_professors():
            return {
            professor.name:professor for professor in self.bd.professors.get()
        }
        
        professor_selector = SearchValue({
                    professor.name:professor for professor in bd.professors.get()
                },
                get_actual_professors                                
        )
        self.professor_selector = professor_selector
        
        
        professor_selector.width = 400
        
        
        
        def get_actual_classrooms():
            return {classroom.name: classroom for classroom in self.bd.classrooms.get()}
        
        
        classroom_selector = SearchValue(
            {classroom.name: classroom for classroom in bd.classrooms.get()},
            get_actual_classrooms
        )
        
        classroom_selector.width = 400
        
        self.classroom_selector = classroom_selector
        # Diseño del sector de aula y de professor 
        classroom_selector.spacing = 100
        
        selector_hours_distribution = SelectorDistributionHours()
        self.selector_hours_distribution = selector_hours_distribution
        
        button_save_changes = ft.IconButton(
            icon = ft.icons.SAVE,
            on_click = lambda e: self.save_changes()
        )
        
        button_cancel = ft.IconButton(
            icon = ft.icons.CANCEL,
            on_click = lambda e: self.cancel()
        )
        
        button_new_subject = ft.IconButton(
            icon = ft.icons.ADD,
            on_click = lambda e: self.new_subject_in_bd()
        )
        
        
        
        navigator = NavigatorBarBack(reference_page_router)
        
        
        down_layout = ft.Row(
                controls = [
                    ft.Column(
                        controls=[
                            name_code_subject,
                            #professor_selector,
                            #classroom_selector
                            groups_selector,
                            
                        ]
                    ),
                    ft.Column(
                        controls=[
                            #selector_hours_distribution,
                            #groups_selector,
                            ft.Row(
                                controls = [
                                    ft.Column(
                                        controls=[
                                            ft.Text("Aula"),
                                            classroom_selector,
                                        ]
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Text("Profesor"),
                                            professor_selector,
                                        ]
                                    )
                                ]
                            ),

                            selector_hours_distribution,
                            ft.Row(
                                controls = [
                                    button_cancel,
                                    button_save_changes,
                                    button_new_subject
                                    ]
                            )        
                            
                        ],
                        spacing=50
                    ),
                    ft.Row(
                        controls=[

                            
                        ],
                        spacing=50
                    ),
                    
                ]
            )
        
        head_layout = navigator
        
        super().__init__(
            content = ft.Column(
                controls=[
                    head_layout,
                    down_layout
                ],
            ),
            margin = 20,
            expand = True
        )
        
        pass 
    
    def save_changes(self):
        print(len(self.bd.subjects.get()))
        pass
    
    
    def cancel(self):
        #enruting for another page
        pass
    
    
        
    def load_subject(self, subject):
        pass  
    
    
    # encargado de regresar un
    def new_subject_in_bd(self):
        name, code = self.name_code_subject.get_name_and_code()
        groups = self.groups_selector.get_groups()
        professor = self.professor_selector.get_value()
        classroom = self.classroom_selector.get_value()
        hours_distribution = self.selector_hours_distribution.get_hours_distribution()
        print("Total de horas", hours_distribution.total())
        
        # crear nueva materia en la base de datos
        
        info_subject = InfoSubject(
            name, 
            code, 
            professor, 
            classroom, 
            groups, 
            hours_distribution
        )
        
        self.bd.subjects.add(info_subject)
        
        pass
        
        
    def set_values_subject(self):
        pass 
        
    
    
def main(page : ft.page):
    subject_editor = SubjectEditor(Bd, lambda: print("hola"))
    page.add(subject_editor)
    
ft.app(target=main)
