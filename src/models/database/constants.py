from .models.Professor_Classroom_Group import PCG
from .models.Subjects import *
from .models.Hours import *

DEFAULT_PCG = PCG()

DEFAULT_SUBJECT = Subject(
    "",
    "",
    None,
    None,
    [],
    HoursComposition(0, 0, 0),
)

DEFAULT_PCG.subjects.append(DEFAULT_SUBJECT)
DEFAULT_PCG.subject_colors.colors[DEFAULT_SUBJECT] = MyColorRGB(0, 0, 0)
