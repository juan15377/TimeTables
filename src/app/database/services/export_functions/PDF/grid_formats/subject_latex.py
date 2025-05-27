from typing import List

class SubjectLatex:
    def __init__(self, db, id_subject, color):
        """
        Initializes a SubjectLatex instance.

        Parameters:
        - db: Database connection object.
        - id_subject: Subject ID.
        - color: Color in RGBA format.

        Attributes:
        - name: Name of the subject.
        - code: Abbreviation for the subject.
        - professor_name: Name of the professor.
        - professor_id: ID of the professor.
        - classroom_name: Name of the classroom.
        - classroom_id: ID of the classroom.
        - careers_names: List of career names.
        - semesters_names: List of semester names.
        - subgroups_names: List of subgroup names.
        - careers_ids: List of career IDs.
        - semesters_ids: List of semester IDs.
        - subgroups_ids: List of subgroup IDs.
        - hours: Total number of hours.
        - color: Color in RGBA format.
        - hours_matrix: Boolean matrix for the schedule.
        """
        cursor = db.db_connection.cursor()

        # Obtener información de la materia
        cursor.execute("SELECT * FROM SUBJECT WHERE ID = ?", (id_subject,))
        subject_info = cursor.fetchone()
        if not subject_info:
            raise ValueError(f"Subject with ID {id_subject} not found.")

        self.name = subject_info[1]
        self.code = subject_info[2]
        self.hours = subject_info[5]

        # Obtener información del profesor
        cursor.execute("""
            SELECT ID, NAME FROM PROFESSOR 
            WHERE ID IN (SELECT ID_PROFESSOR FROM PROFESSOR_SUBJECT WHERE ID_SUBJECT = ?)
        """, (id_subject,))
        professor = cursor.fetchone()
        if professor:
            self.professor_id, self.professor_name = professor
        else:
            self.professor_id = None
            self.professor_name = "Unknown"

        # Obtener información del aula
        cursor.execute("""
            SELECT ID, NAME FROM CLASSROOM
            WHERE ID IN (SELECT ID_CLASSROOM FROM CLASSROOM_SUBJECT WHERE ID_SUBJECT = ?)
        """, (id_subject,))
        classroom = cursor.fetchone()
        if classroom:
            self.classroom_id, self.classroom_name = classroom
        else:
            self.classroom_id = None
            self.classroom_name = "Unknown"

        # Obtener información de carreras, semestres y subgrupos
        cursor.execute("""
            SELECT A.ID AS ID_GROUP, B.ID AS ID_CAREER, B.NAME AS NAME_CAREER, 
                   C.ID AS ID_SEMESTER, C.NAME AS NAME_SEMESTER, D.ID AS ID_SUBGROUP, D.NAME AS NAME_SUBGROUP
            FROM GROUPS A
            INNER JOIN CAREER B ON A.CAREER = B.ID
            INNER JOIN SEMESTER C ON A.SEMESTER = C.ID
            INNER JOIN SUBGROUP D ON A.SUBGROUP = D.ID
            WHERE A.ID IN (SELECT ID_GROUP FROM GROUP_SUBJECT WHERE ID_SUBJECT = ?)
        """, (id_subject,))
        
        group_data = cursor.fetchall()
        
        self.careers_names = [row[2] for row in group_data]
        self.careers_ids = [row[1] for row in group_data]
        self.semesters_names = [row[4] for row in group_data]
        self.semesters_ids = [row[3] for row in group_data]
        self.subgroups_names = [row[6] for row in group_data]
        self.subgroups_ids = [row[5] for row in group_data]

        # Color y matriz de horarios
        self.color = color
        self.hours_matrix = db.subjects.get_matrix_of_allocated_slots(id_subject)

        cursor.close()
