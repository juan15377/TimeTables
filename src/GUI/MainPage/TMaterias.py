import sys

# Importar las bibliotecas necesarias
import flet as ft
import numpy as np
import copy

from src.Logic.Professor_Classroom_Group import DEFAULT_PCG
from src.GUI.MainPage.subject_selector import SubjectSelector
from src.Logic.Colors import RGB_to_hex, MyColorPicker
from src.Logic.Professor_Classroom_Group import Professor, Group, Classroom
from src.Logic.Subjects import Subject
from src.GUI.Utils.SearchValue import SearchValue


# ! tablero de control debe tener un metodo de inicializar con un objecto pga 
# ! este a partir de una inicializacion se debe mantener con operaciones que permitan 
# ! añadir bloques, este debe tener una forma eficiemte de actualizar ciertas partes del objecto para 
# ! cosas de optimizacion, ciertas operaciones como reinciar pga, materia, este descencadenara 
# ! la actualizacion en el nucleo y una actualizacion del tablero, lo cual es costoso de hacer por lo que las 
# ! operaciones permitidas deben ser bien escogidas  
# el tiempo permitido maximo poara la generacion de un tablero deberiaser de de 0.2 segundos 

import flet as ft
import numpy as np


HEIGHT_BUTTON = 50
WIDTH_BUTTON = 150

def initialize_control_board():

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

    def button_container(i, j):
        b = ft.Container(
                content=ft.Text(f""),
                theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK)),
                margin=ft.Margin(top=0, right=0, bottom=0, left=0),
                padding=2,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE24,
                width=WIDTH_BUTTON,
                height=HEIGHT_BUTTON,
                border_radius=5,
            )
        return b


    button_matrix = np.array([[button_container(i, j) for j in range(7)] for i in range(30)])

    
    def time_container(i):
        return ft.Container(
                    theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK)),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    content=ft.Text(daily_hours[i], color="white", size=12),
                    margin=1,
                    padding=0,
                    alignment=ft.alignment.center,
                    width=WIDTH_BUTTON,
                    height=HEIGHT_BUTTON,
                    border_radius=1,
                )
        
    def day_container(i):
        return ft.Container(
                    theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK)),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    content=ft.Text(weekdays[i], color="white", size=12),
                    margin=2,
                    padding=0,
                    alignment=ft.alignment.center,
                    width=WIDTH_BUTTON - 2,
                    height=HEIGHT_BUTTON,
                    border_radius=1,
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
            expand = True
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
        expand = True
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


from typing import Union, Tuple
import flet as ft

