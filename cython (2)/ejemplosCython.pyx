#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# distutils: language = c++
"""
Created on Fri Dec  6 17:16:50 2019

@author: jose
"""

from libcpp.vector cimport vector

def busqueda_binaria(lista, int x):
    cdef int izq = 0 
    cdef int der = len(lista) -1
    while izq <= der:
        medio = (izq+der)/2

        if lista[medio] == x:
            return medio

        elif lista[medio] > x:
            der = medio-1


        else:
            izq = medio+1

    return -1



def QuickSort(vector[int] lista):
    cdef vector[int] izquierda = []
    cdef vector[int] centro = []
    cdef vector[int] derecha = []
    
    if len(lista) > 1:
        pivote = lista[0]
        for i in lista:
            if i < pivote:
                izquierda.push_back(i)
            elif i == pivote:
                centro.push_back(i)
            elif i > pivote:
                derecha.push_back(i)

        return QuickSort(izquierda)+centro+QuickSort(derecha)
    else:
      return lista
 
def multiplicarMatrizCuadrada(vector[vector[int]] matriz1, vector[vector[int]] matriz2, int numElementos):
    resultado = [[0 for col in range(numElementos)] for row in range(numElementos)]
        
    for i in range(numElementos):
        for j in range(numElementos):
            for k in range(numElementos):
                resultado[i][j] += matriz1[i][k] * matriz2[k][j]
                
    return resultado