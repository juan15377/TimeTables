
import sys  

sys.path.append("src/Logic/")
sys.path.append("tests/Logic/")

import flet as ft 
import numpy as np
import time as tm 
from Subjects import Subject, HoursComposition
from Professor_Classroom_Group import PCG, DEFAULT_PCG
import copy
from Colors import MyColorPicker,MyColorRGB, RGB_to_hex
from tests_3 import Bd, materia_1, materia_2
from Subjects import HoursSlotsComposition
from seleccionador_materias import SubjectSelector
from Seleccionador_PGA import buscador_professor,buscador_classroom, buscador_group
# ! tablero de control debe tener un metodo de inicializar con un objecto pga 
# ! este a partir de una inicializacion se debe mantener con operaciones que permitan 
# ! añadir bloques, este debe tener una forma eficiemte de actualizar ciertas partes del objecto para 
# ! cosas de optimizacion, ciertas operaciones como reinciar pga, materia, este descencadenara 
# ! la actualizacion en el nucleo y una actualizacion del tablero, lo cual es costoso de hacer por lo que las 
# ! operaciones permitidas deben ser bien escogidas  
# el tiempo permitido maximo poara la generacion de un tablero deberiaser de de 0.2 segundos 

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
            "9:00 - 9:30 PM", "9:30 - 10:00 PM", "10:00 - 10:30 PM"
    ]

    def button_container(i, j):
        b = ft.Container(
                content=ft.Text(f""),
                theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK)),
                margin=ft.Margin(top=0, right=0, bottom=0, left=0),
                padding=2,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE24,
                width=100,
                height=30,
                border_radius=5,
                expand = False
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
                    width=100,
                    height=30,
                    border_radius=1,
                    expand=False
                )
        
    def day_container(i):
        return ft.Container(
                    theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK)),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    content=ft.Text(weekdays[i], color="white", size=12),
                    margin=2,
                    padding=0,
                    alignment=ft.alignment.center,
                    width=100,
                    height=30,
                    border_radius=1,
                    expand=False
                )
        
    special_container = ft.Container(
                            theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK)),
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            content=ft.Text("Special", color="white", width=1),
                            margin=2,
                            padding=0,
                            alignment=ft.alignment.center,
                            width=100,
                            height=30,
                            border_radius=1,
                            expand = False
                        )
        
    time_containers = [special_container] + [time_container(i) for i in range(30)]
    day_containers = [day_container(i) for i in range(7)]

    time_column = ft.Column(
                    controls=time_containers,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
                    )
    

    day_columns = [ft.Column(controls=[day_containers[i]],
                    horizontal_alignment=ft.alignment.center, 
                    alignment=ft.alignment.center, spacing=2) for i in range(7)]
        

    
    # Add the buttons contained in the button matrix 

    for i in range(30):
        for j in range(7):
            button = button_matrix[i][j]
            day_columns[j].controls.append(button)
                
            

    total_columns = [time_column] + day_columns


    row = ft.Row(
            controls=total_columns,
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            width=840,
            height=1000,  
            expand = False
            )

    grid = ft.Column(
            controls=[row],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            width=840,
            height=400,    
            expand = True
        )
    
    return button_matrix, grid, day_columns




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
        print(positions)
        for position in positions:
            row = position[0]
            block_size = position[1] - position[0] + 1
            block = SubjectBlock(pga, control_board, subject, block_size, (row, column))
            blocks.append(block)
    return blocks


class SubjectBlocks:
    
    def __init__(self) -> None:
        self.subjects = {}
        self.total = np.zeros((30, 7), dtype=object)

    def new(self, subject_block, position):
        subject = subject_block.subject 
        i = position[0] 
        j = position[1]
        if subject in self.subjects:
            self.subjects[subject][i, j] = subject_block
            self.total[i, j] = subject_block
            return None
        self.subjects[subject] = np.zeros((30, 7), dtype=object)
        self.subjects[subject][i, j] = subject_block
        self.total[i, j] = subject_block
        return None 
    
    def get_subject_blocks(self, subject):
        if subject in self.subjects:
            block_list = list(set(self.subjects[subject].flatten().tolist()))
            block_list.remove(0)
            return block_list
        return []
    
    def get_blocks(self, position):
        i = position[0]
        j = position[1]
        if self.total[i, j] != 0:
            return self.total[i, j]
        return []

    
    def delete_block(self, subject, position):  #! Deletes both from total and subject
        i = position[0]
        j = position[1]

        if subject in self.subjects and self.total[i, j] != 0:
            self.subjects[subject][i, j] = 0
            if set(self.subjects[subject].flatten().tolist()) == set([0]):
                del self.subjects[subject]
            return None
        return None
    
    def delete_subject_blocks(self, subject):
        if subject in self.subjects:
            del self.subjects[subject]
            return None
        return None
    
    def delete_all_blocks(self):
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
        print("Size = ", c + ele.size)
        c = c + size
        k = k + 1
        if c == req_pos:
            return k

