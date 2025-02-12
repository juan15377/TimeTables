from .pages.home_page import HomePage 
from .pages.professors_classrooms_groups_pages import ProfessorsPage, ClassroomsPage, GroupsPage
from .pages.subject_pages import NewSubjectPage
from .State import global_state, State
from Route import Router 

router = Router()

router.routes = {
    '/': HomePage,
    '/PROFESSORS': ProfessorsPage,
    '/CLASSROOMS': ClassroomsPage,
    '/GROUPS': GroupsPage,
    '/NEW_SUBJECTS': NewSubjectPage,
    "/PROFESSOR" : ProfessorDetailsPage,
    "/CLASSROOM" : ClassroomDetailsPage,
    "/GROUP" : GroupDetailsPage,
    "/SUBJECT_DETAILS" : SubjectDetailsPage,
    "/EXPORT_SCHEDULE" : ExportPage,
    "/SEARCH_SCHEDULE" : SearchSchedulePage
}

State("current_page", "/")