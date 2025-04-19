from src.schedule_app.database import database_manager 

#database_manager.restart()
#database_manager.professors.new("Juan de jesus")
#database_manager.professors.new("Manuel Nava")
#database_manager.professors.new("Akdiel Novella")
#database_manager.professors.new("Eduardo Miramontes")
#
#database_manager.classrooms.new("Aula 1")
#database_manager.classrooms.new("Aula 2")
#database_manager.classrooms.new("Aula 3")
#database_manager.classrooms.new("Aula 4")
#
##
#database_manager.groups.careers.new("Actuaria")
#database_manager.groups.careers.new("Matematicas")
#
#database_manager.groups.semesters.new("Semestre 1")
#database_manager.groups.semesters.new("Semestre 2")
#database_manager.groups.semesters.new("Semestre 3")
#database_manager.groups.semesters.new("Semestre 4")
#database_manager.groups.semesters.new("Semestre 5")
#
#database_manager.groups.subgroups.new("Grupo A")
#database_manager.groups.subgroups.new("Grupo B")
#
#database_manager.groups.new(1, 1, 2)
#database_manager.groups.new(1, 2, 2)
#database_manager.groups.new(2, 1, 2)
#database_manager.groups.new(2, 2, 2)
#database_manager.groups.new(2, 3, 2)
#
#database_manager.subjects.new(
#    "Calculo Actuarial",
#    "CALACT",
#    1,
#    1,
#    [1],
#    1,
#    3,
#    8
#)
#
#database_manager.subjects.new(
#    "Computo Matematico",
#    "COMPM",
#    2,
#    1,
#    [2, 3],
#    1,
#    4,
#    20
#)
#
#database_manager.subjects.new(
#    "Matematicas Actuariales",
#    "MATACT",
#    2,
#    2,
#    [4],
#    1,
#    4,
#    20
#)
#
#
#database_manager.subjects.new_slot(1, 1, 1, 3)
#database_manager.subjects.new_slot(1, 3, 2, 3)
#database_manager.subjects.new_slot(1, 1, 3, 2)

#database_manager.subjects.new_slot(2, 1, 4, 3)
#database_manager.subjects.new_slot(2, 3, 5, 2)
#database_manager.subjects.new_slot(2, 8, 5, 3)

#database_manager.subjects.new_slot(3, 5, 4, 3)
#database_manager.subjects.new_slot(3, 9, 5, 2)
#database_manager.subjects.new_slot(3, 15, 5, 3)

database_manager.export.pdf.grid_formats.complete_schedule("/home/juan/Escritorio/", "horario")
#print(database_manager.subjects.get_matrix_of_allocated_slots(2))