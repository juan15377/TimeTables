
import sys
import flet as ft

# Agregar ruta al sys.path si no está presente
sys.path.append("src/Logic/")



from dataclasses import dataclass, field
import flet as ft
from flet import ListView, Page, ListTile, app, SearchBar, Text

from typing import Callable



#class SearchValue(ft.Container):
#    
#    def __init__(self, dict_values, reference_get_new_dict, on_change =lambda: None) -> None:
#        self.on_change = on_change
#        self.reference_get_new_dict = reference_get_new_dict
#        
#        values = list(dict_values.values())
#        names = list(dict_values.keys())
#        self.dict_values = dict_values
#        self.value_selected = None
#    
#        def change_value(e):
#            self.value_selected = self.dict_values[self.drop.value]
#            self.on_change()
#            
#        def handle_change(e):
#            list_to_show = [name for name in names if e.data.lower() in name.lower()]
#            self.drop.options.clear()
#            for name in list_to_show:
#                self.drop.options.append(ft.dropdown.Option(name))
#            self.drop.update()
#        
#        self.drop = ft.Dropdown(
#            on_change=change_value,
#            options=[ft.dropdown.Option(name) for name in names]
#        )
#        
#        search_entry = ft.TextField(on_change=handle_change)
#        
#        super().__init__(
#            ft.Column(controls=[search_entry, self.drop]),
#            expand=True,
#            #height=100,
#            #width=600
#            #expand = True
#        )
#        
#    def get_value(self):
#        return self.value_selected or self.drop.value
#    
#    def update(self):
#        dict_values = self.reference_get_new_dict()
#        self.dict_values = dict_values
#        self.value_selected = None
#        self.drop.options.clear()
#        self.drop.options = [ft.dropdown.Option(name) for name in dict_values.keys()]
#        #self.drop.update()
#        #print("Hola Mundo")
#    
#    def deactivate(self):
#        self.drop.options = []
#        self.drop.update()
#        
#    def activate(self):
#        self.update()
#        self.drop.update()
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
#    search_value = SearchValue(valores, get_, on_change = lambda : print("Hola"))
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


class SearchValue(ft.Container):
    def __init__(self, items, reference_get_new_dict, on_change = lambda : None):
        self.items: dict = items
        self.reference_get_new_dict = reference_get_new_dict
        self.lv = ft.ListView()
        self.search_bar= SearchBar(
            bar_hint_text="Type to search...",
            on_change=self.handle_change,
            controls=[self.lv],
            on_tap = lambda e : self.lv.update(),
        )
        
        self.text = ft.Text("")
        
        super().__init__(
            content = ft.Column(
                controls = [
                self.search_bar,
                #self.text,                
                ],
                expand = True
            ),
            expand = True
        )
        self.activated = True
        self.value = None
        
        self.on_change = on_change
        
        self.populate_list_view()
        
    def __post_init__(self):
        self.search_bar = SearchBar(
            bar_hint_text="Type to search...",
            on_change=self.handle_change,
            controls=[self.lv]
        )
        self.populate_list_view()
        self.value = None

    def populate_list_view(self):
        self.lv.controls.clear()  # Clear the list view before populating it again
        for (name, value) in zip(self.items.keys(), self.items.values()):
            self.lv.controls.append(ListTile(title=ft.Text(name), on_click=self.close_anchor, data=(name, value)))

    def handle_change(self, e):
        self.lv.controls.clear()
        if not self.activated:
            return None
        search_query = e.control.value.lower()
        for (name, value) in zip(self.items.keys(), self.items.values()):
            if search_query in str(name).lower() or search_query == "":
                self.lv.controls.append(ListTile(title=ft.Text(name), on_click=self.close_anchor, data=(name, value)))
        self.lv.update()

    def close_anchor(self, e):
        name =  e.control.data[0]
        value = e.control.data[1]  # retrieve the selected item's value from the data tuple
        self.value = value  # store the selected value in the class field for future use
        self.text.value = name 
        selected_item_name = name
        self.search_bar.close_view(selected_item_name)
        super().update()
        self.on_change()
        
        
    def get_value(self):
        return self.value
        print(type(self.value))
    
    def update(self):
        new_dict = self.reference_get_new_dict()
        self.items = new_dict
        self.populate_list_view()
        #self.lv.update()
    
    def deactivate(self):
        self.lv.controls.clear()
        self.lv.update()
        self.value = None
        self.text.value = ""
        self.search_bar.close_view("")
        self.search_bar.update()
        self.activated = False
    
    def activate(self):
        self.items = self.reference_get_new_dict()
        self.populate_list_view()
        self.activated = True
    

#
#def main(page : ft.Page):
#    items = {
#        "1" : 1,
#        "2" : 2,
#        "3" : 3
#    }
#    
#    def get():
#        return {
#        "1" : 1,
#        "2" : 2,
#        "3" : 3,
#        "4" : 4
#    }
#        
#    sv = SearchValue(items, get)
#    
#    con = ft.Row(
#        controls = [sv, sv],
#        expand = True
#    )
#    
#    h = ft.Container(
#        content = con
#    )
#    
#    page.add(h)
#    
#ft.app(target = main)