#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import numpy as np
from html.parser import HTMLParser
import locale
import matplotlib.pyplot as plt
from matplotlib.legend import Legend
from matplotlib.lines import Line2D

# Establecer la configuración que tenga el entorno del usuario
locale.setlocale(locale.LC_ALL,'')

# Directorio donde se almacenarán los resultados
path_resultados = 'resultados/'

# Función que implementa el redondeo de reales de forma correcta
def redondear(numero, decimales):
    numero=numero*(10**decimales)
    numero=numero + 0.5
    numero=(int)(numero)
    numero=numero/(10**decimales)
    
    return numero

# Clase de ayuda para parsear los ficheros html
class MyHTMLParser(HTMLParser):
    
    def __init__(self):
        super().__init__()
        self.values = [] # Values debe ser una variable de instancia y no de clase!! (Si no, se comparterá entre las distintas instancias de la clase)
    
    # analizamos lo que tiene que hacer al encontrar datos
    def handle_data(self, data):
        if '\n' not in data and 'Ciudades' not in data:            
            self.values.append(data)
    #para devolver los valores
    def get_values(self):
        return self.values


# <Ejercicio 1>
# Calcular la variación de la población por provincias desde el año 2011 a 2017 en términos
# absolutos y relativos generando la página web 1 (que debe llamarse variacionProvincias.htm).

# Función para cargar los datos de la población a usar en el ejercicio 1 y devolverlos
# en formato diccionario
# Si cargar_datos_sexos vale False, se eliminan las columnas relativas a los datos
# desagregados por sexos
def cargar_datos_poblacion_provincias(cargar_datos_sexos=False):
    # Cargo el archivo csv codificado como 'latin-1' con los datos de la población
    with open('poblacionProvinciasHM2010-17.csv', encoding='ISO-8859-1', newline='') as file:
        # Leo las líneas del archivo
        lines = file.readlines()
        lines = lines[6:-4] # Elimino las líneas del archivo del principio y final que no se corresponden con datos de población
          
        # Separo los datos usando el módulo csv y los almaceno como un numpy array
        file_csv = csv.reader(lines, delimiter=';')
        arr_csv = np.array(list(file_csv))
        
        if not cargar_datos_sexos:
            # Me quedo solo con los datos de población totales (elimino los relativos a cada sexo)
            arr_csv = arr_csv[:, :9]
        else:
            arr_csv = arr_csv[:, :-1] # Elimino el último elemento de las filas, que se corresponde con el string vacío
        
        # Almaceno los datos usando un diccionario con la siguiente estructura:
        # Claves: la ciudad (código + nombre)
        # Valores: un array de numpy con los datos de población ordenados por años
        dict_csv = dict()
        
        for el in arr_csv:
            curr_key = el[0] # Primera posición -> la ciudad
            curr_val = el[1:].astype('float64') # Resto de posiciones -> los datos de población por años. Los datos los guardo en formato float
            
            dict_csv[curr_key] = curr_val # Añado el elemento al diccionario
        
        return dict_csv
 
# Función que recibe un diccionario con los datos de población y devuelve
# otro diccionario con las variaciones absolutas. Estos datos pueden
# ser de comunidades autónomas o provincias, y totales o desagregados por sexos        
def calcular_variacion_absoluta(datos_poblacion):
    datos_variacion_abs = dict()

    for provincia in datos_poblacion:
        # Calculo de forma eficiente la variación absoluta restando los valores
        # de las poblaciones para los años 2017-2011 con los valores de las poblaciones
        # para los años 2016-2010
        arr_variacion_abs = datos_poblacion[provincia][:-1] - datos_poblacion[provincia][1:]
        
        # Añado el vector de variaciones al diccionario
        datos_variacion_abs[provincia] = arr_variacion_abs
        
    return datos_variacion_abs

# Función que recibe los datos de población y sus variaciones absolutas y devuelve
# un diccionario con las variaciones relativas. Estos datos pueden
# ser de comunidades autónomas o provincias, y totales o desagregados por sexos   
def calcular_variacion_relativa(datos_poblacion, datos_variacion_abs):
    datos_variacion_rel = dict()

    for provincia in datos_poblacion:
        # Calculo de forma eficiente la variación relativa restando los valores
        # de las variaciones absolutas de las poblaciones para los años 2017-2011
        # entre los datos de población para los años 2016-2010
        arr_variacion_rel = (datos_variacion_abs[provincia][:] / datos_poblacion[provincia][1:]) * 100
        
        # Añado el vector de variaciones al diccionario
        datos_variacion_rel[provincia] = arr_variacion_rel
        
    return datos_variacion_rel

