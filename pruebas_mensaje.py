import cv2
import os
import boto3
from botocore.exceptions import ClientError
import json2dic

# Diccionario con imagenes
json_path = './JSON/datos_usuarios.json'
rutas = json2dic.convertirJson2Dic(json_path)


# FUNCIONES PARA LA COMPARACIÓN DE ROSTROS

def obtener_bytes_imagen(ruta_imagen):
    with open(ruta_imagen, "rb") as imagen:
        return imagen.read()

def compararRostros(ruta_imagen1,ruta_imagen2):
    bytes_1 = obtener_bytes_imagen(ruta_imagen1)
    bytes_2 = obtener_bytes_imagen(ruta_imagen2)

    cliente = boto3.client('rekognition')
    try:
        respuesta = cliente.compare_faces(SourceImage = {'Bytes' : bytes_1}, 
                                          TargetImage = {'Bytes': bytes_2},
                                          SimilarityThreshold = 60,
                                          QualityFilter = 'NONE')
        
        ### QUALITY FILTER: NONE'|'AUTO'|'LOW'|'MEDIUM'|'HIGH'

    except ClientError as error:
        print("Ocurrio un error al llamar a la API:",error)

    ## Variable que indica si se encontró una similaridad
    person_found = False
    similarity = 0
    
    if respuesta and respuesta.get('ResponseMetadata').get('HTTPStatusCode') == 200:
        # UnmatchedFaces
        for i in respuesta['UnmatchedFaces']:
        #     # print(i)
        #     # print('Los rostros comparados no son de la misma persona.')
            similarity = 0
            person_found = False
            

        # FaceMatches
        for i in respuesta['FaceMatches']:
            # SIMILARITY
            # print('Similarity: ', i['Similarity'])
            similarity = float(i['Similarity'])
            person_found = True
            
            # CONFIDENCE
            # print('Confidence: ', i['Face']['Confidence'])
            
    return similarity, person_found
            
            
# CAPTURAR FOTOGRAFÍAS USANDO LA CÁMARA
def crearCarpetaFotos():
    if not os.path.exists('Rostros encontrados'):
        print('Carpeta creada: Rostros encontrados')
        os.makedirs('Rostros encontrados')

def capturarFotos():
    # cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cap = cv2.VideoCapture(0)
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

    count = 0
    while True:
        ret,frame = cap.read()
        frame = cv2.flip(frame,1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = frame.copy()

        faces = faceClassif.detectMultiScale(gray, 1.3, 5)

        k = cv2.waitKey(1)
        if k == 27:     ## PRESIONA LA TECLA ESC PARA SALIR DE LA CÁMARA
            break

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y),(x+w,y+h),(128,0,255),2)
            rostro = auxFrame[y:y+h,x:x+w]
            rostro = cv2.resize(rostro,(150,150), interpolation=cv2.INTER_CUBIC)
            if k == ord('s'):
                cv2.imwrite('Rostros encontrados/rostro_{}.jpg'.format(count),rostro)
                cv2.imshow('rostro',rostro)
                count = count +1
        cv2.rectangle(frame,(10,5),(600,25),(255,255,255),-1)
        cv2.putText(frame,'Presione S para almacenar los rostros encontrados y ESC para cerrar.',(10,20), 2, 0.5,(128,0,255),1,cv2.LINE_AA)
        cv2.imshow('frame',frame)

    cap.release()
    cv2.destroyAllWindows()
    

# COMPARAMOS LA PRIMERA FOTOGRAFÍA GUARDADA CON LAS IMÁGENES GUARDADAS EN LA BD

def actualizacionStatus():
    crearCarpetaFotos()
    capturarFotos()
    
    ruta_img1 = './Rostros encontrados/rostro_0.jpg'
    
    status_analisis = 0     # 0 = Algo salió mal (intentar otra vez), 1 = OK, 2 = la persona no está en la BD
    persona_identificada = -1
    
    for i in range(len(rutas)):
        
        ruta_img2 = rutas[i][3]
        similaridad, person_found = compararRostros(ruta_img1, ruta_img2)
        
        if (person_found == True) & (similaridad > 80):
            status_analisis = 1
            persona_identificada = i
                
        elif (person_found == True) & (similaridad <= 80):
            status_analisis = 0
            
        elif (person_found == False) & (similaridad <= 80):
            status_analisis = 2
    
    return status_analisis, persona_identificada


def getInfo():
    
    datos_alumnos = []      # Esta lista guardará la información del alumno siempre y cuando se haya reconocido al padre
    info_status = ''     # Mensaje que se mostrará al realizar la comparación entre las fotos
    
    actual_Status, persona_tutor = actualizacionStatus()
    
    if actual_Status == 0:
        info_status = 'Su rostro no se está identificando correctamente, por favor coloquelo de nuevo en el recuadro cuidando que sus facciones se distingan con claridad.'
        datos_alumnos.append('NULL')
        
    elif actual_Status == 2:
        info_status = 'Su rostro no está registrado en la base de datos, por favor pase con la persona encargada en la entrada.'
        datos_alumnos.append('NULL')
        
    elif actual_Status == 1:
        info_status = 'Rostro reconocido correctamente. Su(s) hijo(s) esta(n) en camino a la puerta de salida, por favor espere su llegada.'
        for h in range(len(rutas[persona_tutor][5])):
            datos_alumnos.append([rutas[i][5][h], rutas[i][6][h], rutas[i][7][h], "Llegó padre"])  # Nombre hijo(s), Edad, Grupo
        
    return info_status, datos_alumnos


if __name__ == "__main__":
    
    mensaje, datos_alumnos = getInfo()      # Lista de alumnos que tienen permitido salir
    
    # Puede que un padre tenga varios hijos registrados, por eso sale una lista con los datos de cada uno
    if datos_alumnos[0] != 'NULL':
        print(mensaje)
        for i in range(len(datos_alumnos)):
            print("Alumno: ", datos_alumnos[i][0], "\tEdad: ", datos_alumnos[i][1], "\tGrupo: ", datos_alumnos[i][2], "\tEstado: ", datos_alumnos[i][3], "\n")
            
    else:
        print(mensaje)