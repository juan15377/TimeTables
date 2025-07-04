
from src.app.database.services.export_functions.PDF.grid_formats import SubjectLatex, GridLatex, SymbologyLatex

class GroupLatex:
    def __init__(self, db, id_group):
        # para la plantilla solo necesito 
        # necesitamos extraer el nombre de la carrera, del semestre y del subgrupo 
        self.db = db  
        self.id_group = id_group

        cursor = db.execute_query(f"""
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


        self.subjects_ids = self.db.groups.get_subjects(id_group)

    def create_template_string(self):
        """Create the LaTeX string for the grid and the symbolic representation of the subjects."""
        grid = GridLatex()
        symbol = SymbologyLatex()
        symbol.type = 2  # Type 1: professor view

        for id_subject in self.subjects_ids:
            color = self.db.groups.get_subject_color(id_subject)
            subject_latex = SubjectLatex(self.db, id_subject, color)
            grid.add_subject(subject_latex)
            symbol.add_subject(subject_latex)

        grid_string = grid.compile_to_latexstring()
        symbol_string = symbol.to_latex_string()

        #      \\subsection{{{self.name_career + self.name_semester +  self.name_subgroup}}}

        template = f"""
        \\vspace*{{.1cm}}
        
        \\begin{{flushright}}
            {{\\LARGE \\textbf{{Group}}: {self.name_career + " " + self.name_semester + " " + self.name_subgroup}}}
        \\end{{flushright}}
        \\vspace{{1cm}}

        {grid_string}

        {symbol_string}

        \\newpage
        """
        return template



def create_groups_latex(db, ids_groups= None):
    """Create the LaTeX string for all groups."""
    # tomo todo los grupos que tienen 

    cursor = db.execute_query("""
    SELECT A.ID AS ID_GROUP, B.ID AS ID_CAREER, B.NAME AS NAME_CAREER, C.ID AS ID_SEMESTER, C.NAME AS NAME_SEMESTER, D.ID AS ID_SUBGROUP, D.NAME AS NAME_SUBGROUP
	FROM GROUPS A
	INNER JOIN CAREER B ON A.CAREER = B.ID
	INNER JOIN SEMESTER C ON A.SEMESTER = C.ID
	INNER JOIN SUBGROUP D ON A.SUBGROUP = D.ID
    ORDER BY B.ID, C.ID, D.ID
    """)

    first_row = cursor.fetchone()

    #checar que la lista de professores no sea vacia
    
    if first_row == None:
        return f"""
            \\section{{Grupos}}
            """
            

    id_group = first_row[0]

    id_career = first_row[1]
    career_name = first_row[2]
    id_semester = first_row[3]
    semester_name = first_row[4]
    id_subgroup = first_row[5]
    subgroup_name = first_row[6]

    group_latex = GroupLatex(db, id_group)
    group_latex_cont = group_latex.create_template_string()
    latex_str = f""" 
        \\section{{Grupos}}
        \\subsection{{{career_name}}}\n
        \\subsubsection{{{semester_name}}}\n
        \\subsubsubsection{{{subgroup_name}}}\n
        {group_latex_cont}
    """

    old_career_id = first_row[1]
    old_semester_id = first_row[3]
    old_subgroup_id = first_row[5]

    for row in cursor:

        id_group = row[0]
        

        if not ids_groups == None: # se estan seleccionando unos grupos
            # se seleccionan todos los grupos
            if  not id_group in ids_groups:
                continue

        id_career =     row[1]
        career_name =   row[2]
        id_semester =   row[3]
        semester_name = row[4]
        id_subgroup =   row[5]
        subgroup_name = row[6]

        # ! a question to changes the career
        # ! para añadir el contenido de latex del siguiente 

        group_latex = GroupLatex(db, id_group)
        group_latex_cont = group_latex.create_template_string()

        if id_career != old_career_id:
            latex_str += f"""
            \\subsection{{{career_name}}}\n
            \\subsubsection{{{semester_name}}}\n
            \\subsubsubsection{{{subgroup_name}}}\n
            {group_latex_cont}
            """
        elif id_semester != old_semester_id:
            # simplemente le añadimos la parte de la subseccion de un nuevo semestre
            latex_str += f"""
            \\subsubsection{{{semester_name}}}\n
            \\subsubsubsection{{{subgroup_name}}}\n
            {group_latex_cont}
            """ 
        else:
            latex_str += f"""
            \\subsubsubsection{{{subgroup_name}}}\n
            {group_latex_cont}
            """
        
        old_career_id = id_career
        old_semester_id = id_semester
        old_subgroup_id = id_subgroup
        
    return latex_str


    pass 
