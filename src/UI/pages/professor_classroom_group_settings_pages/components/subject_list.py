from src.UI.database import database
from typing import Callable

import flet as ft
class SubjectList(ft.ListView):
    
    def __init__(self, page, call_refresh_subjects : Callable):
        self.page = page
        self.call_refresh_subjects = call_refresh_subjects
        
        super().__init__(
            controls = [],
            expand = True,
        )
        
        self.update(update = False)
        
            
    def edit_subject(self, s):
        # This should open a new window to edit subject information
        pass 

    def add_subject(self):
        self.reference_to_add_subject()
        pass
    
    def update(self, update = True):
        # tambie se tiene que actualizar el header
        
        subjects = self.get_subjects()
        subjects_list = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("name Subject")),
                ft.DataColumn(ft.Text("progress")),
                ft.DataColumn(ft.Text("professor")),
                ft.DataColumn(ft.Text("Classroom")),
                ft.DataColumn(ft.Text("total hours")),
                ft.DataColumn(ft.Text("delete")),
                ft.DataColumn(ft.Text("edit")),
            ],
        )

        for subject in subjects:
            
            def delete_subject_from_bd(subject):
                self.db.subjects.remove(subject)
                self.update()
                
            def edit_subject_from_bd(subject):
                self.edit_subject(subject)
                self.update()
                
            name = subject.name 
            progress = ft.ProgressBar(expand=True)
            progress.value = 1 - subject.remaining() / subject.total() if subject.total() != 0 else 1 
            
            subjects_list.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(name)),
                        ft.DataCell(progress),
                        ft.DataCell(ft.Text(subject.professor.name, expand = True)),
                        ft.DataCell(ft.Text(subject.classroom.name, expand = True)),
                        ft.DataCell(ft.Text(str(subject.hours_distribution.total()))),
                        ft.DataCell(ft.Container(content=ft.IconButton(icon = ft.icons.DELETE,
                                                                       on_click=lambda e, s=subject: delete_subject_from_bd(s)),
                                                 
                                                 ), 
                        ),
                        ft.DataCell(ft.Container(content=ft.IconButton(icon = ft.icons.EDIT,
                                                                       on_click=lambda e, s=subject: edit_subject_from_bd(s)),
                                                 
                                                 )
                        ),
                    ],
                ),

            )
        
        self.controls = [subjects_list]
        if update:
            super().update()