# Función que crea la hoja de estilo que van a usar todas las tablas de la
# práctica
def crear_hoja_estilo_tablas(path_css):
    fileEstilo=open(path_css,"w", encoding="utf8")

    estilo="""  table, th, td {
                    border-collapse: collapse;    
                    border:1px solid black;
                    font-family: Arial, Helvetica, sans-serif;
                    padding: 8px;     
                }  """
    
    fileEstilo.write(estilo)
    fileEstilo.close()

# Función que devuelve el fragmento de código html asociado a una tabla
# tit_col_1 -> Títulos de las columnas que aparecen en la cabecera de la tabla
# colspans_tit_1 -> Colspans de cada uno de los títulos de tit_col_1
# tit_col_2 -> Títulos de las columnas que aparecen debajo de tit_col_1. Su colspan es de 1.
# datos_filas -> Matriz con los datos de las filas a añadir. Sus elementos son strings.
def crear_codigo_html_tabla(tit_col_1, colspans_tit_1, tit_col_2, datos_filas, path_csv=None):
    cod_html = "<p><table>"
    
    # Añado la cabecera de la tabla correspondiente a tit_col_1
    cod_html += "<tr><th></th>" # El primer título es vacío
    
    for nom, colspan in zip(tit_col_1, colspans_tit_1):
        cod_html +="""<th colspan="{}">{}</th>""".format(colspan, nom)
        
    cod_html += "</tr>"
    
    # Añado la cabecera de la tabla correspondiente a tit_col_2
    cod_html+="<tr><th></th>" # El primer título es vacío
    
    for nom in tit_col_2:
        cod_html+="<th>{}</th>".format(nom)
    
    cod_html+="</tr>"
    
    # Añado las filas
    for fila in datos_filas:
        cod_html+="<tr>"
        
        for elem in fila:
            cod_html+="<td>{}</td>".format(elem)
    
        cod_html+="</tr>"  
   
    cod_html+="</table></p>"
    
    return cod_html
    
# Cargo los datos de la población
datos_poblacion = cargar_datos_poblacion_provincias(cargar_datos_sexos=False)

# Calculo la variación absoluta para cada provincia y año
datos_variacion_abs = calcular_variacion_absoluta(datos_poblacion)

# Calculo la variación relativa para cada provincia y año
datos_variacion_rel = calcular_variacion_relativa(datos_poblacion, datos_variacion_abs)
    
# Creo la web

# Creo la hoja de estilos
nombre_css = "estilo.css"
crear_hoja_estilo_tablas(path_resultados + nombre_css)

# Añado el encabezado y títulos
pagina_variacion = """<!DOCTYPE html><html>
<head><title>Web 1</title>
<link rel="stylesheet" href={}>
<meta charset="utf8"></head>
<body><h1>Resumen por provincias</h1>
<h2>Variación anual en la población por provincias</h2>""".format(nombre_css)

# Obtengo la información para rellenar la tabla

tit_col_1 = ["Variación absoluta", "Variación relativa"]
colspans_tit_1 = [7, 7]

years = ["2017", "2016", "2015", "2014", "2013", "2012", "2011"]
tit_col_2 = years*2

# Creo las filas
mat_filas = []

# Recorro los elementos de los diccionarios de las variaciones
for (comunidad, var_abs), (_, var_rel) in zip(datos_variacion_abs.items(), datos_variacion_rel.items()):
    # Creo la fila como <comunidad> <variaciones absolutas> <variaciones relativas>
    nueva_fila = [comunidad]
    
    # Formateo las variaciones absolutas para que no tengan decimales y tengan el punto de los miles
    nueva_fila += list(map(lambda num: locale.format_string('%.0f', num, grouping=True),
                           var_abs.tolist()))
    
    # Formateo las variaciones relativas para que tengan 2 decimales y tengan el punto de los miles
    nueva_fila += list(map(lambda num: locale.format_string('%.2f', redondear(num, 2), grouping=True),
                           var_rel.tolist()))
    
    # La añado a la matriz
    mat_filas.append(nueva_fila)

