import flet as ft
import sys 

sys.path.append("/src/Logic")
from materias import CHoras, CBloques



class CounterHours(ft.Container):

    def __init__(self):

        txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

        def minus_click(e):
            if float(self.txt_number.value) > 0:
                txt_number.value = str(float(txt_number.value) - .5)
                self.txt_number.update()

        def plus_click(e):
            txt_number.value = str(float(txt_number.value) + .5)
            self.txt_number.update()

        c = ft.Row(
                [
                    ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                    txt_number,
                    ft.IconButton(ft.icons.ADD, on_click=plus_click),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        super().__init__(content=c)

        self.txt_number = txt_number

    def get_value(self):
        return float(self.txt_number.value)
    
    def set_value(self, value):
        self.txt_number.value = str(value)
        #self.txt_number.update()



class EditorHours(ft.Container):

    def __init__(self):
        
        horas_totales = CounterHours()
        horas_minimas = CounterHours()
        horas_maximas = CounterHours()
        
        check = ft.Checkbox(adaptive=True, label="Activar", value=True)
        
        diseño = ft.Column(
            controls = [
                ft.Row(
                    controls = [
                        ft.Text("Total Hours"),
                        horas_totales,
                        check
                    ],
                    spacing = 50
                ),
                
                ft.Row(
                    controls = [
                        ft.Text("Minimun Hours"),
                        horas_minimas,
                        ft.Text("Horas maximas"),
                        horas_maximas
                    ],
                    spacing=20
                )
            ],
            spacing= 30
        )
        
        self.horas_totales = horas_totales
        self.horas_minimas = horas_minimas
        self.horas_maximas = horas_maximas
        self.check = check
        
        super().__init__(
            content = diseño,
            padding= 30
        )
        pass

    def get(self):
        return CHoras(
            self.horas_totales.get_value(),
            self.horas_minimas.get_value(),
            self.horas_maximas.get_value(),
        )
        
    def set_value(self, choras):
        self.horas_totales.set_value(choras.total())
        self.horas_minimas.set_value(choras.minimo())
        self.horas_maximas.set_value(choras.maximo())
    
    def is_active(self):
        return self.check.value
    
    def set_activate(self, active):
        self.check.value = active
        self.check.update()




class EditorBlocks(ft.Container):

    def __init__(self):
        self.blocks = []
        self.counter_hours = CounterHours()
        self.check =  ft.Checkbox(adaptive=True, label="Activar", value=True)
        self.drop_blocks = ft.Column(
            width=100,
            height=100,
            scroll = ft.ScrollMode.ALWAYS,
            alignment= ft.alignment.center
        )
        
        buton_add = ft.TextButton(
            text="Agregar",
            on_click=lambda e : self.add_block(),
        )
        
        buton_remove = ft.TextButton(
            text="Quitar",
            on_click= lambda e : self.remove_block(),
        )
        
        buton_reset = ft.TextButton(
            text="Reiniciar",
            on_click= lambda e : self.reset(),
        )
        
        diseño = ft.Row(
            controls=[
                ft.Text("Bloques"),
                self.counter_hours,
                self.drop_blocks,
                buton_add,
                buton_remove,
                buton_reset,
                self.check,
            ],
            spacing=20
        )
        
        super().__init__(
            content = diseño
        )
        

    def add_block(self):
        length_block = self.counter_hours.get_value()
        if length_block == 0 :
            return None # no se aceptan bloques de tamaño cero
        self.drop_blocks.controls.append(ft.Text(str(length_block), text_align= ft.alignment.center))
        self.blocks.append(length_block)
        self.drop_blocks.update()


    def remove_block(self):
        if len(self.blocks) == 0:
            return None # si ya esta vacia no se le puede quitar uno 
        self.drop_blocks.controls.pop()
        self.blocks.pop()
        self.drop_blocks.update()
        
    def reset(self):
        self.drop_blocks.controls.clear()
        self.blocks.clear()
        self.counter_hours.set_value(0)
        self.drop_blocks.update()


    def get(self) -> CBloques:
        return CBloques(self.blocks) 
    
    def set_blocks(self, cbloques):
        self.blocks = cbloques.get()
        self.drop_blocks.controls.clear()
        for block in self.blocks:
            self.drop_blocks.controls.append(ft.Text(str(block), text_align= ft.alignment.center))
        self.drop_blocks.update()

    def set_activate(self, active : bool):
        self.check.value = active
        self.check.update()
    


class SelectorComHours(ft.Container):

    def __init__(self, comphours = CHoras(0,0,0)):

        self.selector_hours = EditorHours()
        self.selector_blocks = EditorBlocks()

        if type(comphours) == CHoras:
            self.selector_hours.set_value(comphours)
            self.selector_hours.check.value = True
            self.selector_blocks.check.value = False
        else:
            self.selector_blocks.set_blocks(comphours) # is type of CBloques
            self.selector_blocks.check.value = True
            self.selector_hours.check.value = False

        def change_selection_hours(e):
            self.selector_blocks.set_activate(not self.selector_hours.check.value)


        def change_selection_blocks(e):
            self.selector_hours.set_activate(not self.selector_blocks.check.value)


            
        self.selector_blocks.check.on_change = change_selection_blocks
        self.selector_hours.check.on_change = change_selection_hours

        T = ft.Tabs(
            selected_index=1,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Composicion por Horas",
                    content=ft.Container(
                        content=self.selector_hours, alignment=ft.alignment.center
                    ),
                ),
                ft.Tab(
                    text = "Composicion por bloques",
                    content=self.selector_blocks,
                ),

            ],
            expand=1,
        )

        super().__init__(
            content=T,
            width=800,
            height=600,
            padding=30
        )

    def get(self):
        if self.selector_hours.check.value:
            return self.selector_hours.get()
        else:
            return self.selector_blocks.get()




def main(page : ft.Page):
    fila = SelectorComHours()
    
    def imprimir(e):
        print(fila.get())
        
    boton = ft.TextButton(
        text = "Imprimir",
        on_click = imprimir
    )
    
    page.add(fila, boton )

ft.app(target=main)