class SubjectBlock(ft.Container):
    """
    Represents a block of a subject within the timetable. This class handles all the necessary logic
    for interacting with the database, including assigning and removing class blocks, adjusting the
    class time, and changing the block's color.

    Attributes:
        pcg (Union[Professor, Classroom, Group]): The professor, classroom, or group associated with the block.
        control_board (ControlBoardSubjectSlots): The timetable (control board) where the subject block is placed.
        subject (Subject): The subject to which this block belongs.
        size (int): The size of the block in half-hour intervals.
        position (Tuple[int, int]): The position where the block is placed in the timetable.
        color_picker (MyColorPicker): The color picker used to change the block color.
    
    Methods:
        change_individual_block_color(self, color): Changes the color of the block.
    
    Args:
        pcg (Union[Professor, Classroom, Group]): Can be a professor, a classroom, or a group.
        control_board (ControlBoardSubjectSlots): The timetable (control board) where the subject block will be placed.
        subject (Subject): The subject to which this block belongs.
        size (int): The size of the block in half-hour intervals.
        position (Tuple[int, int]): The position where the block will be placed in the timetable.
    """
    
    def __init__(self, 
                 pcg: Union['Professor', 'Classroom', 'Group'], 
                 control_board: 'ControlBoardSubjectSlots', 
                 subject: 'Subject', 
                 size: int, 
                 position: Tuple[int, int]) -> None:
        """
        Initializes a SubjectBlock with the given parameters, validates the input types, and sets up the block.

        Args:
            pcg (Union[Professor, Classroom, Group]): The entity (professor, classroom, or group) associated with the subject.
            control_board (ControlBoardSubjectSlots): The timetable control board where the subject block will be placed.
            subject (Subject): The subject to which this block belongs.
            size (int): The size of the block in half-hour intervals.
            position (Tuple[int, int]): The position of the block on the timetable grid.
        """
        # Initialize instance variables
        self.subject = subject
        self.size = size  # Size represents the number of half-hours
        self.board = control_board
        self.position = position
        self.pcg = pcg

        # Set up color picker for the block
        color_picker = MyColorPicker()
        original_color = pcg.subject_colors.colors[subject]
        color_picker.update_color(original_color)
        self.color_picker = color_picker

        # Function to delete the block from the timetable
        def delete_block(self):
            self.board.turn_off_board()
            self.board.remove_block(subject, self.position, self.size)

        # Function to change the subject color
        def change_subject_color(self):
            color = self.color_picker.get_color()
            self.board.change_subject_color(self.subject, color)

        # Function to move the block (remove and re-enable availability for insertion)
        def move_block(self):
            self.board.remove_block(subject, self.position, self.size)
            self.board.load_availability(self.size, self.subject)

        # Create menu items for block options
        menuitem_INFO = ft.MenuItemButton(
            content=ft.Row(controls=[ft.Icon(name=ft.icons.INFO), ft.Text("Info")]),
            on_click=lambda e: print("Hello Everyone")
        )

        menuitem_DELETE = ft.MenuItemButton(
            content=ft.Row(controls=[ft.Icon(name=ft.icons.DELETE), ft.Text("Delete")]),
            on_click=lambda e: delete_block(self)
        )

        menuitem_MOVE = ft.MenuItemButton(
            content=ft.Row(controls=[ft.Icon(name=ft.icons.MOVE_DOWN), ft.Text("Move")]),
            on_click=lambda e: move_block(self)
        )

        menuitem_COLOR = ft.SubmenuButton(
            content=ft.Text("Color"),
            leading=ft.Icon(ft.icons.COLOR_LENS),
            controls=[
                ft.MenuItemButton(content=ft.Container(content=self.color_picker, width=200, height=170))
            ],
            on_close=lambda e: change_subject_color(self),
        )

        # Tooltip and name display for the subject
        text_name = ft.Tooltip(
            message=self.subject.name,
            content=ft.Text(self.subject.code, size=23, color=ft.colors.BLACK),
            text_style=ft.TextStyle(size=15, color=ft.colors.BLACK),
        )

        # Subject block container with color and tooltip
        subject_container = ft.Container(
            content=text_name,
            width=WIDTH_BUTTON,
            height=(HEIGHT_BUTTON * self.size + (self.size - 1) * 2),
            alignment=ft.alignment.center,
            bgcolor=RGB_to_hex(original_color),
            padding=0,
            margin=ft.Margin(top=0, right=0, bottom=0, left=0),
            border_radius=5,
            on_hover=lambda e: ft.Tooltip(message="This is tooltip")
        )

        # Menu options for the block with a submenu containing the options
        menu_options = ft.MenuBar(
            controls=[
                ft.SubmenuButton(
                    content=subject_container,
                    controls=[
                        menuitem_INFO,
                        menuitem_DELETE,
                        menuitem_MOVE,
                        menuitem_COLOR,
                    ],
                    width=WIDTH_BUTTON,
                    height=(HEIGHT_BUTTON * self.size + (self.size - 1) * 2),
                    menu_style=ft.MenuStyle(padding=0),
                    style=ft.ButtonStyle(padding=0)
                ),
            ],
            style=ft.MenuStyle(padding=0),
            data=self.size
        )

        super().__init__(content=menu_options)

    def change_individual_block_color(self, color: str) -> None:
        """
        Changes the color of the subject block.

        Args:
            color (str): The color to change the block to, in RGB hex format.
        """
        color = RGB_to_hex(color)
        self.content.controls[0].content.bgcolor = color
        self.content.update()


import numpy as np
from typing import List, Union

