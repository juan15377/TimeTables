from ..core import db_connection, DB_PATH

import sqlite3
from .services import ExportFunctions
        
from .professors_classrooms_groups_manager import ProfessorsManager, ClassroomManager, GroupsManager
from .subjects_manager import SubjectsManager 

class DataBaseManager:

    def __init__(self, db_connection):
        self.__db_connection = db_connection

        def is_intersect(row_1, t1, row_2, t2):
            if row_1 == row_2:
                return True
            elif row_1 > row_2:
                return row_2 + t2 > row_1
            else:
                return row_1 + t1 > row_2

        # Conectar a SQLite

        # Registrar la función en SQLite
        self.__db_connection.create_function("is_intersect", 4, is_intersect)


        cursor = self.__db_connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.close()

        self.professors = ProfessorsManager(self.__db_connection)
        self.classrooms = ClassroomManager(self.__db_connection)
        self.groups = GroupsManager(self.__db_connection)

        self.subjects = SubjectsManager(self.__db_connection)

        self.export = ExportFunctions(self)

    def restart(self):
        cursor = self.__db_connection.cursor()

        cursor.execute("""
            DELETE FROM PROFESSOR;
        """)

        cursor.execute("""
            DELETE FROM CLASSROOM;
        """)

        cursor.execute("""
            DELETE FROM CAREER;
        """)

        cursor.execute("""
            DELETE FROM SEMESTER;
        """)

        cursor.execute("""
            DELETE FROM SUBGROUP;
        """)

        self.__db_connection.commit()
        
    def backup(self, file_path):
        destino = sqlite3.connect(file_path)

        # Hacer backup
        with destino:
            self.__db_connection.backup(destino)

        destino.close()
        
    def execute_query(self, query, parameters=None):
        cursor = self.__db_connection.cursor()
        try:
            if parameters is None:
                cursor.execute(query)
            else:
                cursor.execute(query, parameters)
            return cursor
        except Exception as e:
            raise Exception(f"Database query failed: {e}")

        
    def import_database(self, database_path):
        try:
            self.restart()  # reinicia la base de datos

            src_db = database_path
            dest_db = DB_PATH

            # Conectarse a la base de datos destino
            conn = sqlite3.connect(dest_db)
            cursor = conn.cursor()

            # Adjuntar la base de datos origen como un alias
            cursor.execute(f"ATTACH DATABASE '{src_db}' AS origen")

            # Obtener la lista de tablas compartidas entre ambas
            tables = cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name IN "
                "(SELECT name FROM origen.sqlite_master WHERE type='table')"
            ).fetchall()

            if not tables:
                print("No se encontraron tablas compartidas entre las bases de datos.")
                return

            # Copiar los datos tabla por tabla
            for (table,) in tables:
                print(f"Copiando datos de la tabla: {table}")
                query = f"""
                    INSERT OR IGNORE INTO main.{table}
                    SELECT * FROM origen.{table}
                """
                cursor.execute(query)

            # Finalizar
            conn.commit()

        except sqlite3.Error as e:
            print(f"Error al trabajar con la base de datos: {e}")
            conn.rollback()  # Revertir en caso de error
        finally:
            # Detach y cerrar conexión
            cursor.execute("DETACH DATABASE origen")
            conn.close()



#db.professors.new("Gerardo")
#db.classrooms.new("Aula 2")
#db.groups.subgroups.new("Grupo C")
#db.groups.new(1, 1, 3)
#db.subjects.new("Calculo",
#                "CAL",
#                2,
#                2,
#                [2],
#                1,
#                4,
#                10)

database_manager = DataBaseManager(db_connection)

#db.subjects.new_slot(4, 3, 4, 2)