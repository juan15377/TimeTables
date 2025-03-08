from src.tests.database_example import database_example
from src.UI.pages.subject_pages.new_subject_page import NewSubjectPage 
import flet as ft

def main(page : ft.Page):
    
    subject_page = NewSubjectPage(page, "")
    page.add(subject_page)
    
ft.app(main)