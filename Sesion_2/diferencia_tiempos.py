#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
5. Hacer un programa para calcular la diferencia en horas:minutos:segundos entre dos instantes de
tiempo dados en horas:minutos:segundos.
"""
import math

i1 = input("Introduzca el primer instante de tiempo en formato h m s: ").split()
h1, m1, s1 = [int(x) for x in i1]

i2 = input("Introduzca el segundo instante de tiempo en formato h m s: ").split()
h2, m2, s2 = [int(x) for x in i2]

s_totales_1 = h1*3600 + m1 *60 + s1
s_totales_2 = h2*3600 + m2*60 + s2

s_diff = abs(s_totales_1 - s_totales_2)

h_fin = s_diff // 3600
s_diff = s_diff % 3600

m_fin = s_diff // 60
s_diff = s_diff % 60

s_fin = s_diff

print("\nLa diferencia entre los dos instantes en formato h m s es:", h_fin, m_fin, s_fin)