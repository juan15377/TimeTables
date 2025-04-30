from ..core import db_connection, DB_PATH

from typing import Dict, Callable
import random
import sqlite3
import numpy as np
from typing import Dict, Callable, List



def get_available_slots(min_slots: float, max_slots: float, sum_slots: float) -> List[int]:
    if sum_slots < min_slots:
        return [0]  # Devuelve 0 si no hay suficientes slots disponibles

    possible_slots = list(range(int(min_slots), int(max_slots) + 1))

    available_slots = [
        value for value in possible_slots
        if (sum_slots - value == 0) or (sum_slots - value >= min_slots and value <= sum_slots)
    ]

    return available_slots

def get_available_slots_subject(db_connection, id_subject: int) -> List[int]:
    cursor = db_connection.cursor()

    # Obtener total de slots asignados a la materia
    cursor.execute("SELECT TOTAL_SLOTS, MINIMUM_SLOTS, MAXIMUM_SLOTS FROM SUBJECT WHERE ID = ?", (id_subject,))
    result = cursor.fetchone()

    if result is None:
        return []  # Si no se encuentra la materia, retorna una lista vacía

    total_slots, min_slots, max_slots = result

    # Obtener la suma de slots ya utilizados
    cursor.execute("SELECT COALESCE(SUM(LEN), 0) FROM SUBJECT_SLOTS WHERE ID_SUBJECT = ?", (id_subject,))
    used_slots = cursor.fetchone()[0]

    cursor.close()
    # Calcular los slots disponibles
    return get_available_slots(min_slots, max_slots, total_slots - used_slots)

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


def check_availability_subjects_by_new_slot(db_connection, row_position, column_position, len_slot, ids_subjects):
    # Asegurar que sea lista de enteros
    if isinstance(ids_subjects, str):
        ids_subjects = [int(x.strip()) for x in ids_subjects.split(',')]

    if not ids_subjects:
        return False

    placeholders = ','.join(['?'] * len(ids_subjects))

    query = f"""
    SELECT * FROM SUBJECT_SLOTS A
    WHERE (
        ? BETWEEN A.ROW_POSITION AND A.ROW_POSITION + A.LEN -1 -- SI INICIA DESDE EL BLOQUE YA LO INTERSECTA
        OR ? + ? -1 BETWEEN A.ROW_POSITION AND A.ROW_POSITION + A.LEN -1 
    )
    AND A.COLUMN_POSITION = ?
    AND A.ID_SUBJECT IN ({placeholders})
    """

    params = [
        row_position, 
        row_position, len_slot,
        column_position
    ] + ids_subjects
    

    cursor = db_connection.cursor()
    cursor.execute(query, params)      
    result =   cursor.fetchone() is None
    cursor.close()
    
    return result 

def check_availability_slot_under_professor(db_connection, row_pos: int, column_pos: int, len_slot: int, id_professor: int) -> bool:
    cursor = db_connection.cursor()

    # ! Restricciones fuertes 
    # Verificar si el profesor tiene disponibilidad en el horario solicitado
    query = """
    SELECT 1 FROM PROFESSOR_AVAILABILITY A
    WHERE A.ID_PROFESSOR = ?
    AND A.COLUMN_POSITION = ?
    AND A.VAL = FALSE
    AND A.ROW_POSITION BETWEEN ? AND ?
    """

    cursor.execute(query, (id_professor, column_pos, row_pos, row_pos + len_slot - 1))

    if cursor.fetchone() is None:  # No encontró restricciones de disponibilidad
        # Obtener los IDs de las materias del profesor
        query = """
        SELECT GROUP_CONCAT(A.ID_SUBJECT) FROM PROFESSOR_SUBJECT A
        WHERE A.ID_PROFESSOR = ?
        """
        cursor.execute(query, (id_professor,))
        subject_ids = cursor.fetchone()[0]

        if subject_ids and check_availability_subjects_by_new_slot(db_connection, row_pos, column_pos, len_slot, subject_ids):
            cursor.close()
            
            return True
        else:
            cursor.close()
            
            print("no se pudo")
            return False
    else:
        raise Exception(f"El profesor con ID = {id_professor} no cumple con la disponibilidad.")

    return False

