import dearpygui.dearpygui as dpg

class SwitchButton:
    def __init__(self, parent, pos=(10, 10), ancho=60, alto=30, callback=None):
        self.estado = False
        self.ancho = ancho
        self.alto = alto
        self.radio_bola = alto // 2
        self.callback = callback

        # Crear drawlist
        with dpg.drawlist(width=ancho, height=alto, parent=parent, pos=pos) as self.drawlist:
            pass

        # Agregar handler para clics
        with dpg.item_handler_registry() as self.handler:
            dpg.add_item_clicked_handler(callback=self._on_click)
        dpg.bind_item_handler_registry(self.drawlist, self.handler)

        self._dibujar()

    def _on_click(self, sender, app_data):
        self.estado = not self.estado
        self._dibujar()
        if self.callback:
            self.callback(self.estado)

    def _dibujar(self):
        dpg.delete_item(self.drawlist, children_only=True)

        fondo_color = (0, 200, 0, 255) if self.estado else (100, 100, 100, 255)
        pos_bola_x = self.ancho - self.radio_bola if self.estado else self.radio_bola

        dpg.draw_rectangle(
            (0, 0),
            (self.ancho, self.alto),
            fill=fondo_color,
            rounding=self.radio_bola,
            thickness=0,
            parent=self.drawlist,
        )

        dpg.draw_circle(
            (pos_bola_x, self.alto // 2),
            self.radio_bola - 2,
            color=(255, 255, 255, 255),
            fill=(255, 255, 255, 255),
            parent=self.drawlist,
        )


# ------------------- CONFIGURACIÓN -------------------
dpg.create_context()

# Tema oscuro
with dpg.theme() as dark_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (25, 25, 25), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (230, 230, 230), category=dpg.mvThemeCat_Core)

# Ventana principal
with dpg.window(label="Interruptor Visual", width=250, height=150) as main_win:
    SwitchButton(parent=main_win, pos=(40, 40), ancho = 60, alto = 15, callback=lambda estado: print("Switch:", estado))

dpg.bind_theme(dark_theme)
dpg.create_viewport(title="Switch en DearPyGui", width=300, height=200)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
