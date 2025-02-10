import sys
import flet as ft
import numpy as np
import copy

from .constants import *
from .components import SubjectBlock, SubjectBlocks
from utils import *
from src.models.database import *
from src.UI.components.search_value import SearchValue



# ! tablero de control debe tener un metodo de inicializar con un objecto pga 
# ! este a partir de una inicializacion se debe mantener con operaciones que permitan 
# ! añadir bloques, este debe tener una forma eficiemte de actualizar ciertas partes del objecto para 
# ! cosas de optimizacion, ciertas operaciones como reinciar pga, materia, este descencadenara 
# ! la actualizacion en el nucleo y una actualizacion del tablero, lo cual es costoso de hacer por lo que las 
# ! operaciones permitidas deben ser bien escogidas  
# el tiempo permitido maximo poara la generacion de un tablero deberiaser de de 0.2 segundos 

def initialize_schedule_grid():

    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    daily_hours = [
            "7:00 - 7:30 AM", "7:30 - 8:00 AM", "8:00 - 8:30 AM", "8:30 - 9:00 AM", 
            "9:00 - 9:30 AM", "9:30 - 10:00 AM", "10:00 - 10:30 AM", "10:30 - 11:00 AM", 
            "11:00 - 11:30 AM", "11:30 - 12:00 PM", "12:00 - 12:30 PM", "12:30 - 1:00 PM",
            "1:00 - 1:30 PM", "1:30 - 2:00 PM", "2:00 - 2:30 PM", "2:30 - 3:00 PM",
            "3:00 - 3:30 PM", "3:30 - 4:00 PM", "4:00 - 4:30 PM", "4:30 - 5:00 PM",
            "5:00 - 5:30 PM", "5:30 - 6:00 PM", "6:00 - 6:30 PM", "6:30 - 7:00 PM",
            "7:00 - 7:30 PM", "7:30 - 8:00 PM", "8:00 - 8:30 PM", "8:30 - 9:00 PM",
            "9:00 - 9:30 PM", "9:30 - 10:00 PM"
    ]

    def animated_button(e):
        color = 1
        if e.control.data:
            e.control.margin = 2.5
            e.control.height = HEIGHT_BUTTON - 5
            e.control.width = WIDTH_BUTTON - 5
            e.control.data = False  
            e.control.update()
            return None
        e.control.padding = 2
        e.control.margin = ft.Margin(top=0, right=0, bottom=0, left=0)
        e.control.data = True  
        e.control.height = HEIGHT_BUTTON 
        e.control.width = WIDTH_BUTTON
        e.control.update()

    def button_container(i, j):
        b = ft.Container(
                content=ft.Text(f""),
                theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.YELLOW)),
                margin=ft.Margin(top=0, right=0, bottom=0, left=0),
                padding=2,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE70,
                width=WIDTH_BUTTON,
                height=HEIGHT_BUTTON,
                border_radius=5,
                on_hover= animated_button,
                data = True,
                ink_color= "blue",
                animate=ft.animation.Animation(100, ft.AnimationCurve.EASE_IN_OUT)
            )
        return b


    button_matrix = np.array([[button_container(i, j) for j in range(7)] for i in range(30)])

    
    def time_container(i):
        return ft.Container(
                    theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK)),
                    bgcolor=ft.colors.LIGHT_BLUE_100,
                    content=ft.Text(daily_hours[i], color="black", size=15),
                    margin=1,
                    padding=0,
                    alignment=ft.alignment.center,
                    width=WIDTH_BUTTON,
                    height=HEIGHT_BUTTON,
                    border_radius=5,
                )
        
    def day_container(i):
        return ft.Container(
                    theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK)),
                    bgcolor=ft.colors.BLUE,
                    content=ft.Text(weekdays[i], color="white", size=12),
                    margin=2,
                    padding=0,
                    alignment=ft.alignment.center,
                    width=WIDTH_BUTTON - 2,
                    height=HEIGHT_BUTTON,
                    border_radius=5,
                )
    
    special_container = ft.Container(
                            theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK)),
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            content=ft.Text("", color="white", width=12),
                            margin=2,
                            padding=0,
                            alignment=ft.alignment.center,
                            width=WIDTH_BUTTON - 1,
                            height=HEIGHT_BUTTON,
                            border_radius=1,
                            #expand = True
                        )
        
    time_containers = [time_container(i) for i in range(30)]
    day_containers = [day_container(i) for i in range(7)]

    time_column = ft.Column(
                    controls=time_containers,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
                    )
    

    day_columns = [ft.Column(controls=[],
                    horizontal_alignment=ft.alignment.center, 
                    alignment=ft.alignment.center, spacing=2,) for i in range(7)]
        
    
    days_row = [special_container] + [ft.Column(controls=[day_containers[i]],
                    horizontal_alignment=ft.alignment.center, 
                    alignment=ft.alignment.center, spacing=2,) for i in range(7)]
    # Add the buttons contained in the button matrix 

    for i in range(30):
        for j in range(7):
            button = button_matrix[i][j]
            day_columns[j].controls.append(button)
                
    
    day_row = ft.Row(controls = days_row, spacing=0)

    total_columns = [time_column] + day_columns



    row = ft.Row(
            controls = total_columns,
            spacing=2,
            vertical_alignment=ft.CrossAxisAlignment.START,
            #scroll=ft.ScrollMode.AUTO,
            #width=500,
            #height=995,  
            #expand = True
            )

    grid = ft.Column(
            controls=[row],
            #alignment=ft.MainAxisAlignment.START,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            #width=100,
            #height=550,    
            expand = True
        )
    
    grid = ft.Column(
        controls = [day_row] + [grid],
    )
    
    grid = ft.Row(
        controls = [grid],
        scroll = ft.ScrollMode.ALWAYS,
        expand = True
    )
    
    cont = ft.Container(
        content = grid,
        expand = True,
        alignment= ft.alignment.center_left
    )

    return button_matrix, cont, day_columns


