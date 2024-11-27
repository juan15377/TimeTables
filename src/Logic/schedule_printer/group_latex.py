from symbology import SymbolLatex
from schedulegrid import GridLatex

class GroupLatex:
    def __init__(self, key_career, career, key_semester, semester, key_group, group):
        self.key_career = key_career
        self.career = career
        self.key_semester = key_semester
        self.semester = semester
        self.key_group = key_group
        self.group = group
        self.subjects = []

    def add_subject(self, subject):
        """Adds a subject to the group's list of subjects."""
        self.subjects.append(subject)

def create_groups_latex(composite_groups):
    """Creates a LaTeX string for all groups."""
    careers = {group.key_career: group.career for group in composite_groups}
    semesters = {group.key_semester: group.semester for group in composite_groups}
    groups = {group.key_group: group.group for group in composite_groups}

    semester_flags = {key: False for key in semesters}
    group_flags = {key: False for key in groups}

    result = "\\section{Groups} \n"

    for key_career, career in careers.items():
        result += f"\\subsection{{{career}}}\n"
        for key_semester, semester in semesters.items():
            for key_group, group_name in groups.items():
                for comp_group in composite_groups:
                    is_same_career = comp_group.key_career == key_career
                    is_same_semester = comp_group.key_semester == key_semester
                    is_same_group = comp_group.key_group == key_group

                    if is_same_career and is_same_semester and is_same_group:
                        if not semester_flags[key_semester]:
                            result += f"\\subsubsection{{{semester}}}\n"
                            semester_flags[key_semester] = True
                        if not group_flags[key_group]:
                            result += f"\\subsubsubsection{{{group_name}}}\n"
                            group_flags[key_group] = True

                        grid = GridLatex()
                        symbol = SymbolLatex()
                        symbol.type = 2  # Type 2: Group view

                        for subject in comp_group.subjects:
                            grid.add_subject(subject)
                            symbol.add_subject(subject)

                        grid_str = grid.to_latex_string()
                        symbol_str = symbol.to_latex_string()

                        result += f"""
                        \\begin{{flushright}}
                        {{\\LARGE \\textbf{{Career}}: {career}}}
                        \\end{{flushright}}
                         \\vspace{{1cm}}
                
                        {grid_str}

                        {symbol_str}
                        
                        \\newpage
                        """

                group_flags[key_group] = False
            semester_flags[key_semester] = False

    return result
