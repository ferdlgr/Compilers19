#Este programa pertenece a la parte 3 del proyecto de la clase diseño de compiladores del 
#semestre Agosto-Diciembre 2019
#A01366101

#exit from sys funciona como mecanismo de catch de errores, si se despliega con el comando el traceback se visualiza el procesamiento sintactico
#desafortunadamente la prueba de recuperacion de errores no fuesatisfactoria, si reconoce el error se dirige al emcanismo de salida
#imprime el arbol y reconoce que el elemento no se encontro en la tabla
#ah� se dirige el mecanismo de salida, no reinicia
from sys import exit

#arreglos de almacenamiento funcional como la tabla de valores,simbs
tables, values, current, n = [], [], 0, 0

def globales(prog, pos, long):
    global programa
    global posicion
    global progLong
    programa = prog
    posicion = pos
    progLong = long

#implementa el arbol basado en reglas del alcance definido para c- , usando el resultado del parser
def semantica(arbol, imprime=True):
    global current, n
    n = 2
    tabla(arbol)
    current = 0
    recorre(arbol, 0)

#define las tablas de símbolos, usa recursion para los recorridos, tabla por cada rango
def tabla(t, imprime=True, alcance=0):
    global current

    
    def isEmpty(var, alcance): return True if var not in tables[alcance] else False
    

    if t is None or type(t) is int:
        return
    if t[0] == 'start program':
        tables.append({'alcance': alcance})
        tabla(t[1], imprime, alcance)
    elif t[0] == 'declaration list' or t[0] == 'compound stmt' or t[0] == 'local declarations' or t[0] == 'statement list':
        for x in t:
            tabla(x, imprime, alcance)
    elif t[0] == 'statement' or t[0] == 'expression stmt' or t[0] == 'expression' or t[0] == 'selection stmt' or t[0] == 'iteration stmt':
        for x in t:
            tabla(x, imprime, alcance)
    elif t[0] == 'return stmtm' or t[0] == 'return stmtm' or t[0] == 'simple expression' or t[0] == 'additive expression' or t[0] == 'term':
        for x in t:
            tabla(x, imprime, alcance)
    elif t[0] == 'factor' or t[0] == 'args' or t[0] == 'arg list':
        for x in t:
            tabla(x, imprime, alcance)
    elif t[0] == 'declaration':
        tabla(t[1], imprime, alcance)
    elif t[0] == 'var declaration':
        if isEmpty(t[2], alcance):
            if len(t) == 4:
                tables[alcance][t[2]] = t[1][1]
            else:
                tables[alcance][t[2]] = f"{t[1][1]}, {t[3]}, {str(t[4])}, {t[5]}"
    elif t[0] == 'fun declaration':
        current += 1
        tables.append({'alcance': current})
        if isEmpty(t[2], alcance):
            if t[4][1] == 'void':
                tables[0][t[2]] = f"{t[1][1]}, fun, void"
            else:
                tables[0][t[2]] = f"{t[1][1]}, fun"
                checkParams(t[2], t[4], current)
            tabla(t[6], imprime, current)
    elif t[0] == 'var':
        if not validations(t[1], alcance):
            exit()
    elif t[0] == 'call':
        if not validations(t[1], alcance):
            exit()
        else:
            for x in t:
                tabla(x, imprime, alcance)
            print("tables for x in t")
            print(tables ,"\n")
            print("ast vals")
            print (t)
            
#Recibe el output del parser(AST) y realiza el recorrido
def recorre(t, alcance):
    global current
    if t is None or type(t) is int:
        return
    nextStep = t[0]
    if nextStep == 'start program' or nextStep == 'declaration' or nextStep == 'statement' or nextStep == 'expression stmt':
        recorre(t[1], alcance)
    elif nextStep == 'declaration list' or nextStep == 'compound stmt' or nextStep == 'statement list':
        for x in t:
            recorre(x, alcance)
    elif nextStep == 'fun declaration':
        current += 1
        recorre(t[6], current)
    elif nextStep == 'expression':
        if len(t) == 4:
            if t[1][1] in tables[alcance] and tables[alcance][t[1][1]] == 'int':
                if markVal(t[3], t[1][1], alcance):
                    return True
                else:
                    print(f"Error: Assigned value {t[1][1]} is different than {tables[alcance][t[1][1]]}")
                    exit()
        else:
            recorre(t[1], alcance)
    elif nextStep == 'simple expression':
        if len(t) == 2:
            checkFunc(t[1], alcance)

