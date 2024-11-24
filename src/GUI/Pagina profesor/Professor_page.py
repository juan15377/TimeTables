import flet as ft
import sys  
import time as tm 
sys.path.append("tests/Logic/")
sys.path.append("src/Logic/")
# Object responsible for creating a list
from tests_3 import Bd
from Professor_Classroom_Group import Professor, Classroom, Group

class Header(ft.Container):

    def __init__(self, DB, pga, listviewpga):
        self.DB = DB 
        self.pga = pga
        self.listviewpga = listviewpga

        pga_name = pga.name
        self.name = pga_name

        pb = ft.ProgressBar(width=400)
        pb.value = pga.methods.completion_rate()

        def delete_pga(pga):

            if type(pga) == Professor:
                self.DB.professors.remove(pga)
            elif type(pga) == Classroom:
                self.DB.classrooms.remove(pga)
            else:
                self.DB.groups.remove(pga)
            self.listviewpga.update_expansions()
            self.listviewpga.update()

        button_remove_pga = ft.Container(
                            content=ft.Text("Delete"),
                            on_click=lambda e, pga=pga: delete_pga(pga),
                            bgcolor=ft.colors.RED,
                            width=70,
                            height=30,
                            alignment=ft.alignment.center
                            )

        Title = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(pga.name),
                        pb,
                        ft.Container(
                            content=ft.Text("Delete"),
                            on_click=lambda e, pga=pga: delete_pga(pga),
                            bgcolor=ft.colors.RED,
                            width=70,
                            height=30,
                            alignment=ft.alignment.center
                            ),
                        ft.Container(
                            content=ft.Text("Edit"),
                            on_click=lambda e: self.listviewpga.edit(pga),
                            bgcolor=ft.colors.YELLOW,
                            width=70,
                            height=30,
                            alignment=ft.alignment.center
                        )           
                    ],
                    spacing=50
                ),
                height=50,
                width=1200,
                border_radius=10,
            )
        
        super().__init__(
            content=Title)


class SubjectListView(ft.Column):

    def __init__(self, DB, pga, listviewpga):
        self.DB = DB 
        self.listviewpga = listviewpga
        self.pga = pga

        subjects = []

        button_new_subject = ft.TextButton(
            text="Add Subject",
            on_click=lambda e: self.add_subject(),
            width=200,
            height=30,
        )

        for subject in self.pga.get_subjects():
            name = subject.name 
            progress = ft.ProgressBar(width=400)
            progress.value = 1 - subject.remaining() / subject.total() if subject.total != 0 else 1 
            subject_view = ft.Row(
                controls=[
                    ft.Text(name),
                    progress,
                    ft.Container(content=ft.Text("Details"), 
                                 on_click=lambda e, s=subject: self.edit_subject(s)),
                ],
                spacing=70
            )
            subjects.append(subject_view)
            
        super().__init__(
            controls=[button_new_subject] + subjects,  # Add button for adding new subjects
            alignment=ft.alignment.top_left,
            scroll=ft.ScrollMode.ALWAYS,  # Enable scrolling in the column
            width=1200,
            height=300
        )
    
    def edit_subject(self, s):
        # This should open a new window to edit subject information
        pass 

    def add_subject(self):
        pass


def filter_expansions(expansions, coincidence):
    # This should filter expansions that match the coincidence
    new_expansions = []

    for expansion in expansions:
        if coincidence.lower() in expansion.data.lower():  # Data stores the name of the PGA
            new_expansions.append(expansion)
    return new_expansions


class ListViewPGA(ft.Container):

    def __init__(self, pgas, DB, creating):
        self.DB = DB  
        self.pgas = pgas

        def search_now(e):
            self.update_expansions()
            print("Value changed")
            coincidence = e.control.value
            if coincidence == "":
                self.update()
                return None  # Does not filter anything
            self.search(coincidence)

        self.update_expansions()

        search_pga = ft.TextField(
                        label="Search now",
                        on_change=search_now
                    )

        textfield_new_teacher = ft.TextField(
                            label="New",
                            border=ft.InputBorder.UNDERLINE,
                            filled=True,
                            hint_text="Name",
                            max_length=50
                            )
        
        def add_new(DB):
            name = textfield_new_teacher.value
            creating.new(name)
            textfield_new_teacher.value = ""
            textfield_new_teacher.update()
            # Update the component by adding a new element with empty subjects
            self.update_expansions() 
            self.update()
            pass 

        button_new_teacher = ft.TextButton(
                            text="Add",
                            on_click=lambda e, DB=self.DB: add_new(DB),
                            width=100,
                            height=30,
                            )

        top_section = ft.Row(
            controls=[
                search_pga,
                textfield_new_teacher,
                button_new_teacher
            ]
        )

        expansions_column = ft.Column(
            controls=self.expansions,
            scroll=ft.ScrollMode.ALWAYS,  # Enable scrolling in the column
            width=800,
            height=600,
            )

        super().__init__(
            content=ft.Column(
                controls=[top_section] + [expansions_column],
            ),
            width=1200,
            height=600,
        )


    def update_expansions(self):
        expansions = []

        for pga in self.pgas():
            header = Header(self.DB, pga, self)
            subject_list = SubjectListView(self.DB, pga, self)
            expansion = ft.ExpansionTile(
                            title=header,
                            subtitle=ft.Text("Subjects"),
                            affinity=ft.TileAffinity.LEADING,
                            controls=[
                                ft.Container(
                                    content=subject_list,
                                    height=200,  # Set height to allow scrolling
                                )
                            ],
                            data=header.name
                        )
            expansions.append(expansion)

        self.expansions = expansions


    def search(self, coincidence):
        self.expansions = filter_expansions(self.expansions, coincidence)
        self.update()


    def update(self):
        expansions = self.expansions
        self.content.controls[1] = ft.Column(
                                    controls=expansions,
                                    scroll=ft.ScrollMode.ALWAYS,  # Enable scrolling in the column
                                    width=1200,
                                    height=600,
                                    )
        super().update()
        pass


time_init = tm.time()
test_object = ListViewPGA(Bd.professors.get, Bd, Bd.professors)
time_out = tm.time()

print(f"Time taken = {time_out -  time_init}")


def main(page: ft.Page):
    page.add(test_object) 

ft.app(main)
