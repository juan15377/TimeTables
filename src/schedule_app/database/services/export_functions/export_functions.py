
from .PDF import PDFExport

class ExportFunctions:
    
    def __init__(self, db):
        
        self.pdf = PDFExport(db)
        