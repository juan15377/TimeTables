
import sys
import flet as ft
from dataclasses import dataclass, field
from flet import ListView, Page, ListTile, app, SearchBar, Text
from typing import Callable



class SearchBarItems(ft.Container):
    def __init__(self, items : list, refresh_items : Callable, on_change = lambda : None):
        self.items: dict = items
        self.refresh_items = refresh_items
        self.lv = ft.ListView()
        self.search_bar= SearchBar(
            bar_hint_text="Type to search...",
            on_change=self.handle_change,
            controls=[self.lv],
            on_tap = lambda e : self.lv.update(),
        )
        
        
        super().__init__(
            content = self.search_bar,
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
        selected_item_name = name
        self.search_bar.close_view(selected_item_name)
        super().update()
        self.on_change()
        
        
    def get_value(self):
        return self.value
        print(type(self.value))
    
    def update(self):
        new_dict = self.refresh_items()
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
        self.items = self.refresh_items()
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
#    sv = SearchBarItems(items, get)
#    
#    con = ft.Row(
#        controls = [sv],
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