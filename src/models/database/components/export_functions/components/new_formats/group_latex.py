from .symbology import SymbologyLatex
from .schedule_grid import GridLatex
from .subject_latex import SubjectLatex


class GroupLatex:
    def __init__(self, db, id_group):
        # para la plantilla solo necesito 
        # necesitamos extraer el nombre de la carrera, del semestre y del subgrupo 
        self.db = db  
        self.id_group = id_group
        cursor = self.db.db_connection.cursor()

        cursor.execute(f"""
        SELECT A.ID AS ID_GROUP, B.ID AS ID_CAREER, B.NAME AS NAME_CAREER, C.ID AS ID_SEMESTER, C.NAME AS NAME_SEMESTER, D.ID AS ID_SUBGROUP, D.NAME AS NAME_SUBGROUP
        FROM GROUPS A
        INNER JOIN CAREER B ON A.CAREER = B.ID
        INNER JOIN SEMESTER C ON A.SEMESTER = C.ID
        INNER JOIN SUBGROUP D ON A.SUBGROUP = D.ID
        WHERE A.ID = {id_group}
        """
        )

        info_group = cursor.fetchall()[0]

        self.name_career = info_group[2]
        self.name_semester = info_group[4]
        self.name_subgroup = info_group[6]


        self.subjects_ids = self.bd.groups.get_subjects(id_group)

    def create_template_string(self):
        """Create the LaTeX string for the grid and the symbolic representation of the subjects."""
        grid = GridLatex()
        symbol = SymbologyLatex()
        symbol.type = 2  # Type 1: professor view

        for id_subject in self.subjects_ids:
            color = self.bd.groups.get_subject_color(id_subject)
            subject_latex = SubjectLatex(self.db, id_subject, color)
            grid.add_subject(subject_latex)
            symbol.add_subject(subject_latex)

        grid_string = grid.compile_to_latexstring()
        symbol_string = symbol.to_latex_string()

        template = f"""
        \\subsection{{{self.name_career + self.name_semester +  self.name_subgroup}}}
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
