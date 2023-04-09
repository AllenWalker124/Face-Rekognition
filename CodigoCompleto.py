import cv2
import os
import boto3
from botocore.exceptions import ClientError
import json2dic

# Diccionario con imagenes

# rutas = {0 : ['Jesus', './Rostros Personas/Jesus_before.jpg', './Rostros Personas/Jesus_after.jpg', 'Jesus hijo 1'],
#          1 : ['Miguel', './Rostros Personas/Miguel_before.jpg', './Rostros Personas/Miguel_after.jpg', 'Miguel hijo 1'],
#          2 : ['Karla', './Rostros Personas/Karla_before.jpg', './Rostros Personas/Karla_after.jpg', 'Karla hijo 1'],
#          3 : ['Jared', './Rostros Personas/Jared_before.jpg', './Rostros Personas/Jared_after.jpg', 'Jared hijo 1'],
#          4 : ['Raul', './Rostros Personas/Raul_before.jpg', './Rostros Personas/Raul_after.jpg', 'Raul hijo 1']
#          }

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

    if respuesta and respuesta.get('ResponseMetadata').get('HTTPStatusCode') == 200:
        # UnmatchedFaces
        for i in respuesta['UnmatchedFaces']:
            # print(i)
            print('Los rostros comparados no son de la misma persona.')

        # FaceMatches
        for i in respuesta['FaceMatches']:
            # FACE
            # print('BoundingBoxWidth: ',i['Face']['BoundingBox']['Width'])
            # print('BoundingBoxHeight: ',i['Face']['BoundingBox']['Height'])

            # QUALITY
            # print('QualityBrightness: ',i['Face']['Quality']['Brightness'])
            # print('QualitySharpness: ',i['Face']['Quality']['Sharpness'])
            
            # SIMILARITY
            print('Similarity: ', i['Similarity'])
            
            # CONFIDENCE
            print('Confidence: ', i['Face']['Confidence'])
            
            
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
        cv2.rectangle(frame,(10,5),(450,25),(255,255,255),-1)
        cv2.putText(frame,'Presione s para almacenar los rostros encontrados y presione ESC para cerrar la cámara.',(10,20), 2, 0.5,(128,0,255),1,cv2.LINE_AA)
        cv2.imshow('frame',frame)

    cap.release()
    cv2.destroyAllWindows()

# COMPARAMOS LA PRIMERA FOTOGRAFÍA GUARDADA CON LAS IMÁGENES GUARDADAS EN LA BD

if __name__ == "__main__":
    crearCarpetaFotos()
    capturarFotos()
    
    ruta_img1 = './Rostros encontrados/rostro_0.jpg'
        
    for i in range(len(rutas)):
        for j in range(1,3):
            ruta_img2 = rutas[i][j]
            
            print('Comparado con: ' + rutas[i][0])
            compararRostros(ruta_img1, ruta_img2)
            
            # print('\n')