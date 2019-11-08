#!/usr/bin/env python3
# -*- coding: utf-8 -*-

numero1 = 0.1 + 0.1 + 0.1
numero2 = 0.3

if numero1 == numero2:
    print("Son iguales")
else:
    print("Son diferentes!")
    
# Solución a la imprecisión de los float
    
from decimal import Decimal, getcontext

a = Decimal('0.1')
b = a+a+a

if b == Decimal('0.3'):
    print("Son iguales")
else:
    print("Son diferentes!")