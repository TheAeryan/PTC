# -*- coding: utf-8 -*-

import numpy as np
import cv2
import vrep

from predecir import clusterizar_y_clasificar, obtener_datos_laser_simulador
from caracteristicas import dist

def agrupar_clusters_en_objetos(clusters_dict, y_pred, umbral_dist=0.4):
    """
    Recibe los clusters creados (en formato de una lista de clusters) y
    la clase predicha y devuelve una lista de diccionarios con los objetos,
    sus posiciones (x, y) y sus clases.
    
    @umbral_dist Distancia máxima entre los centroides de dos clusters
                 para que se consideren del mismo objeto.
    """
    
    # <Calculo el centroide de cada cluster> 
    cent_clusters = []
    
    for cluster in clusters_dict:
        cent_x = float(np.average(cluster['puntosX']))
        cent_y = float(np.average(cluster['puntosY']))
        
        cent_clusters.append((cent_x, cent_y))
        
    # <Agrupo los clusters cercanos en objetos>
    
    # Lista de objetos detectados
    obj_dict = []
    
    # Almacena si cada cluster ha sido incluido ya
    # Un cluster puede ser incluido solo, sin ser agrupado con otro,
    # o puede agruparse con otro cluster y formar ambos el mismo objeto
    clusters_incluidos = [False] * len(clusters_dict)
    
    for i in range(len(clusters_dict)-1):
        # Me salto el cluster i si ya ha sido incluido
        if clusters_incluidos[i] == False:
            # Intengo agrupar el cluster i con algún otro cluster cercano y de la misma clase
            for j in range(i+1, len(clusters_dict)):
                # Me aseguro de que el cluster[j] no haya sido añadido todavía
                if clusters_incluidos[j] == False:
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
                            
                            # Añado el objeto a la lista de objetos
                            nuevo_obj= {'tipoObjeto':int(y_pred[i]),
                                        'posX':pos_obj_x, 'posY':pos_obj_y}
                            
                            obj_dict.append(nuevo_obj)
                            
                            # Marco los clusters como ya incluidos
                            clusters_incluidos[i] = clusters_incluidos[j] = True
            
            # Si el cluster i no ha sido agrupado con ningún otro, forma un
            # objeto él solo
            if clusters_incluidos[i] == False:
                nuevo_obj= {'tipoObjeto':int(y_pred[i]),
                                        'posX':cent_clusters[i][0],
                                        'posY':cent_clusters[i][1]}
                
                obj_dict.append(nuevo_obj)
                
                clusters_incluidos[i] = True
                
    return obj_dict
   
def tomar_foto_objetos(objetos_dict, clientID):
    """
    Recibe los objetos detectados en la escena y, tras orientar al
    robot hacia cada uno, le toma una foto.
    """
    
    # <Obtengo la referencia de los motores y de la cámara>
    
    # Motores
    _, left_motor_handle=vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_oneshot_wait)
    _, right_motor_handle=vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_oneshot_wait)
     
    # Cámara
    _, camhandle = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
        
    velocidad = 0.35 #Variable para la velocidad de los motores
    
    #Iniciar la camara y esperar un segundo para llenar el buffer
    _, resolution, image = vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_streaming)
    time.sleep(1)
    
    # <Tomo una foto de cada objeto>

    lista_ims = []    
    
    for obj in objetos_dict:
        # <Oriento el robot hacia el objeto>
        pass
    

if __name__=='__main__':
    # <Recibo los datos del láser de la escena y clasifico los objetos>
    
    # Recibo los datos del láser de la escena de test
    # 'False' porque no quiero que termine la simulación todavía
    datos_laser, clientID = obtener_datos_laser_simulador(False)

    # Realizo todo el proceso de clustering y clasificación de los
    # puntos del láser
    
    # Parámetros para el algoritmo de salto
    min_puntos_cluster = 3
    max_puntos_cluster = 50
    umbral_distancia = 0.04
    
    clusters_dict, y_pred = clusterizar_y_clasificar([datos_laser],
                             min_puntos_cluster,
                             max_puntos_cluster, umbral_distancia,
                             'clasificador.pkl', 'piernasDataset.csv')

    # <Agrupo los clusters en objetos>
    objetos_dict = agrupar_clusters_en_objetos(clusters_dict, y_pred)
    
    # <Para cada objeto, oriento el robot hacia él y le tomo una foto>
    obj_ims = tomar_foto_objetos(objetos_dict, clientID)
