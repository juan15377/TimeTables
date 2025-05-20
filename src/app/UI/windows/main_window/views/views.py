from src.app.database import database_manager
from .grid_views import ProfessorGridView, ClassroomGridView, GroupGridView 
from .list_views import GroupsManager, ProfessorsManager,ClassroomsManager 

MAIN_WINDOW_VIEWS = {
    "PROFESSOR-GRID" : ProfessorGridView(),
    "PROFESSOR-LIST" : ProfessorsManager(database_manager),
    "CLASSROOM-GRID" : ClassroomGridView(),
    "CLASSROOM-LIST" : ClassroomsManager(database_manager),
    "GROUP-GRID" : GroupGridView(),
    "GROUP-LIST" : GroupsManager(database_manager)
}

