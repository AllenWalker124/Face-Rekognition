from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import os
import rekognition

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        
# CAPTURAR FOTOGRAFÍAS USANDO LA CÁMARA
def crearCarpetaFotos():
    if not os.path.exists('Rostros encontrados'):
        print('Carpeta creada: Rostros encontrados')
        os.makedirs('Rostros encontrados')

# INTERFAZ        
        
def visualizar():
    global cap
    ret, frame = cap.read()
    
    if ret == True:
        frame = imutils.resize(frame, width=640)
        frame = deteccion_facilal(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)

        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, visualizar)
    else:
        lblVideo.image = ""
        lblInfoVideoPath.configure(text="")
        btnIniciarCamara.configure(state="active")
        btnEnd.configure(state="disabled")
        cap.release()

def capturar_video():
    global cap
    
    btnEnd.configure(state="active")
    lblInfoVideoPath.configure(text="")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    visualizar()
    
def tomar_foto(count, rostro):
    cv2.imwrite('Rostros encontrados/rostro_{}.jpg'.format(count), rostro)
    # cv2.imshow('rostro_{}'.format(count), rostro)

def deteccion_facilal(frame):
    frame = cv2.flip(frame, 1)
    auxFrame = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)
    count = 0
    
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        rostro = auxFrame[y:y+h, x:x+w]
        rostro = cv2.resize(rostro,(150,150), interpolation=cv2.INTER_CUBIC)
        tomar_foto(count, rostro)
        count = count + 1
            
    return frame

def reconocer_persona():
    btnReiniciar.configure(state="active")
    
    # UNA VEZ TENEMOS LA FOTO, REALIZAMOS LA COMPARACIÓN DE ROSTROS
    ruta_img = './Rostros encontrados/rostro_0.jpg'
    type_msg, msg_notif = rekognition.actualizacionStatus(ruta_img)      # Lista de alumnos que tienen permitido salir
    lblInfo2.image = ""
    
    if type_msg == 1:
        lblInfo2.configure(text=msg_notif, fg="green")
    else:
        lblInfo2.configure(text=msg_notif, fg="red")
    
def reiniciar():
    lblVideo.image = ""
    lblInfo2.configure(text=msg_inicial, fg="black")
    lblInfoVideoPath.configure(text="")
    btnIniciarCamara.configure(state="active")
    cap.release()
    cv2.destroyAllWindows()
    btnReiniciar.configure(state="disabled")

crearCarpetaFotos()
cap = None 
root = Tk()

root.title("Reconocimiento facial")

lblInfo1 = Label(root, text="Reconocimiento facial", font="bold")
lblInfo1.grid(column=0, row=0, columnspan=8)

msg_inicial = 'Coloque su rostro en el recuadro de abajo, tratando de que todas sus facciones se distingan perfectamente y espere la \nconfirmación del reconocimiento.'
lblInfo2 = Label(root, text=msg_inicial, font="bold", height=2)
lblInfo2.grid(column=0, row=2, columnspan=8, rowspan=2)

lblInfoVideoPath = Label(root, text="", width=20)
lblInfoVideoPath.grid(column=0, row=4)

lblVideo = Label(root)
lblVideo.grid(column=0, row=5, columnspan=8)


btnIniciarCamara = Button(root, text="Activar cámara", state="active", command=capturar_video)
btnIniciarCamara.grid(column=0, row=6, columnspan=2, pady=10)

btnEnd = Button(root, text="Capturar rostro", state="disabled", command=reconocer_persona)
btnEnd.grid(column=1, row=6, columnspan=4, pady=10)

btnReiniciar = Button(root, text="Reiniciar", state="disabled", command=reiniciar)
btnReiniciar.grid(column=6, row=6, columnspan=2, pady=10)

root.mainloop()