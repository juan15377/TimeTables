import flet as ft
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)

from src.Logic.Bd import BD
from src.GUI.EnrouterPage import EnrouterPage
from src.Logic.Professor_Classroom_Group import *
from src.GUI.MainPage.professor_page_group_pages import *
from src.GUI.Professors_classrooms_groups_pages.prof_class_gro_pages import *


def get_file_path(page):
    """
    Muestra un diálogo para seleccionar un archivo y devuelve la ruta seleccionada.

    Args:
        page: Página de Flet que contiene la interfaz.

    Returns:
        str: La ruta del archivo seleccionado o None si se cancela.
    """
    # Variable para almacenar la ruta seleccionada
    file_path = {"value": None}

    # Manejar el resultado del diálogo de selección de archivo
    def get_file_result(e: FilePickerResultEvent):
        file_path["value"] = e.files[0].path if e.files else None
        page.update()

    # Crear el diálogo de selección de archivo
    get_file_dialog = FilePicker(on_result=get_file_result)

    # Agregar el diálogo al overlay de la página
    if get_file_dialog not in page.overlay:
        page.overlay.append(get_file_dialog)
        page.update()

    # Mostrar el diálogo
    get_file_dialog.pick_files()

    # Esperar hasta que el diálogo se cierre
    while file_path["value"] is None:
        pass  # Esperar hasta que se actualice el valor

    return file_path["value"]

from flet import FilePicker, FilePickerResultEvent

def get_save_file_path(page):
    """
    Muestra un diálogo para seleccionar una ubicación y un nombre para guardar un archivo.

    Args:
        page: Página de Flet que contiene la interfaz.

    Returns:
        str: La ruta del archivo especificado o None si se cancela.
    """
    # Variable para almacenar la ruta seleccionada
    file_path = {"value": None}

    # Manejar el resultado del diálogo de guardar archivo
    def save_file_result(e: FilePickerResultEvent):
        file_path["value"] = e.path if e.path else None
        page.update()

    # Crear el diálogo de guardar archivo
    save_file_dialog = FilePicker(on_result=save_file_result)

    # Agregar el diálogo al overlay de la página
    if save_file_dialog not in page.overlay:
        page.overlay.append(save_file_dialog)
        page.update()

    # Mostrar el diálogo para guardar archivo
    save_file_dialog.save_file()

    # Esperar hasta que el diálogo se cierre
    while file_path["value"] is None:
        pass  # Esperar hasta que se actualice el valor

    return file_path["value"]


def get_save_directory_path(page):
    """
    Muestra un diálogo para seleccionar un directorio y devuelve la ruta seleccionada.

    Args:
        page: Página de Flet que contiene la interfaz.

    Returns:
        str: La ruta del directorio seleccionado o None si se cancela.
    """
    # Variable para almacenar la ruta seleccionada
    directory_path = {"value": None}

    # Manejar el resultado del diálogo de selección de directorio
    def get_directory_result(e: FilePickerResultEvent):
        directory_path["value"] = e.path if e.path else None
        page.update()

    # Crear el diálogo de selección de directorio
    get_directory_dialog = FilePicker(on_result=get_directory_result)

    # Agregar el diálogo al overlay de la página
    if get_directory_dialog not in page.overlay:
        page.overlay.append(get_directory_dialog)
        page.update()

    # Mostrar el diálogo
    get_directory_dialog.get_directory_path()

    # Esperar hasta que el diálogo se cierre
    while directory_path["value"] is None:
        pass  # Esperar hasta que se actualice el valor

    return directory_path["value"]



from flet import FilePicker, FilePickerResultEvent, TextField, AlertDialog, Text, ElevatedButton

from flet import FilePicker, FilePickerResultEvent, TextField, AlertDialog, Text, ElevatedButton

