
import sys  

sys.path.append("/home/juandejesus/Escritorio/Programacion/Proyectos/Horarios/Software/Logica Principal")
sys.path.append("/home/juandejesus/Escritorio/Programacion/Proyectos/Horarios/Software/Pruebas")

import flet as ft 
import numpy as np 
import time as tm 
from materias import Materia, CHoras
from pga import PGA
import copy
from colores import MiColorPicker,MiColorRGB, triada_a_hex
from tests_3 import BD, materia_1, materia_2, materia_3 
from materias import CHoras
from seleccionador_materias import SeleccionadorMaterias
from Seleccionador_PGA import buscador
# ! tablero de control debe tener un metodo de inicializar con un objecto pga 
# ! este a partir de una inicializacion se debe mantener con operaciones que permitan 
# ! añadir bloques, este debe tener una forma eficiemte de actualizar ciertas partes del objecto para 
# ! cosas de optimizacion, ciertas operaciones como reinciar pga, materia, este descencadenara 
# ! la actualizacion en el nucleo y una actualizacion del tablero, lo cual es costoso de hacer por lo que las 
# ! operaciones permitidas deben ser bien escogidas  
# el tiempo permitido maximo poara la generacion de un tablero deberiaser de de 0.2 segundos 


def tablero_control_0():

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

    def boton_contenedor(i,j):
        b = ft.Container(
                content=ft.Text(f""),
                theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK)),
                margin=ft.Margin(top=0, right=0, bottom=0, left=0),
                padding=2,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE24,
                width=100,
                height=30 ,
                border_radius=5,
            )
        return b


    matriz_botones = np.array([[boton_contenedor(i,j) for j in range(7)] for i in range(30)])

    
    def contenedor_hora(i):
        return ft.Container(
                    theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK)),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    content=ft.Text(horas_del_dia[i],color="white",size = 12),
                    margin=1,
                    padding=0,
                    alignment=ft.alignment.center,
                    width=100,
                    height=30,
                    border_radius=1,
                )
        
    def contendor_dia(i):
        return ft.Container(
                    theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK)),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    content=ft.Text(dias_de_la_semana[i],color="white",size = 12),
                    margin=2,
                    padding=0,
                    alignment=ft.alignment.center,
                    width=100,
                    height=30,
                    border_radius=1,
                )
        
    contenedor_especial = ft.Container(
                            theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK)),
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            content=ft.Text("Especial",color="white",width=1),
                            margin=2,
                            padding=0,
                            alignment=ft.alignment.center,
                            width=100,
                            height=30,
                            border_radius=1,
                        )
        
    contendores_horas = [contenedor_especial] + [contenedor_hora(i) for i in range(30)]
    contenedor_dias = [contendor_dia(i) for i in range(7)]

    columna_horas = ft.Column(
                    controls = contendores_horas,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
                    scroll= ft.ScrollMode.AUTO,
                    #expand = True,
                    )
    

    columnas_dias = [ft.Column(controls = [contenedor_dias[i]],
                    horizontal_alignment = ft.alignment.center, 
                    alignment=ft.alignment.center,spacing=2) for i in range(7)]
        

    
        # añadimos los botones contenidos en la matriz de botones 

    for i in range(30):
        for j in range(7):
            boton = matriz_botones[i][j]
            columnas_dias[j].controls.append(boton)
                
            

    columnas_totales = [columna_horas] + columnas_dias


    fila = ft.Row(
            controls= columnas_totales,
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.START,
            scroll= ft.ScrollMode.AUTO,
            )

    cuad = ft.Column(
            controls = [fila],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
            scroll= ft.ScrollMode.AUTO,
            width= 840,
            height= 500,
        )
    return matriz_botones, cuad, columnas_dias


def descomponer_vector(vector):
    pos_in = 0
    posiciones = []
    inicio_cadena = False

    for num, ele in enumerate(vector):
        if ele == 0 and inicio_cadena:
            inicio_cadena = False
            posiciones.append((pos_in, num))
            continue 
        if ele == 1 and (not inicio_cadena):
            inicio_cadena = True
            pos_in = num
            continue 
    if inicio_cadena:
        posiciones.append((pos_in, len(vector)-1))

    return posiciones


# si hago el objecto de TableroControl mutable para solo añadir los bloques 
# uno por uno 


