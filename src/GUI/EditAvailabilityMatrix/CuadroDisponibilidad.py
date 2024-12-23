
import flet as ft
import numpy as np
import time as tm


class EditAvailabilityMatrix(ft.Container):

    def __init__(self) -> None:
        self.__disponibilidad = np.random.choice([False], size=(30, 7))

        dias_de_la_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        horas_del_dia = [
        "7:00 - 7:30 AM", "7:30 - 8:00 AM", "8:00 - 8:30 AM", "8:30 - 9:00 AM", 
        "9:00 - 9:30 AM", "9:30 - 10:00 AM", "10:00 - 10:30 AM", "10:30 - 11:00 AM", 
        "11:00 - 11:30 AM", "11:30 - 12:00 PM", "12:00 - 12:30 PM", "12:30 - 1:00 PM",
        "1:00 - 1:30 PM", "1:30 - 2:00 PM", "2:00 - 2:30 PM", "2:30 - 3:00 PM",
        "3:00 - 3:30 PM", "3:30 - 4:00 PM", "4:00 - 4:30 PM", "4:30 - 5:00 PM",
        "5:00 - 5:30 PM", "5:30 - 6:00 PM", "6:00 - 6:30 PM", "6:30 - 7:00 PM",
        "7:00 - 7:30 PM", "7:30 - 8:00 PM", "8:00 - 8:30 PM", "8:30 - 9:00 PM",
        "9:00 - 9:30 PM", "9:30 - 10:00 PM", "10:00 - 10:30 PM"
        ]

        def contenedor(fila,columna):

            return ft.CupertinoButton(
                    content=ft.Text(""),
                    width=60,
                    height=25,
                    bgcolor=ft.colors.RED,
                    padding=0,
                    border_radius=5,
                    on_click =  lambda e: boton_presionado(e,fila,columna)
            )


        def boton_presionado(e,fila,columna):
            if self.__disponibilidad[fila][columna]:
                self.__disponibilidad[fila][columna] = False
                self.__matriz_contenedores[fila][columna].bgcolor = ft.colors.RED
                self.__matriz_contenedores[fila][columna].update()
                print(self.__disponibilidad)
                return None
            self.__disponibilidad[fila][columna] = True
            self.__matriz_contenedores[fila][columna].bgcolor = ft.colors.GREEN
            self.__matriz_contenedores[fila][columna].update()


        matriz_contendores = [[contenedor(fila,columna) for columna in range(7)] for fila in range(30)]

        self.__matriz_contenedores = matriz_contendores
                

        def contenedor_horas(fila,derecha = True):
            # me da el contenedor respecto una fila
            def activar(fila): # activa toda la fila 

                for columna in range(7):
                    if self.__disponibilidad[fila][columna]:
                        continue # ya esta activada
                    self.__disponibilidad[fila][columna] = True
                    self.__matriz_contenedores[fila][columna].bgcolor = ft.colors.GREEN
                    self.__matriz_contenedores[fila][columna].update()
                    tm.sleep(0.01)

            def desactivar(fila):
                for columna in range(7):
                    if self.__disponibilidad[fila][columna]:
                        self.__disponibilidad[fila][columna] = False
                        self.__matriz_contenedores[fila][columna].bgcolor = ft.colors.RED
                        self.__matriz_contenedores[fila][columna].update()
                        tm.sleep(0.01)


            
            if  not derecha:
                return ft.CupertinoButton(
                content=ft.Text(horas_del_dia[fila], theme_style=ft.TextThemeStyle.BODY_SMALL,color = ft.colors.BLACK,size = 10),
                width=70,
                height=25,
                padding=1,
                border_radius=1,
                bgcolor = ft.colors.WHITE,
                alignment=ft.alignment.center,
                on_click = lambda e:activar(fila)
                ) 
            return ft.CupertinoButton(
            content=ft.Text(horas_del_dia[fila], theme_style=ft.TextThemeStyle.BODY_SMALL,color = ft.colors.BLACK,size = 10),
            width=70,
            height=25,
            padding=1,
            border_radius=1,
            bgcolor = ft.colors.WHITE,
            alignment=ft.alignment.center,
            on_click = lambda e:desactivar(fila)
            ) 
            

        def contenedor_dia(columna,superior = True):

            def activar_(columna):
                for fila in range(30):
                    if self.__disponibilidad[fila][columna]:
                        continue
                    self.__disponibilidad[fila][columna] = True
                    self.__matriz_contenedores[fila][columna].bgcolor = ft.colors.GREEN
                    self.__matriz_contenedores[fila][columna].update()
                    tm.sleep(0.01)



            def desactivar_(columna):
                for fila in range(30):
                    if self.__disponibilidad[fila][columna]:
                            self.__disponibilidad[fila][columna] = False
                            self.__matriz_contenedores[fila][columna].bgcolor = ft.colors.RED
                            self.__matriz_contenedores[fila][columna].update()
                            tm.sleep(0.01)

                
            if superior:
                return ft.CupertinoButton(
                content=ft.Text(dias_de_la_semana[columna], theme_style=ft.TextThemeStyle.BODY_SMALL,color = ft.colors.BLACK,size = 10),
                width=60,
                height=30,
                padding=1,
                border_radius=1,
                bgcolor = ft.colors.WHITE,
                alignment=ft.alignment.center,
                on_click = lambda e:activar_(columna)
                ) 
            return ft.CupertinoButton(
            content=ft.Text(dias_de_la_semana[columna], theme_style=ft.TextThemeStyle.BODY_SMALL,color = ft.colors.BLACK,size = 10),
            width=60,
            height=30,
            padding=1,
            border_radius=1,
            bgcolor = ft.colors.WHITE,
            alignment=ft.alignment.center,
            on_click = lambda e:desactivar_(columna)
            ) 
    
        
        contenedores_horas_derecha = [ contenedor_horas(fila,derecha = True) for fila in range(30)]
        contenedores_horas_izquierda = [ contenedor_horas(fila,derecha = False) for fila in range(30)]


        contenedores_dias_superior = [contenedor_dia(columna,superior = True) for columna in range(7)]
        contenedores_dias_inferior = [contenedor_dia(columna,superior = False) for columna in range(7)]


        #print(contenedores_horas,"\n")
        #print(np.transpose(self.__matriz_contenedores))

        def contenedor_vacio():
            return ft.Container(
                content = ft.Text(""),
                width=70,
                height=25,
                padding=1,
                border_radius=1,
                bgcolor = ft.colors.GREEN,
                alignment=ft.alignment.center,
                ) 


        contenedores_cuadricula = np.vstack((np.array([contenedores_horas_izquierda]), np.transpose(self.__matriz_contenedores),np.array([contenedores_horas_derecha])))
       #contenedores_cuadricula = np.vstack((np.array([contenedor_vacio()]) , contenedores_dias_superior , np.array([contenedor_vacio()]) ,contenedores_cuadricula))
       # contenedores_cuadricula = np.vstack(( contenedores_cuadricula , np.array([contenedor_vacio()]) , contenedores_dias_infierior , np.array([contenedor_vacio()])))
        columnas_cuadricula = [ft.Column(controls=i, alignment=ft.MainAxisAlignment.START, spacing=2) for i in contenedores_cuadricula] 

        fila_superior_dias =  [contenedor_vacio()] + contenedores_dias_superior + [contenedor_vacio()]

        fila_superior_dias = ft.Row(controls = fila_superior_dias,alignment=ft.MainAxisAlignment.START, spacing=2)
    

        fila_inferior_dias = [contenedor_vacio()] + contenedores_dias_inferior + [contenedor_vacio()]

        fila_inferior_dias = ft.Row(controls = fila_inferior_dias,alignment=ft.MainAxisAlignment.START, spacing=2)

        parte_intermedia = ft.Row(
        controls=columnas_cuadricula,
        alignment=ft.MainAxisAlignment.START,
        spacing=2,
        #scroll = ft.ScrollMode.ALWAYS,
        #expand = True

        )
        

        parte_total = ft.Column(
            controls = [fila_superior_dias] + [parte_intermedia] + [fila_inferior_dias],
            scroll = ft.ScrollMode.ALWAYS,
            on_scroll_interval=0,
        )

        parte_total = ft.Column(
            controls = [parte_total],
            scroll = ft.ScrollMode.ALWAYS,
            on_scroll_interval=0,
            expand = True,
            height= 600,
            width= 550

        )

        super().__init__(
            content= parte_total
        )


    def get_matrix(self):
        return self.__disponibilidad
    
    def set_matrix(self,matriz):

        for fila in range(30):
            for columna in range(7):
                if matriz[fila][columna] == self.__disponibilidad[fila][columna]:
                    continue
                if matriz[fila][columna]:
                    self.__disponibilidad[fila][columna] = True
                    self.__matriz_contenedores[fila][columna].bgcolor = ft.colors.GREEN
                    continue 
                self.__disponibilidad[fila][columna] = False
                self.__matriz_contenedores[fila][columna].bgcolor = ft.colors.RED
        self.update()
                

#print(np.array([1,2,3] + np.array([1,2,3])))



    



