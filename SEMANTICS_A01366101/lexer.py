# This code was made with ply lexer based on the documentation
# src: https://www.dabeaz.com/ply/ply.html#ply_nn2
from ply import *

# All of the tokens available in the language
keywords = {
    'int': 'INT',
    'void': 'VOID',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'return': 'RETURN'
} 
# symbols & others
tokens = [
    'PLUS','MINUS', 'TIMES','DIVIDE', 'LT','LE', 'GREATER','LESS',
    'COMPARE','NE', 'EQUAL','SEMICOLON', 'COMMA','LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET','LBLOCK', 'RBLOCK','COMMENTS', 'ID',
    'NUMBER','ENDFILE'
] + list(keywords.values())

# Define regular expression of our symbols so it's 
# easy to identify them
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

# The t_TokenName is asyntaxis required by ply.lex
def t_ID(t):
    r'[a-zA-Z][a-zA-Z]*'
    t.type = keywords.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    # Regex to identify comment block, do nothing
    # src: https://stackoverflow.com/questions/16160190/regular-expression-to-find-c-style-block-comments
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
    # ply.lex puts everything in one line so we need to split it
    # to get the correct pos of the error
    line = t.lexer.lexdata.split('\n')[errorline - 1]
    tabPos = line.find(t.lexer.lexdata[t.lexer.lexpos])
    print("Syntax Error @ line " + str(errorline) + ":" + str(tabPos))
    print(line)
    print(' ' * tabPos + '^')
    t.lexer.skip(1)

lexer = lex.lex()
