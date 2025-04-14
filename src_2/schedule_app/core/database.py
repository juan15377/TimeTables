import sqlite3
from pathlib import Path

# Ruta base del archivo de la base de datos
DB_NAME = "TimeTables.db"
DB_PATH = Path(__file__).resolve().parent / "TimeTables.db"

def get_connection():
    """
    Devuelve una conexión a la base de datos SQLite.
    Asegura que el archivo esté en la raíz del proyecto.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    
    def is_intersect(row_1, t1, row_2, t2):
        if row_1 == row_2:
            return True
        elif row_1 > row_2:
            return row_2 + t2 > row_1
        else:
            return row_1 + t1 > row_2

    # Conectar a SQLite
    # Registrar la función en SQLite
    conn.create_function("is_intersect", 4, is_intersect)
    
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    
    return conn

def init_db():
    """
    Inicializa la base de datos si es necesario.
    Crea tablas, verifica integridad, etc.
    """

    query_create_tables = [
        """CREATE TABLE PROFESSOR(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT
        );""",

        """CREATE TABLE CLASSROOM(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT
        );""",

        """CREATE TABLE CAREER(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT
        );""",

        """CREATE TABLE SEMESTER(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT
        );""",

        """CREATE TABLE SUBGROUP(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT
        );""",

        """CREATE TABLE GROUPS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CAREER INTEGER NOT NULL,
            SEMESTER INTEGER NOT NULL,
            SUBGROUP INTEGER NOT NULL,
            
            CONSTRAINT CAREER_FK FOREIGN KEY (CAREER) REFERENCES CAREER(ID) ON DELETE CASCADE,
            CONSTRAINT SEMESTER_FK FOREIGN KEY (SEMESTER) REFERENCES SEMESTER(ID) ON DELETE CASCADE,
            CONSTRAINT SUBGROUP_FK FOREIGN KEY (SUBGROUP) REFERENCES SUBGROUP(ID) ON DELETE CASCADE
        );""",

        """CREATE TABLE SUBJECT (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT,
            CODE TEXT,
            MINIMUM_SLOTS INTEGER CHECK(MINIMUM_SLOTS > 0),
            MAXIMUM_SLOTS INTEGER CHECK(MAXIMUM_SLOTS > MINIMUM_SLOTS),
            TOTAL_SLOTS INTEGER CHECK(TOTAL_SLOTS > 0)
        );""",

        """CREATE TABLE PROFESSOR_COLORS (
            ID_PROFESSOR INTEGER,
            ID_SUBJECT INTEGER,
            RED INTEGER CHECK (red >= 0 AND red <= 255),
            GREEN INTEGER CHECK (green >= 0 AND green <= 255),
            BLUE INTEGER CHECK (blue >= 0 AND blue <= 255),

            PRIMARY KEY (ID_PROFESSOR, ID_SUBJECT),
            CONSTRAINT PROFESSOR_FK FOREIGN KEY (ID_PROFESSOR) REFERENCES PROFESSOR(ID) ON DELETE CASCADE,
            CONSTRAINT SUBJECT_FK FOREIGN KEY (ID_SUBJECT) REFERENCES SUBJECT(ID) ON DELETE CASCADE
        );""",

        """CREATE TABLE CLASSROOM_COLORS (
            ID_CLASSROOM INTEGER,
            ID_SUBJECT INTEGER,
            RED INTEGER CHECK (red >= 0 AND red <= 255),
            GREEN INTEGER CHECK (green >= 0 AND green <= 255),
            BLUE INTEGER CHECK (blue >= 0 AND blue <= 255),
            
            PRIMARY KEY (ID_CLASSROOM, ID_SUBJECT),
            CONSTRAINT CLASSROOM_FK FOREIGN KEY (ID_CLASSROOM) REFERENCES CLASSROOM(ID) ON DELETE CASCADE,
            CONSTRAINT SUBJECT_FK FOREIGN KEY (ID_SUBJECT) REFERENCES SUBJECT(ID) ON DELETE CASCADE
        );""",

        """CREATE TABLE GROUP_COLORS (
            ID_GROUP INTEGER,
            ID_SUBJECT INTEGER,
            RED INTEGER CHECK (red >= 0 AND red <= 255),
            GREEN INTEGER CHECK (green >= 0 AND green <= 255),
            BLUE INTEGER CHECK (blue >= 0 AND blue <= 255),

            PRIMARY KEY (ID_GROUP, ID_SUBJECT),
            CONSTRAINT GROUP_FK FOREIGN KEY (ID_GROUP) REFERENCES GROUPS(ID) ON DELETE CASCADE,
            CONSTRAINT SUBJECT_FK FOREIGN KEY (ID_SUBJECT) REFERENCES SUBJECT(ID) ON DELETE CASCADE
        );""",

        """CREATE TABLE PROFESSOR_SUBJECT (
            ID_PROFESSOR INTEGER,
            ID_SUBJECT INTEGER,

            PRIMARY KEY (ID_PROFESSOR, ID_SUBJECT),
            CONSTRAINT PROFESSOR_FK FOREIGN KEY (ID_PROFESSOR) REFERENCES PROFESSOR(ID) ON DELETE CASCADE,
            CONSTRAINT SUBJECT_FK FOREIGN KEY (ID_SUBJECT) REFERENCES SUBJECT(ID) ON DELETE CASCADE
        );""",

        """CREATE TABLE CLASSROOM_SUBJECT (
            ID_CLASSROOM INTEGER,
            ID_SUBJECT INTEGER,

            PRIMARY KEY (ID_CLASSROOM, ID_SUBJECT),
            CONSTRAINT CLASSROOM_FK FOREIGN KEY (ID_CLASSROOM) REFERENCES CLASSROOM(ID) ON DELETE CASCADE,
            CONSTRAINT SUBJECT_FK FOREIGN KEY (ID_SUBJECT) REFERENCES SUBJECT(ID) ON DELETE CASCADE
        );""",

        """CREATE TABLE GROUP_SUBJECT (
            ID_GROUP INTEGER,
            ID_SUBJECT INTEGER,

            PRIMARY KEY (ID_GROUP, ID_SUBJECT),
            CONSTRAINT GROUP_FK FOREIGN KEY (ID_GROUP) REFERENCES GROUPS(ID) ON DELETE CASCADE,
            CONSTRAINT SUBJECT_FK FOREIGN KEY (ID_SUBJECT) REFERENCES SUBJECT(ID) ON DELETE CASCADE
        );""",

        """CREATE TABLE SUBJECT_SLOTS(
            ID_SLOT INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_SUBJECT INTEGER,
            ROW_POSITION INTEGER,
            COLUMN_POSITION INTEGER,
            LEN INTEGER CHECK (LEN > 0),

            CONSTRAINT SUBJECT_FK FOREIGN KEY (ID_SUBJECT) REFERENCES SUBJECT(ID) ON DELETE CASCADE
        );""",

        """CREATE TABLE PROFESSOR_AVAILABILITY (
            ID_PROFESSOR INTEGER,
            ROW_POSITION INTEGER,
            COLUMN_POSITION INTEGER,
            VAL BOOLEAN,

            PRIMARY KEY (ID_PROFESSOR, ROW_POSITION, COLUMN_POSITION),
            CONSTRAINT PROFESSOR_FK FOREIGN KEY (ID_PROFESSOR) REFERENCES PROFESSOR(ID) ON DELETE CASCADE
        );""",

        """CREATE TABLE CLASSROOM_AVAILABILITY (
            ID_CLASSROOM INTEGER,
            ROW_POSITION INTEGER,
            COLUMN_POSITION INTEGER,
            VAL BOOLEAN,

            PRIMARY KEY (ID_CLASSROOM, ROW_POSITION, COLUMN_POSITION),
            CONSTRAINT CLASSROOM_FK FOREIGN KEY (ID_CLASSROOM) REFERENCES CLASSROOM(ID) ON DELETE CASCADE
        );""",

        """CREATE TABLE GROUP_AVAILABILITY (
            ID_GROUP INTEGER,
            ROW_POSITION INTEGER,
            COLUMN_POSITION INTEGER,
            VAL BOOLEAN,

            PRIMARY KEY (ID_GROUP, ROW_POSITION, COLUMN_POSITION),
            CONSTRAINT GROUP_FK FOREIGN KEY (ID_GROUP) REFERENCES GROUPS(ID) ON DELETE CASCADE
        );"""
    ]

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Habilitar las restricciones de claves foráneas
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Ejecutar las consultas para crear todas las tablas
    for query in query_create_tables:
        cursor.execute(query)        

    # Habilitar las restricciones de claves foráneas

#init_db()

db_connection = get_connection()