import boto3
from botocore.exceptions import ClientError

# Diccionario con imagenes

# rutas = {'Jesus':['./Rostros Personas/Jesus_before.jpg', './Rostros Personas/Jesus_after.jpg'],
#          'Miguel':['./Rostros Personas/Miguel_before.jpg', './Rostros Personas/Miguel_after.jpg'],
#          'Karla':['./Rostros Personas/Karla_before.jpg', './Rostros Personas/Karla_after.jpg'],
#          'Jared':['./Rostros Personas/Jared_before.jpg', './Rostros Personas/Jared_after.jpg'],
#          'Raul':['./Rostros Personas/Raul_before.jpg', './Rostros Personas/Raul_after.jpg']
#          }

# 0 - Jesus
# 1 - Miguel
# 2 - Karla
# 3 - Jared
# 4 - Raul 

rutas = {0 : ['Jesus', './Rostros Personas/Jesus_before.jpg', './Rostros Personas/Jesus_after.jpg'],
         1 : ['Miguel', './Rostros Personas/Miguel_before.jpg', './Rostros Personas/Miguel_after.jpg'],
         2 : ['Karla', './Rostros Personas/Karla_before.jpg', './Rostros Personas/Karla_after.jpg'],
         3 : ['Jared', './Rostros Personas/Jared_before.jpg', './Rostros Personas/Jared_after.jpg'],
         4 : ['Raul', './Rostros Personas/Raul_before.jpg', './Rostros Personas/Raul_after.jpg']
         }

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
        
        #QUALITY FILTER: NONE'|'AUTO'|'LOW'|'MEDIUM'|'HIGH'

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
            
def main():
    # ruta_imagen_1 = './Rostros Personas/zack_before.png'
    # ruta_imagen_2 = './Rostros Personas/zack_after.png'
    # ruta_imagen_1 = './Rostros Personas/patrick-dempsey_before.png'
    # ruta_imagen_2 = './Rostros Personas/patrick-dempsey_after.png'
    # ruta_imagen_1 = './Rostros Personas/Bale_before.png'
    # ruta_imagen_2 = './Rostros Personas/Bale_after.png'
    
    # ruta_imagen_1 = './Rostros Personas/Miguel_before.jpg'
    # ruta_imagen_2 = "./Rostros Personas/Miguel_after.jpg"
    # compararRostros(ruta_imagen_1, ruta_imagen_2)
    
    # rutas[][0] == Nombre de la persona
    # rutas[][1] == Primera foto
    # rutas[][2] == Segunda foto
    
    # img1 = rutas[0][1]
    img1 = './Rostros encontrados/rostro_0.jpg'
    
    for i in range(len(rutas)):
        for j in range(1,3):
            img2 = rutas[i][j]
            
            print('Comparado con: ' + rutas[i][0])
            compararRostros(img1, img2)
            
            print('\n')
            
    
main()