class ControlBoardSubjectSlots(ft.Container):

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
            content=self.grid
        )
        
        # Generate subject blocks for each subject in the PGA
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
        previous_elements = copy.copy(self.day_columns[j].controls)

        row_rel = get_absolute_position(previous_elements, i + 1)
        news_elements = replace_element(previous_elements,
                                            row_rel,
                                            row_rel + size - 1,
                                            subject_block)
        
        
        print("Tamaño = ", subject_block.size)
        print(subject_block.subject.allocated_subject_matrix)
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


        
class SubjectBlock(ft.Container):

    def __init__(self, pga, control_board, subject, size, position) -> None:
        self.subject = subject
        self.size = size  # Size represents the number of half-hours
        self.board = control_board
        self.position = position
        self.pga = pga

        # Color picker for the block
        color_picker = MyColorPicker()
        original_color = pga.subject_colors.colors[subject]
        color_picker.update_color(original_color)
        self.color_picker = color_picker

        # Function to delete the block
        def delete_block(self):
            position = self.position
            self.board.turn_off_board()
            self.board.remove_block(subject, position, size)

        # Function to change the subject color
        def change_subject_color(subject, board):
            color = self.color_picker.get_color()
            board.change_subject_color(subject, color)

        # Function to move the block (delete and re-enable availability for insertion)
        def move_block(self):
            position = self.position
            self.board.remove_block(subject, position, size)
            self.board.load_availability(size, subject)

        # Creating menu items for block options
        menuitem_INFO = ft.MenuItemButton(content= ft.Row(controls = [ft.Icon(name=ft.icons.INFO), ft.Text("Info")]),
                                         on_click= lambda e: print("Hello Everyone")
                        )
        
        menuitem_DELETE = ft.MenuItemButton(content= ft.Row(controls = [ft.Icon(name=ft.icons.DELETE), ft.Text("Delete")]),
                                            on_click= lambda e: delete_block(self)
                            )
        
        menuitem_MOVE = ft.MenuItemButton(content= ft.Row(controls = [ft.Icon(name=ft.icons.MOVE_DOWN), ft.Text("Move")]),
                                           on_click= lambda e: move_block(self)
                        )

        menuitem_COLOR =  ft.SubmenuButton(
                            content=ft.Text("Color"),
                            leading=ft.Icon(ft.icons.COLOR_LENS),
                            controls=[
                                ft.MenuItemButton(
                                    content=ft.Container(content=self.color_picker, width=200, height=170),
                                )
                            ],
                            on_close= lambda e: change_subject_color(subject, control_board),
                        )

        # Tooltip and name display for the subject
        text_name = ft.Tooltip(
                        message=subject.name,
                        content=ft.Text(subject.code, size=23, color=ft.colors.BLACK),
                        text_style=ft.TextStyle(size=15, color=ft.colors.BLACK),
                    )
        
        subject_container = ft.Container(content=text_name,
                                         width=100,
                                         height=(30*size + (size-1)*2),
                                         alignment=ft.alignment.center,
                                         bgcolor=RGB_to_hex(original_color),
                                         padding=0,
                                         margin=ft.Margin(top=0, right=0, bottom=0, left=0),
                                         border_radius=5,
                                         on_hover=lambda e: ft.Tooltip(message="This is tooltip",)
                                    )

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
                        width=100,
                        height=(30*size + (size-1)*2),
                        menu_style=ft.MenuStyle(padding=0),
                        style=ft.ButtonStyle(padding=0)
                    ),  
            ],
            style=ft.MenuStyle(
                                padding=0,
                    ),
            data=size
        )

        super().__init__(
            content=menu_options
        )



    def change_individual_block_color(self, color):
        color = RGB_to_hex(color)
        self.content.controls[0].content.bgcolor = color
        self.content.update()
        print("actualizado")
        print(self.content.controls[0].content.bgcolor)




