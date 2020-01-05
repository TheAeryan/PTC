# -*- coding: utf-8 -*-

import numpy as np
import cv2
import vrep
import time
import math
import os

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
    
    for i in range(len(clusters_dict)):
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
   
def tomar_foto_objetos(objetos_dict, clientID, robothandle):
    """
    Recibe los objetos detectados en la escena y, tras orientar al
    robot hacia cada uno, le hace una foto.
    
    @return Devuelve la lista de fotos tomadas de los objetos.
    """
    
    # <Obtengo la referencia de los motores y de la cámara>
    
    # Motores
    _, left_motor_handle=vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_oneshot_wait)
    _, right_motor_handle=vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_oneshot_wait)
     
    # Cámara
    _, camhandle = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
        
    #Variable para la velocidad de los motores
    velocidad = 0.2 # Muevo el robot lentamente para centrar bien los objetos en la cámara
    
    #Iniciar la camara y esperar un segundo para llenar el buffer
    _, resolution, image = vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_streaming)
    time.sleep(1)
    
    # <Tomo una foto de cada objeto>

    # Imágenes de cada objeto    
    lista_ims = []    
    
    for obj in objetos_dict:
        # Calculo la orientación del robot
        # Solo me interesa la rotación en el eje Z (valor gamma)
        robot_orient=vrep.simxGetObjectOrientation(clientID, robothandle, 0, vrep.simx_opmode_oneshot_wait)[1][2]
        
        # Calculo la orientación del objeto
        obj_orient = math.atan2(obj['posY'], obj['posX'])
        
        # Le resto pi/2 para que esté en el formato de los ángulos de euler
        obj_orient -= math.pi/2
        
        # Elijo en qué sentido rotar el robot
                
        # Calculo los valores de las orientaciones entre 0 y 2pi radianes
        robot_orient_posit = robot_orient % math.pi*2
        obj_orient_posit = obj_orient % math.pi*2
        
        # Veo en qué sentido de rotación la distancia es menor
        dist_sentido_1 = (obj_orient_posit - robot_orient_posit) % math.pi*2
        dist_sentido_2 = math.pi*2 - dist_sentido_1
        
        # Roto el robot en el sentido más corto al objeto
        if dist_sentido_1 < dist_sentido_2:
            vrep.simxSetJointTargetVelocity(clientID, right_motor_handle,velocidad,vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(clientID, left_motor_handle,0,vrep.simx_opmode_streaming)
        else:
            vrep.simxSetJointTargetVelocity(clientID, left_motor_handle,velocidad,vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(clientID, right_motor_handle,0,vrep.simx_opmode_streaming)
        
        # Muevo el robot hasta que su orientación sea más o menos la del objeto
        umbral_dif_orientaciones = 0.01
        
        while abs(obj_orient - robot_orient) > umbral_dif_orientaciones:
            time.sleep(0.01) # Intervalo cada cual se comprueba si el objeto ya está centrado en la cámara
            robot_orient=vrep.simxGetObjectOrientation(clientID, robothandle, 0, vrep.simx_opmode_oneshot_wait)[1][2]
          
        # Paro los motores
        vrep.simxSetJointTargetVelocity(clientID, left_motor_handle,0,vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(clientID, right_motor_handle,0,vrep.simx_opmode_streaming)    
           
        # Tomo una foto del objeto
        
        #Guardar frame de la camara, rotarlo y convertirlo a BGR
        _, resolution, image=vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_buffer)
        img = np.array(image, dtype = np.uint8)
        img.resize([resolution[0], resolution[1], 3])
        img = np.rot90(img,2)
        img = np.fliplr(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        # Añado la foto a la lista
        lista_ims.append(img)
        
                
    #detenemos la simulacion
    vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot_wait)
    
    #cerramos la conexion
    vrep.simxFinish(clientID)
    
    # Devuelvo la lista de imágenes de los objetos
    return lista_ims

def crear_web(objetos_dict, y_true, obj_ims, archivo_web, carpeta_ims='.'):
    """
    Crea una web de nombre @archivo_web que muestra una tabla con la
    información de los objetos clasificados, incluidas sus imágenes.
    
    @objetos_dict Información de los objetos, en forma de lista de diccionarios.
    @y_true Lista de clases verdaderas de los objetos de @objetos_dict
    @obj_ims Imágenes tomadas de cada uno de los objetos
    @carpeta_ims Carpeta donde se guardan las imágenes @obj_ims a usar
                 para la web. Si la carpeta no existe se crea.
    """

    # Asocia a cada clase su nombre
    dict_clases = {0:'No Pierna', 1:'Pierna'}

    # <Creo una carpeta para guardar las imágenes, a no ser que exista ya>
    if carpeta_ims != '.':
        if not os.path.isdir(carpeta_ims):
            os.mkdir(carpeta_ims) # Creo la carpeta

    # <Guardo las imágenes en la carpeta>
    
    # Lista con los nombres de los archivos de las imágenes
    nombres_ims = []
    
    for ind, im in enumerate(obj_ims):
        nombre_im = '{}/img_{}.jpg'.format(carpeta_ims, ind)
        nombres_ims.append(nombre_im)
        
        cv2.imwrite(nombre_im, im) # Guardo la imagen

    # <Creo el código html de la tabla>
    
    html_web = """<!DOCTYPE html><html>
    <head><title>Resultados</title>
    <meta charset="utf8"></head>
    <body><h1>Tabla con los objetos clasificados</h1>
    <style type="text/css">
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
          text-align: center;
          padding: 10px;
        }
    </style>
    <table>
    <tr>
        <th>Tipo de objeto</th>
        <th>Valor de la predicción</th>
        <th>Distancia al robot</th>
        <th>Imagen del objeto</th>
    </tr>"""
    
    for obj, path_im, clase_real in zip(objetos_dict, nombres_ims, y_true):
        # Tipo de objeto
        tipo_obj = dict_clases[clase_real]
        
        # Valor de la predicción
        val_pred = dict_clases[obj['tipoObjeto']]
        
        # Distancia al robot
        dist_robot = dist(0,0,obj['posX'],obj['posY'])
        
        # Añado la fila correspondiente a 'obj'
        html_web+= \
        """
        <tr>
            <td>{}</td>
            <td>{}</td>
            <td>{:.2f}</td>
            <td><img src="{}" alt="Imagen Objeto" /></td>
        </tr>
        """.format(tipo_obj, val_pred, dist_robot, path_im)
        
    html_web += \
    """
    </table>
    </body>
    </html>
    """
    
    # <Guardo el archivo de la web>
    
    with open(archivo_web, 'w') as f:
        f.write(html_web)
        

if __name__=='__main__':
    # <Recibo los datos del láser de la escena y clasifico los objetos>
    
    # Recibo los datos del láser de la escena de test
    # 'False' porque no quiero que termine la simulación todavía
    datos_laser, clientID, robothandle = obtener_datos_laser_simulador(False)

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
    print("\nTomando fotos de los objetos...")
    
    obj_ims = tomar_foto_objetos(objetos_dict, clientID, robothandle)
    
    print("\nFotos tomadas!")
    
    # <Creo la página web>
    
    # Clases verdaderas
    y_true = [1, 1, 0, 1, 0, 0, 1, 0]
    
    crear_web(objetos_dict, y_true, obj_ims, 'resultados.html', 'imagenes_web')
