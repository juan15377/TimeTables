
# falta una estructura que sea capaz de colocar un buscador sobre un conjunto de estructura como aulas 
# y poder seleccionarlos 

import sys
sys.path.append("src/Logic/")
import flet as ft

class SearchValue(ft.Container):
    
    def __init__(self, dict_values, reference_get_new_dict, on_change =lambda: None) -> None:
        self.on_change = on_change
        self.reference_get_new_dict = reference_get_new_dict
        
        values = list(dict_values.values())
        names = list(dict_values.keys())
        self.dict_values = dict_values
        self.value_selected = None
    
        def change_value(e):
            self.value_selected = self.dict_values[self.drop.value]
            self.on_change()
            
        def handle_change(e):
            list_to_show = [name for name in names if e.data.lower() in name.lower()]
            self.drop.options.clear()
            for name in list_to_show:
                self.drop.options.append(ft.dropdown.Option(name))
            search_entry.update()
            self.drop.update()
        
        self.drop = ft.Dropdown(
            on_change=change_value,
            options=[ft.dropdown.Option(name) for name in names]
        )
        
        search_entry = ft.TextField(on_change=handle_change)
        
        super().__init__(
            ft.Column(controls=[search_entry, self.drop]),
            expand=False,
            height=100,
            width=600
        )
        
    def get_value(self):
        return self.value_selected or self.drop.value
    
    def update(self):
        dict_values = self.reference_get_new_dict()
        self.dict_values = dict_values
        self.value_selected = None
        self.drop.options.clear()
        self.drop.options = [ft.dropdown.Option(name) for name in dict_values.keys()]
        #self.drop.update()
    
    def deactivate(self):
        self.drop.options = []
        self.drop.update()
        
    def activate(self):
        self.update()
        self.drop.update()
#
#
#def main(page:ft.page):
#    
#    valores = {
#        "1":1,
#        "2":2,
#        "3":3,
#        "4":4,
#        "5":5,
#        "6":6,
#    }
#    
#    def get_():
#        return {
#        "1":1,
#        "2":2,
#        "3":3,
#        "4":4,
#        "5":5,
#    }
#        
#    search_value = SearchValue(valores, get_)
#    
#    
#    button_update = ft.IconButton(
#        icon = ft.icons.SAFETY_CHECK,
#        on_click = lambda e: search_value.update(),
#    )
#    
#    button_activate = ft.IconButton(
#        icon = ft.icons.ADD,
#        on_click = lambda e: search_value.activate(),
#    )
#    
#    button_deactivate = ft.IconButton(
#        icon = ft.icons.DELETE,
#        on_click = lambda e: search_value.deactivate(),
#    )
#    
#    
#    page.add(search_value, button_update, button_activate, button_deactivate)
#    
#
#
#ft.app(main)
#