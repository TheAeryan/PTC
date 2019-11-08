#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
3. Realizar un programa que lea una cantidad de horas, minutos y segundos con valores arbitrarios,
y los transforme en una expresion de tiempo convencional en la que los minutos y segundos dentro
del rango [0,59]. Por ejemplo, dadas 10 horas, 119 minutos y 280 segundos, debera dar como
resultado 12 horas, 3 minutos y 40 segundos.
"""

entrada = input("Introduzca el número de horas, minutos y segundos: ")
entrada = entrada.split()
h, m, s = [int(x) for x in entrada]

# Convierto todo a segundos
s_totales = h*60*60 + m*60 + s

h_fin = s_totales // (60*60)
s_totales = s_totales % (60*60)

m_fin = s_totales // 60
s_totales = s_totales % 60

s_fin = s_totales

print("El tiempo final es: {} horas {} minutos y {} segundos".format(h_fin, m_fin, s_fin))

