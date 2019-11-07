# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:29:03 2019

@author: Eugenio

Ejemplo para leer los valores de las tablas de HTML
"""
from html.parser import HTMLParser
#https://docs.python.org/3.7/library/html.parser.html?highlight=html%20parser

class MyHTMLParser(HTMLParser):

    values = []
    # analizamos lo que tiene que hacer al encontrar datos
    def handle_data(self, data):
        if '\n' not in data and 'Ciudades' not in data:            
            self.values.append(data)
    #para devolver los valores
    def get_values(self):
        return self.values
    
       

#leemos el fichero de Comunidades
#el valor de codificacion es necesario en linux
        
comunidadesFich=open('comunidadesAutonomas.htm', 'r', encoding="windows-1250")

comString=comunidadesFich.read()

inicioTab=comString.find('<td>01')
finTab=comString.find('</tbody>')

comString=comString[inicioTab:finTab]

print(comString)

parser = MyHTMLParser()

parser.feed(comString)

comun_lista=parser.get_values()


print(comun_lista)



