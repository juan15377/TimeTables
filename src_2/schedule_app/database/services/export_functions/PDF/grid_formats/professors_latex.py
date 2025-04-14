from .symbology import SymbologyLatex
from .schedule_grid import GridLatex
from .subject_latex import SubjectLatex


class ProfessorLatex:
    def __init__(self, db, id_professor):
        self.id_professor = id_professor 
        self.db = db
        # obtener la informacion del professor

        self.name = db.professors.get_name(id_professor)
        self.subjects_ids = db.professors.get_subjects(id_professor)
        print("ids_subjects = ", self.subjects_ids)

    def add_subject(self, subject):
        """Add a subject to the professor's list of subjects."""
        self.subjects.append(subject)


    def create_template_string(self):
        """Create the LaTeX string for the grid and the symbolic representation of the subjects."""
        grid = GridLatex()
        symbol = SymbologyLatex()
        symbol.type = 1  # Type 1: professor view

        for id_subject in self.subjects_ids:
            color = self.db.professors.get_subject_color(id_subject)
            subject_latex = SubjectLatex(self.db, id_subject, color) 
            
            grid.add_subject(subject_latex) 
            symbol.add_subject(subject_latex) 

        grid_string = grid.compile_to_latexstring()
        symbol_string = symbol.to_latex_string()

        template = f"""
        \\subsection{{{self.name}}}
        \\vspace*{{.1cm}}
        
        \\begin{{flushright}}
            {{\\LARGE \\textbf{{Professor}}: {self.name}}}
        \\end{{flushright}}
        \\vspace{{1cm}}

        {grid_string}

        {symbol_string}

        \\newpage
        """
        return template


def create_professors_latex(db, ids_professors=None):

    cursor = db.db_connection.cursor()

    cursor.execute("""
        SELECT ID FROM PROFESSOR
    """)
    
    if ids_professors == None:
        professors_latex = [ProfessorLatex(db, id_professor[0]) for id_professor in cursor]
    else:
        professors_latex = [ProfessorLatex(db, id_professor[0]) for id_professor in cursor if id_professor[0] in ids_professors]
        
    """Create the LaTeX string for all professors."""
    result = "\\section{Professors} \n"
    for professor_tex in professors_latex:
        template = professor_tex.create_template_string()
        result += f"{template}\n"
    return result

