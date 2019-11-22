#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Carlos Núñez Molina
"""


"""
10. Leer una frase de teclado e implementar una función que devuelva una lista de pares en la que
debe aparecer cada letra junto a su frecuencia de aparición. Los espacios no se deben tener en
cuenta. Dicha lista debe estar ordenada atendiendo al orden ascendente de las letras. Ejemplo: ante
la entrada “programa” debe dar como salida [('a', 2), ('g', 1), ('m',1), ('o', 1), ('p',1), ('r',2)].
"""

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
     # Creo un set con los caracteres de frase, menos el espacio
     set_carac = set(frase)
     set_carac.discard(' ') # Elimina el espacio en blanco, en caso de existir en el set
     
     # Lo paso a una lista y ordeno los caracteres por orden alfabético
     list_carac_ord = sorted(list(set_carac))
     
     # Uso la función count para obtener el número de ocurrencias
     # de cada caracter en la frase
     list_frec_ord = [(carac, frase.count(carac)) for carac in list_carac_ord]
     
     return list_frec_ord
        
if __name__ == '__main__':
    frase = input('Introduzca una frase: ')
    
    # Obtengo las frecuencias con cada una de las dos funciones
    lista_frecuencias1 = devolverFrecuenciasLetras1(frase)
    lista_frecuencias2 = devolverFrecuenciasLetras2(frase)
    
    print("<Lista de frecuencias>")
    print("\nSin los métodos de string:", lista_frecuencias1)
    print("\nCon los métodos de string:", lista_frecuencias2)