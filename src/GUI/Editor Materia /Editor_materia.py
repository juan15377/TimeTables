import flet as ft 

from nombre_abreviatura import NameCodeSubject # encargado del nombre y codigo de la materia 
from selector_grupos import GroupSelector  # para saber en que grupos se dara la materia
from seleccionar_aula_profesor import SearchValue # para saber en que aula y que profesor dara la materia 
from seleccionar_composicion_horas import SelectorDistributionHours
import sys 

sys.path.append("src/Logic/")
sys.path.append("tests/Logic/")

from Subjects import InfoSubject

from tests_3 import Bd


# esta clase tiene dos objectivos, que carguen los datos de una materia y desde este se puedan editar estos
# otro es que esta clase tiene es que sea capaz de crear una nueva materia 
class SubjectEditor(ft.Container):
    
    def __init__(self, page : ft.Page, bd, subject = False, page_router = '/'):
        self.bd = bd
        
        name_code_subject = NameCodeSubject("", "")
        self.name_code_subject = name_code_subject
        name_code_subject.spacing = 50
        
        groups_selector = GroupSelector(bd)
        self.groups_selector = groups_selector
        
        professor_selector = SearchValue({
            professor.name:professor for professor in bd.professors.get()
        })
        
        self.professor_selector = professor_selector
        
        classroom_selector = SearchValue(
            {classroom.name: classroom for classroom in bd.classrooms.get()}
        )
        
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
        
        super().__init__(
            content= ft.Row(
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
    subject_editor = SubjectEditor(page, Bd)
    page.add(subject_editor)
    
ft.app(target=main)
