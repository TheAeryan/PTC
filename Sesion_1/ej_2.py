"""
Realizar un programa que solicite el radio de una circunferencia y calcule su longitud y el
área del círculo mostrando la salida por pantalla.
"""
import math

entrada = input('Inserte el radio de la circunferencia: ')

radio = float(entrada)

longitud = 2*math.pi*radio
area = math.pi*radio*radio

print('La longitud de la circunferencia es %f' % longitud)
print('El area del círculo es %f' % area)