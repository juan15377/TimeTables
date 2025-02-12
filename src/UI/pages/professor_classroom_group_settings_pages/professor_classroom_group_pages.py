from src.UI.components.edit_availability_matrix import EditAvailabilityMatrix 
from components import *
from .components import NameEditor, SubjectList



class BaseSettingsPCG(ft.Container):
    
    def __init__(self, pcg, page):
            
        
        self.edit_matrix_availability = EditAvailabilityMatrix()
        
        self.edit_matrix_availability.set_matrix(pcg.availability_matrix, update = False)
        
        self.pcg_name_editor = NameEditor(pcg.name)
        
        def get_subjects():
            return pcg.get_subjects()
        
        def save_changes_matrix_availability(e):
            new_availability_matrix = self.edit_matrix_availability.get_matrix()
            professor.set_availability_matrix(new_availability_matrix)# ? este metodo es delicadop
        
        self.subject_list = SubjectList(page, get_subjects)
        
        button_add_subject = ft.IconButton(icon = ft.icons.ADD,
                                            on_click=lambda e: page.go("/NEW_SUBJECT") )
        
        button_save_changes_matrix_availability = ft.IconButton(icon = ft.icons.DELETE,
                                                    on_click = save_changes_matrix_availability)
        
        
        left_layout = ft.Column(
            controls = [
                self.edit_matrix_availability,
                button_save_changes_matrix_availability,
            ],
            expand = True
        )
        
        right_layout = ft.Column(
            controls = [
                ft.Row(
                    controls = [
                    self.pcg_name_editor,
                    ],
                    expand = False
                    
                ),
                button_add_subject,
                self.subject_list,
            ],
            expand = True
        )
                
        super().__init__(
            content = ft.Column(
                controls = [
                    ft.Row(
                        controls = [
                            left_layout,
                            right_layout,
                        ],
                        expand = True
                    )

                ],
                expand = True
            ),
            expand = True
        )
        

class ProfessorSettingsPage(BaseSettingsPCG):
    
    def __init__(self, page, key):
        
        professor = database.professors.get_by_key(key)
        
        super().__init__(professor, page)
        
        pass   
    
class ClassroomSettingsPage(BaseSettingsPCG):
    
    def __init__(self, page, key):
        
        classroom = database.classrooms.get_by_key(key)
        
        super().__init__(classroom, page)
        
        pass
    
class GroupSettingsPage(BaseSettingsPCG):
    
    def __init__(self, page, key):
        
        group = database.groups.get_by_key(key)
        
        super().__init__(group, page)
        
        pass
    
    pass