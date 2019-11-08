#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
7. Realizar un programa que pida el nombre de una persona, primer apellido, segundo apellido y
que muestre por pantalla como sería el nombre completo en una sola línea. También mostrar el
nombre completo pero al revés. Finalmente volver a descomponer el nombre completo en sus tres
componentes y mostrarlos por pantalla.
"""

nombre = input("Introduzca el nombre de la persona: ")
primer_apell = input("Introduzca el primer apellido: ")
seg_apell = input("Introduzca el segundo apellido: ")

nombre_completo = nombre + ' ' + primer_apell + ' ' + seg_apell
print("Nombre completo:", nombre_completo)

nombre_completo_rev = nombre_completo[::-1]
print("Nombre completo al revés:", nombre_completo_rev)

lista_nombre = nombre_completo.split()
print("Nombre completo dividido")
print("Nombre:", lista_nombre[0])
print("Primer apellido:", lista_nombre[1])
print("Segundo apellido:", lista_nombre[2])