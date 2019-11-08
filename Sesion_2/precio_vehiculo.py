#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
1. Calcular precio de un vehículo suponiendo que tenemos que pedir como datos de entrada los
siguientes: precio bruto del vehículo, porcentaje de ganancia del vendedor, IVA a aplicar. El precio
base se calcula incrementando el precio bruto con el porcentaje de ganancia. El precio final será el
precio base incrementado con el porcentaje de IVA.
"""

print("Introduzca los datos para calcular el precio del vehículo:")
prec_bruto = float(input("- Precio bruto (euros): "))
porc_ganancia = float(input("- Porcentaje de ganancia del vendedor: "))
IVA = float(input("- IVA: "))

prec_base = prec_bruto + prec_bruto*porc_ganancia/100

prec_final = prec_base + prec_base*IVA/100

print("\nEl precio final es {} €".format(prec_final))