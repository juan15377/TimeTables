# import flet as ft
# from flet import TextField, ListView, Page, ListTile, app, SearchBar,Text

# def main(page: Page):
#     # Define the list of languages
#     all_lang = ['English', 'Japanese', 'Cantonese', 'English Canadian']

#     # Function to handle search bar input changes
#     def handle_change(e):
#         # Clear the current list view
#         lv.controls.clear()
#         # Filter and append languages that contain the search query
#         search_query = e.control.value.lower()
#         for lang in all_lang:
#             if search_query in lang.lower():
#                 lv.controls.append(ListTile(title=ft.Text(lang), on_click=close_anchor, data=lang))
#         # Update the list view to show the filtered results
#         lv.update()

#     # Function to handle selection from the list view
#     def close_anchor(e):
#         # Get the selected language
#         selected_lang = e.control.data
#         # Set the search bar text to the selected language
#         ele2.close_view(selected_lang)
#         # Update the search bar to reflect the selected language
#         ele2.update()

#     # Create a list view for displaying the search results
#     lv = ListView()

#      # Populate the list view with all languages as default selection choices
#     for lang in all_lang:
#         lv.controls.append(ListTile(title=ft.Text(lang), on_click=close_anchor, data=lang))

#     # Create a search bar element
#     ele2 = SearchBar(
#         bar_hint_text="Type to search...",
#         on_change=handle_change,
#         controls=[lv]
#     )

#     # Add the search bar to the page
#     page.add(ele2)

# # Run the Flet app
# if __name__ == '__main__':
#     app(target=main)


from dataclasses import dataclass, field
import flet as ft
from flet import ListView, Page, ListTile, app, SearchBar, Text

from typing import Callable


class SearchableDropdown(ft.Container):
    def __init__(self, items, reference_get_new_dict):
        self.items: dict = items
        self.reference_get_new_dict = reference_get_new_dict
        self.lv = ft.ListView()
        self.search_bar: self.search_bar = SearchBar(
            bar_hint_text="Type to search...",
            on_change=self.handle_change,
            controls=[self.lv],
            on_tap = lambda e : self.lv.update()
        )
        
        self.text = ft.Text("")
        
        super().__init__(
            content = ft.Column(
                controls = [
                self.search_bar,
                self.text,                
            ]
            )
        )
        self.activated = True
        self.value = None
        
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
        self.text.update()
        self.search_bar.close_view("")
        self.search_bar.update()
        self.activated = False
    
    def activate(self):
        self.items = self.reference_get_new_dict()
        self.populate_list_view()
        self.activated = True
    

def main(page: Page):
    all_lang = {"1" : 1, 2 : "2"}
    diff_list = ['abc','abcdef','def', 'xyz']
    
    def get_new_dict():
        return {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
            "g": 7,
            "h": 8,
            "i": 9,
            "j": 10,
            "k": 11,
            "l": 12,
            "m": 13,
            "n": 14,
            "o": 15,
            "p": 16,
            "q": 17,
            "r": 18,
            "s": 19,
            "t": 20,
            "u": 21,
            "v": 22,
            "w": 23,
            "x": 24,
            "y": 25,
            "z": 26,
        }
        
    searchable_dropdown = SearchableDropdown(all_lang, get_new_dict)
    

    
    
    buton_get_value = ft.TextButton(
        text = "Get Value",
        on_click=lambda e: print(searchable_dropdown.get_value())
    )
    
    buton_deactivate = ft.TextButton(
        text = "Deactivate",
        on_click=lambda e: searchable_dropdown.deactivate()
    )
    
    button_update = ft.TextButton(
        text = "Update",
        on_click=lambda e: searchable_dropdown.update()
    )
    
    button_activate = ft.TextButton(
        text = "Activate",
        on_click=lambda e: searchable_dropdown.activate()
    )

    page.add(
        searchable_dropdown,
        buton_get_value,
        buton_deactivate,
        button_update,
        button_activate,
        )


for (i, j) in zip([1,2], [3,4]):
    print(i,j)

if __name__ == '__main__':
    app(target=main)