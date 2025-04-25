from .components.grid_subjects import ScheduleGrid 
from src.app.database import database_manager
from .views import ProfessorGridView, ClassroomGridView, GroupGridView 
from .views import GestorProfesores, ClassroomsManager 

VIEWS = {
    "PROFESSOR-GRID" : ProfessorGridView(),
    "PROFESSOR-LIST" : GestorProfesores(database_manager),
    "CLASSROOM-GRID" : ClassroomGridView(),
    "CLASSROOM-LIST" : ClassroomsManager(database_manager),
    "GROUP-GRID" : GroupGridView(),
    "GROUP-LIST" : None
}

