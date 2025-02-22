from .symbology import SymbologyLatex
from .schedulegrid import GridLatex
from .symbology import DICT_TYPES_SYMBOLOGY
from .subject_latex import SubjectLatex


class ProfessorLatex:
    def __init__(self, professor):
        self.professor = professor
        self.name = professor.name
        self.subjects = professor.get_subjects()
        
    def add_subject(self, subject):
        """Add a subject to the professor's list of subjects."""
        self.subjects.append(subject)

    def create_template_string(self):
        """Create the LaTeX string for the grid and the symbolic representation of the subjects."""
        grid = GridLatex()
        symbol = SymbologyLatex()
        symbol.type = 1  # Type 1: professor view

        for subject in self.subjects:
            subject_latex = SubjectLatex(subject, self.professor)
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


def create_professors_latex(professors):
    professors_latex = [ProfessorLatex(professor) for professor in professors]
    """Create the LaTeX string for all professors."""
    result = "\\section{Professors} \n"
    for professor_tex in professors_latex:
        template = professor_tex.create_template_string()
        result += f"{template}\n"
    return result

