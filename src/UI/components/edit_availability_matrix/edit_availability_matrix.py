
import flet as ft
import numpy as np
import time as tm
# el cuadro tendra 4 colores

# - verde indicara que existe disponibilidad y no hay ninguna materia ocupando ese espacio
# - rojo indicara que no hay forma de ocupar ese espacio por restricciones ajenas al programa 
# - azul indica que que hay bloques de materia colocados en esos espacios 
# - amarillo indica que hay materia colocadas en esos espacios y se esta quitando esta posibilidad y con ellos ese bloque de materia


COLORS_STATES_EDIT_AVAI_MATRIX = {
    1 : "green",
    2 : "red",
    3 : "blue",
    4 : "yellow"
}

CHANGE_STATES = {
    1 : 2, # si se encuentra en 1 pasara al 2 al momento que se quiera pasar al estado
    2 : 1, #
    3 : 4, #
    4 : 3, #
}

# las filas y columnas tendran dos modos 

class EditAvailabilityMatrix(ft.Container):

    def __init__(self) -> None:
        self.__states = np.random.choice([1], size=(30, 7))

        days_weekday = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        day_hours = [
        "7:00 - 7:30 AM", "7:30 - 8:00 AM", "8:00 - 8:30 AM", "8:30 - 9:00 AM", 
        "9:00 - 9:30 AM", "9:30 - 10:00 AM", "10:00 - 10:30 AM", "10:30 - 11:00 AM", 
        "11:00 - 11:30 AM", "11:30 - 12:00 PM", "12:00 - 12:30 PM", "12:30 - 1:00 PM",
        "1:00 - 1:30 PM", "1:30 - 2:00 PM", "2:00 - 2:30 PM", "2:30 - 3:00 PM",
        "3:00 - 3:30 PM", "3:30 - 4:00 PM", "4:00 - 4:30 PM", "4:30 - 5:00 PM",
        "5:00 - 5:30 PM", "5:30 - 6:00 PM", "6:00 - 6:30 PM", "6:30 - 7:00 PM",
        "7:00 - 7:30 PM", "7:30 - 8:00 PM", "8:00 - 8:30 PM", "8:30 - 9:00 PM",
        "9:00 - 9:30 PM", "9:30 - 10:00 PM", "10:00 - 10:30 PM"
        ]

        def button_container(row,column):

            return ft.Container(
                    content=ft.Text(""),
                    bgcolor=COLORS_STATES_EDIT_AVAI_MATRIX[1],
                    width=30,
                    height=50,
                    padding=0,
                    border_radius=5,
                    on_click =  lambda e: change_state(e,row,column),
                    expand=True
            )


        def change_state(e, row, column):
            self.__states[row, column] = CHANGE_STATES[self.__states[row, column]]
            self.__button_matrix[row, column].bgcolor = COLORS_STATES_EDIT_AVAI_MATRIX[self.__states[row, column]]
            self.__button_matrix[row][column].update()
            pass 


        button_matrix = [[button_container(row,column) for column in range(7)] for row in range(30)]
        

        self.__button_matrix = np.array(button_matrix)
                

        def hours_buttons(row):
            # me da el contenedor respecto una fila
            def activate_hours(fila): # activa toda la fila 
            
                for column in range(7):
                    if self.__states[row, column] in [1, 3]:
                        continue # ya esta activada
                    change_state(1, row, column)
                    tm.sleep(0.01)

            def deactivate_hours(fila):
                for column in range(7):
                    if self.__states[row, column] in [1, 3]:
                        change_state(1, row, column)
                        tm.sleep(0.01)


            return ft.Container(
                content=ft.Text(day_hours[row],weight="bold", color=ft.colors.WHITE, expand = True, size = 13),
                width=30,
                height=50,
                padding=0,
                border_radius=5,
                expand=True,
                on_click = lambda e, row = row: activate_hours(row),
                on_long_press = lambda e, row = row: deactivate_hours(row),
                bgcolor = "red",
                alignment= ft.alignment.center
                ) 
            

        def days_buttons(column):

            def activate_days(column):
                for row in range(30):
                    if self.__states[row, column] in [1, 3]:
                        continue # ya esta activada
                    change_state(1, row, column)
                    tm.sleep(0.01)

            def deactivate_days(column):
                for row in range(30):
                    if self.__states[row, column] in [1, 3]:
                        change_state(1, row, column)
                        tm.sleep(0.01)


            return ft.Container(
                content=ft.Text(days_weekday[column], weight="bold", color=ft.colors.WHITE, expand = True, size = 13),
                width=30,
                height=50,
                padding=0,
                border_radius=5,
                expand=True,
                on_click = lambda e, column = column: activate_days(column),
                on_long_press = lambda e, column = column: deactivate_days(column),
                bgcolor = "blue",
                alignment= ft.alignment.center
                ) 


        def contenedor_vacio():
            return ft.CupertinoButton(
            content= ft.Text(""),
            padding=1,
            border_radius=1,
            bgcolor = ft.colors.WHITE,
            alignment=ft.alignment.center,
            expand = True
            ) 
        
        contenedores_horas_derecha = [ hours_buttons(row) for row in range(30)]
        contenedores_horas_izquierda = [hours_buttons(row) for row in range(30)]

        
        contenedores_dias_superior = [days_buttons(column) for column in range(7)]
        contenedores_dias_inferior = [days_buttons(column) for column in range(7)]

        cont_vacio = contenedor_vacio()

        fila_superior = ft.Row([cont_vacio] + contenedores_dias_superior)
        fila_inferior = ft.Row([cont_vacio] + contenedores_dias_inferior, expand = True)
        
        filas_matriz_principal = [ft.Row(controls = [hour_left] + fila, expand = True ) 
                                  for (hour_left, fila, hour_right) in zip(contenedores_horas_izquierda, button_matrix, contenedores_horas_derecha)]
        
        principal = ft.ListView(
            controls = filas_matriz_principal,
            spacing=5,
            item_extent=10,
            expand = True
        )

        super().__init__(
            content= ft.Column(
                controls = [fila_superior,
                            principal,
                            ],
                expand = True
            ),
            expand = True
        )
        
    def get_availability_matrix(self):

        def boolean_state(state):
            if state in [1, 3]:
                return True 
            else: 
                return False
            
        new_availability_matrix = np.vectorize(boolean_state)(self.__states)

        print("new_availability_matrix")
        
        print(new_availability_matrix)
        return new_availability_matrix
    
    

    def set_states(self, pcg, update = True):
        # los de color verde seran los de las disponibilidad inicial
        # los de color rojo aquellos es que no
        # los azules se pueden obtener como la diferencia
        allocated_subject_matrix = pcg.get_allocate_subjects_matrix()
        initial_availability_matrix = pcg.initial_availability_matrix()
        
        
        for row in range(30):
            for column in range(7):
                if not initial_availability_matrix[row, column]:
                    self.__states[row, column] = 2
                elif allocated_subject_matrix[row, column]:
                    self.__states[row, column] = 3
                else:
                    self.__states[row, column] = 1
                self.__button_matrix[row, column].bgcolor = COLORS_STATES_EDIT_AVAI_MATRIX[self.__states[row, column]]
        if update:
            self.update()
    
#print(np.array([1,2,3] + np.array([1,2,3])))

