#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Carlos Núñez Molina
"""

def redondear(numero, decimales):
    numero=numero*(10**decimales)
    numero=numero + 0.5
    numero=(int)(numero)
    numero=numero/(10**decimales)
    
    return numero

def calcularCapitalFinal(capitalInicial, interes):
    cantidad_interes = capitalInicial * (interes / 100)
    capital_final = capitalInicial + cantidad_interes
    capital_final = redondear(capital_final, 2)
    
    return capital_final
    
def calcularCapitalFinalAnios(capitalInicial, interes, num_anios):
    capital_actual = capitalInicial
    
    for _ in range(num_anios):
        capital_actual = calcularCapitalFinal(capital_actual, interes)
        
    return capital_actual