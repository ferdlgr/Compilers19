#tanto el lexer, el parser y semantica poseen sus definiciones de globales 
#para el correcto funcionamiento de la prueba con script, los tokens
#se encuentran definidos en el lexer, este unicamente sirve si se prueba un archivo empty
from enum import Enum
 
class TokenType(Enum):
    ENDFILE = '$'