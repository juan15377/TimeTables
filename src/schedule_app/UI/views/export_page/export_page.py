import dearpygui.dearpygui as dpg

from src.schedule_app.UI.views.export_page.list_classrooms import ListaAulasApp
from src.schedule_app.UI.views.export_page.list_professors import ListaProfesoresApp
from src.schedule_app.UI.views.export_page.list_groups import ListaGruposApp
from src.schedule_app.database import database_manager

import dearpygui.dearpygui as dpg

# Crear el contexto y viewport
dpg.create_context()
dpg.create_viewport(title="Gestión de Aulas", width=600, height=500)

# Crear la ventana principal
with dpg.window(label="Lista de Profesores", tag="ventana_principal", width=1000, height=700):
    with dpg.group(horizontal=True):
        dpg.add_button(label="Exportar Horario Completo")
        dpg.add_button(label="Exportar Horario Completo en un solo archivo")
    
    dpg.add_spacing()
    dpg.add_separator()

        
    with dpg.tab_bar(tag="test_tab_bar"):
        # Tab 1
        with dpg.tab(label="Professor", tag="test_tab_1"):
            ListaProfesoresApp(database_manager)
                        
        # Tab 2
        with dpg.tab(label="Grupo", tag="test_tab_2"):
                #grilla.setup_ui()
            l = ListaGruposApp()
            l.setup_ui()
                
            pass            
        with dpg.tab(label="Aula", tag="test_tab_3"):
            ListaAulasApp()
            pass
            
                

# Configuración e inicio de la app
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
