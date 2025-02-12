import flet as ft  
from src.UI.database import database

class NewProfessorOrClassroom(ft.Container):
    
    def __init__(self, save_reference, list_p):
        
        self.textfield_new = ft.TextField()
        self.save_reference = save_reference
        self.list_p = list_p
        
        def add(e):
            self.save_reference(self.textfield_new.value)
            list_p.update_()
            self.textfield_new.value = ""
            self.textfield_new.update()
            self.list_p.update()
        
        button_new = ft.FloatingActionButton(
            icon = ft.icons.ADD,
            on_click = lambda e: add(e),
            text = "new",
            width = 190
        )
        
        super().__init__(
            content = ft.Row(
                controls = [
                    self.textfield_new,
                    button_new,
                ]
            )
        )
        
class NewProfessor(NewProfessorOrClassroom):
    
    def __init__(self, list_professors):
        super().__init__(database.professors.new, list_professors)
        
        
class NewClassroom(NewProfessorOrClassroom):
    
    def __init__(self, list_classrooms):
        super().__init__(database.classrooms.new, list_classrooms)
        