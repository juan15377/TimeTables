from typing import Dict, Callable
import random
import sqlite3
import numpy as np
import sqlite3
from typing import List

#from .components.export_functions import ExportFunctionsLatex


def insert_default_availability_matrix(type_, id_type, db_concection):
    cursor = db_concection.cursor()
    for row in range(1,31):
        for column in range(1,8):
            if type_ == "PROFESSOR":
                cursor.execute("INSERT INTO PROFESSOR_AVAILABILITY (ID_PROFESSOR, ROW_POSITION, COLUMN_POSITION, VAL) VALUES (?, ?, ?, ?)", (id_type, row, column, True ))
            elif type_ == "CLASSROOM":
                cursor.execute("INSERT INTO CLASSROOM_AVAILABILITY (ID_CLASSROOM, ROW_POSITION, COLUMN_POSITION, VAL) VALUES (?, ?, ?, ?)", (id_type, row, column, True ))
            else:
                cursor.execute("INSERT INTO GROUP_AVAILABILITY (ID_GROUP, ROW_POSITION, COLUMN_POSITION, VAL) VALUES (?, ?, ?, ?)", (id_type, row, column, True )) 
    cursor.close()
    db_concection.commit()

def delete_subjects_before_delete(type_, db_connection, id_type):
    cursor = db_connection.cursor()

    valid_types = {"PROFESSOR", "CLASSROOM", "GROUP"}
    if type_ not in valid_types:
        raise ValueError("Tipo no válido")

    query = f"DELETE FROM SUBJECT WHERE ID IN (SELECT ID_SUBJECT FROM {type_}_SUBJECT WHERE ID_{type_} = ?)"
    print(query)
    cursor.execute(query, (id_type,))


    db_connection.commit()


def delete_subject_slots_after_update_availability(db_connection, type_, id_type, row_position, column_position, val):
    cursor = db_connection.cursor()

    valid_types = {"PROFESSOR", "CLASSROOM", "GROUP"}
    if type_ not in valid_types:
        raise ValueError("Tipo no válido")
    
    cursor = db_connection.cursor()
    # si el cambio en la nueva posicion insersecta con algunos de los bloques entonces se debe eliminar
    cursor.execute(f"""DELETE FROM SUBJECT_SLOTS WHERE ID_SUBJECT IN (SELECT ID_{type_} FROM {type_}_SUBJECT WHERE ID_{type_} = {id_type}) 
                   AND COLUMN_POSITION = {column_position}
                   AND {row_position} BETWEEN ROW_POSITION AND ROW_POSITION +  LEN-1
                   AND NOT {"TRUE" if val else "FALSE"}""")

    db_connection.commit()


class BaseManager:

    def __init__(self, type_, db_connection):
        self.db_connection = db_connection 

        valid_types = {"PROFESSOR", "CLASSROOM", "GROUP"}
        if type_ not in valid_types:
            raise ValueError("Tipo no válido")

        self.type_ = type_ 

    def new(self, name):

        cursor = self.db_connection.cursor()

        
        if self.type_ == "GROUP":
            cursor.execute(f"INSERT INTO {self.type_}S (NAME) VALUES (?)", (name,))
        else:
            cursor.execute(f"INSERT INTO {self.type_} (NAME) VALUES (?)", (name,))
            
        self.db_connection.commit()


        new_type_id = cursor.lastrowid

        insert_default_availability_matrix(self.type_, new_type_id, self.db_connection)

    def remove(self, id_type):

        delete_subjects_before_delete(self.type_, self.db_connection, id_type)
        if id_type is None:
            return None 
        
        cursor = self.db_connection.cursor()
        try:
            if self.type_ == "GROUP":
                query = f"DELETE FROM GROUPS WHERE ID = {id_type}"
                print(query)
                cursor.execute(query)
                return None
            query = f"DELETE FROM {self.type_} WHERE ID = {id_type}"
            print(query)
            cursor.execute(query)
            self.db_connection.commit()
            
        except:
            self.db_connection.rollback()
            



    def update_availability(self, id_type, row_position, column_position, new_val):

        cursor = self.db_connection.cursor()
        query = f"""
            UPDATE {self.type_}_AVAILABILITY
            SET VAL = {"TRUE" if new_val else "FALSE"}
            WHERE ID_{self.type_} = {id_type} AND 
                ROW_POSITION = {row_position} AND 
                COLUMN_POSITION = {column_position}
        """

        cursor.execute(query)

        self.db_connection.commit()


        delete_subject_slots_after_update_availability(self.db_connection, self.type_, id_type, row_position, column_position, new_val)


        pass

    def get_subject_color(self, id_subject):
        
        if id_subject == None:
            return None
        cursor = self.db_connection.cursor()

        cursor.execute(f"""
            SELECT RED, GREEN, BLUE 
            FROM {self.type_}_COLORS WHERE ID_SUBJECT = {id_subject}
        """)

        results = cursor.fetchall()
        return results[0]

        
    def set_subject_color(self, id, id_subject, red, green, blue):
        cursor = self.db_connection.cursor()

        query = f"""
            UPDATE {self.type_}_COLORS 
            SET RED = ?, GREEN = ?, BLUE = ?
            WHERE ID_SUBJECT = ? AND ID_{self.type_} = ?
        """
        cursor.execute(query, (red, green, blue, id_subject, id))

        self.db_connection.commit()


    def get_name(self, id):
        cursor = self.db_connection.cursor()

        cursor.execute(f"""
            SELECT NAME FROM {self.type_} 
            WHERE ID = {id}
        """
        )

        result = cursor.fetchone()[0]
        cursor.close()
        
        return result
    
    def get_subjects(self, id):

        cursor = self.db_connection.cursor()

        query = f"""
            SELECT ID_SUBJECT FROM {self.type_}_SUBJECT 
            WHERE ID_{self.type_} = ?
        """
        cursor.execute(query, (id,))
        result = [row[0] for row in cursor.fetchall()]
        cursor.close()
        
        return result
    
    
    def get(self):
        cursor = self.db_connection.cursor()

        cursor.execute(f"""
            SELECT ID FROM {self.type_}
        """)
        
        result = list(map(lambda x : x[0], cursor.fetchall()))
        
        cursor.close()
        
        return result
    
    def restart_subjects_slots(self, id_type):
        cursor = self.db_connection.cursor()
        
        cursor.execute(f"""
        DELETE FROM SUBJECT_SLOTS
        WHERE ID_SUBJECT IN (
                        SELECT ID_SUBJECT 
                        FROM {self.type_}_SUBJECT
                        WHERE ID_{self.type_} = {id_type}
                    )    
        """)
        
        cursor.close()
        
        self.db_connection.commit()
        
        
        