def get_save_directory_and_filename(page):
    """
    Muestra un diálogo para seleccionar un directorio y luego solicita un nombre para el archivo.

    Args:
        page: Página de Flet que contiene la interfaz.

    Returns:
        tuple: Una tupla con la ruta seleccionada y el nombre del archivo (ruta, nombre) o None si se cancela.
    """
    # Variables para almacenar el directorio y el nombre del archivo
    directory_path = {"value": None}
    file_name = {"value": None}

    # Manejar el resultado del diálogo de selección de directorio
    def get_directory_result(e: FilePickerResultEvent):
        directory_path["value"] = e.path if e.path else None
        if directory_path["value"]:
            # Mostrar diálogo para pedir el nombre del archivo
            page.dialog = name_dialog
            page.dialog.open = True
            page.update()

    # Crear el diálogo de selección de directorio
    get_directory_dialog = FilePicker(on_result=get_directory_result)

    # Crear el cuadro de diálogo para pedir el nombre del archivo
    name_field = TextField(label="Nombre del archivo", hint_text="Introduce el nombre del archivo sin extensión")

    def save_name(e):
        file_name["value"] = name_field.value.strip()
        if file_name["value"]:
            name_dialog.open = False
            page.update()

    name_dialog = AlertDialog(
        title=Text("Introduce el nombre del archivo"),
        content=name_field,
        actions=[
            ElevatedButton("Guardar", on_click=save_name),
            ElevatedButton("Cancelar", on_click=lambda e: close_dialog()),
        ],
    )

    def close_dialog():
        name_dialog.open = False
        directory_path["value"] = None  # Cancelar todo si el usuario no introduce el nombre
        page.update()

    # Agregar el FilePicker al overlay de la página
    if get_directory_dialog not in page.overlay:
        page.overlay.append(get_directory_dialog)
        page.update()

    # Mostrar el diálogo para seleccionar el directorio
    get_directory_dialog.get_directory_path()  # Método correcto

    # Esperar hasta que ambos valores sean proporcionados
    while directory_path["value"] is None or file_name["value"] is None:
        pass  # Esperar hasta que se seleccionen ambos valores

    if directory_path["value"] and file_name["value"]:
        return directory_path["value"], file_name["value"]
    return None


def preload_database(page):
    pass

# cada vez que se reinicia la base de datos, o se carga se deben, crear 6 paginas nuevas con 
# sus ciertas referencias
class Pages():
    
    def __init__(self,
                        professors_page,
                        classrooms_page,
                        groups_page):

    
        self.professors_page = professors_page
        self.classrooms_page = classrooms_page
        self.groups_page = groups_page
        
# falta un boton para regresar a la pagina principal

