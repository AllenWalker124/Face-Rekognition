import boto3
from botocore.exceptions import ClientError
import actualizar_datos

# Diccionario con imagenes

photos_path = actualizar_datos.get_images_path()
informacion_alumnos = actualizar_datos.get_students_data()


CON_THRES = 95
SIM_THRES = 95

# FUNCIONES PARA LA COMPARACIÓN DE ROSTROS

def obtener_bytes_imagen(ruta_imagen):
    with open(ruta_imagen, "rb") as imagen:
        return imagen.read()

def compararRostros(bytes_1,bytes_2):
    cliente = boto3.client('rekognition')
    try:
        respuesta = cliente.compare_faces(SourceImage = {'Bytes' : bytes_1}, 
                                          TargetImage = {'Bytes': bytes_2},
                                          SimilarityThreshold = 60,
                                          QualityFilter = 'NONE')
        
        ### QUALITY FILTER: NONE'|'AUTO'|'LOW'|'MEDIUM'|'HIGH'

    except ClientError as error:
        print("Ocurrio un error al llamar a la API:",error, '\n')
    
    if respuesta and respuesta.get('ResponseMetadata').get('HTTPStatusCode') == 200:
        
        if respuesta["FaceMatches"] == None:
            return False
        
        for i in respuesta['FaceMatches']:
            similaridad = float(i['Similarity'])
            confianza =  float(i['Face']['Confidence'])
            
            if similaridad > SIM_THRES or confianza > CON_THRES:
                return True


# COMPARAMOS LA PRIMERA FOTOGRAFÍA GUARDADA CON LAS IMÁGENES GUARDADAS EN LA BD

def actualizacionStatus(ruta_img1):
    
    isPerson = False
    msg_notificacion = ''
    type_msg = 0    # Variable para cambiar el color del msg que se muestra en la interfaz
    
    bytes_1 = obtener_bytes_imagen(ruta_img1)
    
    for i in range(len(photos_path)):
        Person = i
        ruta_img2 = photos_path[i][1]
        bytes_2 = obtener_bytes_imagen(ruta_img2)
        isPerson = compararRostros(bytes_1, bytes_2)
                
        if isPerson:
            break
    
    if isPerson:
        type_msg = 1
        msg_notificacion = 'Rostro reconocido correctamente: ' + photos_path[Person][0] + '\nsu(s) hijo(s) esta(n) en camino a la puerta de salida, por favor espere su llegada.'    
        actualizar_datos.actualizarBD(photos_path[Person][0])

    else:
        msg_notificacion = 'Su rostro no se está identificando correctamente, por favor coloquelo de nuevo en el recuadro \ncuidando que sus facciones se distingan con claridad (no lentes, no cubrebocas).'
        
    return type_msg, msg_notificacion