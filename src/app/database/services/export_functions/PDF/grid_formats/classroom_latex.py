
from .symbology import SymbologyLatex
from .schedule_grid import GridLatex
from .subject_latex import SubjectLatex

class ClassroomLatex:
    def __init__(self, db, id_classroom):
        self.id_classroom = id_classroom
        self.db = db  

        self.name = self.db.classrooms.get_name(id_classroom)
        self.subjects_ids = self.db.classrooms.get_subjects(id_classroom)

    def create_template_string(self):
        """Create the LaTeX string for the grid and symbolic representation of the subjects."""
        grid = GridLatex()
        symbology = SymbologyLatex()
        symbology.type = 3  # Type 3: classroom view

        for id_subject in self.subjects_ids:
            color = self.db.classrooms.get_subject_color(id_subject)
            subject_latex = SubjectLatex(self.db, id_subject, color)
            grid.add_subject(subject_latex)
            symbology.add_subject(subject_latex)

        grid_string = grid.compile_to_latexstring()
        symbol_string = symbology.to_latex_string()

        template = f"""
        \\subsection{{{self.name}}}
        \\vspace*{{.1cm}}
        
        \\begin{{flushright}}
            {{\\LARGE \\textbf{{Classroom}}: {self.name}}}
        \\end{{flushright}}
        \\vspace{{1cm}}

        {grid_string}

        {symbol_string}

        \\newpage
        """
        return template


def create_classrooms_latex(db, ids_classrooms = None):


    cursor = db.execute_query("""
        SELECT ID FROM CLASSROOM
    """)

    if ids_classrooms == None:
        classrooms_latex = [ClassroomLatex(db, id_classroom[0]) for id_classroom in cursor.fetchall()]
    else:
        classrooms_latex = [ClassroomLatex(db, id_classroom[0]) for id_classroom in cursor.fetchall() if id_classroom[0] in ids_classrooms]


    """Create the LaTeX string for all classrooms."""
    result = "\\section{Classrooms} \n"
    for classroom in classrooms_latex:
        template = classroom.create_template_string()
        result += f"{template}\n"
    return result
