#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Carlos Núñez Molina
"""

# Usando remove
def eliminar_els_sin_lista_auxiliar_1(lista, elem):
    quedan_elementos = True
    
    while quedan_elementos:
        try:
            lista.remove(elem)
        except ValueError:
            quedan_elementos = False
    
    return lista

# Iterando sobre la lista (removiendo los elementos uno a uno con del)
def eliminar_els_sin_lista_auxiliar_2(lista, elem):
    i = len(lista)-1
    
    while i >= 0:
        if lista[i] == elem:
            del lista[i]
            
        i-=1
    
    return lista

# Usando index y del, eliminando un slice
def eliminar_els_sin_lista_auxiliar_3(lista, elem):
    ind_min = lista.index(elem)
    ind_max = lista[::-1].index(elem)
    ind_max = len(lista) - ind_max
    
    del lista[ind_min:ind_max]
    
    return lista   

# Usando index y del, repitiendo el proceso hasta que no hay elementos
def eliminar_els_sin_lista_auxiliar_4(lista, elem):
    quedan_elementos = True
    
    while quedan_elementos:
        try:
            index = lista.index(elem)
            del lista[index]
        except ValueError:
            quedan_elementos = False
    
    return lista  

# Usando "in"
def eliminar_els_sin_lista_auxiliar_5(lista, elem):
    while elem in lista:
        lista.remove(elem)
    
    return lista  

# Iterando sobre la lista (removiendo los elementos uno a uno con pop)
def eliminar_els_sin_lista_auxiliar_6(lista, elem):
    i = len(lista)-1
    
    while i >= 0:
        if lista[i] == elem:
            lista.pop(i)
            
        i-=1
    
    return lista

if __name__ == '__main__':
    lista = [1,3,5,7,7,7,7,8,10,12,15]
    elem = 7
    
    print("\nMétodo 1:", eliminar_els_sin_lista_auxiliar_1(lista.copy(), elem))
    print("\nMétodo 2:", eliminar_els_sin_lista_auxiliar_2(lista.copy(), elem))
    print("\nMétodo 3:", eliminar_els_sin_lista_auxiliar_3(lista.copy(), elem))
    print("\nMétodo 4:", eliminar_els_sin_lista_auxiliar_4(lista.copy(), elem))
    print("\nMétodo 5:", eliminar_els_sin_lista_auxiliar_5(lista.copy(), elem))
    print("\nMétodo 6:", eliminar_els_sin_lista_auxiliar_6(lista.copy(), elem))