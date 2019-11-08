"""
Realizar un programa que solicite los dos catetos de un triángulo rectángulo y que calcule la
hipotenusa mostrando la salida por pantalla.
"""
import math

entrada = input('Inserte las longitud de los dos catetos del triángulo rectángulo: ')

l1, l2 = entrada.split(' ')
l1 = float(l1)
l2 = float(l2)

hipotenusa = math.sqrt(l1*l1 + l2*l2)

print('La longitud de la hipotenusa es %f' % hipotenusa)