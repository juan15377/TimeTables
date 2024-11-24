import flet as ft 
import sys

sys.path.append("tests/Logic/")

from tests_3 import Bd
from Colors import RGB_to_hex

class LoadSubject():

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
            width = 100
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
                    icon_size=20,
                    tooltip="Pause record",
                    on_click = lambda e : up_value(self),
                    width=80
                    ) 
        
        down_button = ft.IconButton(
                    icon=ft.icons.ARROW_DOWNWARD,
                    icon_color="blue400",
                    icon_size=20,
                    tooltip="Play record",
                    on_click=lambda e : down_value(self),
                    width = 80
                    )
        
        block_selection = ft.Column(
            controls = [
                up_button,
                vbloque_drop,
                down_button
            ],
            width= 80,
            height= 100
        )

        def load_subject():
            size = int(float(self.vbloques_drop.value) * 2) 
            if size == 0:
                return None
            self.board.load_availability(size, self.subject)

        self.block_selection = block_selection
        original_color = pga.subject_colors.colors[subject]

        subject_container = ft.Container(content= ft.Text(subject.code,
                                    size= 35, color = ft.colors.BLACK),
                                    width=150,
                                    height=100,
                                    alignment=ft.alignment.center,
                                    bgcolor= RGB_to_hex(original_color),
                                    padding=0,
                                    margin = ft.Margin(top=0, right=0, bottom=0, left=0),
                                    border_radius=5,
                                    on_click= lambda e : load_subject(),
                                    ink=True)
        

        self.subject_container = subject_container
        self.content = ft.Row(
            controls = [
                self.block_selection,
                self.subject_container
            ]
        )
        
    def update_subject(self, subject):
        new_color = self.pga.subject_colors.colors[subject]
        new_name = subject.code
        self.subject_container.content = ft.Text(new_name,
                                    size=35, color = ft.colors.BLACK)
        
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

    def __init__(self, pga, board):
        self.pga = pga
        subject_0 = pga.get_subjects()[0]
        subject_loader = LoadSubject(pga, subject_0, board)
        self.subject_loader = subject_loader

        self.load_subject_list()

    def update(self):
        self.subject_list.controls.clear()
        self.add_subjects_to_list()
        self.subject_loader.update_blocks()
        subject = self.subject_loader.subject 
        self.subject_loader.update_subject(subject)
        self.subject_list.update()

    def add_subjects_to_list(self):

        for subject in self.pga.get_subjects():
            progress_bar = ft.ProgressBar(width = 150, height = 10)
            completed_value =  1 - subject.remaining() / subject.total()
            progress_bar.value = completed_value
            color = RGB_to_hex(self.pga.subject_colors.colors[subject])
            text_name = ft.Container(
                content = ft.Text(subject.code, size = 20, expand = True, color = ft.colors.BLACK),
                bgcolor= color,
                width=100,
                height=30,
                padding=0,
                margin=ft.Margin(top=0, right=0, bottom=0, left=0),
                border_radius=5,
                alignment= ft.alignment.center
                )
            
            subject_container = ft.Container(
                content= ft.Row(controls = [
                    text_name,
                    ft.Text("    "),
                    progress_bar
                ]),
                on_click= lambda e, s = subject : self.subject_loader.update_subject(s),
                #on_hover= lambda e : paint(e),
                ink = True,
                ink_color= "blue40",
                    )
            self.subject_list.controls.append(subject_container)


    def load_subject_list(self):

        subject_list = ft.Column(spacing=10, alignment=ft.alignment.top_center,
                                   height= 300,
                                   width= 300,
                                   scroll= ft.ScrollMode.AUTO)
        self.subject_list = subject_list


        self.add_subjects_to_list()

        

        content =ft.Column( 
            controls = [self.subject_list,
                        self.subject_loader.content]
                        
            )
        
        super().__init__(
            content
        )
