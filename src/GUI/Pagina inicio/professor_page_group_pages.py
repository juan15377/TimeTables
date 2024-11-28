from TMaterias import ControlBlocksSubject
from TMaterias import SearchValue
from TMaterias import Bd
from TMaterias import DEFAULT_PCG

import sys 
sys.path.append("src/GUI/Enrutador/")


class ProfesorMainPage(ControlBlocksSubject):
    
    def __init__(self, bd, reference_enrouter_page):
        
        def change_professor(e):
            selected = self.professor_search.get_value()
            self.set_pcg(selected)
            
        def get_actual_profesors():
            return {
            professor.name: professor for professor in bd.professors.get()
            }

        
        self.professor_search =  SearchValue({
            professor.name: professor for professor in bd.professors.get()
            },
            get_actual_profesors,
            on_change = change_professor
            )
        
        def change_to_professors(e):
            reference_enrouter_page('/PROFESSORS') # cambiar la pagina de profesores
        
        super().__init__(bd, DEFAULT_PCG, self.professor_search, change_to_professors)
        
    def update(self):
        self.professor_search.update()
        

class ClassroomMainPage(ControlBlocksSubject):
    
    def __init__(self, bd, reference_enrouter_page):
        
        def change_classroom(e):
            seleccionado = self.classroom_search.get_value()
            self.set_pcg(seleccionado)
            
        def get_actual_classrooms():
            return {
            classroom.name: classroom for classroom in bd.classrooms.get()
            }


        self.classroom_search = SearchValue({
            classroom.name: classroom for classroom in Bd.classrooms.get()
            },
            get_actual_classrooms,  # setear los valores de la búsqueda  
            on_change = change_classroom
        )
        
        def change_to_classrooms(e):
            reference_enrouter_page('/CLASSROOMS') # cambiar la pagina de aulas 
        
        super().__init__(bd, DEFAULT_PCG, self.classroom_search, change_to_classrooms)
        
    def update(self):
        self.classroom_search.update()
        
class GroupMainPage(ControlBlocksSubject):
    
    def __init__(self, bd, reference_enrouter_page):
        
        def change_group(e):
            seleccionado = self.group_search.get_value()
            self.set_pcg(seleccionado)

        def get_actual_groups():
            return {
            group.career.name + " " + group.semester.name + " " + group.subgroup.name: group for group in bd.groups.get()
            }
        
        self.group_search = SearchValue({
            group.career.name + " " + group.semester.name + " " + group.subgroup.name:group for group in Bd.groups.get()
            },
            get_actual_groups,  # setear los valores de la búsqueda
            on_change = change_group
        )
        
        def change_to_groups(e):
            reference_enrouter_page('/GROUPS') # cambiar la pagina a 

        super().__init__(bd, DEFAULT_PCG, self.group_search, change_to_groups)
    
    def update(self):
        self.group_search.update()
    

#lista = [0]
#
#def main(page : ft.Page):
#    boardsubject = ControlBlocksSubject(Bd, professor)
#    def cambiar_professor(e):
#        print(e.data)
#        professor_2 = Bd.professors.get()[lista[0]%2]
#        boardsubject.set_pcg(professor_2)
#        lista[0] = lista[0] + 1
#    
#    boton_cambiar_professor = ft.TextButton(
#        text = "cambiar",
#        on_click= lambda e: cambiar_professor(e),
#    )
#
#    page.add(boardsubject, boton_cambiar_professor)
#
#ft.app(main)

# necesito una estructura 