#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
4. Realizar un programa para una caja de un supermercado que lea un precio desde el teclado y una
cantidad entregada por el cliente (se supone que cantidad >= precio) y obtenga en la pantalla el
numero mnimo de monedas de 1 euro, 50 centimos, 10 centimos y 1 centimo que se deben dar de
cambio. Por ejemplo, si precio es 1.12 euros y cantidad es 5 euros, debe dar como resultado 3
monedas de 1 euro, 1 moneda de 50 centimos, 3 monedas de 10 centimos y 8 monedas de 1
centimo.
"""
import math

precio = float(input("Introduzca el precio del artículo en euros: "))
pagado = float(input("Introduzca la cantidad pagada por el cliente en euros: "))

dif = pagado - precio

# Lo transformo a céntimos
cent_totales = math.floor(dif*100)

num_1_euro = cent_totales // 100
cent_totales = cent_totales % 100

num_50_cent = cent_totales // 50
cent_totales = cent_totales % 50

num_10_cent = cent_totales // 10
cent_totales = cent_totales % 10

num_1_cent = cent_totales

print("El cambio a dar es:")
print("- Monedas de 1€:", num_1_euro)
print("- Monedas de 50 cent:", num_50_cent)
print("- Monedas de 10 cent:", num_10_cent)
print("- Monedas de 1 cent:", num_1_cent)