# Creo la tabla a partir de la información obtenida
fragmento_tabla = crear_codigo_html_tabla(tit_col_1, colspans_tit_1, tit_col_2, mat_filas)
pagina_variacion += fragmento_tabla

# Añado las etiquetas de cierre para marcar el final del código html
pagina_variacion+="</body></html>"

# Guardo los datos en el archivo variacionProvincias.htm
with open(path_resultados + 'variacionProvincias.htm', 'w', encoding='utf8') as file:
    file.write(pagina_variacion)


# <Ejercicio 2>
# Usando el listado de comunidades autónomas que podemos obtener del fichero
# comunidadesAutonomas.htm, así como de las provincias de cada comunidad autónoma
# que de comunidadAutonoma-Provincia.htm y los datos de poblacionProvinciasHM2010-
# 17.csv, hay que generar una página web 2 (fichero poblacionComAutonomas.htm) con una tabla con
# los valores de población de cada comunidad autónoma en cada año de 2010 a 2017, indicando también
# los valores desagregados por sexos

# Función que lee un fichero html dado por 'path' y devuelve una lista con los datos
# de la tabla del fichero entre 'puntoInicio' y 'puntoFin'
def cargar_datos_tabla_html(path, puntoInicio='<td>01', puntoFin='</tbody>'):
    # Leo el archivo, usando la codificación latin-1
    comunidadesFich=open(path, 'r', encoding="ISO-8859-1")
    
    comString=comunidadesFich.read()
    
    inicioTab=comString.find(puntoInicio) # Punto de inicio de la tabla
    finTab=comString.find(puntoFin) # Final de la tabla
    
    comString=comString[inicioTab:finTab]
    
    #print(comString)
    
    parser = MyHTMLParser() # Parseo la información html usando la clase de ayuda MyHTMLParser
    
    parser.feed(comString)
    
    comun_lista=parser.get_values() # Obtengo los valores ya parseados
    
    #print(comun_lista)
    
    comunidadesFich.close()
    
    return comun_lista
    

# Cargo los datos de la población, tanto totales como desagregados por sexos
datos_pob_provincias = cargar_datos_poblacion_provincias(cargar_datos_sexos=True)
del datos_pob_provincias['Total Nacional'] # Elimino los datos totales, ya que solo me interesan los de las provincias

# Me creo un diccionario idéntico pero donde las claves solo tienen el código de la comunidad, sin tener el nombre de esta
datos_pob_provincias = {key.split()[0]: val for (key, val) in datos_pob_provincias.items()}

# Cargo los datos de las comunidades autónomas
datos_comunidades = cargar_datos_tabla_html('comunidadesAutonomas.htm')

# Creo un diccionario donde las claves son los códigos de las comunidades y los valores
# los nombres de estas
# Uso rstrip para eliminar los espacios en blanco tras las claves
dict_cod_nom_comunidades = {cod.rstrip(): nom for (cod, nom) in zip(datos_comunidades[0::2], datos_comunidades[1::2])}

# Cargo los datos de las provincias de cada comunidad autónoma
datos_prov_y_com = cargar_datos_tabla_html('comunidadAutonoma-Provincia.htm')

# Creo un diccionario donde las claves son los códigos de provincias y los
# valores los códigos de comunidades autónomas
codigos_prov_y_com = {cod_pro: cod_auto
for (cod_auto, nom_auto, cod_pro, nom_pro) in zip(datos_prov_y_com[::4],
datos_prov_y_com[1::4], datos_prov_y_com[2::4], datos_prov_y_com[3::4])}

# Me creo un diccionario para almacenar las poblaciones de las comunidades autónomas
# Su estructura es la siguiente:
# Claves -> comunidades (pareja código, nombre)
# Valores -> datos de población: un numpy array con los valores de población ordenados como en el archivo csv

# Inicializo el diccionario con los códigos de las comunidades y arrays de poblaciones inicializados a 0
valores_ini_dict_pob_comunidades = [(cod_auto, np.zeros(shape=(8*3), dtype='int64')) for cod_auto in dict_cod_nom_comunidades]
dict_pob_comunidades = dict(valores_ini_dict_pob_comunidades)