def check_availability_slot_under_classroom(db_connection, row_pos: int, column_pos: int, len_slot: int, id_classroom: int) -> bool:
    cursor = db_connection.cursor()

    # ! Restricciones fuertes 
    # Verificar si el aula está disponible en el horario solicitado
    query = """
    SELECT 1 FROM CLASSROOM_AVAILABILITY A
    WHERE A.ID_CLASSROOM = ?
    AND A.COLUMN_POSITION = ?
    AND A.VAL = FALSE
    AND A.ROW_POSITION BETWEEN ? AND ?
    """
    
    cursor.execute(query, (id_classroom, column_pos, row_pos, row_pos + len_slot - 1))
    result = cursor.fetchone()
    if result is None:  # No encontró restricciones de disponibilidad
        # Obtener los IDs de las materias asignadas al aula
        query = """
        SELECT GROUP_CONCAT(A.ID_SUBJECT) FROM CLASSROOM_SUBJECT A
        WHERE A.ID_CLASSROOM = ?
        """
        cursor.execute(query, (id_classroom,))
        subject_ids = cursor.fetchone()[0]

        if subject_ids and check_availability_subjects_by_new_slot(db_connection, row_pos, column_pos, len_slot, subject_ids):
            return True
        else:
            return False
    else:
        raise Exception(f"El aula con ID = {id_classroom} no cumple con la disponibilidad.")

    return False

def check_availability_slot_under_group(db_connection, row_pos: int, column_pos: int, len_slot: int, id_group: int) -> bool:
    cursor = db_connection.cursor()

    # ! Restricciones fuertes 
    # Verificar si el grupo está disponible en el horario solicitado
    query = """
    SELECT 1 FROM GROUP_AVAILABILITY A
    WHERE A.ID_GROUP = ?
    AND A.COLUMN_POSITION = ?
    AND A.VAL = FALSE
    AND A.ROW_POSITION BETWEEN ? AND ?
    """
    
    cursor.execute(query, (id_group, column_pos, row_pos, row_pos + len_slot - 1))

    if cursor.fetchone() is None:  # No encontró restricciones de disponibilidad
        # Obtener los IDs de las materias asignadas al grupo
        query = """
        SELECT GROUP_CONCAT(A.ID_SUBJECT) FROM GROUP_SUBJECT A
        WHERE A.ID_GROUP = ?
        """
        cursor.execute(query, (id_group,))
        subject_ids = cursor.fetchone()[0]

        if subject_ids and check_availability_subjects_by_new_slot(db_connection, row_pos, column_pos, len_slot, subject_ids):
            return True
        else:
            return False
    else:
        raise Exception(f"El grupo con ID = {id_group} no cumple con la disponibilidad.")

    return False


def insert_color_of_new_subject(db_connection: str, id_professor: int, id_classroom: int, ids_groups: str, id_subject: int):
    """
    Inserta colores aleatorios para un nuevo sujeto/profesor/aula/grupo
    
    Args:
        db_path: Ruta a la base de datos SQLite
        id_professor: ID del profesor
        id_classroom: ID del aula
        ids_groups: Cadena JSON con array de IDs de grupos (ej. '[1, 2, 3]')
        id_subject: ID del sujeto/materia
    """
    cursor = db_connection.cursor()

    range_red_l, range_red_u = 100, 255
    range_green_l, range_green_u = 100, 255
    range_blue_l, range_blue_u = 100, 255

    def generate_color():
        return (random.randint(range_red_l, range_blue_u),
                random.randint(range_green_l, range_green_u),
                random.randint(range_blue_l, range_blue_u))

    prof_red, prof_green, prof_blue =  generate_color()

    cursor.execute("""
        INSERT INTO PROFESSOR_COLORS(ID_PROFESSOR, ID_SUBJECT, RED, GREEN, BLUE)
        VALUES (?, ?, ?, ?, ?)
        """, (id_professor, id_subject, prof_red, prof_green, prof_blue))

    room_red, room_green, room_blue = generate_color()

    cursor.execute("""
            INSERT INTO CLASSROOM_COLORS(ID_CLASSROOM, ID_SUBJECT, RED, GREEN, BLUE)
            VALUES (?, ?, ?, ?, ?)
        """, (id_classroom, id_subject, room_red, room_green, room_blue))

    for id_group in ids_groups:
            group_red, group_green, group_blue = generate_color()

            cursor.execute("""
                    INSERT INTO GROUP_COLORS(ID_GROUP, ID_SUBJECT, RED, GREEN, BLUE)
                    VALUES (?, ?, ?, ?, ?)
                """, (id_group, id_subject, group_red, group_green, group_blue))

    db_connection.commit()
    print("Se completo la inserccion del color")

