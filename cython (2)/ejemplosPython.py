#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 17:41:26 2019

@author: jose
"""


def QuickSort(lista):
    izquierda = []
    centro = []
    derecha = []
    if len(lista) > 1:
        pivote = lista[0]
        for i in lista:
            if i < pivote:
                izquierda.append(i)
            elif i == pivote:
                centro.append(i)
            elif i > pivote:
                derecha.append(i)
        #print(izquierda+["-"]+centro+["-"]+derecha)
        return QuickSort(izquierda)+centro+QuickSort(derecha)
    else:
      return lista

def multiplicarMatrizCuadrada(matriz1, matriz2, numElementos):
    resultado = [[0 for col in range(numElementos)] for row in range(numElementos)]
    """resultado = list()
    for i in range(numElementos):
        listaNueva = list()
        for j in range(numElementos):
            listaNueva.append(0)
        resultado.append(listaNueva)"""
        
        
    for i in range(numElementos):
        for j in range(numElementos):
            for k in range(numElementos):
                resultado[i][j] += matriz1[i][k] * matriz2[k][j]
                
    return resultado
        

        
    