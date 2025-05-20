from src.app.database import database_manager 


#database_manager.import_database("/home/juan/Música/backup.db")

database_manager.subjects.new(
    "Matematicas Actuariales",
    "MATACT",
    2,
    2,
    [4],
    1,
    4,
    20,
    True
)
#database_manager.subjects.new_slot(1, 1, 1, 3)

print(database_manager.subjects.get_strong_constraints_matrix(2))
print(database_manager.subjects.get_weak_constraints_matrix(2))