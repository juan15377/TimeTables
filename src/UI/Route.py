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
        self.body = ft.Container(expand = True)

    def set_route(self, stub: str, view: Callable):
        self.routes[stub] = view
    
    def set_routes(self, route_dictionary: dict):
        """Sets multiple routes at once. Ex: {"/": IndexView }"""
        self.routes.update(route_dictionary)

    "example : Route = RouteChangeEvent(route='/', name='route_change', data='/')"
    def route_change(self, route , page):
        
        _page = route.route.split("?")[0]
        queries = route.route.split("?")[1:]
        
        # se actualiza la pagina actual y la pagina anterior
        previous_route = global_state.get_state_by_key('current_page').get_state()
        State("current_page", _page)
        State("previous_page", previous_route)
        
        
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

