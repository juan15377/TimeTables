import flet as ft
import numpy as np
from src.models.database import PCG, DEFAULT_PCG, RGB_to_hex
from src.tests.database_example import database_example
# Definición de medidas
WIDTH_BUTTON = 100
HEIGHT_BUTTON = 60

def replace_element(vector, start, end, element):
    left_part = vector[0:start]
    right_part = vector[end+1:]

    return np.concatenate((left_part, [element], right_part))

def insert_elements(vector, pos, new_elements):
    vector = np.insert(vector, pos, new_elements)
    vector = np.delete(vector, len(new_elements) + pos)
    return vector

def get_absolute_position_export(vector, req_pos):
    c = 0
    position = 0
    for ele in vector:
        print(ele.data)
        if c == req_pos:
            return position
        if ele.data == None:  # it is a block on the board, if not a subject block
            c = c + 1
            position = position + 1
            if c == req_pos:
                return position
            continue
        size = ele.data[2]
        c = c + size
        position = position + 1
        if c == req_pos:
            return position




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

def generate_subject_containers(pcg : PCG):
    # Given a set of subjects, it will return a list of subject blocks that will be inserted
    # using internal methods.
    blocks = []
    
    for subject in pcg.subjects:
        hours_placed = subject.allocated_subject_matrix
        for column in range(7):
            column_ = hours_placed[:, column]
            positions = decompose_vector(column_)
            for position in positions:
                row = position[0]
                block_size = position[1] - position[0] 
                if position[1] == 29:
                    block_size += 1
                    
                block = ft.Container(
                    bgcolor= RGB_to_hex(pcg.subject_colors.colors[subject]), # color of subject
                    content=ft.Text(f"{subject.code}", size=17, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color = ft.colors.BLACK),
                    padding=0,
                    alignment=ft.alignment.center,
                    width=WIDTH_BUTTON,
                    height=HEIGHT_BUTTON * block_size + (block_size-1),
                    border_radius=3,
                    data = (row, column, block_size)
                )
                blocks.append(block)
    return blocks

class ExportScheduleGrid(ft.Container):
    
    def __init__(self, pcg : PCG = DEFAULT_PCG):
        
        self.pcg = pcg

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
            pass

        def button_container(i, j):
            b = ft.Container(
                    content=ft.Text(f""),
                    theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.YELLOW)),
                    margin=ft.Margin(top=0, right=0, bottom=0, left=0),
                    padding=5,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.WHITE70,
                    width=WIDTH_BUTTON,
                    height=HEIGHT_BUTTON,
                    border_radius=1,
                    on_hover= animated_button,
                    ink_color= "blue",
                    animate=ft.animation.Animation(100, ft.AnimationCurve.EASE_IN_OUT)
                )
            return b

        button_matrix = np.array([[button_container(i, j) for j in range(7)] for i in range(30)])
        
        def time_container(i):
            return ft.Container(
                        theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK)),
                        bgcolor=ft.colors.LIGHT_BLUE_100,
                        content=ft.Text(daily_hours[i], size=13, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color = ft.colors.BLACK, expand = True),
                        margin=1,
                        padding=0,
                        alignment=ft.alignment.center,
                        width=WIDTH_BUTTON,
                        height=HEIGHT_BUTTON-1,
                        border_radius=5,
                    )
            
        def day_container(i):
            return ft.Container(
                        theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK)),
                        bgcolor=ft.colors.BLUE,
                        content=ft.Text(weekdays[i], size=13, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        margin=2,
                        padding=0,
                        alignment=ft.alignment.center,
                        width=WIDTH_BUTTON - 3,
                        height=HEIGHT_BUTTON -30,
                        border_radius=5,
                    )

        special_container = ft.Container(
                                theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK)),
                                bgcolor=ft.colors.SURFACE_VARIANT,
                                content=ft.Text("", color="white", width=12),
                                margin=1,
                                padding=0,
                                alignment=ft.alignment.center,
                                width=WIDTH_BUTTON - 1,
                                height=HEIGHT_BUTTON - 30,
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
                        alignment=ft.alignment.center, spacing=1,) for i in range(7)]
            
        
        days_row = [special_container] + [ft.Column(controls=[day_containers[i]],
                        horizontal_alignment=ft.alignment.center, 
                        alignment=ft.alignment.center, spacing=1,) for i in range(7)]
        # Add the buttons contained in the button matrix 

        for i in range(30):
            for j in range(7):
                button = button_matrix[i][j]
                day_columns[j].controls.append(button)
                    
        
        day_row = ft.Row(controls = days_row, spacing=0)

        total_columns = [time_column] + day_columns



        row = ft.Row(
                controls = total_columns,
                spacing=1,
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

        self.button_matrix = button_matrix
        self.cont = cont
        self.day_columns = day_columns
        
        super().__init__(
            content = cont,
            expand = True
        )
            
        containers_subjects = generate_subject_containers(self.pcg)
        
        self.fill_subjects(containers_subjects)
        
    
    
    def fill_subjects(self, containers_subjects):
        
        for container_subject in containers_subjects:
            row, col, size = container_subject.data
            
            col_buttons = self.day_columns[col].controls
            relative_position = get_absolute_position_export(col_buttons, row)
            
            col_buttons = replace_element(col_buttons, row, row + size-1, container_subject)

            self.day_columns[col].controls = col_buttons
        pass 
    pass 
