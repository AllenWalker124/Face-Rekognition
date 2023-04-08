import cv2

# Abrimos la cámara
cap = cv2.VideoCapture(0)

# Establecer dimensiones
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)  # ancho 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)  # ancho

# Tomar una imagen
ret, frame = cap.read()

# Guardamos la imagen en un archivo
cv2.imwrite('C:/Users/caran/OneDrive/Documentos/Tareas 6to Semestre/Interacción Humano-Máquina/Proyectos/AWS Rekognition/Fotos Capturadas/foto.jpg', frame)

# Liberamos la cámara
cap.release()