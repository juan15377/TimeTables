# habra 6 rutas 

from .routes import CALLBACK_UPDATE_ROUTES

class RouteManager:
    
    def __init__(self, callback_routes):
        self.callback_routes = callback_routes 
        pass 
    
    def change_route(self, route):
        self.callback_routes[route]()
        pass
    

route_manager = RouteManager(CALLBACK_UPDATE_ROUTES)
    