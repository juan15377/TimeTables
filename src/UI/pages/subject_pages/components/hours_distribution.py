import sys
import flet as ft

from src.models.database import HoursComposition, HoursSlotsComposition

class CounterHours(ft.Container):

    def __init__(self):
        txt_number = ft.TextField(value="0", text_align=ft.TextAlign.CENTER, width=60)

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

class EditorHours(ft.Container):

    def __init__(self):
        total_hours = CounterHours()
        minimum_hours = CounterHours()
        maximum_hours = CounterHours()
        
        check = ft.Checkbox(adaptive=True, label="Activate", value=True)
        
        layout = ft.Column(
            controls = [
                ft.Row(
                    controls = [
                        ft.Text("Total Hours"),
                        total_hours,
                        check
                    ],
                    expand = True
                ),
                
                ft.Row(
                    controls = [
                        ft.Text("Minimum Hours"),
                        minimum_hours,
                        ft.Text("Maximum Hours"),
                        maximum_hours
                    ],
                    spacing=20,
                    expand = True
                    
                )
            ],
            spacing= 30,
            expand = True
        )
        
        self.total_hours = total_hours
        self.minimum_hours = minimum_hours
        self.maximum_hours = maximum_hours
        self.check = check
        
        super().__init__(
            content = layout,
            padding= 5,
            expand = True
        )

    def get(self):
        return HoursComposition(
            self.minimum_hours.get_value(),
            self.maximum_hours.get_value(),
            self.total_hours.get_value(),
        )
        
    def set_value(self, hours):
        self.total_hours.set_value(hours.total())
        self.minimum_hours.set_value(hours.minimum())
        self.maximum_hours.set_value(hours.maximum())
    
    def is_active(self):
        return self.check.value
    
    def set_activate(self, active):
        self.check.value = active
        self.check.update()

class EditorBlocks(ft.Container):

    def __init__(self):
        self.blocks = []
        self.counter_hours = CounterHours()
        self.check =  ft.Checkbox(adaptive=True, label="Activate", value=True)
        self.drop_blocks = ft.Column(
            width=100,
            height=100,
            scroll = ft.ScrollMode.ALWAYS,
            alignment= ft.alignment.center
        )
        
        button_add = ft.TextButton(
            text="Add",
            on_click=lambda e : self.add_block(),
        )
        
        button_remove = ft.TextButton(
            text="Remove",
            on_click= lambda e : self.remove_block(),
        )
        
        button_reset = ft.TextButton(
            text="Reset",
            on_click= lambda e : self.reset(),
        )
        
        layout = ft.Column(
            controls=[
                ft.Row(
                    controls = [
                        ft.Text("Blocks"),
                        self.counter_hours,
                        self.drop_blocks,
                    ],
                    expand = True
                ),
                ft.Row(
                    controls = [
                        button_add,
                        button_remove,
                        button_reset,
                        self.check,
                    ],
                    expand = True
                )
            ],
            spacing= 10,
            expand = True
        )
        
        super().__init__(
            content = layout,
            expand = True
        )
        
    def add_block(self):
        block_length = self.counter_hours.get_value()
        if block_length == 0:
            return None  # blocks of size zero are not allowed
        self.drop_blocks.controls.append(ft.Text(str(block_length), text_align= ft.alignment.center))
        self.blocks.append(block_length)
        self.drop_blocks.update()

    def remove_block(self):
        if len(self.blocks) == 0:
            return None  # cannot remove if the list is empty
        self.drop_blocks.controls.pop()
        self.blocks.pop()
        self.drop_blocks.update()
        
    def reset(self):
        self.drop_blocks.controls.clear()
        self.blocks.clear()
        self.counter_hours.set_value(0)
        self.drop_blocks.update()

    def get(self) -> HoursSlotsComposition:
        return HoursSlotsComposition(self.blocks) 
    
    def set_blocks(self, blocks):
        self.blocks = blocks.get()
        self.drop_blocks.controls.clear()
        for block in self.blocks:
            self.drop_blocks.controls.append(ft.Text(str(block), text_align= ft.alignment.center))
        self.drop_blocks.update()

    def set_activate(self, active: bool):
        self.check.value = active
        self.check.update()

class SelectorDistributionHours(ft.Container):

    def __init__(self, comp_hours = HoursComposition(0, 0, 0)):

        self.selector_hours = EditorHours()
        self.selector_blocks = EditorBlocks()

        if isinstance(comp_hours, HoursComposition):
            self.selector_hours.set_value(comp_hours)
            self.selector_hours.check.value = True
            self.selector_blocks.check.value = False
        else:
            self.selector_blocks.set_blocks(comp_hours)  # it is a type of CBloques
            self.selector_blocks.check.value = True
            self.selector_hours.check.value = False

        def change_selection_hours(e):
            self.selector_blocks.set_activate(not self.selector_hours.check.value)

        def change_selection_blocks(e):
            self.selector_hours.set_activate(not self.selector_blocks.check.value)

        self.selector_blocks.check.on_change = change_selection_blocks
        self.selector_hours.check.on_change = change_selection_hours

        tabs = ft.Tabs(
            selected_index=1,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Hours Composition",
                    content=ft.Container(
                        content=self.selector_hours, 
                        alignment=ft.alignment.center
                        )
                ),
                ft.Tab(
                    text="Blocks Composition",
                    content=ft.Container(
                        content = self.selector_blocks, 
                        alignment=ft.alignment.center
                        )
                ),
            ],
            width= 600,
            height=600
        )

        super().__init__(
            content=tabs,
            width=650,
            height=230,
            expand = True
        )

    def get_hours_distribution(self):
        if self.selector_hours.check.value:
            return self.selector_hours.get()
        else:
            return self.selector_blocks.get()

# def main(page: ft.Page):
#     selector = SelectorDistributionHours()
    
#     def print_selection(e):
#         print(selector.get())
        
#     button = ft.TextButton(
#         text="Print",
#         on_click=print_selection
#     )
    
#     page.add(selector, button)

# ft.app(target=main)
