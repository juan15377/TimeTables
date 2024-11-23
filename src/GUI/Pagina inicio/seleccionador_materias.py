import flet as ft 
from tests_3 import BD
from colores import triada_a_hex

class CargarMateria():

    def __init__(self, pga, materia, tablero):
        self.materia = materia
        self.tablero = tablero
        self.pga = pga

        def buscar_opcion(nombre):
            for option in  vbloque_drop.options:
                if nombre == option.key:
                    return option
            return None

        bloques = materia.composicion_horas.get_bloques_disponibles()
        self.bloques = bloques

        vbloque_drop = ft.Dropdown(
            options = [
                ft.dropdown.Option(str(bloque))
                for bloque in bloques
            ],
            width = 100
        )
        self.vbloques_drop = vbloque_drop
        self.pos = 0
        self.vbloques_drop.value = 0

        def up_valor(self):

            self.pos = (self.pos + 1) % len(self.bloques)

            nuevo_valor = str(self.bloques[self.pos])
            #print(self.pos)
            self.vbloques_drop.value = nuevo_valor
            self.vbloques_drop.update()
            self.seleccion_de_bloques.update()

        def down_valor(self):
            self.pos = (self.pos - 1) % len(self.bloques)
            
            nuevo_valor = str(self.bloques[self.pos])
            if nuevo_valor == None :
                self.down_valor()

            self.vbloques_drop.value = nuevo_valor
            self.vbloques_drop.update()
            self.seleccion_de_bloques.update()


        boton_arriba = ft.IconButton(
                    icon=ft.icons.ARROW_UPWARD,
                    icon_color="blue400",
                    icon_size=20,
                    tooltip="Pause record",
                    on_click = lambda e : up_valor(self),
                    width=80
                    ) 
        
        boton_abajo = ft.IconButton(
                    icon=ft.icons.ARROW_DOWNWARD,
                    icon_color="blue400",
                    icon_size=20,
                    tooltip="Play record",
                    on_click=lambda e : down_valor(self),
                    width = 80
                    )
        
        seleccion_de_bloques = ft.Column(
            controls = [
                boton_arriba,
                vbloque_drop,
                boton_abajo
            ],
            width= 80,
            height= 100
        )

        def cargar_materia():
            tamaño = int(float(self.vbloques_drop.value) * 2) 
            if tamaño == 0:
                return None
            self.tablero.cargar_disponibilidad(tamaño, self.materia)

        self.seleccion_de_bloques = seleccion_de_bloques
        color_original = pga.colores_materias.color[materia]

        cont_MATERIA = ft.Container(content= ft.Text(materia.abreviatura,
                                    size= 35, color = ft.colors.BLACK),
                                    width=150,
                                    height=100,
                                    alignment=ft.alignment.center,
                                    bgcolor= triada_a_hex(color_original),
                                    padding=0,
                                    margin = ft.Margin(top=0, right=0, bottom=0, left=0),
                                    border_radius=5,
                                    on_click= lambda e : cargar_materia(),
                                    ink=True)
        

        self.cont_MATERIA = cont_MATERIA
        self.contenido = ft.Row(
            controls = [
                self.seleccion_de_bloques,
                self.cont_MATERIA
            ]
        )
        
    def actualizar_materia(self, materia):
        nuevo_color = self.pga.colores_materias.color[materia]
        nuevo_nombre = materia.abreviatura 
        self.cont_MATERIA.content = ft.Text(nuevo_nombre,
                                    size=35, color = ft.colors.BLACK)
        
        self.cont_MATERIA.bgcolor = triada_a_hex(nuevo_color)
        self.materia = materia 
        self.contenido.update()
        self.update_bloques()



    def update_bloques(self):
        bloques = self.materia.composicion_horas.get_bloques_disponibles()
        self.vbloques_drop.options.clear()
    
        for bloque in bloques:
            self.vbloques_drop.options.append(ft.dropdown.Option(str(bloque)))
        
        self.pos = 0 
        self.vbloques_drop.value = bloques[0] 
        self.bloques = bloques 
        self.vbloques_drop.update()
        self.seleccion_de_bloques.update()






class SeleccionadorMaterias():

    def __init__(self, pga, tablero):
        self.pga = pga
        materia_0 = pga.get_materias()[0]
        cargador_materia = CargarMateria(pga, materia_0, tablero)
        self.cargador_materia = cargador_materia

        self.cargar_lista_materias()

    def update(self):
        self.lista_materias.controls.clear()
        self.agregar_materias_lista()
        self.cargador_materia.update_bloques()
        materia = self.cargador_materia.materia 
        self.cargador_materia.actualizar_materia(materia)
        self.lista_materias.update()

    def agregar_materias_lista(self):

        for materia in self.pga.get_materias():
            barra_com = ft.ProgressBar(width = 150, height = 10)
            valor_completado =  1 - materia.faltantes() / materia.total()
            barra_com.value = valor_completado
            color = triada_a_hex(self.pga.colores_materias.color[materia])
            text_nombre = ft.Container(
                content = ft.Text(materia.abreviatura, size = 20, expand = True, color = ft.colors.BLACK),
                bgcolor= color,
                width=100,
                height=30,
                padding=0,
                margin=ft.Margin(top=0, right=0, bottom=0, left=0),
                border_radius=5,
                alignment= ft.alignment.center
                )
            
            cont_mat = ft.Container(
                content= ft.Row(controls = [
                    text_nombre,
                    ft.Text("    "),
                    barra_com
                ]),
                on_click= lambda e, m = materia : self.cargador_materia.actualizar_materia(m),
                #on_hover= lambda e : pintar(e),
                ink = True,
                ink_color= "blue40",
                    )
            self.lista_materias.controls.append(cont_mat)


    def cargar_lista_materias(self):

        lista_materias = ft.Column(spacing=10, alignment=ft.alignment.top_center,
                                   height= 300,
                                   width= 300,
                                   scroll= ft.ScrollMode.AUTO)
        self.lista_materias = lista_materias


        self.agregar_materias_lista()

        

        contenido =ft.Column( 
            controls = [self.lista_materias,
                        self.cargador_materia.contenido]
                        
            )
        self.contenido = contenido




