from src.app.UI.components.windows_manager import WindowManager, windows_manager
from src.app.UI.views.list_subjects.list_subjects import GestorMaterias 
from src.app.database import database_manager


MAIN_WINDOW_TAG = "main_window"
SUBJECTS_MANAGER_WINDOW_TAG = "subjects_manager_window"
NEW_SUBJECT_WINDOW_TAG = "new_subject_window"
EXPORT_WINDOW_TAG = "export_window_tag"
SAVE_FILE_WINDOW_TAG = "save_file_window"
IMPORT_DATABASE_WINDOW = "import_database_window"

gestor_materias = GestorMaterias(database_manager)


windows_manager.register_window(gestor_materias)