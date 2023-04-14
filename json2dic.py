import json

def convertirJson2Dic(json_path):
    
    # json_path = './JSON/datos_usuarios.json'
    file = open(json_path, "r", encoding="UTF-8")
    jsonContent = file.read()
    aList = json.loads(jsonContent)

    diccionario = set()
    elements = aList["Datos Usuarios"]
    
    for element in elements:
        diccionario.add((element["tutor_1"], element["tutor_2"], element["tutor_3"], element["foto_1"], element["foto_2"], element["foto_3"], tuple(element["hijos"]), tuple(element["edad_hijos"]), tuple(element["grupos"])))

    diccionario = list(diccionario)
    diccionario.sort()
    
    return diccionario