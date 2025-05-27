import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.window(label="Tabla Semanal", width=800, height=300):
    with dpg.table(header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp):
        # Agrega las columnas (una para cada día)
        hours = [
            "7:00-7:30", "7:30-8:00", "8:00-8:30", "8:30-9:00", "9:00-9:30", "9:30-10:00", "10:00-10:30",
                        "10:30-11:00", "11:00-11:30", "11:30-12:00", "12:00-12:30", "12:30-1:00", "1:00-1:30", "1:30-2:00",
                        "2:00-2:30", "2:30-3:00", "3:00-3:30", "3:30-4:00", "4:00-4:30", "4:30-5:00", "5:00-5:30", 
                        "5:30-6:00", "6:00-6:30", "6:30-7:00", "7:00-7:30", "7:30-8:00", "8:00-8:30", "8:30-9:00", "9:00-9:30", "9:30-10:00"
        ]
        dias = ["Hora", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        for dia in dias:
            dpg.add_table_column(label=dia)

        # Agrega una fila de ejemplo (puedes agregar más según lo necesites)
                
        with dpg.table_row():   
            with dpg.group(horizontal=False):       
                for _ in hours:
                    dpg.add_button(label = _, width=-1, height=30)
            
            for column in range(7):
                 with dpg.group(horizontal=False):       
                    for row in range(30):
                        dpg.add_button(label = f"{(row, column)}", width=-1, height=30)
                

dpg.create_viewport(title='Tabla de los Días de la Semana', width=820, height=340)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
