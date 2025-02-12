from src.UI.State import global_state 
from src.UI.components import alerts 
from typing import dict, Callable
from src.UI.database import database


def auto_save_database(page):
    auto_save_path = global_state.get_state_by_key("auto_save_path")
    
    if auto_save_path is not None:
        database.save(auto_save_database)
        alert_changes_save = (page, self.save_path_default)
        alert_changes_save.show()
        return None
            