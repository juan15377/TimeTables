import flet as ft 


class OnlineSwitch(ft.Container):
    def __init__(self, classroom_selector):
        
        
        def deactivate():
            classroom_selector.deactivate()
        
        def activate():
            classroom_selector.activate()
            
            
        def change_value(e):
            if switch.value:
                deactivate()
            else:
                activate()
        
        switch = ft.Switch(label="Online", value=False)
        self.switch = switch
        switch.on_change = change_value
        
        
        super().__init__(
            content = switch
        )
        
    def is_online(self):
        return self.switch.value
    
        
        