professor = Bd.professors.get()[0]
T = ControlBoardSubjectSlots(professor)

subject = Bd.subjects.get()[0]
print(professor.get_subjects())

# def mostrar_colocacion_materia():
#         T.cargar_disponibilidad(4, materia_1)
#         print(materia_1.disponibilidad, "\n \n")
        


# boton =ft.TextButton(
#         text = "Presiona",
#         on_click= lambda e : mostrar_colocacion_materia()
#     )

print(len(professor.get_subjects()))
# Tablero = ft.Row(controls = [T.cuadricula, boton])

# #lista_materia = SeleccionadorMaterias(BD.profesores.get()[0], 1).lista_materias
# selec_bloques = CargarMateria(BD.profesores.get()[0], BD.materias.get()[0], T)
# print(BD.materias.get()[0].composicion_horas.get_bloques_disponibles())

# !!! principal class 
class ControlBlocksSubject(ft.Container):

    def __init__(self, Bd, pcg, search):
        boardsubjects = ControlBoardSubjectSlots(pcg)
        self.search = search
        self.pcg = pcg
        row = ft.Column(
        controls = [
                search,
                ft.Row(
                    controls = [      
                        boardsubjects,
                        boardsubjects.subject_selector,
                    ]
                )
                ],
            expand=False,
            spacing=40,
        )

        super().__init__(
            content = ft.Row(
                controls = [row],
            ),
        )
        
    def set_pcg(self, pcg):
        boardsubjects = ControlBoardSubjectSlots(pcg)
        self.pcg = pcg
        row = ft.Column(
        controls = [
                self.search,
                ft.Row(
                    controls = [      
                        boardsubjects,
                        boardsubjects.subject_selector,
                    ]
                )
                ],
            expand=False,
            spacing=40,
        )
        
        del super().content.controls[0]
        super().content.controls.append(row)
        
        super().update()
        
    def update(self):
        boardsubjects = ControlBoardSubjectSlots(self.pcg)
        row = ft.Column(
        controls = [
                self.search,
                ft.Row(
                    controls = [      
                        boardsubjects,
                        boardsubjects.subject_selector,
                    ]
                )
                ],
            expand=False,
            spacing=40,
        )
        
        del super().content.controls[0]
        super().content.controls.append(row)   
    
# programar el caso base de no hay profesor ni ninguna materia

def cambiar_professor(e, bd = Bd):
    seleccionado = buscador_professor.get_value()
    content_professor.set_pcg(seleccionado)


def cambiar_classroom(e, bd = Bd):
    seleccionado = buscador_classroom.get_value()
    content_classroom.set_pcg(seleccionado)


def cambiar_group(e, bd = Bd):
    seleccionado = buscador_group.get_value()
    content_group.set_pcg(seleccionado)

buscador_professor.on_change = cambiar_professor
buscador_classroom.on_change = cambiar_classroom
buscador_group.on_change = cambiar_group

content_professor = ControlBlocksSubject(Bd, DEFAULT_PCG, buscador_professor)
content_classroom = ControlBlocksSubject(Bd, DEFAULT_PCG, buscador_classroom)
content_group = ControlBlocksSubject(Bd, DEFAULT_PCG, buscador_group)

#
#lista = [0]
#
#def main(page : ft.Page):
#    boardsubject = ControlBlocksSubject(Bd, professor)
#    def cambiar_professor(e):
#        print(e.data)
#        professor_2 = Bd.professors.get()[lista[0]%2]
#        boardsubject.set_pcg(professor_2)
#        lista[0] = lista[0] + 1
#    
#    boton_cambiar_professor = ft.TextButton(
#        text = "cambiar",
#        on_click= lambda e: cambiar_professor(e),
#    )
#
#    page.add(boardsubject, boton_cambiar_professor)
#
#ft.app(main)

