import flet as ft
from typing import Union, Tuple
from ...constants import HEIGHT_BUTTON, WIDTH_BUTTON

        
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
                 position: Tuple[int, int],
                 enrouter) -> None:
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
        self.enrouter = enrouter

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
            self.board.load_availability(self.size, self.subject, self.enrouter)

        # Create menu items for block options
        menuitem_INFO = ft.SubmenuButton(
            content=ft.Row(controls=[ft.Icon(name=ft.icons.INFO), ft.Text("Info")]),
            controls = [
                ft.MenuItemButton(content=ft.Container(content= ft.Text("Hola Mundo"), width=200, height=170))
            ],
            on_close = lambda e: print("Hello World")
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
                        menuitem_DELETE,
                        menuitem_MOVE,
                        menuitem_INFO,
                        menuitem_COLOR,
                    ],
                    width=WIDTH_BUTTON,
                    height=(HEIGHT_BUTTON * self.size + (self.size - 1) * 2),
                    menu_style=ft.MenuStyle(padding=0),
                    style=ft.ButtonStyle(padding=0)
                ),
            ],
            style=ft.MenuStyle(padding=0),
            data=self.size,
        )
        

            
        super().__init__(content=menu_options,
                         data = True,
                         animate=ft.animation.Animation(100, ft.AnimationCurve.EASE_IN_OUT))

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

class SubjectBlocksManager:
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

