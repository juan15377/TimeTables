import dearpygui.dearpygui as dpg
from typing import Dict, List, Set
import random


from src.app.database import database_manager
from src.app.UI.components.schedule_availability.schedule_availability import HorarioDisponibilidadApp


import dearpygui.dearpygui as dpg
from typing import Dict, List, Set
import random

import re 

def get_id(cadena):
    """
    Extrae el número de id de una cadena con formato como:
    "semestre 1 ( id = 1)2"
    """
    coincidencia = re.search(r'id\s*=\s*(\d+)', cadena)
    if coincidencia:
        return int(coincidencia.group(1))
    return None



class ItemsGroupsManager():
    
    __instance = None 
    
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self, db):
        self.db = db  
        
        self.careers = {}
        self.semesters = {}
        self.subgroups = {}
        
        
        self.groups = {}
        
        self.update()
        
        
    def update_groups(self):
        
        self.groups = self.get_filtered_groups()
        
    def update_careers(self, update_groups = True):
        
        cursor = self.db.execute_query("""
        SELECT ID, NAME 
        FROM CAREER;
        """)
        
        self.careers: Set[str] = {f"{name} (id = {id}) " for (id, name) in cursor}
        
        cursor.close()
        if update_groups:
            self.update_groups()  
                        
        
        
    def update_semesters(self, update_groups = True):
        
        cursor = self.db.execute_query("""
            SELECT ID, NAME 
            FROM SEMESTER;
        """)
        
        self.semesters: Set[str] = {f"{name} (id = {id}) " for (id, name) in cursor}
        cursor.close()     
        
        if update_groups:
            self.update_groups()

        
    def update_subgroups(self, update_groups = True):
        cursor = self.db.execute_query("""
        SELECT ID, NAME 
        FROM SUBGROUP;
        """)
    
        self.subgroups: Set[str] = {f"{name} (id = {id}) " for (id, name) in cursor}
        cursor.close()
        
        if update_groups:
            self.update_groups()
            

            
    def get_careers(self):
        return self.careers 
    
    def get_semesters(self):
        return self.semesters 
    
    def get_subgroups(self):
        return self.subgroups 
    
    def get_groups(self):
        return self.groups 
    
    def update(self):
        self.update_careers(update_groups=False)
        self.update_semesters(update_groups=False)
        self.update_subgroups(update_groups=False)
        
        self.update_groups()
    
    def get_filtered_groups(self, coincidence = None, career_id = None, semester_id = None, subgroup_id = None):
        
        # Prepara filtros seguros
        parse_career = "TRUE" if career_id is None else "C.ID = ?"
        parse_semester = "TRUE" if semester_id is None else "S.ID = ?"
        parse_subgroup = "TRUE" if subgroup_id is None else "SG.ID = ?"

        coincidence = "" if coincidence is None else coincidence

        # Arma la consulta con placeholders
        query = f"""
        SELECT 
            A.ID AS GROUP_ID,
            C.NAME, S.NAME, SG.NAME,
            CASE 
            WHEN NOT CAST(SUM(COALESCE(CC.TOTAL_SLOTS, 0)) AS REAL) = 0 THEN
                CAST(SUM(COALESCE(CC.COMPLETED_SLOTS, 0)) AS REAL) / 
                CAST(SUM(COALESCE(CC.TOTAL_SLOTS, 0)) AS REAL) 
            ELSE 
                1
            END AS COMPLETION_RATE
        FROM GROUPS A
        JOIN CAREER C ON A.CAREER = C.ID
        JOIN SEMESTER S ON A.SEMESTER = S.ID
        JOIN SUBGROUP SG ON A.SUBGROUP = SG.ID
        LEFT JOIN GROUP_SUBJECT B ON A.ID = B.ID_GROUP
        LEFT JOIN (
            SELECT 
                S.ID AS SUBJECT_ID, 
                S.TOTAL_SLOTS, 
                SUM(COALESCE(SS.LEN, 0)) AS COMPLETED_SLOTS
            FROM SUBJECT S
            LEFT JOIN SUBJECT_SLOTS SS ON S.ID = SS.ID_SUBJECT
            GROUP BY S.ID, S.TOTAL_SLOTS
        ) CC ON B.ID_SUBJECT = CC.SUBJECT_ID
        WHERE {parse_career}
            AND {parse_semester}
            AND {parse_subgroup}
            AND C.NAME || S.NAME || SG.NAME LIKE ?
        GROUP BY A.ID;
        """

        # Arma la lista de parámetros en el orden correcto
        params = []
        if career_id is not None:
            params.append(career_id)
        if semester_id is not None:
            params.append(semester_id)
        if subgroup_id is not None:
            params.append(subgroup_id)

        # Agrega el parámetro para la coincidencia parcial
        params.append(f"%{coincidence}%")

        # Ejecuta la consulta
        cursor = self.db.execute_query(query, params)
        
        
        filter_groups = [{
            "id" : id,
            "nombre" : get_group_name(id, name_career, name_semester, name_subgroup),
            "carrera" : name_career,
            "semestre" : name_semester,
            "subgrupo" : name_subgroup,
            "progress" : progress
        } for (
            id, 
            name_career, 
            name_semester,
            name_subgroup,
            progress) in cursor]
        
        cursor.close()
        
        return filter_groups
        
        
        pass 


def get_group_name(id_group, name_career, name_semester, name_subgroup):
    return f"{name_career} | {name_semester} | {name_subgroup} ( id = {id_group} )"
    pass 

def get_id(cadena):
    """
    Extrae el número de id de una cadena con formato como:
    "semestre 1 ( id = 1)2"
    """
    coincidencia = re.search(r'id\s*=\s*(\d+)', cadena)
    if coincidencia:
        return int(coincidencia.group(1))
    return None



items = ItemsGroupsManager(database_manager)

#print(items.get_groups())