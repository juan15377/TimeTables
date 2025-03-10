
import sys
import flet as ft
from src.UI.database import database
from .components import * 
from src.UI.components.search_bar_items import SearchBarItems
from src.models.database import *
from src.UI.components.alerts import *


# esta clase tiene dos objectivos, que carguen los datos de una materia y desde este se puedan editar estos
# otro es que esta clase tiene es que sea capaz de crear una nueva materia 

def is_avaible_subject(professor, classroom, groups, hours_distribution, is_online, page):
    
    if professor == None:
        alert = Alert("No se ah seleccionado el professor", page)
        alert.show()
        return False
    if classroom == None and not is_online:
        alert = Alert("No se ah seleccionado el Aula correctamente", page)
        alert.show()
        return False 
    if groups == []:
        alert = Alert("No se ah seleccionado ningun Grupo", page)
        alert.show()
        return False
    if sum(hours_distribution.get_avaible_hours()) == 0:
        alert = Alert("La seleccion de distribuccion de horas es incorrecta", page)
        alert.show()
        return False
    if is_online:
        return True
    if classroom == None:
        return False
    return True



class NewSubjectPage(ft.Container):
    
    __instance = None
    
    def __new__(cls, page, key_subject):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        else:
            print("Extrajo la misma instancia")
            return cls.__instance 
        
    
    def __init__(self, page, key_subject):
        if not hasattr(self, "initialized"):  # Evitar reejecución de __init__
            self.page = page
            
            self.show_to_new_subject = lambda e : AlertNewSubject(self.page).show()
            
            name_code_subject = NameCodeSubject("", "")
            self.name_code_subject = name_code_subject
            
            groups_selector = GroupSelector()
            self.groups_selector = groups_selector
            
            
            
            def get_actual_professors():
                return {
                professor.name:professor for professor in database.professors.get()
            }
            
            professor_selector = SearchBarItems({
                    professor.name : professor for professor in database.professors.get()
                    },
                    get_actual_professors,
                    bar_hint_text= "selecciona un Profesor"
                                
            )
            self.professor_selector = professor_selector
            
            
            #professor_selector.width = 400
            
            
            def get_actual_classrooms():
                return {classroom.name: classroom for classroom in database.classrooms.get()}
            
            
            classroom_selector = SearchBarItems(
                items={classroom.name: classroom for classroom in database.classrooms.get()},
                refresh_items=  get_actual_classrooms,
                bar_hint_text= "selecciona una Aula"
            )
            
            online_switch = OnlineSwitch(classroom_selector)
            self.online_switch = online_switch
            
            
            #classroom_selector.width = 400
            
            self.classroom_selector = classroom_selector
            # Diseño del sector de aula y de professor 
            #classroom_selector.spacing = 100
            
            selector_hours_distribution = SelectorDistributionHours()
            self.selector_hours_distribution = selector_hours_distribution
        
            
            
            button_new_subject = ft.FloatingActionButton(
                text = "New Subject",
                icon = ft.icons.ADD,
                on_click = lambda e: self.new_subject_in_bd(),
                expand = False
            )
            
            select_room = ft.Row(
                controls = [
                    classroom_selector,
                    online_switch,
                ],
            )
            
            column_room_and_professor = ft.Column(
                controls = [
                    ft.Row(
                        [ft.Column(
                            controls = [
                                ft.Text("Aula"),
                                select_room,
                            ],
                            expand = True
                        )
                        ],
                        expand = False
                    ),
                    
                    ft.Column(
                        controls = [
                            ft.Text("Profesor"),
                            ft.Row([professor_selector], expand = False)
                        ],
                    expand = False
                    )
                ],
                expand = False,
                
            )
        
            
            left_layout = ft.Column(
                            controls=[
                                ft.Row(
                                    controls = [name_code_subject],
                                    expand = False,
                                    
                                ),
                                ft.Column(
                                    controls = [
                                        ft.Text("Grupos en la que se impartira la nateria"),
                                        groups_selector
                                    ],
                                ),

                            ],
                            alignment= ft.alignment.center,
                            spacing=10,
                            expand=True,
                        )
            
            
            right_layout = ft.Column(
                controls = [
                    column_room_and_professor,
                    ft.Row([selector_hours_distribution], expand = True),
                    ft.Column([button_new_subject], alignment= ft.alignment.top_right, expand = True)
                ],
                expand = True,
            )
            
            # ajuste de preferencia de expansion 
            right_layout.controls[0].expand= 2
            right_layout.controls[1].expand = 2
            right_layout.controls[2].expand = 1


            content = ft.Column(
                    controls = [

                        ft.Row(
                            controls=[
                                left_layout,
                                right_layout,
                            ],
                            expand = True
                        )
                    ],
                    expand = True,
                    spacing=40
                )
            
            super().__init__(
                content = content,
                expand = True
            )
        
        pass 
    
    def save_changes(self):
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
        is_online = self.online_switch.is_online()
        
        # crear nueva materia en la base de datos
        
        ##if not is_avaible_subject(professor,
         #                     classroom,
         #                     groups,
         #                     hours_distribution,
         #                     is_online):
         #   return None
        
        print("is viable")
        print(is_avaible_subject(
                        professor,
                        classroom,
                        groups,
                        hours_distribution,
                        is_online,
                        self.page
                        )  )
        
        if is_avaible_subject(
                        professor,
                        classroom,
                        groups,
                        hours_distribution,
                        is_online,
                        self.page
                        ):
            
            info_subject = InfoSubject(
                name, 
                code, 
                professor, 
                classroom, 
                groups, 
                hours_distribution,
                is_online,
            )
            
            self.name_code_subject.restart()
            
            database.subjects.add(info_subject)
            print("Juan de Jesus Venegas Flores")
            
            # show to create new subject 
            self.show_to_new_subject(1)
            
        
        pass
        
        
    def set_values_subject(self):
        pass 
        