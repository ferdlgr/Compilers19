#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This program is expected to pass throug its function the variables received throught the script and
file reading to the global variables, making use of the globalTypes program, its values and tools,
print each token found in the iput file and its definition previously found in gloobalTypes,
in order to execute the program look at the file 'scripting.py' .

This program was coded as part of the Compiler's design class
for the period Aug-Dec 2019 ITESM.

A01366101
Ma. Fernanda Delgado Radillo

"""
#variables y definiciones
#from globalTypes import lexical #objeto

from ply import *

#tokens
keywords = {
    'int': 'INT',
    'void': 'VOID',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'return': 'RETURN'
}
# symbols
tokens = [
    'PLUS','MINUS', 'TIMES','DIVIDE', 'LT','LE', 'GREATER','LESS',
    'COMPARE','NE', 'EQUAL','SEMICOLON', 'COMMA','LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET','LBLOCK', 'RBLOCK','COMMENTS', 'ID',
    'NUMBER','ENDFILE'
] + list(keywords.values())

# Define regular expressions
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_COMMA      = r'\,'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_LBLOCK      = r'\{'
t_RBLOCK      = r'\}'
t_LESS      = r'<'
t_GREATER   = r'>'
t_LE        = r'<='
t_LT        = r'>='
t_COMPARE    = r'=='
t_NE      = r'!='
t_EQUAL    = r'='
t_SEMICOLON = r';'
t_ENDFILE   = r'\$'

t_ignore = ' \t'

from enum import Enum
class TokenType(Enum): ENDFILE = '$'
literals = ['*','/','+','-']


def t_ID(t):
    r'[a-zA-Z][a-zA-Z]*'
    t.type = keywords.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    # Regex to identify comment block, do nothing
    r'\/\*(\*(?!\/)|[^*])*\*\/'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_NUMBER(t):
    r'\d+'
    # ID that starts with numbers
    if t.lexer.lexdata[t.lexpos + len(t.value)].isalpha():
        t_error(t)
    t.value = int(t.value)
    return t

def t_error(t):
    errorline = t.lexer.lineno

    line = t.lexer.lexdata.split('\n')[errorline - 1]
    tabPos = line.find(t.lexer.lexdata[t.lexer.lexpos])
    print("Error de Sintaxis en " + str(errorline) + ":" + str(tabPos))
    print(line)
    print(' ' * tabPos + '^')
    t.lexer.skip(1)

lexer = lex.lex()
