#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This prgram correspond to the script for testing the C- lexical analyzer
in python for the compilers design class.
"""

from globalTypes import *
from lexer import *
 
f = open('sample.c-', 'r')
programa = f.read() # lee todo el archivo a compilar
progLong = len(programa) # longitud original del programa
programa = programa + '$' # agregar un caracoter $ que represente EOF
posicion = 0 # posición del caracter actual del string
 
# función para pasar los valores iniciales de las variables globales
globales(programa, posicion, progLong)
 
token, tokenString = getToken(True)
while (token != TokenType.ENDFILE):
    token, tokenString = getToken(True)
    