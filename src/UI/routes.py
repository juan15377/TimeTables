from .pages.home_page import HomePage 
from .pages.list_professors_classrooms_groups import ProfessorsPage, ClassroomsPage, GroupsPage
from .pages.subject import SubjectEditor

from Route import Router 

router = Router()

router.routes = {
    '/': HomePage,
    '/PROFESSORS': ProfessorsPage,
    '/CLASSROOMS': ClassroomsPage,
    '/GROUPS': GroupsPage,
    '/NEW_SUBJECTS': SubjectEditor,
    "/PROFESSOR" : ProfessorDetailsPage,
    "/CLASSROOM" : ClassroomDetailsPage,
    "/GROUP" : GroupDetailsPage,
    "/SUBJECT_DETAILS" : SubjectDetailsPage,
    "/EXPORT_SCHEDULE" : ExportPage,
    "/SEARCH_SCHEDULE" : SearchSchedulePage
}