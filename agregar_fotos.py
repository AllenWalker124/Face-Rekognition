import mysql.connector
import image_encoding
import re
import os

dir = './Fotos Drive/'

#####
mydb = mysql.connector.connect(
  host="110.238.80.161",
  user="root",
  password="Harveylinux77+",
  database="base-escuela"

)
mycursor = mydb.cursor()

def actualizar_fotos(NombrePadre, Foto_B64):
    sql = "INSERT INTO padres (PadreNombre, PadreFoto) VALUES (%s, %s)"
    val = (NombrePadre, Foto_B64)
    mycursor.execute(sql, val)
    mydb.commit()

#####

with os.scandir(dir) as ficheros:
    ficheros = [fichero.name for fichero in ficheros if fichero.is_file()]
# print(ficheros)

listado_path = []

for i in range(len(ficheros)):
    path = dir + ficheros[i]
    listado_path.append(path)    
# print(listado_path)

# images_b64 = []
for j in range(len(listado_path)):
    code_b64 = str(image_encoding.codificar_b64(listado_path[j]))
    code_b64 = re.sub("b'", "", code_b64)
    # print(code_b64)
    # images_b64.append([ficheros[j], code_b64])
    nombre_tutor = ficheros[j]
    nombre_tutor = re.sub(".jpg", "", nombre_tutor)
    actualizar_fotos(nombre_tutor, code_b64)