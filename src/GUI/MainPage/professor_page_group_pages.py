
from src.GUI.MainPage.TMaterias import ControlBlocksSubject
from src.GUI.Utils.SearchValue import SearchValue
from src.Logic.Professor_Classroom_Group import DEFAULT_PCG


class ProfesorMainPage(ControlBlocksSubject):
    
    def __init__(self, bd, reference_enrouter_page):
        
        def change_professor():
            selected = self.professor_search.get_value()
            self.set_pcg(selected)
            
        def get_actual_profesors():
            return {
            professor.name: professor for professor in bd.professors.get()
            }


        professor_search =  SearchValue({
            professor.name: professor for professor in bd.professors.get()
            },
            get_actual_profesors,
            on_change = change_professor
            )
        
        self.professor_search = professor_search
        
        def change_to_professors():
            reference_enrouter_page('/PROFESSORS') # cambiar la pagina de profesores
        
        super().__init__(bd, DEFAULT_PCG, professor_search, change_to_professors)
        
    def update(self, update = True):
        self.professor_search.update()
        if update:
            super().update()
            #self.professor_search.on_change()  # actualizar la lista de profesores cuando cambia el valor de la búsqueda
            
        pass
        

class ClassroomMainPage(ControlBlocksSubject):
    
    def __init__(self, bd, reference_enrouter_page):
        
        def change_classroom():
            seleccionado = self.classroom_search.get_value()
            self.set_pcg(seleccionado)
            
        def get_actual_classrooms():
            return {
            classroom.name: classroom for classroom in bd.classrooms.get()
            }


        classroom_search = SearchValue({
            classroom.name: classroom for classroom in bd.classrooms.get()
            },
            get_actual_classrooms,  # setear los valores de la búsqueda  
            on_change = change_classroom
        )
        
        
        self.classroom_search = classroom_search
        
        def change_to_classrooms():
            reference_enrouter_page('/CLASSROOMS') # cambiar la pagina de aulas 
        
        super().__init__(bd, DEFAULT_PCG, classroom_search, change_to_classrooms)
        
    def update(self, update = True):
        self.classroom_search.update()
        if update:
            super().update()
            #self.classroom_search.on_change()
            
        
class GroupMainPage(ControlBlocksSubject):
    
    def __init__(self, bd, reference_enrouter_page):
        
        def change_group():
            seleccionado = self.group_search.get_value()
            self.set_pcg(seleccionado)

        def get_actual_groups():
            return {
            group.career.name + " " + group.semester.name + " " + group.subgroup.name: group for group in bd.groups.get()
            }
        
        self.group_search = SearchValue({
            group.career.name + " " + group.semester.name + " " + group.subgroup.name:group for group in bd.groups.get()
            },
            get_actual_groups,  # setear los valores de la búsqueda
            on_change = change_group
        )
        
        
        def change_to_groups():
            reference_enrouter_page('/GROUPS') # cambiar la pagina a 

        super().__init__(bd, DEFAULT_PCG, self.group_search, change_to_groups)
    
    def update(self, update = False):
        self.group_search.update()
        if update:
            super().update()
            #self.group_search.on_change()  # para que se actualice el boton en caso de que haya cambiado el grupo seleccionado en la lista
            
    

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