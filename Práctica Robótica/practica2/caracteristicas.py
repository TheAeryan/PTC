# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import math
import json
import os
import sys

def leer_fichero_json(nombre_fichero):
    """
    Lee el fichero JSON @nombre_fichero y devuelve su contenido como una lista
    de diccionarios.
    """
    objetos = []
    
    # Leo el fichero JSON
    with open(nombre_fichero, 'r') as f:
        for line in f:
            objetos.append(json.loads(line))
            
    return objetos

def guardar_fichero_json(datos, nombre_fichero):
    """
    Guarda @datos (una lista de diccionarios) en el archivo @nombre_fichero
    usando el formato JSON.
    """
    
    # Si el archivo ya existe lanzo una excepción
    if os.path.exists(nombre_fichero):
        raise FileExistsError('¡Ya existe el archivo!')
    
    # Abro el archivo
    with open(nombre_fichero, 'w') as f:
        # Cada elemento de datos es una línea del fichero
        for elem in datos:
            f.write(json.dumps(elem)+'\n')

def dist(x1, y1, x2, y2):
    """
    Calcula la distancia euclídea entre los puntos 1 y 2.
    """
    
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def dist_punto_a_recta(x, y, A, B, C):
    """
    Calcula la distancia del punto (x, y) a la recta Ax + By + C = 0.
    """
    
    return abs(A*x + B*y + C) / math.sqrt(A**2 + B**2)

def obtener_carac_clusters(clusters, es_pierna):
    """
    Devuelve una lista de diccionarios con el número de cluster, sus
    características geométricas y si es pierna o no (parámetro @es_pierna)
    """
    carac_clusters = []
    
    # Obtengo las características de cada cluster
    for cluster in clusters:
        # Obtengo las coordenadas X e Y de los puntos
        puntosX = cluster['puntosX']
        puntosY = cluster['puntosY']
        
        num_puntos = cluster['numero_puntos']
        
        # Coordenadas del primer y último punto
        x_0, y_0 = puntosX[0], puntosY[0]
        x_n, y_n = puntosX[num_puntos-1], puntosY[num_puntos-1]
        
        # <Calculo el perímetro>
        
        perimetro = 0
        
        for i in range(num_puntos-1): # Recorro todos los puntos menos el último
            # Le sumo la distancia euclídea entre el punto i y i+1
            perimetro += dist(puntosX[i], puntosY[i], puntosX[i+1], puntosY[i+1])
    
        # <Calculo la anchura>
        
        # Es la distancia entre el primer y último punto
        anchura = dist(x_0, y_0, x_n, y_n)
        
        # <Calculo la profundidad>
        
        # Calculo la recta (en forma general) que pasa por el primer y último punto
        # r = Ax + By + C
        A = y_n - y_0
        B = x_0 - x_n
        C = y_0*x_n - y_n*x_0
        
        # Calculo la distancia de cada punto a la recta
        dist_puntos_a_recta = [dist_punto_a_recta(puntosX[i], puntosY[i], A, B, C) 
                               for i in range(1, num_puntos-1)] # Me puedo saltar el primer y último punto (su distancia siempre vale 0)
        
        # Calculo el máximo de esas distancias
        profundidad = max(dist_puntos_a_recta)
        
        # <Añado estas características a "carac_clusters">
        carac_cluster_actual = {'numero_cluster':cluster['numero_cluster'],
                                'perimetro':perimetro,
                                'profundidad':profundidad, 'anchura':anchura,
                                'esPierna':es_pierna}
        
        carac_clusters.append(carac_cluster_actual)
        
    return carac_clusters
            

if __name__=='__main__':
    # <Cargo los archivos JSON que contienen los clústeres de piernas y no_piernas>
    
    clusters_piernas = leer_fichero_json('clustersPiernas.json')
    clusters_no_piernas = leer_fichero_json('clustersNoPiernas.json') 
    
    # <Obtengo las características de los clusters>
    caracteristicas_piernas = obtener_carac_clusters(clusters_piernas, 1)
    caracteristicas_no_piernas = obtener_carac_clusters(clusters_no_piernas, 0)
    
    # <Guardo las características en dos ficheros>
    guardar_fichero_json(caracteristicas_piernas, 'caracteristicasPiernas.json')
    guardar_fichero_json(caracteristicas_no_piernas, 'caracteristicasNoPiernas.json')
    
    # <CREAR DATASET - TODO>