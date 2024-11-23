
import sys


sys.path.append("/home/juandejesus/Escritorio/Programacion/Proyectos/Horarios/Software/Pruebas")

import flet as ft
from tests_3 import BD
import time as tm 

class Listview_pga():
    def __init__(self, pga):
        nombre = pga.nombre
        pb = ft.ProgressBar(width=400)
        carga_total = sum([materia.composicion_horas.total() for materia in pga.materias])
        carga_faltante = sum([materia.composicion_horas.faltantes() for materia in pga.materias])

        pb.value = 1 - carga_faltante / carga_total if carga_total != 0 else 1

        contenedor = ft.Row(
            controls = [
                ft.Text(nombre),
                pb
            ],
            spacing=40
        )

        self.contenedor = contenedor
        self.pga = pga
        self.progressbar = pb


    def update(self):
        pga = self.pga
        carga_total = sum([materia.composicion_horas.total for materia in pga.materias])
        carga_faltante = sum([materia.composicion_horas.faltante for materia in pga.materias])

        self.progressbar.value = carga_faltante / carga_total

    


class BusquedaElementos():

    def __init__(self, pgas : list, funciones):
        controles = []

        def close_anchor(e):
            self.barra_busqueda.close_view("Juan de Jesus Venegas Flores")
            self.barra_busqueda.update()

        def handle_change(e):
            valor = self.barra_busqueda.value 
            self.search_value(valor)
            self.barra_busqueda.valor = valor
            self.barra_busqueda.update()

        def handle_submit(e):
            self.reiniciar_valores()


        def handle_tap(e):
            self.reiniciar_valores()


        def hola(e):
            f = e.control.data[1]
            f()
            self.barra_busqueda.close_view()

        c = 0
        for (pga, func) in zip(pgas, funciones):
            listview = Listview_pga(pga)
            controles.append(ft.ListTile(title=listview.contenedor, 
                                         on_click = lambda e : hola(e),
                                         data = (pga.nombre, func)
                                         )
                            )
            c = c + 1
            

        self.controles = controles
    
        barra_busqueda = ft.SearchBar(
            divider_color=ft.colors.BLUE,
            bar_hint_text="Buscar",
            view_hint_text="Nombre",
            on_submit=handle_change,
            on_tap=handle_tap,
            view_elevation=4,
            controls = controles,
            width=700,
            height=50)
        
        self.barra_busqueda = barra_busqueda


    def cambiar_comportamiento(self, pga, f):
        self.dict_func_pga[pga] = f
        self.update_comportamiento()


    def update_controls(self, valor):
        self.barra_busqueda.close_view()
        self.barra_busqueda.update()
        tm.sleep(0.1)
        self.barra_busqueda.open_view()
        self.value = valor
        self.barra_busqueda.update()

    def ejecutar_funcion(self, pga):
        f = self.dict_pga[pga.key]
        f
        print(pga.nombre)
        self.barra_busqueda.close_view()

    def search_value(self, valor):
        if valor == "":
            self.reiniciar_valores()
            return None
    
        nuevos_controles = []
        for control in self.controles:
            print(valor)
            if valor.lower() in control.data[0].lower():
                nuevos_controles.append(control)
        self.barra_busqueda.controls = nuevos_controles
        self.update_controls(valor)

    def reiniciar_valores(self):
        self.barra_busqueda.controls = self.controles
        self.update_controls("")




class seleccionador():

    def __init__(self, pgas):


        texto = ft.TextButton(
            text = ""
        )

        def cambiar(valor):
            texto.text = valor
            texto.update()

        funciones = []

        for pga in pgas:
        # Capturar el valor actual de `profesor` usando un valor predeterminado
            funciones.append(lambda p=pga: cambiar(p.nombre))

        lv = BusquedaElementos(pgas, funciones)

        fila = ft.Column(controls = [lv.barra_busqueda,
                texto])
        self.contenedor = fila 



buscador = seleccionador(BD.profesores.get())


