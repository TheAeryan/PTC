# -*- coding: utf-8 -*- 

import vrep
import sys
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import json
import os
import glob

if __name__ == '__main__':
    nom_fich = input('Introduzca el nombre del fichero (sin la extensión): ')
    str_num_ciclos = input('Introduzca el número de ciclos de lectura: ')
    str_tiempo_espera = input('Introduzca el tiempo en segundos entre ciclos de lectura: ')
    tipo_ejemplos = input("Diga si los ejemplos a capturar son 'positivos' o 'negativos': ")
    
    # Me aseguro de que los parámetros son correctos
    try:
        num_ciclos = int(str_num_ciclos)
    except ValueError:
        print("El número de ciclos debe ser un entero")
        exit()
        
    try:
        tiempo_espera = int(str_tiempo_espera)
    except ValueError:
        print("El tiempo entre ciclos debe ser un entero")
        exit()
        
    assert nom_fich != "", "El nombre del fichero no puede ser vacío"    
    assert num_ciclos > 0, "El número de ciclos debe ser mayor a 0"
    assert tiempo_espera > 0, "El tiempo entre ciclos debe ser mayor a 0"
    assert tipo_ejemplos == 'positivos' or tipo_ejemplos == 'negativos', \
    "Tipo de ejemplos no válidos"
    
    # Creo la carpeta para guardar los datos
    if tipo_ejemplos == 'positivos':
        listaDir=sorted(glob.glob("positivo*"))
        nuevoDir="positivo"+str(len(listaDir))
    else:
        listaDir=sorted(glob.glob("negativo*"))
        nuevoDir="negativo"+str(len(listaDir))
    
    if (os.path.isdir(nuevoDir)):
        sys.exit("Error: ya existe el directorio "+ nuevoDir)
    else:
        os.mkdir(nuevoDir)
        os.chdir(nuevoDir)
        
    #Creamos el fichero JSON para guardar los datos del laser
    #usamos diccionarios
    cabecera={"TiempoSleep":tiempo_espera,
              "MaxIteraciones":num_ciclos}
    
    ficheroLaser=open("{}.json".format(nom_fich), "w")
    
    ficheroLaser.write(json.dumps(cabecera)+'\n')
        
    # Obtenemos los datos de la simulación y los vamos guardando
    
    vrep.simxFinish(-1) #Terminar todas las conexiones
    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) #Iniciar una nueva conexion en el puerto 19999 (direccion por defecto)
    
    # Primero lanzar play en la escena y después ejecutar python
     
    if clientID!=-1:
        print ('Conexion establecida')
    else:
        sys.exit("Error: no se puede conectar. Tienes que iniciar la simulación antes de llamar a este script.") #Terminar este script
     
    #Guardar la referencia al robot
    
    _, robothandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx', vrep.simx_opmode_oneshot_wait)
            
    #Guardar la referencia de los motores
    _, left_motor_handle=vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_oneshot_wait)
    _, right_motor_handle=vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_oneshot_wait)
     
    #Guardar la referencia de la camara
    _, camhandle = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
     
    #acceder a los datos del laser
    _, datosLaserComp = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_streaming)
    
    
    velocidad = 0.35 #Variable para la velocidad de los motores
     
    #Iniciar la camara y esperar un segundo para llenar el buffer
    _, resolution, image = vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_streaming)
    time.sleep(1)
     
    plt.axis('equal')
    plt.axis([0, 4, -2, 2]) 
    
    iteracion=0 
    seguir=True
 
    while(iteracion<num_ciclos and seguir):
        puntosx=[] #listas para recibir las coordenadas x, y z de los puntos detectados por el laser
        puntosy=[]
        puntosz=[]
        returnCode, signalValue = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_buffer) 
        time.sleep(tiempo_espera) #esperamos un tiempo para que el ciclo de lectura de datos no sea muy rápido
        datosLaser=vrep.simxUnpackFloats(signalValue)
        for indice in range(0,len(datosLaser),3):
            puntosx.append(datosLaser[indice+1])
            puntosy.append(datosLaser[indice+2])
            puntosz.append(datosLaser[indice])
        
        print("Iteración: ", iteracion)        
        plt.clf()    
        plt.plot(puntosx, puntosy, 'r.')
        plt.show()
        
        #Guardamos los puntosx, puntosy en el fichero JSON
        lectura={"Iteracion":iteracion, "PuntosX":puntosx, "PuntosY":puntosy}
        #ficheroLaser.write('{}\n'.format(json.dumps(lectura)))
        ficheroLaser.write(json.dumps(lectura)+'\n')
               
        
        #Guardar frame de la camara, rotarlo y convertirlo a BGR
        _, resolution, image=vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_buffer)
        img = np.array(image, dtype = np.uint8)
        img.resize([resolution[0], resolution[1], 3])
        img = np.rot90(img,2)
        img = np.fliplr(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
     
         
        #Convertir img a hsv y detectar colores
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        verde_bajos = np.array([49,50,50], dtype=np.uint8)
        verde_altos = np.array([80, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, verde_bajos, verde_altos) #Crear mascara
     
        #Limpiar mascara y buscar centro del objeto verde
        moments = cv2.moments(mask)
        area = moments['m00']
        if(area > 200):
            x = int(moments['m10']/moments['m00'])
            y = int(moments['m01']/moments['m00'])
            cv2.rectangle(img, (x, y), (x+2, y+2),(0,0,255), 2)
            #Descomentar para printear la posicion del centro
            #print(x,y)
     
            #Si el centro del objeto esta en la parte central de la pantalla (aprox.), detener motores
            if abs(x-256/2) < 15:
                vrep.simxSetJointTargetVelocity(clientID, left_motor_handle,0,vrep.simx_opmode_streaming)
                vrep.simxSetJointTargetVelocity(clientID, right_motor_handle,0,vrep.simx_opmode_streaming)
     
            #Si no, girar los motores hacia la derecha o la izquierda
            elif x > 256/2:
                vrep.simxSetJointTargetVelocity(clientID, left_motor_handle,velocidad,vrep.simx_opmode_streaming)
                vrep.simxSetJointTargetVelocity(clientID, right_motor_handle,-velocidad,vrep.simx_opmode_streaming)
            elif x < 256/2:
                vrep.simxSetJointTargetVelocity(clientID, left_motor_handle,-velocidad,vrep.simx_opmode_streaming)
                vrep.simxSetJointTargetVelocity(clientID, right_motor_handle,velocidad,vrep.simx_opmode_streaming)
     
     
        #Mostrar frame y salir con "ESC"
        cv2.imshow('Image', img)
        cv2.imshow('Mask', mask)
        
        # Guardo en disco la imagen si es la primera o última iteración
        if iteracion == 0 or iteracion == num_ciclos-1:
            cv2.imwrite(nom_fich+str(iteracion)+'.jpg', img)
    
        
        tecla = cv2.waitKey(5) & 0xFF
        if tecla == 27:
            seguir=False
        
        iteracion=iteracion+1
       
    
    #detenemos los motores
    vrep.simxSetJointTargetVelocity(clientID, left_motor_handle,0,vrep.simx_opmode_streaming)
    vrep.simxSetJointTargetVelocity(clientID, right_motor_handle,0,vrep.simx_opmode_streaming)
        
    time.sleep(1)
    
    #detenemos la simulacion
    vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot_wait)
    
    #cerramos la conexion
    vrep.simxFinish(clientID)
    
    #cerramos las ventanas
    cv2.destroyAllWindows()
    
    finFichero={"Iteraciones totales":iteracion}
    #ficheroLaser.write('{}\n'.format(json.dumps(finFichero)))
    ficheroLaser.write(json.dumps(finFichero)+'\n')
    ficheroLaser.close()