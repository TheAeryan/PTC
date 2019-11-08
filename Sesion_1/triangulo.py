""" Realizar un programa que solicite la base y altura de un triángulo y 
calcule su área mostrando la salida por pantalla."""

entrada = input('Inserte la base y altura del triángulo: ')

base, altura = entrada.split(' ')
base = float(base)
altura = float(altura)

area = base*altura / 2

print('El área del triángulo es %f' % area)