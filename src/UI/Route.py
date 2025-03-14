from typing import Callable, Any
import flet as ft
from enum import Enum
from .State import global_state, State


class DataStrategyEnum(Enum):
    QUERY = 0
    ROUTER_DATA = 1
    CLIENT_STORAGE = 2
    STATE = 3

class Router:
    def __init__(self, data_strategy=DataStrategyEnum.QUERY):
        self.data_strategy = data_strategy
        self.data = dict()
        self.routes = {}
        self.body = ft.AnimatedSwitcher( # container animated
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=400,
            reverse_duration=150,
            switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
            switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
            expand=True
        )

    def set_route(self, stub: str, view: Callable):
        self.routes[stub] = view
    
    def set_routes(self, route_dictionary: dict):
        """Sets multiple routes at once. Ex: {"/": IndexView }"""
        self.routes.update(route_dictionary)

    "example : Route = RouteChangeEvent(route='/', name='route_change', data='/')"
    def route_change(self, route , page):
        
        _page = route.route.split("?")[0]
        queries = route.route.split("?")[1:]
        
        # se inserta una nueva ruta
        manager_route = global_state.get_state_by_key('manager_routes').get_state()
        manager_route.new_route(route.route)

    
        _hash = None
        for item in queries:
            key = item.split("=")[0]
            value = item.split("=")[1]
            self.data[key] = value.replace('+', ' ')
            _hash = self.data[key]

        self.body.content = self.routes[_page](page, _hash) 
        self.body.update()

    def set_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        return self.data.get(key)

    def get_query(self, key):
        return self.data.get(key)


class RoutesManagerNavigation():
    
    index_page = -1
    
    def __init__(self):
        self.routes = ["/"]
        
    def new_route(self, route):
        if route == self.routes[-1]:
            return None
        if route == "/" :
            self.routes = []
            self.index_page = -1
        self.routes.append(route)
        self.index_page += 1
        print(self.routes)
        pass  
    
    def get_prevoius(self):
        if self.index_page == 0:
            return self.routes[0]
        self.index_page = self.index_page - 1
        del self.routes[-1]
        return self.routes[self.index_page]
        print(self.routes)
        pass

    def get_actual_route(self):
        return self.routes[self.index_page]
        pass
