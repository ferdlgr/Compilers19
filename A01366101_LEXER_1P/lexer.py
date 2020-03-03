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

@author: mfdelgado
"""
from globalTypes import * #variables y definiciones
#from globalTypes import lexical #objeto 
#globales y gettoken son necesarias para que la prueba
#por script sea exitosa
def globales(prog, pos, long): #las va a recibir del programa entrante y en el script
    global programa 
    global posicion
    global progLong
    programa = prog
    posicion = pos #se asignan los valores del input program y script que nedesita de parametro la funcion
    progLong = long
def getToken(imprime = True):#llamada en script
    if lexical.lexdata == None: # esta vacio?
        lexical.input(programa)
    tkn = lexical.token() #Tokenizador
    if not tkn:
        print('Error en la lectura')# ya no se obtuvo respuesta(no hay token.next)
        return
    else:
        if tkn.value == TokenType.ENDFILE.value: 
            return TokenType.ENDFILE, TokenType.ENDFILE.value #Documento vacìo
        if imprime: 
            print(str(tkn.type) + ' = ' + str(tkn.value)) #lo que esta en el documento
        return tkn.type, tkn.value #id + value
        