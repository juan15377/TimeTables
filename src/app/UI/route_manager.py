# habra 6 rutas 

from .routes import CALLBACK_ROUTES, ID_SELECTED

class RouteManager:
    
    def __init__(self, callback_routes):
        self.callback_routes = callback_routes 
        pass 
    
    def change_route(self, route, query):
        self.callback_routes[route](query)
        pass
    

route_manager = RouteManager(CALLBACK_ROUTES)
    