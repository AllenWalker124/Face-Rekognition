import mysql.connector
import image_encoding
from datetime import datetime

mydb = mysql.connector.connect(
  host="110.238.80.161",
  user="root",
  password="Harveylinux77+",
  database="base-escuela"

)
mycursor = mydb.cursor()

def get_images_path():
    # ver info tabla
    mycursor.execute("SELECT * FROM padres ORDER BY PadreID")
    myresult = mycursor.fetchall()

    lista_nombre_padres = []
    lista_fotos_padres = []
    images_path = []
    
    for x in myresult:
        lista_nombre_padres.append(x[1])
        lista_fotos_padres.append(x[2])
        
    # print(lista_nombre_padres)
    for i in range(len(lista_nombre_padres)):
        image_encoding.decodificar_b64(lista_nombre_padres[i], lista_fotos_padres[i])
        image_encoding.decodificar_b64(lista_nombre_padres[i], lista_fotos_padres[i])
        path = './Rostros Padres/' + lista_nombre_padres[i] + '.jpg'
        images_path.append([lista_nombre_padres[i], path])
        # Nombre Padre, ruta foto de Padre
        
    return images_path


def get_students_data():
    # ver info tabla
    mycursor.execute("SELECT * FROM students ORDER BY StudentName")
    students_data = mycursor.fetchall()

    informacion_alumnos = []

    for alumno in students_data:
        informacion_alumnos.append([alumno[2], alumno[3], alumno[4], alumno[1], alumno[6], alumno[5]])  
        # Tutor 1, Tutor 2, Tutor 3, Nombre Alumno, Edad Alumno, Grupo
        
    return informacion_alumnos


# FUNCIONES PARA ACTUALIZAR LA BD DESPUÉS DE RECONOCER UN ROSTRO
def actualizarAsistencia(nombre_Alumno):
    value = '1'
    commit = 'UPDATE asistencia SET llegoPadre = ' + value + ' WHERE alumno = "' + nombre_Alumno + '"'
    mycursor.execute(commit)
    mydb.commit()

def actualizarAsistencia_2(nombre_Alumno, nombre_Tutor, grupo):
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    value = 1
    estatus = 0
    
    sql = "INSERT INTO asistencia (fecha, alumno, padre, grupo, estatus, llegoPadre) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (formatted_date, nombre_Alumno, nombre_Tutor, grupo, estatus, value)
    mycursor.execute(sql, val)
    mydb.commit()

def actualizarBD(Recognized_Person):
    tutor = '"' + Recognized_Person + '"'
    commit = 'SELECT * FROM students WHERE Tutor_1 = '+ tutor +' or Tutor_2 = '+ tutor +' or Tutor_3 = '+ tutor
    mycursor.execute(commit)
    students_data = mycursor.fetchall()
    
    # obtenemos la lista del nombre de los alumnos que están registrados bajo ese tutor y su grupo
    lista_alumnos = []
    for student in students_data:
        lista_alumnos.append([student[1], student[5]])
        
    # ahora actualizamos la tabla de asistencias usando los nombres de los alumnos
    
    for i in range(len(lista_alumnos)):
        actualizarAsistencia_2(lista_alumnos[i][0], Recognized_Person, lista_alumnos[i][1])
        
def validarRegistroTutor(nombreTutor):
    tutor = '"' + nombreTutor + '"'
    commit = 'SELECT * FROM padres WHERE PadreNombre = ' + tutor
    mycursor.execute(commit)
    tutor_data = mycursor.fetchall()
    
    existe_registro = True
    if tutor_data == []:
        existe_registro = False
    return existe_registro