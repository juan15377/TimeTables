from src.UI.pages.subject_pages.components.hours_distribution import  SelectorDistributionHours, EditorHours
import flet as ft 

def main(page : ft.Page):
    
    page.add(SelectorDistributionHours())

ft.app(main)
