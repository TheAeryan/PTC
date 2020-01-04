# -*- coding: utf-8 -*-

import vrep
import sys
import time
import numpy as np
import joblib
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

import agrupar
import caracteristicas as carac
from caracteristicas import dist

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

def carac_clusters_to_matrix(caracs):
    """
    Transforma las características de los clústeres del formato que devuelve
    la función carac.obtener_carac_clusters al formato que recibe
    como entrada el modelo (un numpy array donde cada fila son las
    características de un clúster).
    """
    
    matrix_carac = [list(elem.values())[1:] for elem in caracs]
    
    # La convierto a numpy array
    matrix_carac = np.array(matrix_carac)
    
    return matrix_carac

def normalizar_dataset_test(X, fich_dataset_train, separador=','):
    """
    Normaliza @X restándole la media y dividiéndolo entre la desviación
    típica del dataset de entrenamiento del fichero de la ruta 
    @fich_dataset_train. Esta operación se hace por cada característica
    por separado.
    """
    # Leo el fichero csv conteniendo los datos
    datos = np.genfromtxt(fich_dataset_train, delimiter=separador) # Me formatea los contenidos del fichero en un numpy array
    
    # Me quedo solo con los atributos (elimino las etiquetas)
    X_train = datos[:,:-1] # Atributos

    # Calculo la media y desviación típica del dataset de entrenamiento
    medias = np.average(X_train, axis=0) # Media de cada característica
    desv_tipicas = np.std(X_train, axis=0) # Desviación típica de cada característica
    
    # Normalizo el dataset X
    X_norm = (X - medias) / desv_tipicas # dataset normalizado
    
    return X_norm

def dibujar_clusteres_clasificados(clusters_dict, y_pred, umbral_dist=0.4):
    """
    Dibuja los puntos de los clústeres usando matplotlib de un color
    diferente según si son clasificados como piernas o no. Además,
    se pinta la posición del objeto cuando se detectan dos clústeres
    cercanos pertenecientes al mismo objeto.
    
    @clusters_dict Clústeres, en formato lista de diccionarios.
    @y_pred        Predicción de la clase de cada clúster.
    @umbral_dist   Cómo de cerca deben de estar dos clústeres consecutivos
                   de la misma clase para que se consideren del mismo objeto.
    """
        
    # Colores de cada clase
    colores = {0:'blue', 1:'red'}
        
    # Dibujo cada cluster        
    for cluster, pred in zip(clusters_dict, y_pred):                        
        plt.scatter(cluster['puntosX'], cluster['puntosY'],
                    s=10,
                    color=colores[int(pred)])
        
    # <Dibujo las posiciones de los objetos>

    # Calculo los centroides de los clusters    
    cent_clusters = []
    
    for cluster in clusters_dict:
        cent_x = float(np.average(cluster['puntosX']))
        cent_y = float(np.average(cluster['puntosY']))
        
        cent_clusters.append((cent_x, cent_y))
        
    # Veo si cada clúster lo puedo agrupar con otro
    for i in range(len(clusters_dict)-1):
        for j in range(i+1, len(clusters_dict)):
            # Para que ambos clústeres puedan ser del mismo objeto,
            # tienen que pertenecer a la misma clase
            if y_pred[i] == y_pred[j]:
                # Calculo la distancia entre sus centroides
                dist_clusters = dist(cent_clusters[i][0], cent_clusters[i][1],
                                     cent_clusters[j][0], cent_clusters[j][1])
                
                # Si están cerca, son del mismo objeto
                if dist_clusters <= umbral_dist:
                    # Calculo la posición del objeto al que pertenecen
                    # los dos clusters
                    pos_obj_x = (cent_clusters[i][0] + cent_clusters[j][0]) / 2
                    pos_obj_y = (cent_clusters[i][1] + cent_clusters[j][1]) / 2
                    
                    # Muestro un punto (con forma de cuadrado) en la posición
                    # del objeto, según la clase a la que pertenece
                    plt.scatter(pos_obj_x, pos_obj_y, s=40,
                                color=colores[int(y_pred[i])],
                                marker='s')
        
    # Muestro las leyendas
    
    leg_no_pierna = mlines.Line2D([], [], color='blue', marker='o',
                          markersize=5, label='No Pierna (0)')
    leg_pierna = mlines.Line2D([], [], color='red', marker='o',
                          markersize=5, label='Pierna (1)')
    
    plt.legend(handles=[leg_no_pierna, leg_pierna], loc='upper left')

                 
    plt.show()

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
    
    # <Uso el clasificador entrenado para clasificar los clústeres>
    
    # Cargo el clasificador
    clasificador = joblib.load('clasificador.pkl') 
    
    # Convierto las características al formato que acepta el modelo
    # como entrada
    X = carac_clusters_to_matrix(carac_clusters)
    
    # Normalizo las características de la misma forma que el dataset
    # de entrenamiento (uso la media y desviación típica del dataset
    # de entrenamiento)
    X_norm = normalizar_dataset_test(X, 'piernasDataset.csv')
    
    # Uso el clasificador para predecir la clase de cada clúster
    y_pred = clasificador.predict(X_norm)
    
    # <Dibujo los clústers obtenidos según su clase>
    dibujar_clusteres_clasificados(clusters_dict, y_pred)
    
    