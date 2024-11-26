
# falta una estructura que sea capaz de colocar un buscador sobre un conjunto de estructura como aulas 
# y poder seleccionarlos 

import sys 

sys.path.append("src/Logic/")

import flet as ft 

# todo: se considera que los nnombre son unicos 
class SearchValue(ft.Container):
    
    def __init__(self, dict_values, on_change = lambda:None) -> None:
        
        self.on_change = on_change
        
        values = list(dict_values.values())
        names = list(dict_values.keys())
        
        self.value_selected = None
    
        def change_value(e):
            self.value_selected = dict_values[lv.value]
            self.on_change(e)
            
        def handle_change(e):
            list_to_show = [name for (name, value) in zip(names, values) if e.data.lower() in name.lower()]
            lv.options.clear()
            for i in list_to_show:
                lv.options.append(ft.dropdown.Option(f"{i}")),
            search_entry.update()
            lv.update()
            
        lv = ft.Dropdown(
            on_change= change_value,
            options=[ft.dropdown.Option(name) for name in names]
        )
        
        search_entry = ft.TextField(
            on_change=handle_change,
        )
        
        super().__init__(
            ft.Column(
                controls = [
                    search_entry,
                    lv
                ]
            ),
            expand = False,
            height=100,
            width=600
        )
        
        pass
    
    def get_value(self):
        return self.value_selected
    
    

# def main(page):
    
#     objecto = SearchValue({"1":1,
#                            "2":2,
#                            "3":3,
#                            "4":4,
#                            "5":5,
#                            "6":6,
#                            "7":7,
#                            "8":8,
#                            "9":9,
#                            "10":10})
#     buton_ver = ft.TextButton(
#         text = "hola",
#         on_click= lambda e: print(objecto.get_value())
#     )


#     page.add(
#         ft.Row([
#             objecto,
#             buton_ver
#         ],
#             alignment=ft.MainAxisAlignment.CENTER
#         )
#     )

# ft.app(main)