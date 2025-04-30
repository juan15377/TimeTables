import dearpygui.dearpygui as dpg 
from src.app.UI.components.list_subjects.subject_selector import SubjectSelector 
from src.app.database import database_manager 

sub_sel = SubjectSelector(
    2,
    database_manager,
    lambda s, a, u : print("subject_change_callback", "\n",  s, "\n", a, "\n", u, "\n"),
    lambda s, a, u : print("subject_change_callback", "\n" , s, "\n", a, "\n", u, "\n"),
    mode="PROFESSOR"
)

dpg.create_context()

with dpg.window(label="Sistema de Horarios", tag="main_window", width=780, height=580):
    sub_sel.setup_ui()
    dpg.add_button(
        label = "Retornar ID",
        callback= lambda s, a, u : print(sub_sel.get_id())
    )
    # cambiar id_mode  
    dpg.add_button(
        label = "cambiar id mode",
        callback= lambda s, a, u : sub_sel.set_id_mode(1)
    )

dpg.create_viewport(title="Sistema de Horarios", width=1000, height=800)
dpg.set_primary_window("main_window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()