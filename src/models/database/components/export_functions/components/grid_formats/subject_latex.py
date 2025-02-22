import numpy as np

import numpy as np
from typing import List

class SubjectLatex:
    def __init__(self, subject, pcg):
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
        self.name = subject.name
        self.code = subject.code
        self.professor = subject.professor
        self.classroom = subject.classroom
        self.careers = [group.career for group in subject.groups]
        self.semesters = [group.semester for group in subject.groups]
        self.subgroups = [group.subgroup for group in subject.groups]
        self.hours = subject.hours_distribution.total()
        self.color = pcg.subject_colors.colors[subject]
        self.hours_matrix = subject.allocated_subject_matrix
        
        