def generar_bloques_materia(pga, tablero_control, materia):
    # dado un conjunto de materias se dara una lista de bloques de materias las cuales mediante metodos internos 
    # se insertaran 
    horas_colocadas = materia.horas_colocadas
    bloques = []
    for columna in range(7):
        columna_ = horas_colocadas[:,columna]
        posiciones = descomponer_vector(columna_)
        for posicion in posiciones:
            fila = posicion[0]
            tamaño_bloque = posicion[1] - posicion[0] 
            bloque = BloqueMateria(pga, tablero_control, materia, tamaño_bloque, (fila,columna))
            bloques.append(bloque)
    return bloques



class BloquesMaterias():
    
    def __init__(self) -> None:
        self.materias = { }
        self.total = np.zeros((30,7), dtype=object)

    def new(self, bmateria, posicion):
        materia = bmateria.materia 
        i = posicion[0] 
        j = posicion[1]
        if materia in self.materias:
            self.materias[materia][i, j] = bmateria
            self.total[i, j] = bmateria
            return None
        self.materias[materia] =  np.zeros((30,7), dtype=object)
        self.materias[materia][i, j] = bmateria
        self.total[i, j] = bmateria
        return None 
    
    def get_blocks_materia(self, materia):
        if materia in self.materias:
            lista_bloques = list(set((self.materias[materia].flatten().tolist())))
            lista_bloques.remove(0)
            return lista_bloques
        return []
    
    def get_blocks(self, posicion):
        i = posicion[0]
        j = posicion[1]
        if self.total[i, j] != 0:
            return self.total[i, j]
        return []

    
    def delete_block(self, materia, posicion): #! se elimina tanto del total como se la materia
        i = posicion[0]
        j = posicion[1]

        if materia in self.materias and self.total[i, j] != 0:
            self.materias[materia][i, j] = 0
            if set(self.materias[materia].flatten().tolist()) == set([0]):
                del self.materias[materia]
            return None
        return None
    
    def delete_blocks_materia(self, materia):
        if materia in self.bloques:
            del self.bloques[materia]
            return None
        return None
    
    def delete_blocks(self):
        self.materias = { }
        self.total = np.zeros((30,7), dtype=object)

        

def programar_boton(pga, tablero, boton, materia, posicion, tamaño, gestor_materias):
    boton.bgcolor = ft.colors.GREEN_400

    def añadir_bloque():
        bloque = BloqueMateria(pga, tablero, materia, tamaño, posicion)
        tablero.añadir_bloque(bloque)
        tablero.apagar_tablero()
        gestor_materias.update()
        tablero.cuadricula.update()


    boton.on_click = lambda e : añadir_bloque()


def remplazar_elemento(vector, inicio, fin, elemento):
    parte_izquierda = vector[0:inicio]
    parte_derecha = vector[fin+1:]

    return np.concatenate((parte_izquierda,[elemento], parte_derecha))


def insertar_elementos(vector, pos, nuevos_elementos):
    vector = np.insert(vector, pos, nuevos_elementos)
    vector = np.delete(vector,len(nuevos_elementos)+pos)
    return vector


def obtener_posicion_absoluta(vector, pos_req):
    c = 0
    k = 0
    for ele in vector:
        if type(ele) == ft.Container : # es un bloque del tablero, si no es un bloque de una materia 
            c = c +1
            k = k + 1
            if c == pos_req :
                return k
            continue 
        tamaño = ele.tamaño
        print("Tamaño  = ", c + ele.tamaño)
        c = c + tamaño
        k = k + 1
        if c == pos_req :
            return k 



