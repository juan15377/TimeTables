import flet as ft  

from list_selector import ListSelector 
import sys 


sys.path.append("/home/juandejesus/Escritorio/Programacion/Proyectos/Horarios/Software/Pruebas")

from tests_3 import BD  


class TableGroups(ft.Container):

    def __init__(self):
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Carrera")),
                ft.DataColumn(ft.Text("Semestre")),
                ft.DataColumn(ft.Text("Subgrupo")),
                ft.DataColumn(ft.Text("Eliminar")),
                ],
            )
        self.groups = []
        self.table = table


        super().__init__(
            content = ft.Column(
                controls = [table],
                scroll = ft.ScrollMode.ALWAYS,
                on_scroll_interval=0,
                )
        )

    def remove_group(self, group):
        for row_group in self.table.rows:
            if row_group.data == group:
                self.table.rows.remove(row_group) 
        self.groups.remove(group)
        self.table.update()

    
    def add_group(self, group):

        if group in self.groups:
            return None

        self.groups.append(group)
        remove_group_buton = ft.TextButton(
            text = "Eliminar",
            on_click = lambda e, group = group : self.remove_group(group)
        )
        self.table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(group.carrera.nombre)), 
                                                 ft.DataCell(ft.Text(str(group.semestre.nombre))), 
                                                 ft.DataCell(ft.Text(str(group.subgrupo.nombre))),
                                                 ft.DataCell(remove_group_buton)
                                                 ],
                                        data = group,
                                        )
                                )
        self.table.update()


    def get_groups(self):
        return self.groups




class GroupsSelector(ft.Container):

    def __init__(self, BD):

        self.BD = BD 
        self.table_groups = TableGroups()

        carreras = BD.grupos.carreras.get() 
        names_carreras = [carrera.nombre for carrera in carreras]

        carrera_selector = ListSelector(
            ["Todos"] + names_carreras , # este es un valor en el cual permite no escoger ningun elemento con un valor None 
            [None] + carreras 
        )

        semestres = BD.grupos.semestres.get() 

        names_semestres = [semestre.nombre for semestre in semestres] 

        semestre_selector = ListSelector(
            ["Todos"] + names_semestres,
            [None] + semestres
        )

        subgrupos = BD.grupos.subgrupos.get()
        names_subgrupos = [subgrupo.nombre for subgrupo in subgrupos]

        subgrupo_selector = ListSelector(
            ["Todos"] + names_subgrupos,
            [None] + subgrupos
        )

        row_selectors = ft.Column( 
            controls = [carrera_selector,
                        semestre_selector,
                        subgrupo_selector,
                    ]        
                )

        self.carrera_selector = carrera_selector
        self.semestre_selector = semestre_selector
        self.subgrupo_selector = subgrupo_selector


        groups_controls = []

        search_buton = ft.Container(
            content= ft.Text("Buscar", size = 18),
            on_click = lambda e : self.search_groups(self.carrera_selector.get_value(), 
                                                    self.semestre_selector.get_value(), 
                                                    self.subgrupo_selector.get_value()
                                                    ),
            width = 100,
            height = 50,
            ink = True,
            padding = 5,
            margin = 10,
        )

        column_search_groups  = []

        self.column_search_groups = column_search_groups


        for group in self.BD.grupos.get():
            cont_value = ft.Container(
                        content = ft.Text(str(group.carrera.nombre) + " " + str(group.semestre.nombre) + " " + str(group.subgrupo.nombre)),
                        data = group
                    )
            groups_controls.append(ft.ListTile(title=cont_value, 
                                                on_click = lambda e, group = group : self.add_group_to_table(group),
                                                data = group,
                                         )
                                )
        list_view_groups = ft.ListView(
            controls = column_search_groups
        )

        self.list_view_groups = list_view_groups  # guardamos la referencia para actualizarla luego de agregar un grupo a la tabla

        layout_left = ft.Column(
                controls = [row_selectors,
                            search_buton,
                            list_view_groups,
                    ],
                height = 1000,
                width = 300
            )

        layout_right = ft.Container(
                content = self.table_groups,
                height = 300,
                width = 100,
            )

        layout_complete = ft.Row(
            controls = [ layout_left, layout_right ], 
        )


        super().__init__(
            content = layout_complete
        )



    def add_group_to_table(self, group):
        self.table_groups.add_group(group)



    def search_groups(self, carrera, semestre, subgrupo):
        # Buscar grupos que coincidan con los parámetros de búsqueda
        # si la carrera, semestre, subgrupo tiene valor None, entonces 
        # este filtro no se toman en cuenta
        self.column_search_groups.clear()

        for group in self.BD.grupos.get():
            if (carrera is None or carrera == group.carrera) and \
               (semestre is None or semestre == group.semestre) and \
               (subgrupo is None or subgrupo == group.subgrupo):

               self.column_search_groups.append(
                    ft.ListTile(title=ft.Text(str(group.carrera.nombre) + " " + str(group.semestre.nombre) + " " + str(group.subgrupo.nombre)), 
                                             on_click = lambda e, group = group : self.add_group_to_table(group),
                                             data = group,
                                             )
                )
        self.list_view_groups.controls = self.column_search_groups
        self.list_view_groups.update()

    def get_groups(self):
        return self.table_groups.get_groups()



for grupo in BD.grupos.get():
    print(grupo)



def main(page : ft.Page):
    fila = ft.Row(
        controls = [
                GroupsSelector(BD),
        ]
    )

    page.add(
        fila
    )


ft.app(main)