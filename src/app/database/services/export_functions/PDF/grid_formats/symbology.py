

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
        r, g, b = subject.color
        r_normalized, g_normalized, b_normalized = r / 255, g / 255, b / 255

        # Cálculo de luminancia para decidir el color del texto
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        text_color = "white" if luminance < 128 else "black"

        # Generación del símbolo con color adaptativo de texto
        symbol = (
            f"\\cellcolor[rgb]{{{r_normalized:.3f},{g_normalized:.3f},{b_normalized:.3f}}} "
            f"\\textcolor{{{text_color}}}{{\\textbf{{{subject.code}}}}}"
        )
        
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
            1: "\\cellcolor{headercolor}\\textcolor{white}{\\textbf{Symbol}} & \\cellcolor{headercolor}\\textcolor{white}{\\textbf{Subject}} & \\cellcolor{headercolor}\\textcolor{white}{\\textbf{Classroom}} & \\cellcolor{headercolor}\\textcolor{white}{\\textbf{Hours}} & \\cellcolor{headercolor}\\textcolor{white}{\\textbf{Career}} & \\cellcolor{headercolor}\\textcolor{white}{\\textbf{Semester}} & \\cellcolor{headercolor}\\textcolor{white}{\\textbf{Group}}",
            2: "\\cellcolor{headercolor}\\textcolor{white}{\\textbf{Symbol}} & \\cellcolor{headercolor}\\textcolor{white}{\\textbf{Subject}} & \\cellcolor{headercolor}\\textcolor{white}{\\textbf{Professor}} & \\cellcolor{headercolor}\\textcolor{white}{\\textbf{Classroom}} & \\cellcolor{headercolor}\\textcolor{white}{\\textbf{Hours}}",
            3: "\\cellcolor{headercolor}\\textcolor{white}{\\textbf{Symbol}} & \\cellcolor{headercolor}\\textcolor{white}{\\textbf{Subject}} & \\cellcolor{headercolor}\\textcolor{white}{\\textbf{Professor}} & \\cellcolor{headercolor}\\textcolor{white}{\\textbf{Hours}} & \\cellcolor{headercolor}\\textcolor{white}{\\textbf{Career}} & \\cellcolor{headercolor}\\textcolor{white}{\\textbf{Semester}} & \\cellcolor{headercolor}\\textcolor{white}{\\textbf{Group}}"
        }
        
        # Corregidos los formatos de columna eliminando el | final
        column_format_dict = {
            1: "|>{\centering\\arraybackslash}m{2cm}|>{\centering\\arraybackslash}m{4cm}|>{\centering\\arraybackslash}m{2cm}|>{\centering\\arraybackslash}m{2cm}|>{\centering  \\arraybackslash}m{2cm}|>{\centering\\arraybackslash}m{2cm}|>{\centering\\arraybackslash}m{2cm}|",
            2: "|>{\centering\\arraybackslash}m{2cm}|>{\centering\\arraybackslash}m{4cm}|>{\centering\\arraybackslash}m{4cm}|>{\centering\\arraybackslash}m{3.5cm}|>{\centering\\arraybackslash}m{3.5cm}|",
            3: "|>{\centering\\arraybackslash}m{2cm}|>{\centering\\arraybackslash}m{4cm}|>{\centering\\arraybackslash}m{2.15cm}|>{\centering\\arraybackslash}m{1.8cm}|>{\centering\\arraybackslash}m{2cm}|>{\centering\\arraybackslash}m{2cm}|>{\centering\\arraybackslash}m{2cm}|"
        }
        
        # También eliminé \rowcolor de las especificaciones de columna y lo aplicaré por fila
        header = f"""
        \\begin{{tabular}}{{{column_format_dict[self.type]}}}
        \\hline
        \\rowcolor{{backgroundcolor}}
        {headers_dict[self.type]} \\\\
        \\hline
            """
        
        body = ""
        for subject in self.subjects:
            body += f"""
        \\hline
        \\rowcolor{{backgroundcolor}}
        {self._convert_subject_row(subject, self.type)} \\\\
        \\hline
                """
            
        footer = """\\end{tabular}
        """
        
        return header + body + footer