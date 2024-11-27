class Padre:
    def __init__(self):
        self.campo_padre = "Soy un campo del padre"

class Hijo(Padre):
    def mostrar_campo_padre(self):
        print(f"Campo del padre: {self.campo_padre}")  # Acceso directo

# Crear instancia de Hijo
hijo = Hijo()
hijo.mostrar_campo_padre()