class MainPage():
    
    
    def __init__(self, bd, page) -> None:

        # Contenido inicial de cada sección
        
        def change_to_mainpage():
            enrouter_page.main_page = main_page
            enrouter_page.change_page('/')
            professor_page.update()
            classroom_page.update()
            group_page.update()
            page.update()
            
            
        def reference_to_add_subject_professors():
            enrouter_page.navigate_to_new_subject(lambda : enrouter_page.change_page("/PROFESSORS"))
            
        def reference_to_add_subject_classrooms():
            enrouter_page.navigate_to_new_subject(lambda :enrouter_page.change_page('/CLASSROOMS'))
            
        def reference_to_add_subject_groups():
            enrouter_page.navigate_to_new_subject(lambda : enrouter_page.change_page('/GROUPS'))
        
        professors_page = ProfessorsPage(bd, change_to_mainpage, reference_to_add_subject_professors)
        classrooms_page = ClassroomsPage(bd, change_to_mainpage, reference_to_add_subject_classrooms)
        groups_page = GroupsPage(bd, change_to_mainpage, reference_to_add_subject_groups)  
        

        pages = Pages(
            professors_page,
            classrooms_page,
            groups_page
        )
        
        enrouter_page = EnrouterPage(page, pages, bd)
        self.page = page
        self.bd = bd
        
        
        function_reference_change_to_page = enrouter_page.change_page
        professor_page = ProfesorMainPage(bd, function_reference_change_to_page)
        classroom_page = ClassroomMainPage(bd, function_reference_change_to_page)
        group_page = GroupMainPage(bd, function_reference_change_to_page)
        
        
        
        content = ft.Container(
            content= ft.Column([professor_page], alignment=ft.MainAxisAlignment.START, expand=True,
                        height=800,
                        width=600
                        ), 
            expand=True)


        # Callback para manejar los cambios de la NavigationRail
        def on_change(e):
            
            selected_index = e.control.selected_index
            
            # Cambiar el contenido basado en la selección
            if selected_index == 0:  # Profesor
                content.content = ft.Column([professor_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            height=800,
                                            width=600)
                professor_page.update()

            elif selected_index == 1:  # Aula
                content.content = ft.Column([classroom_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            height=800,
                                            width=600)
                classroom_page.update()

            elif selected_index == 2:  # Grupo
                content.content = ft.Column([group_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            height=800,
                                            width=60)
                group_page.update()

            content.update()        
            # Actualizar la página
            
            
        def cargar_base_datos():
            file_path =  get_file_path(self.page)
            bd.load_db(file_path)
            self.restart()
            professor_page.update()
            classroom_page.update()
            group_page.update()
            
        def guardar_base_de_datos():
            save_path = get_save_file_path(self.page)
            bd.save_db(save_path)
            
        def imprimir_horario():
            save_path = get_save_file_path(self.page)
            bd.generate_pdf(save_path)
            
            

        # Barra de navegación
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            leading=ft.Column(
                    controls = [ft.FloatingActionButton(icon=ft.icons.DATA_OBJECT, 
                                            text="Print",
                                            on_click = lambda e: imprimir_horario()),
                                ft.FloatingActionButton(icon=ft.icons.SAVE, 
                                            text="Guargar",
                                            on_click = lambda e: guardar_base_de_datos()),
                                ft.FloatingActionButton(icon=ft.icons.CHARGING_STATION, 
                                            text="Cargar",
                                            on_click = lambda e: cargar_base_datos())
                    ]
                    ),
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

        # Layout principal
        
        main_page = ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    content,  # Contenedor dinámico
                ],
                expand=True,
            )
        page.add(
            main_page
        )
        
    def restart(self):
        bd = self.bd 
        page = self.page
        
        def change_to_mainpage():
            enrouter_page.main_page = main_page
            enrouter_page.change_page('/')
            professor_page.update()
            classroom_page.update()
            group_page.update()
            page.update()
            
            
            
        def reference_to_add_subject_professors():
            enrouter_page.navigate_to_new_subject(lambda : enrouter_page.change_page("/PROFESSORS"))
            
        def reference_to_add_subject_classrooms():
            enrouter_page.navigate_to_new_subject(lambda :enrouter_page.change_page('/CLASSROOMS'))
            
        def reference_to_add_subject_groups():
            enrouter_page.navigate_to_new_subject(lambda : enrouter_page.change_page('/GROUPS'))
        
        professors_page = ProfessorsPage(bd, change_to_mainpage, reference_to_add_subject_professors)
        classrooms_page = ClassroomsPage(bd, change_to_mainpage, reference_to_add_subject_classrooms)
        groups_page = GroupsPage(bd, change_to_mainpage, reference_to_add_subject_groups)  
        

        pages = Pages(
            professors_page,
            classrooms_page,
            groups_page
        )
        
        enrouter_page = EnrouterPage(page, pages, bd)
        self.page = page
        self.bd = bd
        
        
        function_reference_change_to_page = enrouter_page.change_page
        professor_page = ProfesorMainPage(bd, function_reference_change_to_page)
        classroom_page = ClassroomMainPage(bd, function_reference_change_to_page)
        group_page = GroupMainPage(bd, function_reference_change_to_page)
        
        
        
        content = ft.Container(
            content= ft.Column([professor_page], alignment=ft.MainAxisAlignment.START, expand=True,
                        height=800,
                        width=600
                        ), 
            expand=True)


        # Callback para manejar los cambios de la NavigationRail
        def on_change(e):
            
            selected_index = e.control.selected_index
            
            # Cambiar el contenido basado en la selección
            if selected_index == 0:  # Profesor
                content.content = ft.Column([professor_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            height=800,
                                            width=600)
                professor_page.update()

            elif selected_index == 1:  # Aula
                content.content = ft.Column([classroom_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            height=800,
                                            width=600)
                classroom_page.update()

            elif selected_index == 2:  # Grupo
                content.content = ft.Column([group_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            height=800,
                                            width=60)
                group_page.update()

            content.update()        
            # Actualizar la página
            
            
        def cargar_base_datos():
            file_path =  get_file_path(self.page)
            bd.load_db(file_path)
            self.restart()
            professor_page.update()
            classroom_page.update()
            group_page.update()
            
        def guardar_base_de_datos():
            save_path = get_save_file_path(self.page)
            bd.save_db(save_path)
            
        def imprimir_horario():
            save_path = get_save_file_path(self.page)
            bd.generate_pdf(save_path)
            
            

        # Barra de navegación
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            leading=ft.Column(
                    controls = [ft.FloatingActionButton(icon=ft.icons.DATA_OBJECT, 
                                            text="Print",
                                            on_click = lambda e: imprimir_horario()),
                                ft.FloatingActionButton(icon=ft.icons.SAVE, 
                                            text="Guargar",
                                            on_click = lambda e: guardar_base_de_datos()),
                                ft.FloatingActionButton(icon=ft.icons.CHARGING_STATION, 
                                            text="Cargar",
                                            on_click = lambda e: cargar_base_datos())
                    ]
                    ),
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

        # Layout principal
        
        main_page = ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    content,  # Contenedor dinámico
                ],
                expand=True,
            )
        page.controls.clear()
        
        page.add(main_page)
        page.update()


        
# al momento de eliminar una materia todos los bloques que se colocaron dentro de el deben actualizarse



def main(page: ft.Page):
    
    Bd = BD()
    
    MainPage(Bd, page)


ft.app(main)


# ? arreglar el problema de deslizamiento hacia abajo
# ! arreglar el caso de un tablero cuando no se tiene matterias
# ! arreglar el problema cuando no hay profesores, aulao grupos

