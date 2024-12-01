class SubjectLatex:
    def __init__(self, name, code, professor, classroom, careers, semesters, subgroups, hours, color, hours_matrix):
        self.name = name
        self.code = code
        self.professor = professor
        self.classroom = classroom
        self.careers = careers
        self.semesters = semesters
        self.subgroups = subgroups
        self.hours = hours
        self.color = color  # Assume color is a tuple (r, g, b)
        self.hours_matrix = hours_matrix


class SymbolLatex:
    def __init__(self):
        self.subjects = []
        self.type = 1  # 1: professor, 2: group, 3: classroom

    def add_subject(self, subject):
        self.subjects.append(subject)

    def _join_elements(self, vector):
        """Join elements in a vector with ' & '."""
        return " & ".join(vector) + " "

    def _table_elements(self, vector):
        """Create a LaTeX tabular representation for the vector."""
        table = "\\begin{tabular}{c}\n"
        for element in vector[:-1]:
            table += f"{element} \\\\\n\\hline\n"
        table += f"{vector[-1]} \\\\\n"
        table += "\\end{tabular}\n"
        return table

    def _convert_subject(self, subject, type_):
        """Convert a SubjectLatex instance to a LaTeX string based on the type."""
        r, g, b = subject.color.red / 255, subject.color.green / 255, subject.color.blue / 255
        symbol = f"\\cellcolor[rgb]{{{r},{g},{b}}} \\textbf{{{subject.code}}}"

        if type_ == 1:
            vector = [
                symbol,
                subject.name,
                subject.classroom,
                str(subject.hours),
                self._table_elements(subject.careers),
                self._table_elements(subject.semesters),
                self._table_elements(subject.subgroups),
            ]
        elif type_ == 2:
            vector = [
                symbol,
                subject.name,
                subject.professor,
                subject.classroom,
                str(subject.hours),
            ]
        elif type_ == 3:
            vector = [
                symbol,
                subject.name,
                subject.professor,
                str(subject.hours),
                self._table_elements(subject.careers),
                self._table_elements(subject.semesters),
                self._table_elements(subject.subgroups),
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
            1: "|c|c|c|c|c|c|c|",
            2: "|c|c|c|c|c|",
            3: "|c|c|c|c|c|c|c|"
        }

        header = f"""
        \\begin{{longtable}}{{{column_format_dict[self.type]}}}
        \\hline
        {headers_dict[self.type]} \\\\
        \\hline
        """

        body = ""
        for subject in self.subjects:
            body += f"""
            \\hline
            {self._convert_subject(subject, self.type)} \\\\
            \\hline
            """

        footer = "\\end{longtable}"
        return header + body + footer