class SubjectBlocks:
    """
    Manages the scheduling of subject blocks within a timetable. This class allows for adding new subject blocks,
    retrieving existing blocks, and deleting blocks from the timetable. It works by storing blocks in a dictionary
    and a global timetable matrix.

    Attributes:
        subjects (dict): A dictionary where each subject maps to a 30x7 matrix (representing days and time slots)
                          containing the subject blocks.
        total (numpy.ndarray): A 30x7 matrix containing all subject blocks across all subjects.
    
    Methods:
        new(subject_block, position): Adds a new subject block at the specified position in the timetable.
        get_subject_blocks(subject): Returns a list of all blocks associated with a specific subject.
        get_blocks(position): Returns the block at a specific position in the timetable.
        delete_block(subject, position): Deletes the subject block from both the subject's timetable and the global timetable.
        delete_subject_blocks(subject): Deletes all blocks associated with a specific subject.
        delete_all_blocks(): Clears all subject blocks from the timetable.
    """

    def __init__(self) -> None:
        """
        Initializes the SubjectBlocks object. Creates an empty dictionary for subjects and a global timetable matrix.

        Attributes:
            subjects (dict): A dictionary that holds subject blocks.
            total (numpy.ndarray): A global timetable matrix where blocks are stored.
        """
        self.subjects = {}
        self.total = np.zeros((30, 7), dtype=object)

    def new(self, subject_block, position: Tuple[int, int]) -> None:
        """
        Adds a new subject block at the specified position in the timetable.

        Args:
            subject_block: The subject block to be added.
            position (Tuple[int, int]): The position (i, j) where the block will be placed in the timetable.
            
        If the subject already exists in the timetable, the block is added at the given position.
        If the subject does not exist, a new entry is created in the `subjects` dictionary and the block is placed.
        """
        subject = subject_block.subject
        i, j = position
        
        # Check if the subject already exists in the timetable
        if subject in self.subjects:
            self.subjects[subject][i, j] = subject_block
            self.total[i, j] = subject_block
            return None

        # If the subject doesn't exist, create a new entry
        self.subjects[subject] = np.zeros((30, 7), dtype=object)
        self.subjects[subject][i, j] = subject_block
        self.total[i, j] = subject_block
        return None
    
    def get_subject_blocks(self, subject: 'Subject') -> List[object]:
        """
        Returns all subject blocks associated with a specific subject.

        Args:
            subject (Subject): The subject for which the blocks are retrieved.
        
        Returns:
            List[object]: A list of subject blocks associated with the given subject.
            If no blocks are found, returns an empty list.
        """
        if subject in self.subjects:
            block_list = list(set(self.subjects[subject].flatten().tolist()))
            block_list.remove(0)  # Remove empty cells
            return block_list
        return []
    
    def get_blocks(self, position: Tuple[int, int]) -> Union[List[object], None]:
        """
        Retrieves the block(s) at a specific position in the timetable.

        Args:
            position (Tuple[int, int]): The position (i, j) of the block in the timetable.
        
        Returns:
            List[object] or None: The list of blocks at the specified position, or an empty list if no block exists.
        """
        i, j = position
        if self.total[i, j] != 0:
            return self.total[i, j]
        return []

    def delete_block(self, subject: 'Subject', position: Tuple[int, int]) -> None:
        """
        Deletes a subject block at a specific position from both the subject's timetable and the global timetable.

        Args:
            subject (Subject): The subject whose block is being deleted.
            position (Tuple[int, int]): The position (i, j) of the block to be deleted.
        
        If the subject has no more blocks in the timetable, it will be removed from the `subjects` dictionary.
        """
        i, j = position
        if subject in self.subjects and self.total[i, j] != 0:
            self.subjects[subject][i, j] = 0
            # Check if there are no more blocks for this subject
            if set(self.subjects[subject].flatten().tolist()) == set([0]):
                del self.subjects[subject]
            return None
        return None
    
    def delete_subject_blocks(self, subject: 'Subject') -> None:
        """
        Deletes all blocks associated with a specific subject from the timetable.

        Args:
            subject (Subject): The subject whose blocks are being deleted.
        
        Removes all subject blocks associated with the given subject from both the subject's timetable
        and the global timetable.
        """
        if subject in self.subjects:
            del self.subjects[subject]
            return None
        return None
    
    def delete_all_blocks(self) -> None:
        """
        Clears all subject blocks from the timetable.

        Resets the `subjects` dictionary and the global timetable matrix.
        """
        self.subjects = {}
        self.total = np.zeros((30, 7), dtype=object)


        
def schedule_button(pga, board, button, subject, position, size, subject_manager):
    button.bgcolor = ft.colors.GREEN_400

    def add_block():
        block = SubjectBlock(pga, board, subject, size, position)
        board.add_block(block)
        board.turn_off_board()
        subject_manager.update()
        board.grid.update()

    button.on_click = lambda e: add_block()




def replace_element(vector, start, end, element):
    left_part = vector[0:start]
    right_part = vector[end+1:]

    return np.concatenate((left_part, [element], right_part))




def insert_elements(vector, pos, new_elements):
    vector = np.insert(vector, pos, new_elements)
    vector = np.delete(vector, len(new_elements) + pos)
    return vector