class TableroControl(ft.Container):

    def __init__(self, pga) -> None:
        self.actualizar_pga(pga)


    def actualizar_pga(self, pga: PGA) -> None:
        matriz_botones, cuadricula, columnas_dias = tablero_control_0()

        seleccionador_mat = SeleccionadorMaterias(pga, self)
        self.seleccionador_mat = seleccionador_mat

        self.matriz_botones = matriz_botones
        self.cuadricula = cuadricula
        self.columnas_dias = columnas_dias
        self.bloques_materias = BloquesMaterias()
        self.pga = pga


        super().__init__(
            content = cuadricula
        )

        for materia in pga.materias:
            bloques_materias = generar_bloques_materia(pga, self, materia)
            for bloque_materia in bloques_materias:
                self.añadir_bloque(bloque_materia)


    def cargar_disponibilidad(self, tamaño, materia): # este metodo activas las celdasa para que se pueda añadir un bloque
        # pintara las celdas del tablero respecto a la disponibilidad de la materia en este tablero
        disponibilidad = materia.disponibilidad 
        for fila in range(30):
            for columna in range(7):
                boton = self.matriz_botones[fila, columna]
                if disponibilidad[fila,columna] == 0 :
                    boton.bgcolor = ft.colors.RED 
                    continue 

                if disponibilidad[fila: fila + tamaño, columna].sum() == tamaño:
                    programar_boton(self.pga, self, boton, materia, (fila,columna), tamaño, self.seleccionador_mat)
                    continue 
    
                boton.bgcolor = ft.colors.YELLOW
        self.cuadricula.update()

    def apagar_tablero(self):
        for fila in range(30):
            for columna in range(7):
                boton = self.matriz_botones[fila, columna]
                boton.bgcolor = ft.colors.WHITE24
                boton.on_click = None 
        pass
        self.cuadricula.update()


    def añadir_bloque(self, bmateria) -> None:
        i = bmateria.posicion[0]
        j = bmateria.posicion[1]
        tamaño = bmateria.tamaño
        # reiniciamos la j-columna, pero antes hacemos una copia 
        elementos_anteriores = copy.copy(self.columnas_dias[j].controls)
        #print(elementos_anteriores)
        fila_rel = obtener_posicion_absoluta(elementos_anteriores, i+1)
        elementos_anteriores = remplazar_elemento(elementos_anteriores,
                                                  fila_rel  ,
                                                  fila_rel + tamaño -1 ,
                                                  bmateria)
    
        #print(self.columnas_dias[j].controls)
        self.columnas_dias[j].controls = elementos_anteriores
        #self.columnas_dias[j].update()
        #self.diseño.update()
        self.bloques_materias.new(bmateria, (i, j))
        bmateria.materia.colocar_horas((i,j), bmateria.tamaño )
        pass 

    def eliminar_bloque(self, materia, posicion: tuple, tamaño) -> None:
        i = posicion[0]
        j = posicion[1]
        # suponemos que tenemos un bloque de una materia aqui 
        elementos_anteriores = copy.copy(self.columnas_dias[j].controls) # bien 
        fila_rel = obtener_posicion_absoluta(elementos_anteriores, i+1)
        #elementos_anteriores = np.delete(elementos_anteriores,i+1)
        botones_a_agregar = self.matriz_botones[i:i+tamaño,j]
        elementos_anteriores = insertar_elementos(elementos_anteriores,fila_rel ,botones_a_agregar)
                                                                        
        #np.insert(elementos_anteriores,i,self.matriz_botones[i][j:j+tamaño])

        
        self.columnas_dias[j].controls = elementos_anteriores
        self.columnas_dias[j].update()
        self.bloques_materias.delete_block(materia, posicion)
        materia.eliminar_horas(posicion, tamaño)
        self.seleccionador_mat.update()

    

    def cambiar_color_materia(self, materia, color):
        bloques = self.bloques_materias.get_blocks_materia(materia)
        self.pga.colores_materias.cambiar_color(materia, color)
        for bloque in bloques:
            bloque.color_picker.set_color(color)
            bloque.cambiar_color_bloque_individual(color)
        self.cuadricula.update()
        self.seleccionador_mat.update()
        

        
        
