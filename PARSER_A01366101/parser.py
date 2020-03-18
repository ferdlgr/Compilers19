#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This program is expected to generate an AST as an output, based on the input c- type file recived
as an input which will be analyzed and parsed acoording to the defined grammatical rules that
can be found down in this program. and its tokens definition previously found in the lexer.py program,
in order to execute the program look at the file 'scripting.py'

This program was coded as part of the Compiler's design class
for the period Aug-Dec 2019 ITESM.

A01366101
Ma. Fernanda Delgado Radillo

"""

#importa el lexer(primer proyecto) donde se encuentra la definicion de los tokensy demás variables, se ha modificado el archivo paraincluir las definiciones ahí.
from lexer import tokens
#ply.yacc permite realizar el análisis que yacc realiza para c pero para el lenguaje de programacion python
import ply.yacc as yacc


# Dondesta el inicio de la gramatica
start = 'start'
# porque simbolo empieza si se trata de operaciones, veiene siendo orden de operaciones
precedence = (
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'PLUS', 'MINUS')
)
# funciones que dan la def de regla gramatical
#  yacc ocupa la notacion p_ como t_para lex
def p_fun_declaration(p):
    'fun_declaration : type_specifier ID LPAREN params RPAREN compound_stmt'
    p[0] = ('fun declaration', p[1], p[2], p[3], p[4], p[5], p[6])
#Define la forma del parametro/lista
def p_params(p):
    ''' params      : param_list
                    | VOID
    '''
    p[0] = ('params', p[1])
#Define la forma de mas de un parametro que conforman una lista
def p_param_list(p):
    ''' param_list      : param_list COMMA param
                        | param
    '''
    if len(p) == 3:
        p[0] = ('param list', p[1], p[2], p[3])
    else:
        p[0] = ('param list', p[1])
#Da la pauta de cdonde comenzar
def p_start(p):
    'start    : declaration_list'
    p[0] = ('start program',p[1])
#Da la forma de más de una declaración, en formade lista
def p_declaration_list(p):
    '''     declaration_list    : declaration_list declaration
                                | declaration
    '''
    if len(p) == 3:
        p[0] = ('declaration list', p[1], p[2])
    else:
        p[0] = ('declaration list', p[1])

#Identificador de donde /inicia/termina la funcion
def p_declaration(p):
    '''     declaration     : var_declaration
                            | fun_declaration
                            | ENDFILE
    '''
    p[0] = ('declaration', p[1])

#Declaaracion de una variable con tipo
def p_var_declaration(p):
    '''     var_declaration : type_specifier ID SEMICOLON
                            | type_specifier ID LBRACKET NUMBER RBRACKET SEMICOLON
    '''
    if len(p) == 4:
        p[0] = ('var declaration', p[1], p[2], p[3])
    else:
        p[0] = ('var declaration', p[1], p[2], p[3], p[4], p[5], p[6])
#Identificador tipo de variable
def p_type_specifier(p):
    '''
            type_specifier  : INT
                            | VOID
    '''
    p[0] = ('type specifier',p[1])



def p_param(p):
    ''' param   : type_specifier ID
                | type_specifier LBRACKET RBRACKET
    '''
    if len(p) == 3:
        p[0] = ('param',p[1])
    else:
        p[0] = ('param', p[1], p[2], p[3])

def p_compound_stmt(p):
    'compound_stmt : LBLOCK local_declarations statement_list RBLOCK'
    p[0] = ('compound stmt', p[1], p[2], p[3], p[4])
#Local variables
def p_local_declarations(p):
    ''' local_declarations  : localdeclarations var_declaration
                            |
    '''
    if len(p) == 3:
        p[0] = ("local declarations", p[1], p[2])

#more than 1 statement in list form
def p_statement_list(p):
    ''' statement_list  : statement_list statement
                        |
    '''
    if len(p) == 3:
        p[0] = ('statement list', p[1], p[2])

def p_statement(p):
    ''' statement   : expression_stmt
                    | compound_stmt
                    | selection_stmt
                    | iteration_stmt
                    | return_stmt
    '''
    p[0] = ('statement', p[1])

def p_expression_stmt(p):
    ''' expression_stmt  : expression SEMICOLON
                        | SEMICOLON
    '''
    if len(p) == 3:
        p[0] = ('expression stmt', p[1], p[2])
    else:
        p[0] = ('expression stmt', p[1])

def p_selection_stmt(p):
    ''' selection_stmt  : IF LPAREN expression RPAREN statement
                        | IF LPAREN expression RPAREN statement ELSE statement
    '''
    if len(p) == 6:
        p[0] = ('selection stmt', p[1], p[2], p[3], p[4], p[5])
    else:
        p[0] = ('selection stmt', p[1], p[2], p[3], p[4], p[5], p[6], p[7])

def p_iteration_stmt(p):
    ' iteration_stmt  : WHILE LPAREN expression RPAREN statement'
    p[0] = ('iteration stmt', p[1], p[2], p[3], p[4], p[5])

def p_return_stmt(p):
    ''' return_stmt     : RETURN SEMICOLON
                        | RETURN expression SEMICOLON
    '''
    if len(p) == 4:
        p[0] = ('return stmtm', p[1], p[2])
    else:
        p[0] = ('return stmt', p[1], p[2], p[3])

def p_expression(p):
    ''' expression      : var EQUAL expression
                        | simple_expression
    '''
    if len(p) == 4:
        p[0] = ('expression', p[1], p[2], p[3])
    else:
        p[0] = ('expression', p[1])

def p_var(p):
    ''' var     : ID
                | ID LBRACKET expression RBRACKET
    '''
    if len(p) == 5:
        p[0] = ('var', p[1], p[2], p[3], p[4])
    else:
        p[0] = ('var', p[1])

def p_simple_expression(p):
    ''' simple_expression   : additive_expression relop additive_expression
                            | additive_expression
    '''
    if len(p) == 4:
        p[0] = ('simple expression', p[1], p[2], p[3])
    else:
        p[0] = ('simple expression', p[1])

def p_relop(p):
    ''' relop   : LE
                | LT
                | GREATER
                | LESS
                | COMPARE
                | NE
    '''
    p[0] = ('relop', p[1])

def p_additive_expression(p):
    '''     additive_expression     : additive_expression addop term
                                    | term
    '''
    if len(p) == 4:
        p[0] = ('additive expression', p[1], p[2], p[3])
    else:
        p[0] = ('additive expression', p[1])

def p_addop(p):
    '''     addop   : PLUS
                    | MINUS
    '''
    p[0] = p[1]

def p_term(p):
    ''' term    : term mulop factor
                | factor
    '''
    if len(p) == 4:
        p[0] = ('term', p[1], p[2], p[3])
    else:
        p[0] = ('term', p[1])

def p_mulop(p):
    '''     mulop   : TIMES
                    | DIVIDE
    '''
    p[0] = ('mulop', p[1])

def p_factor(p):
    ''' factor  : LPAREN expression RPAREN
                | ID
                | call
                | NUMBER
    '''
    if len(p) == 4:
        p[0] = ('factor', p[1], p[2] ,p[3])
    else:
        p[0] = ('factor', p[1])

def p_call(p):
    ' call    : ID LPAREN args RPAREN '
    p[0] = ('call', p[1], p[2], p[3], p[4])

def p_args(p):
    ''' args    : arg_list
                |
    '''
    if len(p) == 2:
        p[0] = ('args', p[1])

def p_arg_list(p):
    ''' arg_list    : arg_list COMMA expression
                    | expression
    '''
    if len(p) == 4:
        p[0] = ('arg list', p[1], p[2] ,p[3])
    else:
        p[0] = ('arg list', p[1])


def p_error(p):
    if not p:
        print("EOF")
        return
    while True:
        # Get the next token
        tok = parser.token()
        print("FALLA SIGVALOR := ", tok)
        if not tok or tok.type == 'SEMICOLON' or tok.type == 'RBRACKET': break
    parser.restart()

parser = yacc.yacc(
    debug=True,
    write_tables=False,
    tabmodule="_nomatter",
    errorlog=yacc.NullLogger()
)
#La definición es de suma importancia pues el script de prueba del programa requiere q
#de estas variables para su correcto funcionamiento
def globales(prog, pos, long):
    global programa
    global posicion
    global progLong
    programa = prog
    posicion = pos
    progLong = long
#Esta función imprime el AST con identando en cada vuelta a los nodos
    #descendientes
def printAST(t, count):
    if type(t) is tuple:
        for idx, l in enumerate(t):
            if type(l) is tuple or type(l) is str:
                if len(t) > 1:
                    if idx < 1:
                        if len(t) == 2 and type(t[1]) is str:
                            print('', ' ' * count, t[0])
                        else:
                            print('', ' ' * count,t[0])
                    elif type(l) is str:
                        print('', ' ' * count, l)
                printAST(l, count + 1)

def parse(imprime = True):
    t = parser.parse(programa)
    if imprime:
        printAST(t, 0)
        return t
    else:
        return t
