from src.app.UI.components.windows_manager import windows_manager
from src.app.database import database_manager

from .main_window import MainWindow
from .subjects_manager import SubjectsManager
from .new_subject_window import SubjectRegistrationWindow
from .save_file_window import SaveFileWindow
from .import_database_window import ImportDataBaseWindow
from .schedule_availability_window import ScheduleAvailabilityWindow
from .export_window import ExportWindow

main_window = MainWindow(database_manager)

subjects_manager = SubjectsManager(database_manager)

new_subject_window = SubjectRegistrationWindow(database_manager)

save_file_window = SaveFileWindow(database_manager)

import_database_window = ImportDataBaseWindow(database_manager)

schedule_availability_window = ScheduleAvailabilityWindow(database_manager)

export_window = ExportWindow(database_manager)



windows_manager.register_window(main_window)
windows_manager.register_window(subjects_manager)
windows_manager.register_window(new_subject_window)
windows_manager.register_window(save_file_window)
windows_manager.register_window(import_database_window)
windows_manager.register_window(schedule_availability_window)
windows_manager.register_window(export_window)