class BloqueMateria(ft.Container):

    def __init__(self, pga, tablero_control, materia, tamaño, posicion) -> None:
        self.materia = materia
        self.tamaño = tamaño # el tamaño es la cantidad de medias horas 
        self.tablero = tablero_control
        self.posicion = posicion
        self.pga = pga



        color_picker = MiColorPicker()
        color_original = pga.colores_materias.color[materia]
        color_picker.update_color(color_original)
        self.color_picker = color_picker



        def eliminar_bloque(self):
            posicion = self.posicion
            self.tablero.apagar_tablero()
            self.tablero.eliminar_bloque(materia, posicion, tamaño)


        def cambiar_color_materia(self, materia, tablero):
            color = self.color_picker.get_color()
            tablero.cambiar_color_materia(materia, color)


        def mover_bloque(self):
            # ? este elimina el bloque y activa el tablero para que se pueda volver a insertar 
            posicion = self.posicion
            self.tablero.eliminar_bloque(materia, posicion, tamaño)
            self.tablero.cargar_disponibilidad(tamaño, materia)

        #color = MicolorRGB(100, 100, 50)

        menuitem_INFO = ft.MenuItemButton(content= ft.Row(controls = [ft.Icon(name=ft.icons.INFO),ft.Text("Info")])
                                         ,on_click= lambda e: print("Hola Guapos")
                        )
        
        menuitem_DELETE = ft.MenuItemButton(content= ft.Row(controls = [ft.Icon(name=ft.icons.DELETE),ft.Text("Eliminar")]),
                                            on_click= lambda e: eliminar_bloque(self)
                            )
        
        menuitem_MOVE = ft.MenuItemButton(content= ft.Row(controls = [ft.Icon(name=ft.icons.MOVE_DOWN),ft.Text("Mover")]),
                                           on_click= lambda e: mover_bloque(self)
                        )

        menuitem_COLOR =  ft.SubmenuButton(
                            content=ft.Text("Color"),
                            leading=ft.Icon(ft.icons.COLOR_LENS),
                            controls=[
                                ft.MenuItemButton(
                                    content=ft.Container(content = self.color_picker.contenedor,width=200,height=170),
                                )
                            ],
                            on_close= lambda e: cambiar_color_materia(self, materia, tablero_control),
                        )     
        
        text_name = ft.Tooltip(
                        message=materia.nombre,
                        content=ft.Text(materia.abreviatura, size = 23, color = ft.colors.BLACK),
                        text_style=ft.TextStyle(size=15, color=ft.colors.BLACK),
                    )
        
        cont_MATERIA = ft.Container(content= text_name,
                                    width=100,
                                    height=(30*tamaño + (tamaño-1)*2),
                                    alignment=ft.alignment.center,
                                    bgcolor= triada_a_hex(color_original),
                                    padding=0,
                                    margin = ft.Margin(top=0, right=0, bottom=0, left=0),
                                    border_radius=5,
                                    on_hover = lambda e : ft.Tooltip( message="This is tooltip",)
                                    )

        menu_opciones = ft.MenuBar(
            controls=[
                    ft.SubmenuButton(
                        content = cont_MATERIA,
                        controls=[
                                menuitem_INFO,
                                menuitem_DELETE,
                                menuitem_MOVE,
                                menuitem_COLOR,          
                        ],
                        width = 100,
                        height = (30*tamaño + (tamaño-1)*2),
                        menu_style=ft.MenuStyle(padding = 0
                                    ),
                        style=ft.ButtonStyle( padding = 0,
                                )
                    ),  
            ],
            style = ft.MenuStyle(
                                padding=0,
                    ),
            data = tamaño
        )

        super().__init__(
            content = menu_opciones
        )

        pass


    def cambiar_color_bloque_individual(self, color):
        color = triada_a_hex(color)
        self.content.controls[0].content.bgcolor = color




profesor = BD.profesores.get()[0]
T = TableroControl(profesor)

materia = BD.materias.get()[0]
print(profesor.get_materias())

# def mostrar_colocacion_materia():
#         T.cargar_disponibilidad(4, materia_1)
#         print(materia_1.disponibilidad, "\n \n")
        


# boton =ft.TextButton(
#         text = "Presiona",
#         on_click= lambda e : mostrar_colocacion_materia()
#     )

print(len(profesor.get_materias()))
# Tablero = ft.Row(controls = [T.cuadricula, boton])

# #lista_materia = SeleccionadorMaterias(BD.profesores.get()[0], 1).lista_materias
# selec_bloques = CargarMateria(BD.profesores.get()[0], BD.materias.get()[0], T)
# print(BD.materias.get()[0].composicion_horas.get_bloques_disponibles())

def main(page : ft.Page):
    fila = ft.Row(
        controls = [T,
        T.seleccionador_mat.contenido],
        spacing = 40
     )
    columna = ft.Column(
        controls=  [buscador.contenedor,
                    fila],
    )
    page.add(columna)

ft.app(main)

