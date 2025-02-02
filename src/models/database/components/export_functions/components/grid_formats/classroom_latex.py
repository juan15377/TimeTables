
from .symbology import SymbolLatex
from .schedulegrid import GridLatex

class ClassroomLatex:
    def __init__(self, classroom):
        self.name = classroom.name
        self.subjects = classroom.get_subjects()

    def create_template_string(self):
        """Create the LaTeX string for the grid and symbolic representation of the subjects."""
        grid = GridLatex()
        symbology = SymbologyLatex()
        symbology.type = 3  # Type 3: classroom view

        for subject in self.subjects:
            grid.add_subject(subject)
            symbol.add_subject(subject)

        grid_string = grid.compile_to_latexstring()
        symbol_string = symbol.to_latex_string()

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


def create_classrooms_latex(classrooms):
    """Create the LaTeX string for all classrooms."""
    result = "\\section{Classrooms} \n"
    for classroom in classrooms:
        template = classroom.create_template_string()
        result += f"{template}\n"
    return result
