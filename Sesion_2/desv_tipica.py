#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
2. Dados tres números x1, x2, x3, calcular la desviación típica respecto
 a su media aritmética.
"""
import math

numeros = input("Ingrese los 3 números para calcular su desviación típica: ")
numeros=numeros.split()
a, b, c = [float(x) for x in numeros]

media = (a + b + c) / 3

desv_tipica = math.sqrt(((a - media)**2 + (b - media)**2 + (c - media)**2) / 3)

print("La desviación típica es: {}".format(desv_tipica))