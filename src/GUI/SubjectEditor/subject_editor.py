import sys
import flet as ft

        
from src.GUI.SubjectEditor.name_and_code import NameCodeSubject
from src.GUI.SubjectEditor.groups_selector import GroupSelector
from src.GUI.Utils.SearchValue import SearchValue
from src.GUI.SubjectEditor.hours_distribution import SelectorDistributionHours
from src.GUI.SubjectEditor.online_switch import OnlineSwitch
from src.Logic.Subjects import InfoSubject


class NavigatorBarBack(ft.Container):
    
    def __init__(self, funct_to_back):

        pagelet = ft.Pagelet(
            appbar=ft.AppBar(
                leading=ft.IconButton(icon = ft.icons.ARROW_BACK, 
                                    on_click = lambda e: funct_to_back()),
                leading_width=50,
                title=ft.Text(""),
                center_title=False,
                bgcolor=ft.colors.SURFACE_VARIANT,
                actions=[
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="Item 1"),
                            ft.PopupMenuItem(),  # divider
                            ft.PopupMenuItem(
                                text="Checked item",
                                checked=False,
                            ),
                        ]
                    ),
                ],
            ),
            content=ft.Container(),
            expand=True
        )
            
        
        super().__init__(
            content = pagelet,
            height=50,
            width=100,
            expand = True
        )
        

class Alert():
    
    def __init__(self, alert : str, page):
        self.page = page
        self.alert = alert
        
        def show_alert():
            # Configurar el contenido del diálogo
            alert = ft.AlertDialog(
                title=ft.Text("¡Error!"),
                content=ft.Text(self.alert),
                actions=[
                    ft.TextButton("Aceptar", on_click= lambda e : self.close_alert()),
                    ft.TextButton("Cancelar", on_click= lambda e : self.close_alert()),
                ],
            )
            # Mostrar el diálogo
            page.dialog = alert
            alert.open = True
            page.update()

            def cerrar_alerta(e):
                # Cerrar el diálogo
                page.dialog.open = False
                page.update()

        self.show_alert = show_alert

    def show(self):
        self.show_alert()
        
    def close_alert(self):
        self.page.dialog.open = False
        self.page.update()

class Data:
    def __init__(self) -> None:
        self.counter = 0

class AlertNewSubject():
    
    def __init__(self, page):
        d = Data()
        page.snack_bar = ft.SnackBar(
        content=ft.Text("New Subject Created"),
        action="Alright!",
        )
    
        
        def on_click():
            page.snack_bar = ft.SnackBar(ft.Text(f"New Subject Created"),
                                         bgcolor=ft.colors.GREEN_200)
            page.snack_bar.open = True
            d.counter += 1
            page.update()
        
        self.show = lambda : on_click()
        

# esta clase tiene dos objectivos, que carguen los datos de una materia y desde este se puedan editar estos
# otro es que esta clase tiene es que sea capaz de crear una nueva materia 

def is_avaible_subject(professor, classroom, groups, hours_distribution, is_online, page):
    
    if professor == None:
        alert = Alert("No se ah seleccionado el professor", page)
        alert.show()
        return False
    if classroom == None and not is_online:
        alert = Alert("No se ah seleccionado el Aula correctamente", page)
        alert.show()
        return False 
    if groups == []:
        alert = Alert("No se ah seleccionado ningun Grupo", page)
        alert.show()
        return False
    if sum(hours_distribution. get_avaible_hours()) == 0:
        alert = Alert("La seleccion de distribuccion de horas es incorrecta", page)
        alert.show()
        return False
    if is_online:
        return True
    if classroom == None:
        return False
    return True
    



