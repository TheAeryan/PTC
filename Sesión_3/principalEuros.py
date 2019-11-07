#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Carlos Núñez Molina
"""

from financiacion import *

# Entrada

str_capital_inicial = input("Capital inicial: ")
str_interes_anual = input("% interés anual: ")
num_anios = int(input("Número de años: "))

capital_inicial = float(str_capital_inicial)
interes_anual = float(str_interes_anual)

# Me aseguro de que sea un número decimal
if len(str_capital_inicial.split('.')) > 1 and len(str_interes_anual.split('.')) > 1:
    num_dec_capital_inicial = len(str_capital_inicial.split('.')[1])
    num_dec_interes_anual = len(str_interes_anual.split('.')[1])
    
    entrada_correcta = (capital_inicial > 0) and (interes_anual > 0) and \
                       (num_anios > 0) and (num_dec_capital_inicial == 2) \
                       and (num_dec_interes_anual == 2)
else:
    entrada_correcta = False


while not entrada_correcta:
    str_capital_inicial = input("Capital inicial: ")
    str_interes_anual = input("% interés anual: ")
    num_anios = int(input("Número de años: "))
    
    capital_inicial = float(str_capital_inicial)
    interes_anual = float(str_interes_anual)
    
    # Me aseguro de que sea un número decimal
    if len(str_capital_inicial.split('.')) > 1 and len(str_interes_anual.split('.')) > 1:
        num_dec_capital_inicial = len(str_capital_inicial.split('.')[1]) # Número de posiciones decimales
        num_dec_interes_anual = len(str_interes_anual.split('.')[1])
        
        entrada_correcta = (capital_inicial > 0) and (interes_anual > 0) and \
                           (num_anios > 0) and (num_dec_capital_inicial == 2) \
                           and (num_dec_interes_anual == 2)
    else:
        entrada_correcta = False
                
# Calculo el capital acumulado        
capital_acumulado = calcularCapitalFinalAnios(capital_inicial, interes_anual, num_anios)

# Imprimo el resultado
print(f"\nEl capital acumulado tras aplicar el interés tras {num_anios} años es {capital_acumulado} €.")