#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 11:38:39 2019

@author: aeryan
"""

rows = 5
cols = 3

matriz_ceros = [ [0 for col in range(cols)] for row in range(rows)]

print("Matriz inicial: ", matriz_ceros)

matriz_ceros[1][2] = 3

print("Matriz tras haber cambiado un valor: ", matriz_ceros)

print("\nForma2")

# Forma 2

matriz_ceros = []

for row in range(rows):
    matriz_ceros.append([])

    for col in range(cols):
        matriz_ceros[row].append([])
        matriz_ceros[row][col] = 0

print("Matriz inicial: ", matriz_ceros)

matriz_ceros[1][2] = 3

print("Matriz tras haber cambiado un valor: ", matriz_ceros)      
