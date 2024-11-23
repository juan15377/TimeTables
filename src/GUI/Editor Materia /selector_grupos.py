import flet as ft

def main(page: ft.Page):
    page.add(
        ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Carrera")),
                ft.DataColumn(ft.Text("Semestre")),
                ft.DataColumn(ft.Text("SubGrupo"), numeric=True),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Matematicas")),
                        ft.DataCell(ft.Text("Smith")),
                        ft.DataCell(ft.Text("43")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Actuaria")),
                        ft.DataCell(ft.Text("Semestre 1")),
                        ft.DataCell(ft.Text("19")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Matematicas")),
                        ft.DataCell(ft.Text("Wong")),
                        ft.DataCell(ft.Text("25")),
                    ],
                ),
            ],
        ),
    )

ft.app(target=main)