from par import parser as par
from semantica import printAST

def globales(prog, pos, long):
    global programa
    global posicion
    global progLong
    programa = prog
    posicion = pos
    progLong = long

def parser(imprime = True):
    t = par.parse(programa)
    if imprime:
        printAST(t, 0)
        return t
    else:
        return t