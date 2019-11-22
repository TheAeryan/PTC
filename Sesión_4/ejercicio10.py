#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
10. Leer una frase de teclado e implementar una función que devuelva una lista de pares en la que
debe aparecer cada letra junto a su frecuencia de aparición. Los espacios no se deben tener en
cuenta. Dicha lista debe estar ordenada atendiendo al orden ascendente de las letras. Ejemplo: ante
la entrada “programa” debe dar como salida [('a', 2), ('g', 1), ('m',1), ('o', 1), ('p',1), ('r',2)].
"""

# HACER UNA VERSIÓN CON LAS FUNCIONES DE LIST Y OTRA SIN USARLA

# Función que no usa los métodos de string
def devolverFrecuenciasLetras1(frase):
    dict_frecuencias = dict() # Diccionario que guardará los pares
    
    for letra in frase:
        if letra != ' ': # Me salto los espacios en blanco
            # Compruebo si está en el diccionario
            if letra in dict_frecuencias:
                # Aumento la frecuencia en 1
                dict_frecuencias[letra] = dict_frecuencias[letra] + 1
            # No está en el diccionario
            else:
                # Añado la letra al diccionario con frecuencia 1
                dict_frecuencias[letra] = 1
                
    # Obtengo la lista con los elementos del diccionario
    list_frec = list(dict_frecuencias.items())
    
    # Ordeno los elementos de la lista de forma alfabética según
    # la letra
    list_frec_ord = sorted(list_frec)
                
    # Devuelvo la lista ordenada de frecuencias
    return list_frec_ord
   
# Función que usa los métodos de string
def devolverFrecuenciasLetras2(frase):
     pass
        
if __name__ == '__main__':
    frase = input('Introduzca una frase: ')
    
    # Obtengo las frecuencias con cada una de las dos funciones
    lista_frecuencias1 = devolverFrecuenciasLetras1(frase)
    lista_frecuencias2 = devolverFrecuenciasLetras2(frase)
    
    if lista_frecuencias1 == lista_frecuencias2:
        print("\nLa lista de frecuencias es:", lista_frecuencias1)
    else:
        print("ERROR -> ambas funciones no devuelven el mismo resultado!")