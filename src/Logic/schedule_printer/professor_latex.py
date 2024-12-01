from .symbology import SymbolLatex
from .schedulegrid import GridLatex

class ProfessorLatex:
    def __init__(self, name):
        self.name = name
        self.subjects = []

    def add_subject(self, subject):
        """Add a subject to the professor's list of subjects."""
        self.subjects.append(subject)

    def create_template_string(self):
        """Create the LaTeX string for the grid and the symbolic representation of the subjects."""
        grid = GridLatex()
        symbol = SymbolLatex()
        symbol.type = 1  # Type 1: professor view

        for subject in self.subjects:
            grid.add_subject(subject)
            symbol.add_subject(subject)

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
    """Create the LaTeX string for all professors."""
    result = "\\section{Professors} \n"
    for professor in professors:
        template = professor.create_template_string()
        result += f"{template}\n"
    return result
