import sys
import flet as ft

# Aquí puedes agregar la lógica para la creación de la lista
# Object responsible for creating a list

class NewCompositionGroup(ft.Container): # list_items es la lista que se muestra cuando se ven en al pagina
    def __init__(self, reference_items, items, save_reference, delete_reference, list_items, label):
        
        self.items = items
        self.reference_items = reference_items
        self.save_reference = save_reference
        self.delete_reference = delete_reference
        self.list_items = list_items
        self.drop_items = ft.Dropdown(
        )
        self.texfield_item = ft.TextField(hint_text="Enter item name")
        
        dict_items = {
            item.name:item for item in self.items
        }
        self.dict_items = dict_items
        
        self.drop_items.options = [ft.dropdown.Option(name) for name in dict_items.keys()]
        
        button_add = ft.IconButton(
            on_click= lambda e: self.add_item(),
            icon = ft.icons.ADD,
        )
        
        button_delete = ft.IconButton(
            on_click= lambda e: self.delete_selected(),
            icon = ft.icons.DELETE,
        )
        
        
        super().__init__(
            content= ft.Column(
                controls = [
                    ft.Text(label),
                    ft.Row(
                        controls = [
                            
                            self.texfield_item,
                            button_add,
                            button_delete,
                        ]
                    ),
                    self.drop_items
                ]
            ),
            height= 300,
            width= 400,
            alignment=ft.alignment.center,
            ink=True,
        )

    def update(self):
        self.items = self.reference_items()
        
        dict_items = {
            item.name:item for item in self.items
        }
        self.dict_items = dict_items
        
        self.drop_items.options = [ft.dropdown.Option(name) for name in dict_items.keys()]
        
        self.texfield_item.update()
        self.drop_items.update()
        
    def get(self):
        return self.dict_items[self.drop_items.value]
    

    def add_item(self):
        new_name = self.texfield_item.value
        self.drop_items.options.append(ft.dropdown.Option(new_name))
        self.texfield_item.value = ""
        self.save_reference(new_name)
        self.update()

    def delete_selected(self):
        selected_item = self.get()
        value = self.drop_items.value
        option = self.find_option(value)
        self.delete_reference(selected_item)
        if option != None:
            self.drop_items.options.remove(option)
            # d.value = None
            self.update()
        self.update()
        self.list_items.update_()
        
    def find_option(self, option_name):
        for option in self.drop_items.options:
            if option_name == option.key:
                return option
        return None



class NewCareer(NewCompositionGroup):
    
    def __init__(self, bd, list_items):
        super().__init__(
            reference_items = bd.groups.careers.get,
            items = bd.groups.careers.get(),
            save_reference = bd.groups.careers.new,
            delete_reference = bd.groups.careers.remove,
            list_items = list_items,
            label = "Carrera"
        )
    
    pass  


class NewSemester(NewCompositionGroup):
    
    def __init__(self, bd, list_items):
        
        super().__init__(
            reference_items = lambda: bd.groups.semesters.get(),
            items = bd.groups.semesters.get(),
            save_reference = bd.groups.semesters.new,
            delete_reference = bd.groups.semesters.remove,
            list_items = list_items,
            label = "Semestre"
        )
    
    pass  


class NewSubgroup(NewCompositionGroup):
    
    def __init__(self, bd, list_items):
        
        super().__init__(
            reference_items = lambda: bd.groups.subgroups.get(),
            items = bd.groups.subgroups.get(),
            save_reference = bd.groups.subgroups.new,
            delete_reference = bd.groups.subgroups.remove,
            list_items = list_items,
            label = "Subgrupo"
        )
    
    pass



class NewGroup(ft.Container):
    
    def __init__(self, bd, list_groups):
        self.career = NewCareer(bd,list_groups)
        self.semester = NewSemester(bd, list_groups)
        self.subgroup = NewSubgroup(bd, list_groups)
        
        def add_group(e):
            career = self.career.get()
            semester = self.semester.get()
            subgroup = self.subgroup.get()
            
            if career == None or semester == None or subgroup == None:
                ft.toast("Please select all values")
                return None
            
            bd.groups.new(career, semester, subgroup)
            list_groups.update_()
        
        button_add_group = ft.IconButton(
            on_click= lambda e: add_group(e),
            icon = ft.icons.ADD,  # Icono para agregar un grupo a la BD
        )
        
        super().__init__(
            content= ft.Row(
                controls = [
                    self.career,
                    self.semester,
                    self.subgroup,
                    button_add_group,  # Botón para agregar un grupo a la BD
                ]
            ),
            height= 150,
            width= 1600,
            ink=True,  # Agrega un borde al contenedor para diferenciarlo de otros contenedores en la pantalla.
        )
    
    pass  
