import boto3
from botocore.exceptions import ClientError

def obtenerBitesImg(rutaImg):
    with open(rutaImg, 'rb') as imagen:
        return imagen.read

def compararRostros(rutaImg1, rutaImg2):
    bytes_1 = obtenerBitesImg(rutaImg1)
    bytes_2 = obtenerBitesImg(rutaImg2)
    
    cliente = boto3.client('rekognition')
    
    try:
        respuesta = cliente.compare_faces(SourceImage = {'Bytes': bytes_1}, 
                                          TargetImage = {'Bytes': bytes_2},
                                          SimilarityThreshold = 60,
                                          QualityFilter = 'AUTO')
        
        # QualityFilter = NONE|AUTO|LOW|MEDIUM|HIGH

        if respuesta and respuesta['ResponsableMetadata']['HTTPStatusCode'] == 200:
            # Unmatched Faces
            for i in respuesta['UnmatchedFaces']:
                print(i + ' /n')
                
            # Matched Faces
            for i in respuesta['FaceMatches']:
                print('Similarity: ' + str(i['Similarity']))
                
    except ClientError as error:
        print('Ocurrio un error al llamar a la api Rekognition ' + str(error))
        
if __name__ == "__main__":
    
    ruta_imagen_1 = 'C:/Users/caran/Downloads/zack_before.png'
    ruta_imagen_2 = 'C:/Users/caran/Downloads/zack_after.png'
    
    compararRostros(ruta_imagen_1, ruta_imagen_2)