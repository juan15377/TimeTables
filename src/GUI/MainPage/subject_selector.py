import flet as ft
import sys

from src.Logic.Colors import RGB_to_hex, MyColorPicker
from src.Logic.Subjects import DEFAULT_PCG, DEFAULT_SUBJECT


class LoadSubject(ft.Container):

    def __init__(self, pga, subject, board):
        self.subject = subject
        self.board = board
        self.pga = pga

        def find_option(name):
            for option in vbloque_drop.options:
                if name == option.key:
                    return option
            return None

        blocks = subject.hours_distribution.get_avaible_hours()
        self.blocks = blocks

        vbloque_drop = ft.Dropdown(
            options = [
                ft.dropdown.Option(str(block))
                for block in blocks
            ],
            width = 100,
            expand = True
        )
        self.vbloques_drop = vbloque_drop
        self.pos = 0
        self.vbloques_drop.value = 0

        def up_value(self):

            self.pos = (self.pos + 1) % len(self.blocks)

            new_value = str(self.blocks[self.pos])
            #print(self.pos)
            self.vbloques_drop.value = new_value
            self.vbloques_drop.update()
            self.block_selection.update()

        def down_value(self):
            self.pos = (self.pos - 1) % len(self.blocks)
            
            new_value = str(self.blocks[self.pos])
            if new_value == None :
                self.down_value()

            self.vbloques_drop.value = new_value
            self.vbloques_drop.update()
            self.block_selection.update()


        up_button = ft.IconButton(
                    icon=ft.icons.ARROW_UPWARD,
                    icon_color="blue400",
                    icon_size=30,
                    on_click = lambda e : up_value(self),
                    width=60,
                    ) 
        
        down_button = ft.IconButton(
                    icon=ft.icons.ARROW_DOWNWARD,
                    icon_color="blue400",
                    icon_size=30,
                    on_click=lambda e : down_value(self),
                    width = 60,
                    )

        block_selection = ft.Row(
            controls = [
                vbloque_drop,
                ft.Column(
                    controls = [
                        up_button,
                        down_button
                    ],
                    expand = True
                )
            ],
            expand = True
        )

        def load_subject():
            size = int(float(self.vbloques_drop.value) * 2) 
            if size == 0:
                return None
            self.board.load_availability(size, self.subject)

        self.block_selection = block_selection
        original_color = self.pga.subject_colors.colors[subject]

        subject_container = ft.Container(content= ft.Text(subject.code,
                                    size= 20, color = ft.colors.BLACK),
                                    width=150,
                                    height=100,
                                    alignment=ft.alignment.center,
                                    bgcolor= RGB_to_hex(original_color),
                                    padding=0,
                                    margin = ft.Margin(top=0, right=0, bottom=0, left=0),
                                    border_radius=5,
                                    on_click= lambda e : load_subject(),
                                    expand = True,
                                    ink=True)
        

        self.subject_container = subject_container
        
        self.button_cancel = ft.Container(
                    content = ft.Text("Cancel"),
                    bgcolor= ft.colors.RED_500,
                    expand = True,
                    width=150,
                    height=100,
                    on_click= lambda e : board.turn_off_board(),
                    alignment= ft.alignment.center,
                    border_radius = 5
                )
        
        self.content = ft.Row(
            controls = [
                self.block_selection,
                self.subject_container,
                self.button_cancel
            ],
            spacing = 10,
            expand = True
        )
        
        super().__init__(
            content = self.content,
        )
        
    def update_subject(self, subject):
        new_color = self.pga.subject_colors.colors[subject]
        new_name = subject.code
        self.subject_container.content = ft.Text(new_name,
                                    size=20, color = ft.colors.BLACK)
        
        self.subject_container.bgcolor = RGB_to_hex(new_color)
        self.subject = subject 
        self.content.update()
        self.update_blocks()


    def update_blocks(self):
        blocks = self.subject.hours_distribution.get_avaible_hours()
        self.vbloques_drop.options.clear()
    
        for block in blocks:
            self.vbloques_drop.options.append(ft.dropdown.Option(str(block)))
        
        self.pos = 0 
        self.vbloques_drop.value = blocks[0] 
        self.blocks = blocks 
        self.vbloques_drop.update()
        self.block_selection.update()


class SubjectSelector(ft.Container):

    def __init__(self, board, pga):
        self.pga = pga
        if len(pga.get_subjects()) == 0:
            self.pga = DEFAULT_PCG
        subject_0 = self.pga.get_subjects()[0]
        subject_loader = LoadSubject(self.pga, subject_0, board)
        self.subject_loader = subject_loader

        self.load_subject_list()
        

    def update(self):
        self.subject_list.controls.clear()
        self.add_subjects_to_list()
        self.subject_loader.update_blocks()
        subject = self.subject_loader.subject 
        self.subject_loader.update_subject(subject)
        self.subject_list.update()
        super().update()

    def add_subjects_to_list(self):

        for subject in self.pga.get_subjects():
            progress_bar = ft.ProgressBar(expand = True, bar_height= 6, color= ft.colors.GREEN_500)
            completed_value =  1 - subject.remaining() / subject.total() if subject.total() != 0 else 1
            progress_bar.value = completed_value
            subject_color = self.pga.subject_colors.colors[subject]
            color = RGB_to_hex(subject_color)
            subject_container = ft.Container(
                content = ft.Text(subject.code, size = 20, expand = True, color = ft.colors.BLACK, text_align= ft.alignment.top_left),
                bgcolor = color,
                height = 60,
                width= 120,
                padding = 2,
                margin = ft.Margin(top=0, right=0, bottom=0, left=0),
                border_radius=10,
                alignment= ft.alignment.center,
                )
            
            name_subject = ft.Container(
                content = ft.Text(subject.name, size = 20, color = ft.colors.BLACK),
                alignment= ft.alignment.center,
                expand = True
            )
            
            subject_item = ft.Container(
                content= ft.Row(controls = [
                    subject_container,
                    ft.Text("    "),
                    progress_bar
                    ],
                
                ),
                on_click= lambda e, s = subject : self.subject_loader.update_subject(s),
                #on_hover= lambda e : paint(e),
                ink = True,
                ink_color= ft.colors.GREEN_100,
                padding= 5,
                border_radius= 5,
                bgcolor= ft.colors.WHITE,
                    )
            
            self.subject_list.controls.append(subject_item)


    def load_subject_list(self):

        subject_list = ft.ListView(spacing=10,
                                   expand = True,
                                   )
        
        self.subject_list = subject_list


        self.add_subjects_to_list()

        
        content = ft.Column(
            controls = [
                ft.Container(
                    content = self.subject_list,
                    bgcolor = ft.colors.WHITE54,
                    expand=True,
                    border_radius= 6,
                    padding= 5
                ),
                self.subject_loader
                        ],
            expand = True ,
            )
        
        subjects_label = ft.Container(
            content = ft.Text("Subjects", text_align= ft.alignment.center, size = 20),
            alignment= ft.alignment.center,
            padding= 10
        )
        
        contenedor_borde = ft.Container(
            content= ft.Column(controls = [subjects_label, content],),
            padding=10,
            bgcolor=ft.colors.BLACK87,  # Color de fondo del contenedor interno
            expand = True
        )
    
        
        super().__init__(
            content = contenedor_borde,
            expand = True,
            border_radius= 10,
            theme=ft.Theme.banner_theme,
            bgcolor= ft.colors.WHITE,
            padding = 5,
        )
