#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def funcion1():
    print("Módulo funciones. Función 1.")
    
def funcion2():
    print("Módulo funciones. Función 2.")
    
if __name__ == '__main__':
    print("Módulo funciones llamado como fichero principal.")
    funcion1()
    funcion2()
    
if __name__ == "modulo_funciones":
    print("Módulo funciones está siendo importado")