import flet as ft

from TMaterias import boardsubject
from TMaterias import initialize_control_board



def main(page: ft.Page):
    appbar_text_ref = ft.Ref[ft.Text]()

    def handle_menu_item_click(e):
        print(f"{e.control.content.value}.on_click")
        appbar_text_ref.current.value = e.control.content.value
        page.update()

    def handle_submenu_open(e):
        print(f"{e.control.content.value}.on_open")

    def handle_submenu_close(e):
        print(f"{e.control.content.value}.on_close")

    def handle_submenu_hover(e):
        print(f"{e.control.content.value}.on_hover")

    page.appbar = ft.Container(
        content= ft.Text("puto el que lo lea")
    )
    
    
    ft.AppBar(
        title=ft.Text("Menus", ref=appbar_text_ref),
        center_title=True,
        bgcolor=ft.colors.BLUE,
    )

    menubar = ft.MenuBar(
        expand=True,
        style=ft.MenuStyle(
            alignment=ft.alignment.top_left,
            mouse_cursor={

            },
        ),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("File"),
                on_open=handle_submenu_open,
                on_close=handle_submenu_close,
                on_hover=handle_submenu_hover,
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("About"),
                        leading=ft.Icon(ft.icons.INFO),
                        style=ft.ButtonStyle(
                        ),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Save"),
                        leading=ft.Icon(ft.icons.SAVE),
                        style=ft.ButtonStyle(
                        ),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Quit"),
                        leading=ft.Icon(ft.icons.CLOSE),
                        style=ft.ButtonStyle(
                        ),
                        on_click=handle_menu_item_click,
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("View"),
                on_open=handle_submenu_open,
                on_close=handle_submenu_close,
                on_hover=handle_submenu_hover,
                controls=[
                    ft.SubmenuButton(
                        content=ft.Text("Zoom"),
                        controls=[
                            ft.MenuItemButton(
                                content=ft.Text("Magnify"),
                                leading=ft.Icon(ft.icons.ZOOM_IN),
                                close_on_click=False,
                                style=ft.ButtonStyle(

                                ),
                                on_click=handle_menu_item_click,
                            ),
                            ft.MenuItemButton(
                                content=ft.Text("Minify"),
                                leading=ft.Icon(ft.icons.ZOOM_OUT),
                                close_on_click=False,
                                style=ft.ButtonStyle(
                                ),
                                on_click=handle_menu_item_click,
                            ),
                        ],
                    )
                ],
            ),
        ],
    )

    page.add(ft.Row([menubar]))


#ft.app(main)

a,grid,b = initialize_control_board()


class TabsProfessorClassroomGroup(ft.Container):
    
    def __init__(self, bd):
        t = ft.Tabs(
            expand = True,
            selected_index=1,
            animation_duration=200,
            tabs=[
                ft.Tab(
                    text="Professor",
                    content=ft.Container(
                        content = ft.Container(
                            content = boardsubject,
                            alignment=ft.alignment.center,
                            margin=100,
                            expand = True
                        ),
                        margin= 100,
                        expand = False,
                        adaptive=True
                    ),

                ),
                ft.Tab(
                    text = "Classroom",
                    #tab_content=ft.Icon(ft.icons.SEARCH),
                    content = grid
                ),
                ft.Tab(
                    text="Group",
                    #icon=ft.icons.SETTINGS,
                    content=boardsubject
                ),
            ],
        )
        
        super().__init__(content=t)
        
    
    pass  

import flet as ft

def main(page: ft.Page):
    # Contenido inicial de cada sección
    content = ft.Container(content=ft.Text("Bienvenido, selecciona una opción"), expand=True)

    # Callback para manejar los cambios de la NavigationRail
    def on_change(e):
        selected_index = e.control.selected_index

        # Cambiar el contenido basado en la selección
        if selected_index == 0:  # Profesor
            content.content = ft.Column([ boardsubject], alignment=ft.MainAxisAlignment.START, expand=True,
                                        height=800,
                                        width=600)
        elif selected_index == 1:  # Aula
            content.content = ft.Text("Vista de Aula")
        elif selected_index == 2:  # Grupo
            content.content = ft.Text("Vista de Grupo")
        content.update()        
        # Actualizar la página

    # Barra de navegación
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.FAVORITE_BORDER,
                selected_icon=ft.icons.FAVORITE,
                label="Profesor",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                label="Aula",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("Grupo"),
            ),
        ],
        on_change=on_change,  # Llamar al callback
    )
    
    page.theme_mode = ft.ThemeMode.DARK 

    # Layout principal
    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                content,  # Contenedor dinámico
            ],
            expand=True,
        )
    )

ft.app(main)

import flet as ft

def main(page: ft.Page):

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=100,
        min_extended_width=400,
        leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.FAVORITE_BORDER, selected_icon=ft.icons.FAVORITE, label="Profesor"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                label="Aula",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("Grupo"),
            ),
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
    )

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Column([ boardsubject], alignment=ft.MainAxisAlignment.START, expand=True,
                          height=800,
                          width=600),
            ],
            expand=True,
        )
    )


# ! arreglar el problema de deslizamiento hacia abajo
# ! arreglar el caso de un tablero cuando no se tiene matterias
# ! arreglar el problema cuando no hay profesores, aulao grupos