def get_absolute_position(vector, req_pos):
    c = 0
    k = 0
    for ele in vector:
        if type(ele) == ft.Container:  # it is a block on the board, if not a subject block
            c = c + 1
            k = k + 1
            if c == req_pos:
                return k
            continue
        size = ele.size
        c = c + size
        k = k + 1
        if c == req_pos:
            return k

class ControlBoardSubjectSlots(ft.AnimatedSwitcher):

    def __init__(self, pga = DEFAULT_PCG, update = False) -> None:
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
            content=self.grid,
            expand = True,
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=500,
            reverse_duration=100,
            switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
            switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
        )
        
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
                    schedule_button(self.pga, self, button, subject, (row, col), size, self.subject_selector)
                    continue

                button.bgcolor = ft.colors.YELLOW
        self.grid.update()
        

    def turn_off_board(self):
        for row in range(30):
            for col in range(7):
                button = self.button_matrix[row, col]
                button.bgcolor = ft.colors.WHITE24
                button.on_click = None
        self.grid.update()

    def add_block(self, subject_block, update_slots_block = True) -> None:
        i = subject_block.position[0] # 29
        j = subject_block.position[1] # 29
        size = subject_block.size # 1

        # Reset the j-column, but before doing that, we make a copy
        previous_elements = self.day_columns[j].controls

        row_rel = get_absolute_position(previous_elements, i + 1)
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
        row_rel = get_absolute_position(previous_elements, i + 1)

        # Add the buttons back into the list
        buttons_to_add = self.button_matrix[i:i + size, j]
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


# !!! principal class 
class ControlBlocksSubject(ft.AnimatedSwitcher):

    def __init__(self, bd, pcg, search, to_change, reference_to_get_dict):
        
        self.db = bd
        
        button_to_change_page =  ft.FloatingActionButton(
            icon=ft.icons.ADD,
            on_click=lambda e: to_change(),
            text = "Gestionar datos",
            focus_elevation= 10,
        )
        
        self.reference_to_get_dict = reference_to_get_dict
        
        self.button_to_change_page = button_to_change_page
        
        self.search = search
        
        def change_professor():
            selected = self.search.get_value()
            self.set_pcg(selected)
            
        def get_actual_profesors():
            return 

        
        self.search =  SearchValue({
            professor.name: professor for professor in self.db.professors.get()
            },
            get_actual_profesors,
            on_change = change_professor
        )
                
        self.pcg = pcg
        
        layout = self.get_layout_page(pcg)

        super().__init__(
            content = ft.Row(
                controls = [layout],
                expand=True
            ),
            expand=True,
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=500,
            reverse_duration=100,
            switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
            switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
        )
        
    def get_layout_page(self, pcg):
        boardsubjects = ControlBoardSubjectSlots(pcg)
        self.boardsubjects = boardsubjects
        
        def change_professor():
            selected = self.search.get_value()
            self.set_pcg(selected)
            
        def get_actual_profesors():
            return self.reference_to_get_dict()

        
        self.search =  SearchValue(
            self.reference_to_get_dict(),
            get_actual_profesors,
            on_change = change_professor
        )
        
        name = ""
        
        if type(pcg) == Group:
            name = pcg.career.name + ' ' + pcg.semester.name + ' ' + pcg.subgroup.name
        elif type(pcg) == Professor:
            name = pcg.name
        elif type(pcg) == Classroom:
            name = pcg.name
        

        self.search.text.value = name

        
        layout = ft.Column(
            controls = [
                    ft.Row(
                        controls = [
                                    self.search,
                                    self.button_to_change_page,
                        ],
                        expand = False,
                        spacing=30
                    ),
                    ft.Row(
                        controls = [      
                            self.boardsubjects,
                            self.boardsubjects.subject_selector,
                        ],
                        expand = True
                    )
                    ],
                expand=True,
                spacing=50,
            )
        
        return layout 
                
        
    def set_pcg(self, pcg):
        new_layout = self.get_layout_page(pcg)
        
        self.pcg = pcg

        del super().content.controls[0]
        super().content.controls.append(new_layout)
        
        #self.boardsubjects.update()
        super().update()
        
    def update(self, update = True):
        new_layout = self.get_layout_page(self.pcg)
       
        #print("Se ejecuto")
        del super().content.controls[0]
        super().content.controls.append(new_layout) 
        
        if update:
            super().update()  
    
# programar el caso base de no hay profesor ni ninguna materia

