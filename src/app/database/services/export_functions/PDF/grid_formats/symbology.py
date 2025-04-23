

class SymbologyLatex:
    def __init__(self):
        self.subjects = []
        self.type = 1  #! 1: professor, 2: group, 3: classroom

    def add_subject(self, subject):
        self.subjects.append(subject)

    def _join_elements(self, vector):
        return " & ".join(vector) + " "

    def _table_elements(self, vector):

        """Create a LaTeX tabular representation for the vector."""
        table = "\\begin{itemize}[left=0pt,align=left]"
        for element in vector[:-1]:
            table += "\\item " + f"{element} \n"
        if len(vector) != 0:
            table += "\\item " + f"{vector[-1]} \n"
        table += "\\end{itemize}"
        return table

    def _convert_subject_row(self, subject, type_):
        """Convert a SubjectLatex instance to a LaTeX string based on the type."""
        r, g, b = subject.color 
        r, g, b = r/255, g/255, b/255 

        symbol = f"\\cellcolor[rgb]{{{r},{g},{b}}} \\textbf{{{subject.code}}}"
        
        
        careers_names = subject.careers_names
        semesters_names = subject.semesters_names
        subgroups_names = subject.subgroups_names
        
        if type_ == 1:
            vector = [
                symbol,
                subject.name,
                subject.classroom_name,
                str(subject.hours),
                self._table_elements(careers_names),
                self._table_elements(semesters_names),
                self._table_elements(subgroups_names),
            ]
        elif type_ == 2:
            vector = [
                symbol,
                subject.name,
                subject.professor_name,
                subject.classroom_name,
                str(subject.hours),
            ]
        elif type_ == 3:
            vector = [
                symbol,
                subject.name,
                subject.professor_name,
                str(subject.hours),
                self._table_elements(careers_names),
                self._table_elements(semesters_names),
                self._table_elements(subgroups_names),
            ]
        else:
            return ""
        return self._join_elements(vector)

    def to_latex_string(self):
        """Convert the entire SymbolLatex instance into a LaTeX longtable."""
        headers_dict = {
            1: "\\textbf{Symbol} & \\textbf{Subject} & \\textbf{Classroom} & \\textbf{Hours} & \\textbf{Career} & \\textbf{Semester} & \\textbf{Group}",
            2: "\\textbf{Symbol} & \\textbf{Subject} & \\textbf{Professor} & \\textbf{Classroom} & \\textbf{Hours}",
            3: "\\textbf{Symbol} & \\textbf{Subject} & \\textbf{Professor} & \\textbf{Hours} & \\textbf{Career} & \\textbf{Semester} & \\textbf{Group}"
        }

        column_format_dict = {
            1: "|>{\centering\\arraybackslash}m{2cm}|>{\centering\\arraybackslash}m{4cm}|>{\centering\\arraybackslash}m{2cm}|>{\centering\\arraybackslash}m{2cm}|>{\centering\\arraybackslash}m{2cm}|>{\centering\\arraybackslash}m{2cm}|>{\centering\\arraybackslash}m{2cm}|",
            2: "|>{\centering\\arraybackslash}m{2cm}|>{\centering\\arraybackslash}m{4cm}|>{\centering\\arraybackslash}m{4cm}|>{\centering\\arraybackslash}m{3.5cm}|>{\centering\\arraybackslash}m{3.5cm}|",
            3: "|>{\centering\\arraybackslash}m{2cm}|>{\centering\\arraybackslash}m{4cm}|>{\centering\\arraybackslash}m{2.15cm}|>{\centering\\arraybackslash}m{1.8cm}|>{\centering\\arraybackslash}m{2cm}|>{\centering\\arraybackslash}m{2cm}|>{\centering\\arraybackslash}m{2cm}|"
        }

        header = f"""
        \\begin{{tabular}}{{{column_format_dict[self.type]}}}
        \\hline
        {headers_dict[self.type]} \\\\
        \\hline
        """

        body = ""
        for subject in self.subjects:
            body += f"""
            \\hline
            {self._convert_subject_row(subject, self.type)} \\\\
            \\hline
            """

        footer = """\\end{tabular}
                    """
        return header + body + footer