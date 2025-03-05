import flet as ft  
from src.UI.database import database

class SubjectSettingsPage(ft.Container):
    
    
    def __init__(self, page, query):
        
        subject = database.subjects.get_by_key(query)
        super().__init__(
            content = ft.Text("Hello World")
        )
        pass