class SubjectEditor(ft.Container):
    
    def __init__(self, bd, reference_page_router, page, subject = False):
        self.bd = bd
        self.page = page
        
        self.show_to_new_subject = lambda e : AlertNewSubject(self.page).show()
        
        name_code_subject = NameCodeSubject("", "")
        self.name_code_subject = name_code_subject
        name_code_subject.spacing = 50
        
        groups_selector = GroupSelector(bd)
        self.groups_selector = groups_selector
        
        
        
        def get_actual_professors():
            return {
            professor.name:professor for professor in self.bd.professors.get()
        }
        
        professor_selector = SearchValue({
                    professor.name:professor for professor in bd.professors.get()
                },
                get_actual_professors                                
        )
        self.professor_selector = professor_selector
        
        
        #professor_selector.width = 400
        
        
        
        def get_actual_classrooms():
            return {classroom.name: classroom for classroom in self.bd.classrooms.get()}
        
        
        classroom_selector = SearchValue(
            {classroom.name: classroom for classroom in bd.classrooms.get()},
            get_actual_classrooms
        )
        
        online_switch = OnlineSwitch(classroom_selector)
        self.online_switch = online_switch
        
        
        #classroom_selector.width = 400
        
        self.classroom_selector = classroom_selector
        # Diseño del sector de aula y de professor 
        #classroom_selector.spacing = 100
        
        selector_hours_distribution = SelectorDistributionHours()
        self.selector_hours_distribution = selector_hours_distribution
    
        
        
        button_new_subject = ft.FloatingActionButton(
            text = "New Subject",
            icon = ft.icons.ADD,
            on_click = lambda e: self.new_subject_in_bd(),
            expand = True
        )
        
        left_layout = ft.Column(
                        controls=[
                            ft.Row(
                                controls = [name_code_subject],
                                expand = False,
                                #width=800,
                                height=100
                                
                            ),
                            groups_selector,
                            #button_new_subject  
                            
                        ],
                        alignment= ft.alignment.top_right,
                        spacing=10,
                        expand=True
                    )
        
        
        right_layout = ft.Column(
            controls = [
                ft.Row(
                    controls = [
                        button_new_subject,
                        online_switch
                    ],
                    height=100
                ),

                ft.Column(
                        controls = [ft.Text("Aula"),
                                    classroom_selector,
                                    ],
                        expand = True,
                        #width = 100,
                        height= 50
                        ),
                ft.Column(
                        controls = [
                            ft.Text("Profesor"),
                            professor_selector,
                        ],
                        expand=True,
                        #width = 100,
                        height= 50
                ),
                selector_hours_distribution,
                #ft.Row(
            ],
            expand = True
        )
        
        
        navigator = NavigatorBarBack(reference_page_router)
        
            
        super().__init__(
            content = ft.Column(
                controls = [
                    ft.Row(
                        controls = [
                            navigator
                        ],
                    ),
                    ft.Row(
                        controls=[
                            left_layout,
                            right_layout,
                        ],
                        expand = True
                    )
                ],
                expand = True
            ),
            expand = True
        )
        
        pass 
    
    def save_changes(self):
        pass
    
    
    def cancel(self):
        #enruting for another page
        pass
    
    
        
    def load_subject(self, subject):
        pass  
    
    
    # encargado de regresar un
    def new_subject_in_bd(self):
        name, code = self.name_code_subject.get_name_and_code()
        groups = self.groups_selector.get_groups()
        professor = self.professor_selector.get_value()
        classroom = self.classroom_selector.get_value()
        hours_distribution = self.selector_hours_distribution.get_hours_distribution()
        is_online = self.online_switch.is_online()
        
        # crear nueva materia en la base de datos
        
        ##if not is_avaible_subject(professor,
         #                     classroom,
         #                     groups,
         #                     hours_distribution,
         #                     is_online):
         #   return None
        
        print("is viable")
        print(is_avaible_subject(
                        professor,
                        classroom,
                        groups,
                        hours_distribution,
                        is_online,
                        self.page
                        )  )
        
        if is_avaible_subject(
                        professor,
                        classroom,
                        groups,
                        hours_distribution,
                        is_online,
                        self.page
                        ):
            
            info_subject = InfoSubject(
                name, 
                code, 
                professor, 
                classroom, 
                groups, 
                hours_distribution,
                is_online,
            )
            
            self.bd.subjects.add(info_subject)
            print("Juan de Jesus Venegas Flores")
            
            # show to create new subject 
            self.show_to_new_subject(1)
            
        
        pass
        
        
    def set_values_subject(self):
        pass 
        
    
#    
#def main(page : ft.page):
#    subject_editor = SubjectEditor(Bd, lambda: print("hola"))
#    page.add(subject_editor)
#    
#ft.app(target=main)