def decompose_vector(vector):
    pos_in = 0
    positions = []
    start_sequence = False

    for num, ele in enumerate(vector):
        if ele == 0 and start_sequence:
            start_sequence = False
            positions.append((pos_in, num))
            continue 
        if ele == 1 and (not start_sequence):
            start_sequence = True
            pos_in = num
            continue 
    if start_sequence:
        positions.append((pos_in, len(vector)-1))

    return positions


#print(decompose_vector([0, 1, 1, 0, 1]))

# si hago el objecto de TableroControl mutable para solo añadir los bloques 
# uno por uno 


### refinar 
def generate_subject_blocks(pga, control_board, subject):
    # Given a set of subjects, it will return a list of subject blocks that will be inserted
    # using internal methods.
    hours_placed = subject.allocated_subject_matrix
    blocks = []
    for column in range(7):
        column_ = hours_placed[:, column]
        positions = decompose_vector(column_)
        for position in positions:
            row = position[0]
            block_size = position[1] - position[0] 
            if position[1] == 29:
                block_size += 1
            block = SubjectBlock(pga, control_board, subject, block_size, (row, column))
            blocks.append(block)
    return blocks

        
def schedule_button(pga, board, button, subject, position, size, subject_manager, enrouter):
    button.bgcolor = ft.colors.GREEN_400

    def add_block():
        block = SubjectBlock(pga, board, subject, size, position, enrouter)
        board.add_block(block)
        board.turn_off_board()
        subject_manager.update()
        board.grid.update()

    button.on_click = lambda e: add_block()


def reset_config(button):
    button.padding = 2
    button.margin = ft.Margin(top=0, right=0, bottom=0, left=0)
    button.data = True  
    button.height = HEIGHT_BUTTON 
    button.width = WIDTH_BUTTON

class SubjectScheduleGrid(ft.Container):

    def __init__(self, enrouter, pga = DEFAULT_PCG, update = False) -> None:
        self.enrouter = enrouter
        self.update_pga(pga, update)

    def update_pga(self, pga, update) -> None:
        button_matrix, grid, day_columns = initialize_control_board()

        subject_selector = SubjectSelector(self, pga) # !!!! Cambiar al momento de refactorizar 
        self.subject_selector = subject_selector

        self.button_matrix = button_matrix
        self.grid = grid
        self.day_columns = day_columns
        self.subject_blocks = SubjectBlocks()
        self.pga = pga

        super().__init__(
            content = ft.Row([self.grid, self.subject_selector]),
            expand = True,
        )
        
        self.content.controls[0].expand = 2
        self.content.controls[1].expand = 1
        
        # Generate subject blocks for each subject in the PCG
        for subject in pga.subjects:
            subject_blocks = generate_subject_blocks(pga, self, subject)
            for subject_block in subject_blocks:
                self.add_block(subject_block, update_slots_block = False)
                

    def load_availability(self, size, subject):  # This method activates the cells to add a block
        # Paints the grid cells based on the subject's availability in the board
        availability = subject.availability_matrix
        for row in range(30):
            for col in range(7):
                button = self.button_matrix[row, col]
                if availability[row, col] == 0:
                    button.bgcolor = ft.colors.RED
                    continue

                if availability[row: row + size, col].sum() == size:
                    schedule_button(self.pga, self, button, subject, (row, col), size, self.subject_selector, enrouter)
                    continue

                button.bgcolor = ft.colors.YELLOW
        self.grid.update()
        

    def turn_off_board(self):
        for row in range(30):
            for col in range(7):
                button = self.button_matrix[row, col]
                button.bgcolor = ft.colors.WHITE70
                button.on_click = None
        self.grid.update()

    def add_block(self, subject_block, update_slots_block = True) -> None:
        i = subject_block.position[0] # 29
        j = subject_block.position[1] # 29
        size = subject_block.size # 1

        # Reset the j-column, but before doing that, we make a copy
        previous_elements = self.day_columns[j].controls

        row_rel = get_absolute_position(previous_elements, i)
        news_elements = replace_element(previous_elements,
                                            row_rel,
                                            row_rel + size - 1,
                                            subject_block)
        
        
        self.day_columns[j].controls = news_elements
        self.subject_blocks.new(subject_block, (i, j))
        if update_slots_block:
            subject_block.subject.assign_class_block((i, j), subject_block.size)

    def remove_block(self, subject, position: tuple, size) -> None:
        i = position[0]
        j = position[1]

        previous_elements = copy.copy(self.day_columns[j].controls)
        row_rel = get_absolute_position(previous_elements, i)

        # Add the buttons back into the list
        buttons_to_add = self.button_matrix[i:i + size, j]
        for button in buttons_to_add:
            reset_config(button)
            button.data = True  
        
        previous_elements = insert_elements(previous_elements, row_rel, buttons_to_add)

        self.day_columns[j].controls = previous_elements
        self.day_columns[j].update()
        self.subject_blocks.delete_block(subject, position)
        subject.remove_class_block(position, size)
        self.subject_selector.update()

    def change_subject_color(self, subject, color):
        blocks = self.subject_blocks.get_subject_blocks(subject)
        self.pga.subject_colors.change_color(subject, color)
        for block in blocks:
            block.color_picker.set_color(color)
            block.change_individual_block_color(color)
        self.grid.update()
        self.subject_selector.update()

