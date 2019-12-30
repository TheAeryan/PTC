#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 12:11:01 2019

@author: jose
"""

    
    
import ejemplosCython
import ejemplosPython
import matplotlib.pyplot as plt
from time import time
import random
def grafico(titulo,ejex,ejey,cython,python,tamaño):
    plt.plot(tamaño, cython, color='r', label='cython') # r - red colour
    plt.plot(tamaño, python, color='g', label='python') # g - green colour
    plt.xlabel(ejex)
    plt.ylabel(ejey)
    plt.title(titulo)
    plt.legend()
    plt.grid()# [xstart, xend, ystart, yend]
    plt.show()   
    
inicio = 100000
tiemposCython = list()
tiemposPython = list()
elementos = list()

print("QuickShort")
print("---------------------------------------------------------")
for i in range(1,15):
    numeroElementos = i * inicio
    elementos.append(numeroElementos)
    numeros = [i for i in range(numeroElementos)]
    random.shuffle(numeros)
    
    start_time = time()
    ejemplosCython.QuickSort(numeros)
    elapsed_time = time() - start_time
    tiemposCython.append(elapsed_time)
    
    start_time = time()
    ejemplosPython.QuickSort(numeros)
    elapsed_time = time() - start_time
    tiemposPython.append(elapsed_time)
    print("Número Elementos:{} TiempoCython:{} TiempoPython:{}".format(numeroElementos,tiemposCython[-1],tiemposPython[-1]))
    
ejey = "Tiempo de búsqueda(Segundos)"
ejex = "Numero de elementos"
grafico("Ordenación Quickshort",ejex,ejey,tiemposCython,tiemposPython,elementos)
 

print("Multiplicación de matrices")
print("---------------------------------------------------------")

tiemposCython = list()
tiemposPython = list()
elementos = list()

tamMatriz = 20
for i in range(1,15):
    numeroElementos = i * tamMatriz
    matriz1 = [[random.randrange(10) for col in range(numeroElementos)] for row in range(numeroElementos)]
    matriz2 = [[random.randrange(10) for col in range(numeroElementos)] for row in range(numeroElementos)]

    elementos.append(numeroElementos*numeroElementos)
    start_time = time()
    ejemplosCython.multiplicarMatrizCuadrada(matriz1,matriz2,numeroElementos)
    elapsed_time = time() - start_time
    tiemposCython.append(elapsed_time)
    
    
    start_time = time()
    ejemplosPython.multiplicarMatrizCuadrada(matriz1,matriz2,numeroElementos)
    elapsed_time = time() - start_time
    tiemposPython.append(elapsed_time)
    print("""Numero Elementos:{} TiempoCython:{} TiempoPython:{}""".format(numeroElementos,tiemposCython[-1],tiemposPython[-1]))
ejex = "Número elementos de la matriz" 

grafico("Multiplicación de matrices",ejex,ejey,tiemposCython,tiemposPython,elementos)