# Recorro los datos de población de cada provincia y añado el vector de poblaciones
# a la comunidad autónoma a la que pertenece dicha provincia
for cod_prov in datos_pob_provincias:    
    # Obtengo el código numérico de la comunidad autónoma a la que pertenece
    # esa provincia
    cod_comunidad_prov = codigos_prov_y_com[cod_prov]
    
    # Le sumo el vector de poblaciones de la provincia al vector de poblaciones
    # de la comunidad a la que pertenece    
    dict_pob_comunidades[cod_comunidad_prov] = \
    dict_pob_comunidades[cod_comunidad_prov] + datos_pob_provincias[cod_prov]
        
# Creo la web
    
# Añado el encabezado y títulos
pagina_comunidades = """<!DOCTYPE html><html>
<head><title>Web 2</title>
<link rel="stylesheet" href={}>
<meta charset="utf8"></head>
<body><h1>Resumen por comunidades autónomas</h1>
<h2>Valores de población en comunidades autónomas</h2>""".format(nombre_css)

# Obtengo la información para rellenar la tabla

tit_col_1 = ["Total", "Hombres", "Mujeres"]
colspans_tit_1 = [8, 8, 8]

years=["2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010"]
tit_col_2 = years*3

# Creo las filas
mat_filas = []

# Recorro los elementos de dict_pob_comunidades y cada uno se corresponde con una fila
for key, val in dict_pob_comunidades.items():
    # Cada fila es <clave> <nombre_auto> <poblaciones>
    nueva_fila = [key + " " + dict_cod_nom_comunidades[key]] 
    
    # Formateo las poblaciones para que no tengan decimales y tengan el punto de los miles
    nueva_fila += list(map(lambda num: locale.format_string('%.0f', num, grouping=True),
                           val.tolist()))
        
    # La añado a la matriz
    mat_filas.append(nueva_fila)

# Creo la tabla a partir de la información obtenida
fragmento_tabla = crear_codigo_html_tabla(tit_col_1, colspans_tit_1, tit_col_2, mat_filas)
pagina_comunidades += fragmento_tabla

# Añado las etiquetas de cierre para marcar el final del código html
pagina_comunidades+="</body></html>"

# Guardo los datos en el archivo variacionProvincias.htm
with open(path_resultados + 'poblacionComAutonomas.htm', 'w', encoding='utf8') as file:
    file.write(pagina_comunidades)


# <Ejercicio 3>
# Usando Matplotlib, para las 10 comunidades con más población media de 2010 a 2017, generar un
# gráfico de columnas que indique la población de hombres y mujeres en el año 2017, salvar el gráfico a
# fichero e incorporarlo a la página web 2 del punto R2.
num_com_max = 10 # Número de comunidades (con más habitantes) de las que realizar el gráfico 
    
# Función que crea el gráfico de barras con las autonomías y lo guarda como imagen
def crear_grafico_barras_auto(list_cod_auto, list_pob_hombre, list_pob_mujer, path_salida='grafico_ej_3.png', width=0.35):    
    x = np.arange(len(list_cod_auto))  # La localización de las etiquetas (nombres de las comunidades)
    
    fig, ax = plt.subplots()
    # Pinto las barras de los hombres a la izquierda de las mujeres, estando
    # el centro de cada pareja de barras dado por x
    ax.bar(x - width/2, list_pob_hombre, width, label='Hombre')
    ax.bar(x + width/2, list_pob_mujer, width, label='Mujer')
    
    # Añado las etiquetas
    ax.set_ylabel('Población (2017)') # Etiqueta eje y
    ax.set_title('Población en 2017 de las comunidades más pobladas') # Título del gráfico
    ax.set_xticks(x)           # Escribo los nombres de la comunidad
    ax.set_xticklabels(list_cod_auto) #  correspondiente en cada pareja de barras
    ax.legend() # Pinto la leyenda hombre-mujer
    
    """
    def autolabel(rects):
        # Attach a text label above each bar in *rects*, displaying its height.
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    
    autolabel(barras_hombre)
    autolabel(barras_mujer)"""
    
    plt.savefig(path_salida) # En vez de mostrarlo, lo guardo como imagen
    

