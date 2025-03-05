from .pages.home_page import HomePage 
from .pages.professors_classrooms_groups_pages import ProfessorsPage, ClassroomsPage, GroupsPage
from .pages.subject_pages import NewSubjectPage, SubjectSettingsPage
from .State import global_state, State
from .Route import Router, RoutesManagerNavigation
from .pages.professor_classroom_group_settings_pages import ProfessorSettingsPage, ClassroomSettingsPage, GroupSettingsPage
from .pages.export_page import ExportPage

router = Router()

router.routes = {
    '/': HomePage,
    '/PROFESSORS': ProfessorsPage,
    '/CLASSROOMS': ClassroomsPage,
    '/GROUPS': GroupsPage,
    '/NEW_SUBJECT': NewSubjectPage,
    "/PROFESSOR" : ProfessorSettingsPage,
    "/CLASSROOM" : ClassroomSettingsPage,
    "/GROUP" : GroupSettingsPage,
    "/SUBJECT_DETAILS" : SubjectSettingsPage,
    "/EXPORT_SCHEDULE" : ExportPage,
}

manager_routes = RoutesManagerNavigation()
manager_routes.new_route("/")

State("manager_routes", manager_routes)