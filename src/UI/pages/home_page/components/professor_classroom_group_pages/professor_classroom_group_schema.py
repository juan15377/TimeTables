from .components import BasePCGPage
from src.UI.components.search_bar_items import SearchBarItems
from src.UI.database import database 
from src.models.database.constants import DEFAULT_PCG



class ProfessorHomePage(BasePCGPage):

    def __init__(self, page):
        call_refresh_professors = lambda :{
            professor.name : professor for professor in database.professors.get()
        }

        super().__init__(page, call_refresh_professors)
    
    pass   

class ClassroomHomePage(BasePCGPage):
    
    def __init__(self, page):

        call_refresh_classrooms = lambda :{
            classroom.name : classroom for classroom in database.classrooms.get()
        }
        
        super().__init__(page, call_refresh_classrooms)
        
    pass   

class GroupHomePage(BasePCGPage):
    
    def __init__(self, page):
    
        call_refresh_groups = lambda : {
            group.career.name + " " + group.semester.name + " " + group.subgroup.name : group for group in database.groups.get()
        }
        
        super().__init__(page, call_refresh_groups)
    
    pass