# Marca dentro que rango se encuentra la vatiable y el tipo en el alcance
def markVal(exp, v, alcance):
    if exp[0] == 'expression': return markVal(exp[1], v, alcance)
    elif exp[0] == 'simple expression' or exp[0] == 'additive expression' or exp[0] == 'term':
        for e in exp: return markVal(e, v, alcance)
    elif exp[0] == 'factor':
        if type(exp[1]) is int:
            if v in tables[alcance]:
                if tables[alcance][v] == 'int': return True
            elif v in tables[0]:
                if tables[0][v] == 'int': return True
            else:
                print(f"Error: Variable {exp[1]} is not declared in this alcance")
                exit()
        else:
            if len(exp) == 4: return markVal(exp[2], v, alcance)
            else: return markVal(exp[1], v, alcance)
    elif exp[0] == 'call':
        if exp[1] in tables[0]:
            temp = tables[0][exp[1]].split(",")
            if temp[0] == tables[alcance][v]: return True
            else:
                print(f"Error: Variables no corresponden {temp[0]} y {tables[alcance][v]}")
        else:
            print(f"Error: Unkown method {exp[1]}")
            exit()
    elif exp[0] == 'var':
        if exp[1] in tables[alcance]:
            return True if tables[alcance][exp[1]] == tables[alcance][v] else False
        elif exp[1] in tables[0]:
            return True if tables[0][exp[1]] == tables[0][v] else False
        else:
            print("Unkown error")
            return False


#Da valor a cada funcion en un pase definido
def checkFunc(exp, alcance):
    global values, n
    if exp[0] == 'call':
        if exp[1] in tables[0]:
            values = tables[0][exp[1]].split(",")
            checkFunc(exp[3], alcance)
        else:
            print(f"Error: {exp[1]} no esta definida")
            exit()
    elif exp[0] == 'args' or exp[0] == 'expression': 
        checkFunc(exp[1], alcance)
    elif exp[0] == 'arg list' or exp[0] == 'simple expression' or exp[0] == 'additive expression' or exp[0] == 'term':
        for e in exp: checkFunc(e, alcance)
    elif exp[0] == 'var':
        if exp[1] in tables[alcance]:
            temp = tables[alcance][exp[1]].split(",")
            if temp[0] == values[n]:
                n += 2
                return True
            else:
                print(f"Error: Value of {values[n]} is not {temp[0]}")
                exit()
        elif exp[1] in tables[0]:
            temp = tables[0][exp[1]].split(",")
            if temp[0] == values[n]: return True
            else:
                print(f"Error: Value {values[n]}, is not {temp[0]}")
                exit()
    elif exp[0] == 'factor':
        if type(exp[1]) is int:
            if 'int' == values[n]:
                n += 2
                return True
        else:
            return checkFunc(exp[2], alcance) if len(exp) == 4 else checkFunc(exp[1], alcance)


# Mete los parametros recibidos para el pase
def checkParams(func, params, alcance):
    if params[0] == 'params': checkParams(func, params[1], alcance)
    if params[0] == 'param list':
        for p in params: checkParams(func, p, alcance)
    elif params[0] == 'param':
        tables[alcance][params[2]] = params[1][1]
        tables[0][func] = f"{tables[0][func]}, {params[1][1]}, {params[2]}"


# Validacion por alcance
def validations(var, alcance):
    res = True
    if var not in tables[alcance] and var not in tables[0]:
        print("Error:")
        print(f" No se Encuentra en la tabla \"{var}\" ")
        print("\n Tables")
        print(tables)
        res =  False 
    return res


def printAST(lvl, count):
    if type(lvl) is tuple:
        for idx, l in enumerate(lvl):
            if type(l) is tuple or type(l) is str:
                if len(lvl) > 1:
                    if idx < 1:
                        if len(lvl) == 2 and type(lvl[1]) is str:
                            print(' ', ' ' * count, lvl[0])
                        else:
                            print(' ', ' ' * count, lvl[0])
                    elif type(l) is str:
                        print(' ', ' ' * count, l)
                printAST(l, count + 1)
                #print(tables)