# Calculo la población media de cada comunidad entre 2010 y 2017
# vec_pob[:8] -> las poblaciones totales de la comunidad
dict_pob_media_comunidades = {cod_auto: np.average(vec_pob[:8]) for cod_auto, vec_pob
                              in dict_pob_comunidades.items()}

# Convierto el diccionario en una lista de tuplas y ordeno por las poblaciones
lista_ord_pob_media_com = sorted(dict_pob_media_comunidades.items(),
                                 key=lambda dict_elem: dict_elem[1],
                                 reverse=True)
# Me quedo con los num_com_max (10) valores superiores y vuelvo a convertir la lista a diccionario
dict_com_mas_pobladas = dict(lista_ord_pob_media_com[:num_com_max])

# Obtengo los datos del gráfico para cada comunidad
list_cods_auto = []
list_pob_hombre_auto = []
list_pob_mujer_auto = []

for cod_auto in dict_com_mas_pobladas:
    # Obtengo los datos de cada comunidad y los añado a las listas
    pob_hombre_auto = dict_pob_comunidades[cod_auto][8] # Población de hombres en el año 2017
    pob_mujer_auto = dict_pob_comunidades[cod_auto][16] # Población de mujeres en el año 2017
    
    list_cods_auto.append(cod_auto)
    list_pob_hombre_auto.append(pob_hombre_auto)
    list_pob_mujer_auto.append(pob_mujer_auto)
  
# Creo la gráfica
path_imagen = 'grafico_ej_3.png'
    
crear_grafico_barras_auto(list_cods_auto, list_pob_hombre_auto, list_pob_mujer_auto, path_resultados + path_imagen)

# Añado la gráfica a la web del ejercicio 2

# Fragmento html a añadir
cod_html_imagen = "<h2>Población en 2017 de las comunidades más pobladas</h2> \
<img src={} alt=Gráfico Barras>".format(path_imagen)

# Añado este fragmento a la web

# Cargo los contenidos de la web
pag_entera = ""
with open(path_resultados + 'poblacionComAutonomas.htm', 'r', encoding='utf8') as f:
    pag_entera = f.read()
    
# Le quito las etiquetas del final (</body></html>)
pag_entera = pag_entera[:-14]

# Le añado la web
pag_entera += cod_html_imagen

# Le añado las etiquetas del final
pag_entera += "</body></html>"

with open(path_resultados + 'poblacionComAutonomas.htm', 'w', encoding='utf8') as f:
    f.write(pag_entera)
    
# <Ejercicio 4>
# Generar una página web 3 (fichero variacionComAutonomas.htm) con una tabla con la
# variación de población por comunidades autónomas desde el año 2011 a 2017, indicando variación
# absoluta, relativa y desagregando dicha información por sexos, es decir, variación absoluta (hombres,
# mujeres) y relativa (hombres, mujeres). Para los cálculos, hay que actuar de manera semejante que en el
# apartado R1.

# Separo los datos de las poblaciones de las com. autónomas por sexos
dict_pob_com_hombre = {cod_auto: vec_pob[8:16] for cod_auto, vec_pob in dict_pob_comunidades.items()}
dict_pob_com_mujer = {cod_auto: vec_pob[16:] for cod_auto, vec_pob in dict_pob_comunidades.items()}

# Calculo la variación absoluta segregada por sexos
dict_var_abs_hombre = calcular_variacion_absoluta(dict_pob_com_hombre)
dict_var_abs_mujer = calcular_variacion_absoluta(dict_pob_com_mujer)

# Calculo la variación relativa segregada por sexos
dict_var_rel_hombre = calcular_variacion_relativa(dict_pob_com_hombre, dict_var_abs_hombre)
dict_var_rel_mujer = calcular_variacion_relativa(dict_pob_com_mujer, dict_var_abs_mujer)

# Creo la web
    
# Añado el encabezado y títulos
pagina_var_com = """<!DOCTYPE html><html>
<head><title>Web 3</title>
<link rel="stylesheet" href={}>
<meta charset="utf8"></head>
<body><h1>Resumen por comunidades autónomas</h1>
<h2>Variación de la población en comunidades autónomas</h2>""".format(nombre_css)

