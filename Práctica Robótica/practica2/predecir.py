# -*- coding: utf-8 -*-

import vrep
import sys
import time
import numpy as np

import agrupar
import caracteristicas as carac

def obtener_datos_laser_simulador():
    """
    Se conecta al simulador y obtiene los datos del láser, que devuelve
    como una lista de dos elementos: lista[0] es una lista con las coordenadas
    X de los puntos y lista[1] una lista con las coordenadas Y.
    """
    vrep.simxFinish(-1) #Terminar todas las conexiones
    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) #Iniciar una nueva conexion en el puerto 19999 (direccion por defecto)
    
    # Primero lanzar play en la escena y después ejecutar python
     
    if clientID!=-1:
        print ('Conexion establecida')
    else:
        sys.exit("Error: no se puede conectar. Tienes que iniciar la simulación antes de llamar a este script.") #Terminar este script
     
    #Guardar la referencia al robot
    
    _, robothandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx', vrep.simx_opmode_oneshot_wait)
                 
    #acceder a los datos del laser
    _, datosLaserComp = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_streaming)
    
    # Hay que esperar un segundo antes de poder acceder a los datos del láser
    time.sleep(1)    
    
    puntosx=[] #listas para recibir las coordenadas x, y z de los puntos detectados por el laser
    puntosy=[]
    puntosz=[]
    returnCode, signalValue = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_buffer) 
    
    datosLaser=vrep.simxUnpackFloats(signalValue)
    for indice in range(0,len(datosLaser),3):
        puntosx.append(datosLaser[indice+1])
        puntosy.append(datosLaser[indice+2])
        puntosz.append(datosLaser[indice])
    
    #detenemos la simulacion
    vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot_wait)
    
    #cerramos la conexion
    vrep.simxFinish(clientID)   
    
    # Devuelvo los puntos
    return [puntosx, puntosy]

def clusters_to_dict(clusters):
    """
    Transforma los clusters del formato que devuelve la función
    agrupar.crear_clusters() a un formato de lista de diccionarios 
    (formato que recibe la función caracteristicas.obtener_carac_clusters())
    """
    
    clusters_dict = []
    
    for ind_cluster, cluster in enumerate(clusters):
        num_puntos = len(cluster) # Número de puntos del cluster
            
        puntos = np.array(cluster) # Lo convierto a numpy array para poder separar las coordenadas X e Y
        puntos_X = list(puntos[:,0]) # Los convierto a lista para que puedan ser guardados en el 
        puntos_Y = list(puntos[:,1]) # diccionario
        
        # Creo el diccionario que guarda la información del cluster actual
        dict_cluster = {'numero_cluster':ind_cluster, 'numero_puntos':num_puntos,
                        'puntosX':puntos_X, 'puntosY':puntos_Y}
        
        # Añado el cluster a la lista de clusters
        clusters_dict.append(dict_cluster)

    return clusters_dict

if __name__=='__main__':
    # <Recibo los datos del láser de la escena de test>
    datos_laser = obtener_datos_laser_simulador()

    # <Convierto los datos en clústeres>
    
    # Parámetros para el algoritmo de salto
    min_puntos_cluster = 3
    max_puntos_cluster = 50
    umbral_distancia = 0.04 
    
    clusters = agrupar.crear_clusters([datos_laser], min_puntos_cluster, 
                                        max_puntos_cluster,
                                        umbral_distancia)
    
    # <Obtengo las caracteristicas geométricas de los clústeres>
    
    # Transformo los clusters a un formato de diccionario
    clusters_dict = clusters_to_dict(clusters)
    
    # Obtengo sus características geométricas
    # datos_etiquetados=False, porque no sé si los clusters son de piernas
    # o no
    carac_clusters = carac.obtener_carac_clusters(clusters_dict, False)
    
    
    