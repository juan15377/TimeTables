from src.UI.database import database
from typing import Callable

import flet as ft


class InfoMenuSubject(ft.MenuBar):
    
    def __init__(self, subject):
        
        table_groups = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Carrera", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Semestre", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Subgrupo", weight=ft.FontWeight.BOLD)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        # Ajustar el texto en varias líneas
                        ft.DataCell(ft.Text(group.career.name, width=200)),  # Ancho máximo para el texto
                        ft.DataCell(ft.Text(group.semester.name, width=200)),  # Ancho máximo para el texto
                        ft.DataCell(ft.Text(group.subgroup.name, width=200)),  # Ancho máximo para el texto
                    ]
                )
                for group in subject.groups
            ],
            border=ft.border.all(1, ft.colors.GREY_700),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_700),
            horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_700),
            heading_row_color=ft.colors.RED_800,
            heading_row_height=40,
            data_row_color={"hovered": ft.colors.GREY_800},
            show_checkbox_column=False,
            divider_thickness=0,
            expand = True
        )
        
        info_menu_groups = ft.MenuBar(
            controls=[
                    ft.SubmenuButton(
                        content = ft.Container(ft.Text("Grupos"), padding=10),
                        controls=[
                            table_groups
                        ],
                        menu_style=ft.MenuStyle(padding=0),
                        style=ft.ButtonStyle(padding=0),
                    ),
                ],
                style=ft.MenuStyle(padding=0),
        )
        
        
        super().__init__(
            controls=[
                    ft.SubmenuButton(
                        content = ft.IconButton(icon = ft.icons.DELETE,
                                                                       on_click=  lambda e : print("a")),
                        controls=[
                            ft.Container(ft.Text(subject.professor.name), padding=10),
                            ft.Container(ft.Text(subject.classroom.name), padding=10),
                            info_menu_groups
                        ],
                        menu_style=ft.MenuStyle(padding=0),
                        style=ft.ButtonStyle(padding=0),
                    ),
                ],
                style=ft.MenuStyle(padding=0),
        )
        
        


class SubjectList(ft.ListView):
    
    def __init__(self, page, call_refresh_subjects : Callable):
        self.page = page
        self.call_refresh_subjects = call_refresh_subjects
        
        super().__init__(
            controls = [],
            expand = True
        )
        
        self.update(update = False)
        
            
    def edit_subject(self, subject):
        subject_key = subject.key.key
        self.page.go(F"/SUBJECT_DETAILS?SUBJECT={subject_key}",)
        pass 

    def add_subject(self):
        self.reference_to_add_subject()
        pass
    
    def update(self, update = True):
        # tambie se tiene que actualizar el header
        
        subjects = self.call_refresh_subjects()
        subjects_list = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("name Subject")),
                ft.DataColumn(ft.Text("progress")),
                ft.DataColumn(ft.Text("info")),
                ft.DataColumn(ft.Text("delete")),
                ft.DataColumn(ft.Text("edit")),
            ],
            rows=[],
            border=ft.border.all(1, ft.colors.GREY_700),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_700),
            horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_700),
            heading_row_color=ft.colors.BLUE_800,
            heading_row_height=40,
            data_row_color={"hovered": ft.colors.GREY_800},
            show_checkbox_column=False,
            divider_thickness=0,
            expand = True
        )

        for subject in subjects:
            
            def delete_subject_from_bd(subject):
                database.subjects.remove(subject)
                self.update()
                
            def edit_subject_from_bd(subject):
                self.edit_subject(subject)
                self.update()
                
            name = subject.name 
            progress = ft.ProgressBar(expand=True)
            progress.value = 1 - subject.remaining() / subject.total() if subject.total() != 0 else 1 
            
            
            info_menu = InfoMenuSubject(subject)
            
            subjects_list.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(name, width = 200)),
                        
                        ft.DataCell(progress),
                                                
                        ft.DataCell(ft.Container(content=info_menu,
                                                 
                                                 ), 
                        ),
                        
                        ft.DataCell(ft.Container(content=ft.IconButton(icon = ft.icons.DELETE,
                                                                       on_click=lambda e, s=subject: delete_subject_from_bd(s)),
                                                                       width=15
                                                 
                                                 ), 
                        ),
                        
                        ft.DataCell(ft.Container(content=ft.IconButton(icon = ft.icons.EDIT,
                                                                       on_click=lambda e, s=subject: edit_subject_from_bd(s)),
                                                                        width = 15
                                                 
                                                 )
                        ),
                    ],
                ),

            )
        
        self.controls = [subjects_list]
        if update:
            super().update()