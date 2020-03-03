#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This program is expected to include all the definitions needed for the
lexer.py to work, this program maskes use of ply.lex which allow us to
use the flex/lex tools in python programming language, in order to execute
the program look at the file 'scripting.py' .

This program was coded as part of the Compiler's design class 
for the period Aug-Dec 2019 ITESM.


A01366101
Ma. Fernanda Delgado Radillo

@author: mfdelgado
"""
#ply.lex permite utilizar herramientas como flex/lex 
#para el lenguaje de prog. python
import ply.lex as lex
#ENUM se usa como set de nombres simbolicos para valores de las constantes
from enum import Enum

class TokenType(Enum):
#necesario para prueba del programa
    ENDFILE = '$'
# que tokens estarán disponibles de acuerdo al lenguaje INCLUYENDO PALABRAS RESERVADAS Y SIMBOLOS
tokens = ('COMMENT', 'PLUS', 'MINUS', 'TIMES','EQUAL', 'COMPARE','NOTEQ', 'SEMICOLON','COMMA', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET','LBLOCK', 'RBLOCK', 
    'ID',  'NUM', 'ENDFILE','DIVIDE', 'LESSER', 'LESSEREQ', 'GREATER', 'GREATEREQ','RESERVED','QUOTES','ERROR','breakline')
# Definicion de onesimbols r.exp
t_LBLOCK= r'\{'
t_RBLOCK= r'}'
t_SEMICOLON= ';'
t_LPAREN= r'\('
t_RPAREN= r'\)'
t_PLUS= r'\+'
t_EQUAL= r'='
t_COMPARE= r'=='
t_LESSER= r'<'
t_GREATER= r'>'
t_MINUS= r'-'
t_ENDFILE= r'\$'
t_ignore= ' \t'
t_COMMA= r','
t_TIMES= r'\*'
t_DIVIDE= r'/'
t_LBRACKET= r'\['
t_RBRACKET= r'\]'
t_LESSEREQ=r'<='
t_GREATEREQ=r'>='
t_NOTEQ=r'!='
t_QUOTES=r'"'


def t_RESERVED(t):
    r'if|else|int|void|return|while'
    return t
def t_error(t):
    #Encuentra la linea en la que aparece el error en el lexer
    lpos = t.lexer.lineno
    #se tokeniza la linea para encontrar los valores pues llegan concatenados
    line = t.lexer.lexdata.split('\n')[lpos - 1]
    #Encuentra posición en la linea de acuerdo al caracter
    Pos = line.find(t.lexer.lexdata[t.lexer.lexpos])
    print(line)
    print(' ' * Pos + '^')
    print("Error de formaciòn del token en la linea " + str(lpos) + ":" + str(Pos))
    t.lexer.skip(1)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_]*'
    return t
def t_newline(t):
	r'\n'
	t.lexer.lineno += 1
def t_NUM(t):
	r'\d+'
	#isalpha es una funciòn que verifica la homogeneidad del token, es todo numero o caracter? 
	if t.lexer.lexdata[t.lexpos + len(t.value)].isalpha():
        #error en la formacion de enteros como 10b
		t_error(t)
	t.value = int(t.value)
	return t

def t_COMMENT(t):
    #r'/\/\*.+?\*\/|\/\/.*(?=[\n\r])/'
    r'\/\*(\*(?!\/)|[^*])*\*\/'
    t.lexer.lineno += t.value.count('\n')
    return t
# obj incializado
lexical = lex.lex()