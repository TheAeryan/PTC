# -*- coding: utf-8 -*-

import numpy as np
import time
import matplotlib.pyplot as plt
import json
import os
import glob
import math

# Parámetros fijados con la experimentación para obtener buenos clusters
min_puntos_cluster=1
max_puntos_cluster=20
umbral_distancia = 0.1

distancias = ['Cerca', 'Medio', 'Lejos']

def leer_datos_json(nom_fichero):
    """
    Lee un archivo JSON correspondiente a los datos del simulador y
    devuelve los puntos como una lista de diccionarios.
    """
    
    objetos = []
    
    # Leo el fichero JSON
    with open(nom_fichero, 'r') as f:
        for line in f:
            objetos.append(json.loads(line))
            
    # Devuelvo los puntos como una lista de la forma siguiente:
    # puntos[i] -> puntos de la iteración i
    # puntos[i][0] -> coordenadas X de los puntos de la iteración i
    # puntos[i][1] -> coordenadas Y de los puntos de la iteración i
    puntos = [[obj['PuntosX'], obj['PuntosY']] for obj in objetos[1:-1]]
    
    return puntos

def dist(x1, y1, x2, y2):
    """
    Calcula la distancia euclídea entre los puntos 1 y 2.
    """
    
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def crear_clusters(datos):
    """
    Devuelve los clusters de puntos usando el algoritmo de agrupación
    por distancia de salto.
    """
    
    clusters = []
    
    # Calculo los clusters para los puntos de cada iteración
    for datos_it in datos:
        # Añado el primer punto al posible cluster
        x_prev, y_prev = datos_it[0][0], datos_it[1][0]
        cluster_actual = [[x_prev, y_prev]]
        
        # Recorro el resto de puntos
        for i in range(1, len(datos_it[0])):
            x, y = datos_it[0][i], datos_it[1][i] # Coordenadas del nuevo punto
            
            # Si se va a superar el número máximo de puntos del clúster,
            # este nuevo punto se añade como primer punto del siguiente cluster
            if len(cluster_actual) == max_puntos_cluster:
                # Añado el cluster actual a los clusters
                clusters.append(cluster_actual)
                
                cluster_actual = [[x, y]]
            else:
                # Si la distancia con el punto anterior no supera a umbral_distancia
                # el nuevo punto se incorpora al cluster actual
                if dist(x, y, x_prev, y_prev) <= umbral_distancia:
                    cluster_actual.append([x, y])
                # Si la supera, se crea un nuevo clúster
                else:
                    # Añado el cluster_actual a los clusters siempre que
                    # el número de puntos sea suficiente
                    if len(cluster_actual) >= min_puntos_cluster:
                        clusters.append(cluster_actual)
                    
                    cluster_actual = [[x, y]]
                    
            x_prev, y_prev = x, y
                
    return clusters

if __name__=='__main__':
    # <Leo los puntos>
    
    # Ejemplos positivos
    datos_positivos = []
    
    listaDir=sorted(glob.glob("positivo*")) # Carpetas con los ejemplos positivos
    
    for carpeta in listaDir:
        os.chdir(carpeta) # Cambio el directorio de trabajo a la carpeta
        
        # Obtengo el nombre del archivo json con los datos
        nom_archivo = glob.glob('*.json')[0]
        
        # Leo los datos del archivo
        datos_archivo = leer_datos_json(nom_archivo)
        
        # Los añado a los datos positivos
        datos_positivos += datos_archivo
        
        os.chdir('..') # Vuelvo al antiguo directorio de trabajo

    # Ejemplos negativos
    datos_negativos = []
    
    listaDir=sorted(glob.glob("negativo*")) # Carpetas con los ejemplos negativos
    
    for carpeta in listaDir:
        os.chdir(carpeta) # Cambio el directorio de trabajo a la carpeta
        
        # Obtengo el nombre del archivo json con los datos
        nom_archivo = glob.glob('*.json')[0]
        
        # Leo los datos del archivo
        datos_archivo = leer_datos_json(nom_archivo)
        
        # Los añado a los datos negativos
        datos_negativos += datos_archivo
        
        os.chdir('..') # Vuelvo al antiguo directorio de trabajo
        
    # <Creo los clusters>
    
    # Clusters positivos (de piernas)
    clusters_positivos = crear_clusters(datos_positivos)
    
    # Clusters negativos (de cilindros)
    clusters_negativos = crear_clusters(datos_negativos)        