class ProfessorsManager(BaseManager): 

    def __init__(self, db_connection):
        self.db_connection = db_connection
        super().__init__("PROFESSOR", db_connection)
        pass  



class ClassroomManager(BaseManager): 

    def __init__(self, db_connection):
        self.db_connection = db_connection
        super().__init__("CLASSROOM", db_connection)
        pass  
  
  

class BaseElementsGroupManager:

    def __init__(self, db_connection, type_):

        valid_types = {"CAREER", "SEMESTER", "SUBGROUP"}
        if type_ not in valid_types:
            raise ValueError("Tipo no válido")

        self.type_ = type_ 
        self.db_connection = db_connection

        pass  

    def new(self, name):

        cursor = self.db_connection.cursor() 

        cursor.execute(f"INSERT INTO {self.type_} (NAME) VALUES (?)", (name,))
        
        cursor.close()

        self.db_connection.commit()

        pass  

    def get(self):
        pass 

class CareersManager(BaseElementsGroupManager):

    def __init__(self, db_connection):

        super().__init__(db_connection, "CAREER") 


class SemestersManager(BaseElementsGroupManager):

    def __init__(self, db_connection):

        super().__init__(db_connection, "SEMESTER") 


class SubgroupsManager(BaseElementsGroupManager):

    def __init__(self, db_connection):

        super().__init__(db_connection, "SUBGROUP") 



def check_exists_group(db_connection, id_career, id_semester, id_subgroup):
    cursor = db_connection.cursor()

    # Usamos parámetros en lugar de concatenar directamente las variables
    cursor.execute(
        "SELECT 1 FROM GROUPS WHERE CAREER = ? AND SEMESTER = ? AND SUBGROUP = ?",
        (id_career, id_semester, id_subgroup)
    )

    first_row = cursor.fetchone()
    
    cursor.close()

    # Si first_row es None, no existe; si tiene un valor, entonces existe
    return first_row is not None


class GroupsManager(BaseManager): 

    def __init__(self, db_connection):

        self.db_connection = db_connection

        super().__init__("GROUP", db_connection)

        self.careers = CareersManager(db_connection)
        self.semesters = SemestersManager(db_connection)
        self.subgroups = SubgroupsManager(db_connection)

    def new(self, id_career, id_semester, id_subgroup):
        cursor = self.db_connection.cursor()

        # Verifica el valor de self.type_ antes de ejecutar la consulta

        if check_exists_group(self.db_connection, id_career, id_semester, id_subgroup):
            return None 

        cursor.execute(f"INSERT INTO {self.type_}S (CAREER, SEMESTER, SUBGROUP) VALUES (?, ?, ?)", (id_career, id_semester, id_subgroup))

        cursor.close()
        
        self.db_connection.commit()

        new_type_id = cursor.lastrowid

        insert_default_availability_matrix(self.type_, new_type_id, self.db_connection)

    def get_name(self, id):
        """El nombre es igual a la unión del nombre de la carrera, semestre y subgrupo"""
        
        cursor = self.db_connection.cursor()

        cursor.execute("""
            SELECT B.NAME || ' ' || C.NAME || ' ' || D.NAME
            FROM GROUPS A
            INNER JOIN CAREER B ON A.CAREER = B.ID
            INNER JOIN SEMESTER C ON A.SEMESTER = C.ID
            INNER JOIN SUBGROUP D ON A.SUBGROUP = D.ID
            WHERE A.ID = ?
        """, (id,))  # <-- nota la coma aquí

        result = cursor.fetchone()
        
        cursor.close()
        
        return result[0] if result else None

    
    def get(self):
        cursor = self.db_connection.cursor()

        cursor.execute(f"""
            SELECT ID FROM {self.type_}S
        """)
        
        result = list(map(lambda x : x[0], cursor.fetchall()))
        
        cursor.close()

        return result