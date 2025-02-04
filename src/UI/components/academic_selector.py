import sys
import flet as ft
import time as tm


# Importar otros módulos necesarios
# Asegúrate de que los módulos en "tests/Logic/" existen antes de usarlos.

class ListViewPCG():
    def __init__(self, pcg):
        name = pcg.name  # Changed "nombre" to "name" for consistency with English
        pb = ft.ProgressBar(width=400)
        total_workload = sum([subject.hours_distribution.total() for subject in pcg.subjects])  # Assuming 'materias' is 'subjects'
        remaining_workload = sum([subject.hours_distribution.remaining() for subject in pcg.get_subjects()])

        pb.value = 1 - remaining_workload / total_workload if total_workload != 0 else 1

        container = ft.Row(
            controls = [
                ft.Text(name),
                pb
            ],
            spacing=40
        )

        self.container = container
        self.pcg = pcg
        self.progressbar = pb

    def update(self):
        pcg = self.pcg
        total_workload = sum([subject.workload.total for subject in pcg.subjects])
        remaining_workload = sum([subject.workload.remaining for subject in pcg.subjects])

        self.progressbar.value = remaining_workload / total_workload

    
class ElementSearch():
    
    def __init__(self, pgas: list, functions):
        controls = []

        def close_anchor(e):
            self.search_bar.close_view("Juan de Jesus Venegas Flores")
            self.search_bar.update()

        def handle_change(e):
            value = self.search_bar.value
            self.search_value(value)
            self.search_bar.value = value
            self.search_bar.update()

        def handle_submit(e):
            self.reset_values()

        def handle_tap(e):
            self.reset_values()

        def execute_function(e):
            func = e.control.data[1]
            func()
            self.search_bar.close_view()

        # Initialize controls for the search
        for (pga, func) in zip(pgas, functions):
            list_view = ListViewPCG(pga)
            controls.append(ft.ListTile(
                title=list_view.container, 
                on_click=lambda e: execute_function(e),
                data=(pga.name, func)
            ))

        self.controls = controls
        
        search_bar = ft.SearchBar(
            divider_color=ft.colors.BLUE,
            bar_hint_text="Search",
            view_hint_text="Name",
            on_submit=handle_change,
            on_tap=handle_tap,
            view_elevation=4,
            controls=controls,
            width=700,
            height=50
        )
        
        self.search_bar = search_bar

    def change_behavior(self, pga, f):
        self.function_dict[pga] = f
        self.update_behavior()

    def update_controls(self, value):
        self.search_bar.close_view()
        self.search_bar.update()
        tm.sleep(0.1)  # Assuming tm is time, can import time if needed
        self.search_bar.open_view()
        self.value = value
        self.search_bar.update()

    def execute_function(self, pga):
        f = self.function_dict[pga.key]
        self.search_bar.close_view()

    def search_value(self, value):
        if value == "":
            self.reset_values()
            return None

        new_controls = []
        for control in self.controls:
            if value.lower() in control.data[0].lower():
                new_controls.append(control)
        self.search_bar.controls = new_controls
        self.update_controls(value)

    def reset_values(self):
        self.search_bar.controls = self.controls
        self.update_controls("")

class Selector(ft.Container):

    def __init__(self, options):
        # Create a TextButton to display the selected value
        text_button = ft.TextButton(
            text=""
        )

        # Define a function to change the text of the button
        def change_text(value):
            text_button.text = value
            text_button.update()

        # Initialize the list of functions
        functions = []

        # Loop through the provided `options` and append corresponding functions
        for option in options:
            # Capture the current value of `option` using a default value for the lambda function
            functions.append(lambda o=option: change_text(o.name))

        # Create the ElementSearch instance with the list of `options` and functions
        search_view = ElementSearch(options, functions)

        # Create a vertical column layout with the search bar and text button
        column = ft.Column(controls=[search_view.search_bar, text_button])

        # Store the container as an attribute
        super().__init__(
            column,
            expand = False,
            ink = True
        )
#buscador = Selector(Bd.professors.get())

