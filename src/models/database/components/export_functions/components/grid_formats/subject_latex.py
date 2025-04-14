import numpy as np

import numpy as np
from typing import List

class SubjectLatex:
    def __init__(self, db, id_subject, color):

        """
        Initializes a Materiatex instance.
        Parameters:
        - name: Name of the subject.
        - code: Abbreviation for the subject.
        - professor: Name of the professor.
        - classroom: Classroom location.
        - careers: List of careers.
        - semesters: List of semesters.
        - groups: List of groups.
        - hours: Total number of hours.
        - color: Color in RGBA format.
        - hours_matrix: Boolean matrix for the schedule.
        """

        cursor = db.db_connection.cursor.execute(f"""
            SELECT * FROM SUBJECT 
            WHERE ID = {id_subject} 
            """
        )

        subject_info = cursor.fetchall()[0]

        name = subject_info[0]
        
        self.name = subject_info[1]
        self.code = subject_info[2]
        self.professor = subject.professor
        self.classroom = subject.classroom
        self.careers = [group.career for group in subject.groups]
        self.semesters = [group.semester for group in subject.groups]
        self.subgroups = [group.subgroup for group in subject.groups]
        self.hours = subject_info[5]
        self.color = color
        self.hours_matrix = db.subjects.get_matrix_of_allocated_slots(id_subject)
        
        