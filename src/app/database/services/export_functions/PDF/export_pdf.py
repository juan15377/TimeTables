from .grid_formats import ExportGridFormats 
from .official_formats import ExportOfficialFormats

from src.app.database.services.export_functions.PDF.grid_formats import ExportGridFormats
from src.app.database.services.export_functions.PDF.official_formats import ExportOfficialFormats 

class PDFExport:
    
    def __init__(self,db):
        
        self.grid_formats = ExportGridFormats(db)
        self.official_formats = ExportOfficialFormats()
        
