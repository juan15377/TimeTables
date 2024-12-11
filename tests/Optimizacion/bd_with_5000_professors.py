from src.Logic.Bd import BD

db = BD()

for i in range(300):
    db.professors.new(f"{i}")

db.save_db("/home/juan/Escritorio/5000_professors.pickle")