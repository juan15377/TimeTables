from src.app.database import database_manager 

#for i in range(1000):
#    database_manager.professors.new(str(i))
#    

cursor = database_manager.db_connection.cursor()

cursor.execute("""
 DELETE FROM SUBJECT_SLOTS               
""")

database_manager.db_connection.commit()
