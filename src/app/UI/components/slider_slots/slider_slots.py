import dearpygui.dearpygui as dpg

class DiscreteValueSelector:
    def __init__(self, mode , allowed_values, slider_tag):
        self.allowed_values = allowed_values
        self.window_tag = "main_window"
        self.slider_tag = slider_tag +  "_" + mode
        self.display_tag = "value_display" + "_" +mode  

    def on_slider_changed(self, sender, app_data):
        index = app_data
        real_value = self.allowed_values[index]
        dpg.set_value(self.display_tag, str(real_value))

    def setup_widget(self):
        with dpg.group(horizontal=True):
            dpg.add_slider_int(
                tag=self.slider_tag,
                label="",
                default_value=0,
                min_value=0,
                max_value=len(self.allowed_values) - 1,
                width=-190,
                callback=self.on_slider_changed,
                format=""
            )
            dpg.add_input_text(
                default_value=str(self.allowed_values[0]),
                width=25,
                readonly=True,
                tag=self.display_tag
            ) 
    
    def set_allowed_values(self, new_allowed_values):
        """Actualiza los valores permitidos y reinicia el selector"""
        if not new_allowed_values:
            new_allowed_values = [0]
            
        self.allowed_values = new_allowed_values
        
        # Actualizar el slider
        dpg.configure_item(
            self.slider_tag,
            max_value=len(self.allowed_values) - 1,
            default_value=0
        )
        
        # Actualizar el display
        dpg.set_value(
            self.display_tag,
            str(self.allowed_values[0])
        )
    
    def get_value(self):
        return self.allowed_values[dpg.get_value(self.slider_tag)]
        pass