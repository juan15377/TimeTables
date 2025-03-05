from src.models.database import DataBaseManager

from src.tests.database_example import database_example

database = DataBaseManager()

for i in range(1000):
    database.professors.new(f"{i}")