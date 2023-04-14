import cv2
import os
import boto3
from botocore.exceptions import ClientError
import json2dic

# Diccionario con imagenes
json_path = './JSON/datos_usuarios.json'
rutas = json2dic.convertirJson2Dic(json_path)

CON_THRES = 95
SIM_THRES = 95

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
    
    if respuesta and respuesta.get('ResponseMetadata').get('HTTPStatusCode') == 200:
        
        if respuesta["FaceMatches"] == None:
            return False
        
        for i in respuesta['FaceMatches']:
            similaridad = float(i['Similarity'])
            confianza =  float(i['Face']['Confidence'])
            
            if similaridad > SIM_THRES or confianza > CON_THRES:
                return True
            
            # SIMILARITY
            # similarity = float(i['Similarity'])
            
            # CONFIDENCE
            # print('Confidence: ', i['Face']['Confidence'])
            
            
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
    
    isPerson = False
    info_alumnos = []  # Esta lista guardará la información del alumno siempre y cuando se haya reconocido al padre
    msg_notificacion = ''
    
    for i in range(len(rutas)):
        
        ruta_img2 = rutas[i][3]
        Person = i
        
        isPerson = compararRostros(ruta_img1, ruta_img2)
        
        if isPerson:
            break
    
    if isPerson:
        msg_notificacion = 'Rostro reconocido correctamente, su(s) hijo(s) esta(n) en camino a la puerta de salida, por favor espere su llegada.'    
        for h in range(len(rutas[Person][5])):
            info_alumnos.append([rutas[Person][5][h], rutas[Person][6][h], rutas[Person][7][h], "Llegó padre"])  # Nombre hijo(s), Edad, Grupo
    
    else:
        msg_notificacion = 'Su rostro no se está identificando correctamente, por favor coloquelo de nuevo en el recuadro cuidando que sus facciones se distingan con claridad (no lentes, no cubrebocas).'
        info_alumnos.append('_')
    
    return msg_notificacion, info_alumnos

if __name__ == "__main__":
    
    msg_notif, salidaAlumnos = actualizacionStatus()      # Lista de alumnos que tienen permitido salir
    
    if salidaAlumnos[0] == '_':
        print(msg_notif)
    
    else:
        print(msg_notif)
        # Puede que un padre tenga varios hijos registrados, por eso sale una lista con los datos de cada uno
        for i in range(len(salidaAlumnos)):
            print("Alumno: ", salidaAlumnos[i][0], "\tEdad: ", salidaAlumnos[i][1], "\tGrupo: ", salidaAlumnos[i][2], "\tEstado: ", salidaAlumnos[i][3], "\n")