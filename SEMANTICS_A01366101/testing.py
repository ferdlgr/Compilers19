#archivo de prueba proporcionado en canvas
from semantica import *
from parser import *
from globalTypes import *
f = open('sample.c-', 'r')
programa = f.read() 
progLong = len(programa) 
programa = programa + '$'  
posicion = 0      
globales(programa, posicion, progLong)
AST = parser(True)
semantica(AST, True) 