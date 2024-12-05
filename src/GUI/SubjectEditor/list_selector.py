import flet as ft  
import time as tm 

class ListSelector(ft.Container):


    def __init__(self, tags : list, values : list):

        def click_tag(e, value, tag):
            self.__value = value
            self.__tag = tag
            self.search_bar.close_view()
            self.controls = self.controls
            self.load_tag(tag)

        def close_search_bar():
            self.controls = self.controls 
            #self.search_bar.close_view()


        tag_init = tags[0]
        value_init = values[0]

        self.__tag = tag_init 
        self.__value = value_init


        text_tag = ft.Text(
            tag_init,
            size = 20
        )

        self.text_tag = text_tag


        controls = []

        for (tag, value) in zip(tags, values):

            cont_value = ft.Container(
                            content = ft.Text(tag),
                            data = (tag, value)
                        )

            controls.append(ft.ListTile(title=cont_value, 
                                         on_click = lambda e, value = value, tag = tag: click_tag(e, value, tag),
                                         data = tag
                                         )
                            )
            

        self.controls = controls
    
        search_bar = ft.SearchBar(
                    divider_color=ft.colors.BLUE,
                    bar_hint_text="Buscar",
                    view_hint_text="Nombre",
                    on_submit = lambda e : self.search_tag(),
                    on_tap = lambda e : close_search_bar(),
                    view_elevation=4,
                    controls = controls,
                    width=300,
                    height=50
            )
        
        self.search_bar = search_bar

        super().__init__(
            content = ft.Column(
                controls = [
                    self.search_bar,
                    self.text_tag
                ]
            ),
            width = 300,
            height = 100,
            alignment=ft.alignment.center,
            ink=True,
        )

    def restart_controls(self):
        self.load_controls(self.controls)

    def search_tag(self):
        tag_search = self.search_bar.value
        # show tag coincidents in list selector 
        if tag_search == "":
            self.restart_controls()
            return None 
        
        new_controls = []
        for control in self.controls:
            tag_control = control.data # aqui se almacena el valor de tag de esta opcion (control)
            if tag_search.lower() in tag_control.lower():
                new_controls.append(control)
        
        self.load_controls(new_controls)
        
    def load_controls(self, controls):
        self.search_bar.controls = controls # los controles del objecto no se cambian 
        self.search_bar.close_view()
        self.search_bar.update()
        tm.sleep(0.1)
        self.search_bar.open_view()
        self.search_bar.update()

    def load_tag(self, new_tag):
        self.text_tag.value= new_tag
        self.text_tag.update()


    def get_value(self):
        return self.__value 


#! tags = [
#     "Juan de jesus",
#     "roberto",
#     "Maria",
#     "Pedro",
#     "Jose"
# ]

# values = [
#     1,
#     2,
#     3,
#     4,
#     5
# ]


# lists = ListSelector(tags, values)

# def main(page : ft.Page):

#     boton = ft.TextButton(
#         text = "Click",
#         on_click = lambda e : print(lists.get_value())
#     )
#     page.add(lists,
#     boton)

# ft.app(main)

