from .State import global_state 
from src.UI.components import alerts 
from typing import dict, Callable
from src.UI.database import database

            
class OnKeyboardManager():
    def __init__(self, page, key_event_maps :  [list, None] = None):
        self.page = page
        self.key_events = key_events
        pass
    
    def new_key_event(self, key_event):
        self.key_events.append(key_event)
        pass    
    
    def on_keyboard(e : ft.KeyboardEvent):
        for key_event in self.key_events:
            if (e.key, e.shift, e.ctrl, e.alt, e.meta) == (key_event.key, key_event.shift, key_event.ctrl, key_event.alt, key_event.meta) :
                key_event.event(self.page)  
        pass

class KeyEvent():
    def __init__(key : str, shift : bool, ctrl : bool, alt : bool, meta : bool, event : Callable):
        self.key = key
        self.shift = shift
        self.ctrl = ctrl
        self.alt = alt
        self.meta = meta
        self.event = event
        pass
