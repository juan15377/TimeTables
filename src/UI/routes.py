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
    '/NEW_SUBJECTS': SubjectEditor
}