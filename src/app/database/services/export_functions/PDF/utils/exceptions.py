REPLACE_CHARACTER = {
    # Letras minúsculas con acentos y diéresis
    'á': r"\'a", 'é': r"\'e", 'í': r"\'i", 'ó': r"\'o", 'ú': r"\'u",
    'à': r"\`a", 'è': r"\`e", 'ì': r"\`i", 'ò': r"\`o", 'ù': r"\`u",
    'ä': r'\"a', 'ë': r'\"e', 'ï': r'\"i', 'ö': r'\"o', 'ü': r'\"u',
    'ã': r'\~a', 'õ': r'\~o', 'ñ': r'\~n',

    # Letras mayúsculas con acentos y diéresis
    'Á': r"\'A", 'É': r"\'E", 'Í': r"\'I", 'Ó': r"\'O", 'Ú': r"\'U",
    'À': r"\`A", 'È': r"\`E", 'Ì': r"\`I", 'Ò': r"\`O", 'Ù': r"\`U",
    'Ä': r'\"A ', 'Ë': r'\"E', 'Ï': r'\"I', 'Ö': r'\"O', 'Ü': r'\"U',
    'Ã': r' \~A ', 'Õ': r'\~O', 'Ñ': r'\~N',

    # Reemplazo de comillas dobles
    '"': r' \textquotedblleft  ',  # Comillas de apertura
    '"': r' \textquotedblright ',  # Comillas de cierre
    }


def replace_exceptions(text):
    
    for caracter, latex_char in REPLACE_CHARACTER.items():
        text = text.replace(caracter, latex_char)
    
    return text
