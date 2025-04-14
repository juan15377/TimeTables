from src.models.database.components.export_functions.components.new_formats import * 
from src.models.database.database import db 

print(db.subjects.get_matrix_of_allocated_slots(1))

sub_lat = SubjectLatex(db, 1, (100, 100, 100))

print(sub_lat.semesters_names)

professor_lat = ProfessorLatex(db, 1)

# schedule_grid = GridLatex()
# 
# schedule_grid.add_subject(sub_lat)
# 
# st = schedule_grid.compile_to_latexstring()
# 
# sym_lat = SymbologyLatex()
# 
# sym_lat.add_subject(sub_lat)
# sym_lat.add_subject(sub_lat)
# 
st = professor_lat.create_template_string()
st = LATEX_TEMPLATE(st)

print(st)

st = create_professors_latex(db)
st = LATEX_TEMPLATE(st)
print(st)

