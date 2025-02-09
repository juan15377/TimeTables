import flet as ft 
from src.GUI.EditAvailabilityMatrix.CuadroDisponibilidad import EditAvailabilityMatrix
from src.models.database import Professor, Classroom, Group
class NameEditor(ft.Container):
    
    def __init__(self, name):
        
        self.name = name
        
        def change_name(e):
            self.name = e.control.value
            
        self.name_textfield = ft.TextField(
            value = self.name,
            label="Nombre",
            border=ft.InputBorder.UNDERLINE,
            filled=True,
            hint_text="Insertar Nombre",
            on_change = change_name,
            max_length = 50,
            expand = True
        )
        
        layout = ft.Row(
            controls = [
                self.name_textfield,
            ],
            expand = True
        )
        
        super().__init__(
            content = layout,
            height = 80,
            expand = True
        )
        
    
class SubjectList(ft.ListView):
    
    def __init__(self, db, get_subjects_callback, enrouter_page):
        self.db = db        
        self.enrouter_page = enrouter_page
        self.get_subjects = get_subjects_callback
        
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



class NavigatorBarBackPCG(ft.Container):
    
    def __init__(self, page_back_callback, pcg):
        
        def funct_to_back():
            page_back_callback()

        pagelet = ft.Pagelet(
            appbar=ft.AppBar(
                leading=ft.IconButton(icon = ft.icons.ARROW_BACK, 
                                    on_click = lambda x: funct_to_back()),
                leading_width=50,
                title=ft.Text(""),
                center_title=False,
                bgcolor=ft.colors.SURFACE_VARIANT,
                actions=[
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="Item 1"),
                            ft.PopupMenuItem(),  # divider
                            ft.PopupMenuItem(
                                text="Checked item",
                                checked=False,
                            ),
                        ]
                    ),
                ],
            ),
            content=ft.Container(
                expand=False),
            height=50,
            
        )
            
        
        super().__init__(
            content = pagelet,
            expand=True
        )

class EditorPCG(ft.Container):
    
    def __init__(self, pcg, db, enrouter_page):
        
        page_back_callback = None 
        
        if type(pcg) == Professor:
            page_back_callback = lambda : enrouter_page.change_page("/PROFESSORS") 
        elif type(pcg) == Classroom:
            page_back_callback = lambda : enrouter_page.change_page("/CLASSROOMS") 
        else:
            page_back_callback = lambda : enrouter_page.change_page("/GROUPS") 
            
            
            
        
        self.edit_matrix_availability = EditAvailabilityMatrix()
        
        self.edit_matrix_availability.set_matrix(pcg.availability_matrix, update = False)
        
        self.pcg_name_editor = NameEditor(pcg.name)
        
        def get_subjects():
            return pcg.get_subjects()
        
        def save_changes_matrix_availability(e):
            new_availability_matrix = self.edit_matrix_availability.get_matrix()
            professor.set_availability_matrix(new_availability_matrix)# ? este metodo es delicadop
        
        self.subject_list = SubjectList(db, get_subjects, enrouter_page)
        
        button_add_subject = ft.IconButton(icon = ft.icons.ADD,
                                            on_click=lambda e: enrouter_page.change_page("/PCG/SUBJECT_DETAILS",pcg = pcg) )
        
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
        
        navigator_back = NavigatorBarBackPCG(page_back_callback, pcg)
        
        super().__init__(
            content = ft.Column(
                controls = [
                    ft.Row(
                        controls = [
                            navigator_back,
                        ],
                        expand = False
                    ),
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
        