class SubjectsManager: 
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def new(self, name, code, id_professor, id_classroom, ids_groups, min_slots, max_slots, total_slots):
        cursor = self.db_connection.cursor()
        try:
            # Insertar la materia
            cursor.execute(
                "INSERT INTO SUBJECT (NAME, CODE, MINIMUM_SLOTS, MAXIMUM_SLOTS, TOTAL_SLOTS) VALUES (?, ?, ?, ?, ?) RETURNING ID",
                (name, code, min_slots, max_slots, total_slots)
            )
            id_new_subject = cursor.fetchone()[0]

            cursor.execute("INSERT INTO PROFESSOR_SUBJECT (ID_PROFESSOR, ID_SUBJECT) VALUES (?, ?)", 
                           (id_professor, id_new_subject))
            cursor.execute("INSERT INTO CLASSROOM_SUBJECT (ID_CLASSROOM, ID_SUBJECT) VALUES (?, ?)", 
                           (id_classroom, id_new_subject))

            for id_group in ids_groups:
                cursor.execute("INSERT INTO GROUP_SUBJECT (ID_GROUP, ID_SUBJECT) VALUES (?, ?)", (id_group, id_new_subject))

            insert_color_of_new_subject(self.db_connection, id_professor, id_classroom, ids_groups, id_new_subject)

            # Confirmar transacción
            
            self.db_connection.commit()

        except sqlite3.Error as e:
            print(f"Error en la inserción: {e}")
            self.db_connection.rollback()
        finally:
            cursor.close()


    def remove(self, id_subject):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("DELETE FROM SUBJECT WHERE ID = ?", (id_subject,))
            self.db_connection.commit()
        except sqlite3.Error as e:
            print(f"Error al eliminar la materia: {e}")
            self.db_connection.rollback()
        finally:
            cursor.close()

    def new_slot(self, id_subject, row_position, column_position, len_slot):
        # checar primero si el tamaño de slot es viable bajo las condiciones de la materia

        cursor = self.db_connection.cursor()
        

        if not len_slot in get_available_slots_subject(self.db_connection, id_subject):
            print("El tamaño del slot no cumple con los requerimientos")
            print(len_slot)
            print(get_available_slots_subject(self.db_connection, id_subject))
            return None

        cursor.execute(F"""
                SELECT ID_PROFESSOR
                FROM PROFESSOR_SUBJECT
                WHERE ID_SUBJECT = {id_subject}
                """)
        id_professor = cursor.fetchall()[0][0]


        cursor.execute(F"""
                SELECT ID_CLASSROOM
                FROM CLASSROOM_SUBJECT
                WHERE ID_SUBJECT = {id_subject}
                """)
        
        id_classroom =  cursor.fetchall()[0][0]


        cursor.execute(F"""
                SELECT ID_GROUP
                FROM GROUP_SUBJECT
                WHERE ID_SUBJECT = {id_subject}
                """)
        
        ids_groups = [id_group[0] for id_group in cursor.fetchall()]

        print(check_availability_slot_under_professor(self.db_connection,
                                                       row_position,
                                                       column_position,
                                                       len_slot,
                                                       id_professor))
    
        if not check_availability_slot_under_professor(self.db_connection,
                                                       row_position,
                                                       column_position,
                                                       len_slot,
                                                       id_professor):
            return None 
        
        if not check_availability_slot_under_classroom(self.db_connection,
                                                       row_position,
                                                       column_position,
                                                       len_slot,
                                                       id_classroom):
            return None
        
        for id_group in ids_groups:

            if not check_availability_slot_under_group(self.db_connection,
                                                       row_position,
                                                       column_position,
                                                       len_slot,
                                                       id_group):
                return None 
            
        cursor.execute("""
                INSERT INTO SUBJECT_SLOTS(ID_SUBJECT, ROW_POSITION, COLUMN_POSITION, LEN) VALUES (?, ?, ?, ?);
                       """, (id_subject, row_position, column_position, len_slot))
        
        id_new_slot = cursor.lastrowid

        self.db_connection.commit()
        cursor.close()
        
        print("Nueva slot insertado")
        return id_new_slot
    
    def remove_slot(self, id_slot):
        cursor = self.db_connection.cursor()
        cursor.execute(f"""
            DELETE FROM SUBJECT_SLOTS
            WHERE ID_SLOT = {id_slot}   
        """)
        cursor.close()

        self.db_connection.commit()

    def get_matrix_of_allocated_slots(self, id_subject):
        initial_matrix = np.full((30,7), False)

        # filtro todos los slots de esta materia

        cursor = self.db_connection.cursor()

        cursor.execute(f"""
            SELECT * FROM SUBJECT_SLOTS
            WHERE ID_SUBJECT = {id_subject}
        """)

        slots_subject = cursor.fetchall()
        print(slots_subject)

        for slot in slots_subject:
            row_position = slot[2]
            column_position = slot[3]
            len_slot = slot[4]
            
            initial_matrix[row_position-1:row_position+len_slot-1, column_position-1] = True
        
        cursor.close()
        
        return initial_matrix
        
    def get_allowed_slots(self, id_subject):
        return get_available_slots_subject(self.db_connection, id_subject)
    
    def get_strong_constraints_matrix(self, id_subject):
        
        query = """
        SELECT P_A.ROW_POSITION, P_A.COLUMN_POSITION, MIN(P_A.VAL, C_A.VAL, G_A.VAL) AS VAL
        FROM (
            SELECT ROW_POSITION, COLUMN_POSITION, VAL
            FROM PROFESSOR_AVAILABILITY
            WHERE ID_PROFESSOR IN (SELECT ID_PROFESSOR FROM PROFESSOR_SUBJECT WHERE ID_SUBJECT = ?)
            ) AS P_A
        LEFT JOIN (
            SELECT ROW_POSITION, COLUMN_POSITION, VAL
            FROM CLASSROOM_AVAILABILITY
            WHERE ID_CLASSROOM IN (SELECT ID_CLASSROOM FROM CLASSROOM_SUBJECT WHERE ID_SUBJECT = ?)
            ) AS C_A ON P_A.ROW_POSITION = C_A.ROW_POSITION AND P_A.COLUMN_POSITION = C_A.COLUMN_POSITION
        LEFT JOIN (
            SELECT 
                ROW_POSITION, 
                COLUMN_POSITION, 
                MIN(CASE WHEN VAL = 1 THEN 1 ELSE 0 END) AS VAL
            FROM 
                GROUP_AVAILABILITY
            WHERE 
                ID_GROUP IN (SELECT ID_GROUP FROM GROUP_SUBJECT WHERE ID_SUBJECT = ?)
            GROUP BY 
                ROW_POSITION, COLUMN_POSITION
        ) AS G_A ON P_A.ROW_POSITION = G_A.ROW_POSITION AND P_A.COLUMN_POSITION = G_A.COLUMN_POSITION
        ORDER BY P_A.ROW_POSITION, P_A.COLUMN_POSITION;
        
        """
        
        initial_matrix = np.full((30,7), False)

        # filtro todos los slots de esta materia

        cursor = self.db_connection.cursor()

        cursor.execute(query, (id_subject, id_subject, id_subject))

        cells_availability = cursor.fetchall()

        for cell in cells_availability:
            row_position = cell[0]
            column_position = cell[1]
            val = cell[2]
            
            initial_matrix[row_position-1, column_position-1] = val
        
        cursor.close()
        
        return initial_matrix
        pass  
    
    def get_weak_constraints_matrix(self, id_subject):
        cursor = self.db_connection.cursor()

        # Obtener ID del profesor - CORRECCIÓN PRINCIPAL
        cursor.execute("""
        SELECT ID
        FROM PROFESSOR
        WHERE ID IN (SELECT ID_PROFESSOR FROM PROFESSOR_SUBJECT WHERE ID_SUBJECT = ?)
        """, (id_subject,))
        professor_row = cursor.fetchone()
        id_professor = professor_row[0] if professor_row else None

        # Obtener ID del aula
        cursor.execute("""
        SELECT ID
        FROM CLASSROOM
        WHERE ID IN (SELECT ID_CLASSROOM FROM CLASSROOM_SUBJECT WHERE ID_SUBJECT = ?)
        """, (id_subject,))
        classroom_row = cursor.fetchone()
        id_classroom = classroom_row[0] if classroom_row else None

        # Obtener IDs de grupos
        cursor.execute("""
        SELECT ID
        FROM GROUPS
        WHERE ID IN (SELECT ID_GROUP FROM GROUP_SUBJECT WHERE ID_SUBJECT = ?)
        """, (id_subject,))
        ids_groups = [row[0] for row in cursor.fetchall()]  # fetchall() siempre devuelve una lista (puede estar vacía)

        # Resto del código permanece igual como en la corrección anterior...
        # Obtener slots del profesor
        cursor.execute("""
        SELECT ROW_POSITION, COLUMN_POSITION, LEN
        FROM SUBJECT_SLOTS
        WHERE ID_SUBJECT IN (
            SELECT ID_SUBJECT 
            FROM PROFESSOR_SUBJECT 
            WHERE ID_PROFESSOR = ?
        )
        """, (id_professor,))
        slots_professor = cursor.fetchall() or []

        # Obtener slots del aula
        cursor.execute("""
        SELECT ROW_POSITION, COLUMN_POSITION, LEN
        FROM SUBJECT_SLOTS
        WHERE ID_SUBJECT IN (
            SELECT ID_SUBJECT 
            FROM CLASSROOM_SUBJECT 
            WHERE ID_CLASSROOM = ?
        )
        """, (id_classroom,))
        slots_classroom = cursor.fetchall() or []

        # Obtener slots de los grupos
        if ids_groups:
            groups_placeholders = ','.join(['?'] * len(ids_groups))
            cursor.execute(f"""
            SELECT ROW_POSITION, COLUMN_POSITION, LEN
            FROM SUBJECT_SLOTS
            WHERE ID_SUBJECT IN (
                SELECT ID_SUBJECT 
                FROM GROUP_SUBJECT 
                WHERE ID_GROUP IN ({groups_placeholders})
            )
            """, ids_groups)
            slots_groups = cursor.fetchall() or []
        else:
            slots_groups = []

        # Combinar todos los slots
        total_slots = slots_professor + slots_classroom + slots_groups

        # Crear matriz inicial
        initial_matrix = np.full((30, 7), True)

        # Procesar slots para marcar como no disponibles
        for slot in total_slots:
            row_position = slot[0]  # Primer elemento es ROW_POSITION
            column_position = slot[1]  # Segundo es COLUMN_POSITION
            len_slot = slot[2]  # Tercero es LEN

            # Asegurar que los índices estén dentro de los límites
            start_row = max(0, row_position - 1)
            end_row = min(30, start_row + len_slot)
            col = max(0, min(6, column_position - 1))

            initial_matrix[start_row:end_row, col] = False

        cursor.close()

        return initial_matrix

        pass 
        
