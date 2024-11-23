import flet as ft
import sys  
import time as tm 
sys.path.append("/home/juandejesus/Escritorio/Programacion/Proyectos/Horarios/Software/Pruebas")
sys.path.append("/home/juandejesus/Escritorio/Programacion/Proyectos/Horarios/Software/Logica Principal")
# objecto encargado de crear una lista 
from tests_3 import BD 
from pga import Profesor, Aula, Grupo

class Encabezado(ft.Container):

    def __init__(self, BD, pga, listviewpga):
        self.BD = BD 
        self.pga = pga
        self.listviewpga = listviewpga


        nombre_pga = pga.nombre
        self.nombre = nombre_pga


        pb = ft.ProgressBar(width=400)
        pb.value = pga.m1.completado()


        def eliminar_pga(pga):

            if type(pga) == Profesor:
                self.BD.profesores.remove(pga)
            elif type(pga) == Aula:
                self.BD.aulas.remove(pga)
            else:
                self.BD.grupos.remove(pga)
            self.listviewpga.update_expansions()
            self.listviewpga.update()

        buton_remove_pga = ft.Container(
                            content = ft.Text("Eliminar"),
                            on_click = lambda e, pga = pga : eliminar_pga(pga) ,
                            bgcolor = ft.colors.RED,
                            width = 70,
                            height = 30,
                            alignment = ft.alignment.center
                            )



        Titulo = ft.Container(
                content = ft.Row(
                    controls = [
                        ft.Text(pga.nombre),
                        pb,
                        ft.Container(
                            content = ft.Text("Eliminar"),
                            on_click = lambda e, pga = pga : eliminar_pga(pga) ,
                            bgcolor = ft.colors.RED,
                            width = 70,
                            height = 30,
                            alignment = ft.alignment.center
                            ),
                        ft.Container(
                            content = ft.Text("Editar"),
                            on_click = lambda e : self.listviewpga.editar(pga),
                            bgcolor = ft.colors.YELLOW,
                            width = 70,
                            height = 30,
                            alignment = ft.alignment.center
                        )           
                    ],
                    spacing = 50
                ),
                height = 50,
                width = 1200,
                border_radius = 10,
            )
        
        super().__init__(
            content = Titulo)



class listviewMaterias(ft.Column):

    def __init__(self, BD, pga, listviewpga):
        self.BD = BD 
        self.listviewpga = listviewpga
        self.pga = pga

        materias = []

        buton_new_materia = ft.TextButton(
            text="Agregar Materia",
            on_click=lambda e: self.añadir_materia(),
            width=200,
            height=30,
        )

        for materia in self.pga.get_materias():
            nombre = materia.nombre 
            progreso = ft.ProgressBar(width=400)
            progreso.value = 1 - materia.faltantes() / materia.total() if materia.total != 0 else 1 
            materia_view = ft.Row(
                controls = [
                    ft.Text(nombre),
                    progreso,
                    ft.Container(content=ft.Text("Detalles"), 
                                 on_click= lambda e, m = materia : self.editar_materia(m)),
                ],
                spacing = 70
            )
            materias.append(materia_view)
            
        super().__init__(
            controls =  [buton_new_materia] + materias, #! falta agregar el boton de añaidr una nueva materia
            alignment = ft.alignment.top_left,
            scroll=ft.ScrollMode.ALWAYS,  # Habilitar el scroll en la columna
            width = 1200,
            height = 300
        )
    
    def editar_materia(self, m):
        # esto debera abirir una ventana nueva donde se pueda editar la informacion de una materia
        pass 

    def añadir_materia(self):
        pass


def filter_expansions(expansions, coincidence):
    # esto debera filtrar las expansiones que coincidan con la coincidencia
    new_expansions = []

    for expansion in expansions:
        if coincidence.lower() in expansion.data.lower(): # en data almacenamos el nombre del pga
            new_expansions.append(expansion)
    return new_expansions


class ListViewPGA(ft.Container):

    def __init__(self, pgas, BD, creating):
        self.BD = BD  
        self.pgas = pgas


        def searchnow(e):
            self.update_expansions()
            print("Cambio valor")
            coincidence = e.control.value
            if coincidence == "":
                self.update()
                return None # no filtra nada
            self.search(coincidence)


        self.update_expansions()

        search_pga = ft.TextField(
                        label="Search now",
                        on_change=searchnow
                    )

        textfield_new_teacher = ft.TextField(
                            label="Nuevo",
                            border=ft.InputBorder.UNDERLINE,
                            filled=True,
                            hint_text="Nombre",
                            max_length = 50
                            )
        
        def add_new(BD):
            name = textfield_new_teacher.value
            creating.new(name)
            textfield_new_teacher.value = ""
            textfield_new_teacher.update()
            # actualizar el componenete añadiendole un nuevo elemento con materias vacias
            self.update_expansions() 
            self.update()
            pass 

        
        buton_new_teacher = ft.TextButton(
                            text = "Agregar",
                            on_click = lambda e, BD = self.BD : add_new(BD),
                            width = 100,
                            height = 30,
                            )

        parte_superior = ft.Row(
            controls = [
                search_pga,
                textfield_new_teacher,
                buton_new_teacher
            ]

        )

        expansions_column = ft.Column(
            controls = self.expansions,
            scroll=ft.ScrollMode.ALWAYS,  # Habilitar el scroll en la columna
            width = 800,
            height = 600,
            )

        super().__init__(
            content = ft.Column(
                controls = [parte_superior] + [expansions_column],
            ),
            width = 1200,
            height = 600,
        )


    def update_expansions(self):
        expansiones = []

        for pga in self.pgas():
            encabezado = Encabezado(self.BD, pga, self)
            list_materias = listviewMaterias(self.BD, pga, self)
            expansion = ft.ExpansionTile(
                            title = encabezado,
                            subtitle= ft.Text("Materias"),
                            affinity=ft.TileAffinity.LEADING,
                            controls=[
                                ft.Container(
                                    content=list_materias,
                                    height=200,  # Fijar una altura para permitir el scroll
                                )
                            ],
                            data = encabezado.nombre
                        )
            expansiones.append(expansion)

        self.expansions = expansiones


    def search(self, coincidence):
        self.expansions = filter_expansions(self.expansions, coincidence)
        self.update()



    def update(self):
        expansiones = self.expansions
        self.content.controls[1] = ft.Column(
                                    controls = expansiones,
                                    scroll=ft.ScrollMode.ALWAYS,  # Habilitar el scroll en la columna
                                    width = 1200,
                                    height = 600,
                                    )
        super().update()
        pass



time_init = tm.time()
objecto_prueba = ListViewPGA(BD.profesores.get, BD, BD.profesores)
time_out = tm.time()


print(f"tiempo tomado = {time_out -  time_init}")


def main(page :ft.page):
    page.add(objecto_prueba) 

ft.app(main) 
