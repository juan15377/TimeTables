from .symbology import SymbologyLatex
from .schedulegrid import GridLatex
from .subject_latex import SubjectLatex
class GroupLatex:
    def __init__(self, group):
        self.group_ = group
        self.key_career = group.career.key.key
        self.career = group.career.name
        self.key_semester = group.semester.key.key
        self.semester = group.semester.name
        self.key_group = group.subgroup.key.key
        self.group = group.subgroup.name
        self.subjects = group.get_subjects()

    def create_template_string(self):
        """Create the LaTeX string for the grid and the symbolic representation of the subjects."""
        grid = GridLatex()
        symbol = SymbologyLatex()
        symbol.type = 2  # Type 1: professor view

        for subject in self.subjects:
            subject_latex = SubjectLatex(subject, self.group_)
            grid.add_subject(subject_latex)
            symbol.add_subject(subject_latex)

        grid_string = grid.compile_to_latexstring()
        symbol_string = symbol.to_latex_string()

        template = f"""
        \\subsection{{{self.career + self.semester +  self.group}}}
        \\vspace*{{.1cm}}
        
        \\begin{{flushright}}
            {{\\LARGE \\textbf{{Group}}: {self.career + self.semester +  self.group}}}
        \\end{{flushright}}
        \\vspace{{1cm}}

        {grid_string}

        {symbol_string}

        \\newpage
        """
        return template


def create_groups_latex(groups):
    """Create the LaTeX string for all groups."""
    
    groups_latex = [GroupLatex(group) for group in groups]
    careers = {group.key_career: group.career for group in groups_latex}
    semesters = {group.key_semester: group.semester for group in groups_latex}
    groups = {group.key_group: group.group for group in groups_latex}

    semester_flags = {key: False for key in semesters}
    group_flags = {key: False for key in groups}

    result = "\\section{Groups} \n"

    for key_career, career in careers.items():
        result += f"\\subsection{{{career}}}\n"
        for key_semester, semester in semesters.items():
            for key_group, group_name in groups.items():
                for comp_group in groups_latex:
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
                        symbol = SymbologyLatex()
                        symbol.type = 2  # Type 2: Group view

                        for subject in comp_group.subjects:
                            subject_latex = SubjectLatex(subject, comp_group.group_)
                            grid.add_subject(subject_latex)
                            symbol.add_subject(subject_latex)

                        grid_str = grid.compile_to_latexstring()
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