# Obtengo la información para rellenar la tabla

tit_col_1 = ["Variación absoluta hombres", "Variación relativa hombres", "Variación absoluta mujeres", 
             "Variación relativa mujeres"]
colspans_tit_1 = [7, 7, 7, 7]

years = ["2017", "2016", "2015", "2014", "2013", "2012", "2011"]
tit_col_2 = years*4

# Creo las filas
mat_filas = []

# Recorro los elementos de los diccionarios de las variaciones
for (cod_auto, var_abs_hombre), (_, var_rel_hombre), (_, var_abs_mujer), (_, var_rel_mujer) in \
zip(dict_var_abs_hombre.items(), dict_var_rel_hombre.items(), dict_var_abs_mujer.items(), dict_var_rel_mujer.items()):
    # Creo la fila como <codigo_auto nom_auto> <variaciones>
    nueva_fila = [cod_auto + " " + dict_cod_nom_comunidades[cod_auto]]
    
    # Variación hombres
    
    # Formateo las variaciones absolutas para que no tengan decimales y tengan el punto de los miles
    nueva_fila += list(map(lambda num: locale.format_string('%.0f', num, grouping=True),
                           var_abs_hombre.tolist()))
    
    # Formateo las variaciones relativas para que tengan 2 decimales y tengan el punto de los miles
    nueva_fila += list(map(lambda num: locale.format_string('%.2f', redondear(num, 2), grouping=True),
                           var_rel_hombre.tolist()))
    
    # Variación mujeres
    
    # Formateo las variaciones absolutas para que no tengan decimales y tengan el punto de los miles
    nueva_fila += list(map(lambda num: locale.format_string('%.0f', num, grouping=True),
                           var_abs_mujer.tolist()))
    
    # Formateo las variaciones relativas para que tengan 2 decimales y tengan el punto de los miles
    nueva_fila += list(map(lambda num: locale.format_string('%.2f', redondear(num, 2), grouping=True),
                           var_rel_mujer.tolist()))
    
    # La añado a la matriz
    mat_filas.append(nueva_fila)

# Creo la tabla a partir de la información obtenida
fragmento_tabla = crear_codigo_html_tabla(tit_col_1, colspans_tit_1, tit_col_2, mat_filas)
pagina_var_com += fragmento_tabla

# Añado las etiquetas de cierre
pagina_var_com += "</body></html>"

# Guardo los datos en el archivo variacionComAutonomas.htm
with open(path_resultados + 'variacionComAutonomas.htm', 'w', encoding='utf8') as file:
    file.write(pagina_var_com)

# <Ejercicio 5>
# Usando Matplotlib, para las 10 comunidades elegidas en el punto R3 generar un gráfico de líneas
# que refleje la evolución de la población total de cada comunidad autónoma desde el año 2010 a 2017,
# salvar el gráfico a fichero e incorporarlo a la página web 3 del punto R4.

# Función que recibe un diccionario con los códigos de las comunidades y sus poblaciones y
# genera un gráfico de líneas
def crear_grafico_lineas_auto(dict_pob_autos):
    pass
    

# A partir de dict_com_mas_pobladas, obtengo un diccionario con las claves de las comunidades
# más pobladas y sus poblaciones
dict_pob_com_mas_pobladas = {cod_auto: dict_pob_comunidades[cod_auto] for cod_auto in dict_com_mas_pobladas}    

# Creo el gráfico
crear_grafico_lineas_auto(dict_pob_com_mas_pobladas)



# PREGUNTAR DUDAS:
# He cargado bien los datos? (he hecho bien lo de eliminar las filas de delante y
# atrás, así como las columnas del final?)
# > Preguntar si he pintado bien el gráfico de barras del ej. 3 y qué hacer con
# los nombres de las comunidades que se solapan. Poner códigos y una leyenda con los códigos y los nombres.

# ~ Para comprobar la generalidad de la solución: al darle el fichero comunidadesAutonomasBis.htm
# (que tiene menos comunidades autónomas) todo debería funcionar a la primera (solo me debería dar
# la información de esas comunidades autónomas). Con que eso funcione, se considerará que la
# solución es general!!!
    
    
    
