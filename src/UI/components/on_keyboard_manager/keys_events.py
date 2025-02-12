
from .key_event_manager import KeyEvent 
from .events import auto_save_database

KEYS_EVENTS = [
    KeyEvent(
        "S",
        True,
        True,
        False,
        False,
        auto_save_database
    ),

    
]