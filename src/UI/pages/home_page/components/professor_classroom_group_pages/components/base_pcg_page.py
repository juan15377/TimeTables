import flet as ft

class BasePCGPage(ft.Container):

    def __init__(self, db, pcg, search, enrouter, route, reference_to_get_dict):
        
        self.db = db
        
        button_to_change_page = ft.FloatingActionButton(
            icon=ft.icons.ADD,
            on_click=lambda e: enrouter.change_page(route),
            text = "Gestionar datos",
            focus_elevation= 10,
        )
        
        self.reference_to_get_dict = reference_to_get_dict
        
        self.button_to_change_page = button_to_change_page
                
        def change_professor():
            selected = self.search.get_value()
            self.set_pcg(selected)
            
        def get_actual_profesors():
            return {
            professor.name: professor for professor in self.db.professors.get()
            }

        
        self.search =  search
                
        self.pcg = pcg
        
        button_reset_subjects = ft.FloatingActionButton(
            icon=ft.icons.REFRESH,
            on_click=lambda e: to_change(),
            text = "Gestionar datos",
            focus_elevation= 10,
        )
        
        self.boardsubjects = ControlBoardSubjectSlots(pcg)
        
        
        self.layout = ft.Column(
            controls = [
                    ft.Row(
                        controls = [
                                    self.search,
                                    self.button_to_change_page,
                                    button_reset_subjects
                        ],
                        expand = False,
                        spacing=10
                    ),
                    ft.Row(
                        controls = [      
                            self.boardsubjects,
                        ],
                        expand = True
                    )
                    ],
                expand=True,
                spacing=50,
            )

        super().__init__(
            content = ft.Row(
                controls = [self.layout],
                expand=True
            ),
            expand=True,
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=500,
            reverse_duration=100,
            switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
            switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
        )
        
    # debe existir un metodo que actualize ambos 
    # 
        
    def get_layout_page(self, pcg):
        boardsubjects = ControlBoardSubjectSlots(enrouter, pga = pcg)
        self.boardsubjects = boardsubjects
        
        button_reset_subjects = ft.FloatingActionButton(
            icon=ft.icons.REFRESH,
            on_click=lambda e: to_change(),
            text = "Gestionar datos",
            focus_elevation= 10,
        )
        
        def change_professor():
            selected = self.search.get_value()
            self.set_pcg(selected)
            
        def get_actual_profesors():
            return self.reference_to_get_dict()
        
        
        self.layout = ft.Column(
            controls = [
                    ft.Row(
                        controls = [
                                    self.search,
                                    self.button_to_change_page,
                                    button_reset_subjects
                        ],
                        expand = False,
                        spacing=30
                    ),
                    ft.Row(
                        controls = [      
                            self.boardsubjects,
                        ],
                        expand = True
                    )
                    ],
                expand=True,
                spacing=50,
            )
        
        return layout 
                
        
    def set_pcg(self, pcg):
        self.update_boardsubjects(pcg)
        self.search.update()
        
        self.pcg = pcg

        #super().content.controls.append(new_layout)
        #self.boardsubjects.update()
        print("Se cargo")
        super().update()
        
        
    def update(self, update = True):
        self.update_boardsubjects(self.pcg)
       
        if update:
            super().update()  
            self.search.update()
            
    def update_boardsubjects(self, new_pcg):
        boardsubjects = ControlBoardSubjectSlots(new_pcg)
        self.boardsubjects = boardsubjects
        
        self.layout.controls[1].controls = [self.boardsubjects]
        
        self.layout.update()
        
        pass

class ControlBlocksSubjects(ft.AnimatedSwitcher):

    def __init__(self, db, pcg, search, enrouter, route, reference_to_get_dict):
        
        self.db = db
        
        button_to_change_page = ft.FloatingActionButton(
            icon=ft.icons.ADD,
            on_click=lambda e: enrouter.change_page(route),
            text = "Gestionar datos",
            focus_elevation= 10,
        )
        
        self.reference_to_get_dict = reference_to_get_dict
        
        self.button_to_change_page = button_to_change_page
                
        def change_professor():
            selected = self.search.get_value()
            self.set_pcg(selected)
            
        def get_actual_profesors():
            return {
            professor.name: professor for professor in self.db.professors.get()
            }

        
        self.search =  search
                
        self.pcg = pcg
        
        button_reset_subjects = ft.FloatingActionButton(
            icon=ft.icons.REFRESH,
            on_click=lambda e: to_change(),
            text = "Gestionar datos",
            focus_elevation= 10,
        )
        
        self.boardsubjects = ControlBoardSubjectSlots(pcg)
        
        
        self.layout = ft.Column(
            controls = [
                    ft.Row(
                        controls = [
                                    self.search,
                                    self.button_to_change_page,
                                    button_reset_subjects
                        ],
                        expand = False,
                        spacing=10
                    ),
                    ft.Row(
                        controls = [      
                            self.boardsubjects,
                        ],
                        expand = True
                    )
                    ],
                expand=True,
                spacing=50,
            )

        super().__init__(
            content = ft.Row(
                controls = [self.layout],
                expand=True
            ),
            expand=True,
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=500,
            reverse_duration=100,
            switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
            switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
        )
        
    # debe existir un metodo que actualize ambos 
    # 
        
    def get_layout_page(self, pcg):
        boardsubjects = ControlBoardSubjectSlots(enrouter, pga = pcg)
        self.boardsubjects = boardsubjects
        
        button_reset_subjects = ft.FloatingActionButton(
            icon=ft.icons.REFRESH,
            on_click=lambda e: to_change(),
            text = "Gestionar datos",
            focus_elevation= 10,
        )
        
        def change_professor():
            selected = self.search.get_value()
            self.set_pcg(selected)
            
        def get_actual_profesors():
            return self.reference_to_get_dict()
        
        
        self.layout = ft.Column(
            controls = [
                    ft.Row(
                        controls = [
                                    self.search,
                                    self.button_to_change_page,
                                    button_reset_subjects
                        ],
                        expand = False,
                        spacing=30
                    ),
                    ft.Row(
                        controls = [      
                            self.boardsubjects,
                        ],
                        expand = True
                    )
                    ],
                expand=True,
                spacing=50,
            )
        
        return layout 
                
        
    def set_pcg(self, pcg):
        self.update_boardsubjects(pcg)
        self.search.update()
        
        self.pcg = pcg

        #super().content.controls.append(new_layout)
        #self.boardsubjects.update()
        print("Se cargo")
        super().update()
        
        
    def update(self, update = True):
        self.update_boardsubjects(self.pcg)
       
        if update:
            super().update()  
            self.search.update()
            
    def update_boardsubjects(self, new_pcg):
        boardsubjects = ControlBoardSubjectSlots(new_pcg)
        self.boardsubjects = boardsubjects
        
        self.layout.controls[1].controls = [self.boardsubjects]
        
        self.layout.update()
        
        pass