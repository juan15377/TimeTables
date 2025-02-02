
from src.GUI.MainPage.TMaterias import ControlBlocksSubject
from src.GUI.Utils.SearchValue import SearchValue
from src.Logic.database import DEFAULT_PCG
 
class MainPagePCG(ControlBlocksSubject):
    
    def __init__(self, bd, enrouter, route_to_go, call_get_items):
        
        def change_item():
            selected = self.bar_search.get_value()
            self.set_pcg(selected)
        
        bar_search = SearchValue(
            call_get_items(),
            call_get_items,
            on_change = change_item
        )
        
        self.bar_search = bar_search
        
        super().__init__(bd, DEFAULT_PCG, 
                         bar_search, enrouter, 
                         route_to_go, call_get_items)
        
    
    def update(self, update = True):
        self.bar_search.update()
        if update:
            super().update()
            #self.subject_search.on_change()  # actualizar la lista de materias cuando cambia el valor de la búsqueda
        pass


class ProfesorMainPage(MainPagePCG):
    
    def __init__(self, bd, enrouter):
        
        call_get_professors = lambda: {
            professor.name: professor for professor in bd.professors.get()
        }
        
        route_to_go = '/PROFESSORS'
        
        super().__init__(bd, enrouter, route_to_go, call_get_professors)
        
        
class ClassroomMainPage(MainPagePCG):
    
    def __init__(self, bd, enrouter):
        
        call_get_classrooms = lambda: {
            classroom.name: classroom for classroom in bd.classrooms.get()
        }
        
        route_to_go = '/CLASSROOMS'
        
        super().__init__(bd, enrouter, route_to_go, call_get_classrooms)
        

class GroupMainPage(MainPagePCG):
    
    def __init__(self, bd, enrouter):
        
        call_get_groups = lambda: {
            group.career.name + " " + group.semester.name + " " + group.subgroup.name: group for group in bd.groups.get()
        }
        
        route_to_go = '/GROUPS'
        
        super().__init__(bd, enrouter, route_to_go, call_get_groups)
