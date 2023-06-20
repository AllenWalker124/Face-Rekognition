import base64
import os

def crearCarpetaFotosPadres():
    if not os.path.exists('Rostros Padres'):
        print('Carpeta creada: Rostros Padres')
        os.makedirs('Rostros Padres')

crearCarpetaFotosPadres()

def codificar_b64(img_path):
    image = open(img_path, 'rb')
    image_read = image.read()
    image_64_encode = base64.b64encode(image_read)
    return image_64_encode


def decodificar_b64(name, image_64_encode):
    # print('imagen codificada: ', image_64_encode)
    image_64_decode = base64.b64decode(image_64_encode)
    new_img_path = './Rostros Padres/'+ name +'.jpg'
    image_result = open(new_img_path, 'wb')
    image_result.write(image_64_decode)