from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import os
import rekognition
import ctypes

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        
# CAPTURAR FOTOGRAFÍAS USANDO LA CÁMARA
def crearCarpetaFotos():
    if not os.path.exists('Rostros encontrados'):
        print('Carpeta creada: Rostros encontrados')
        os.makedirs('Rostros encontrados')

# FUNCIÓN PARA BOTÓN 'BUSCAR PADRE'
def enviarDatos():
    mensaje = mensajeTxt.get(1.0, "end-1c")
    print(mensaje)
    Ventana.destroy()
    
    
def pantallaCarga():
    lblVideo.configure(text="Buscando rostro en la base de datos.\nPor favor espere un momento...")


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
        btnIniciarCamara.configure(fg="blue", state="active")
        btnTomarFoto.configure(fg="green", state="disabled")
        cap.release()

def capturar_video():
    global cap
    
    btnIniciarCamara.configure(fg="blue", state="disabled")
    btnTomarFoto.configure(fg="green", state="active")
    btnReiniciar.configure(fg="red", state="active")
    
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
    # UNA VEZ TENEMOS LA FOTO, REALIZAMOS LA COMPARACIÓN DE ROSTROS
    ruta_img = './Rostros encontrados/rostro_0.jpg'
    type_msg, msg_notif = rekognition.actualizacionStatus(ruta_img)      # Lista de alumnos que tienen permitido salir
    lblInfo2.image = ""
    
    if type_msg == 1:
        lblInfo2.configure(text=msg_notif, fg="#29BF12", justify="center")
    else:
        lblInfo2.configure(text=msg_notif, fg="#F21B3F", justify="center")
    
def reiniciar():
    lblVideo.image = ""
    lblInfo2.configure(text=msg_inicial, fg="Black", justify="center")
    btnIniciarCamara.configure(fg="blue", state="active")
    cap.release()
    cv2.destroyAllWindows()
    btnTomarFoto.configure(fg="green", state="disabled")
    btnReiniciar.configure(fg="red", state="disabled")

################################################################################

crearCarpetaFotos()
cap = None 

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
ancho, alto = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# print(ancho, alto)

alto = alto - 100

dim_window = str(ancho) + 'x' + str(alto)

################################################################################
Ventana=Tk()
Ventana.title("Face 2 Pick Up")
Ventana.configure(bg="#F8EDEB")
Ventana.geometry(dim_window)



# lbl_0 = Label(Ventana, text="", font = ("calibri", 6, "bold"), bg="#F8EDEB")
# lbl_0.grid(row=0, column=1, columnspan=3)

# # logo
# img = ImageTk.PhotoImage(Image.open("./Logo/L3_3.png"))
# label = Label(Ventana, image = img, bg="#F8EDEB")
# label.grid(row=1, column=1, columnspan=3)

# # Información
# # lblInfo0 = Label(Ventana, text="Reconocimiento facial", font = ("calibri", 22, "italic", "bold"), fg="#168AAD", justify="center", bg="#F8EDEB")
# # lblInfo0.grid(row=0, column=1, columnspan=3)


# lbl_1 = Label(Ventana, text="", font = ("calibri", 12, "bold"), bg="#F8EDEB")
# lbl_1.grid(row=2, column=1, columnspan=3)

# msg_inicial = 'Coloque su rostro en el recuadro de abajo, tratando de que todas sus facciones se distingan\nperfectamente y espere la confirmación del reconocimiento.'
# lblInfo2 = Label(Ventana, text=msg_inicial, font=("calibri", 14, "bold"), fg="Black", justify="center", bg="#F8EDEB")
# lblInfo2.grid(row=3, column=1, columnspan=3)

# lbl_3 = Label(Ventana, text="", font = ("calibri", 12, "bold"), bg="#F8EDEB")
# lbl_3.grid(row=4, column=1, columnspan=3)

# # Ventana video
# frmBorde = Frame(Ventana,bg="#FFB5A7",height=500,width=200, padx=20, pady=20)
# frmBorde.grid(row=5, column=1)

# frmTabla = Frame(Ventana,bg="#FCD5CE",height=500, width=660, padx=20, pady=20)
# frmTabla.grid(row=5, column=2)

# frmBorde2 = Frame(Ventana,bg="#FFB5A7",height=500,width=200, padx=20, pady=20)
# frmBorde2.grid(row=5, column=3)

# lblVideo = Label(Ventana)
# lblVideo.grid(row=5, column=2)

# # Botones
# lbl_4 = Label(Ventana, text="", font = ("calibri", 7, "bold"), bg="#F8EDEB")
# lbl_4.grid(row=6, column=1, columnspan=3)

# frmBotones = Frame(Ventana,bg="#F8EDEB",height=100,width=100,padx=5,pady=5)
# frmBotones.grid(row=7, column=1, columnspan=3)

# # grid botones:
# btnIniciarCamara = Button(frmBotones,text="Activar cámara",font=("calibri", 14, "bold"),fg="blue", state="active", command=capturar_video)
# btnIniciarCamara.grid(row=1,column=2, padx=20)
# btnTomarFoto = Button(frmBotones,text="Capturar rostro",font=("calibri", 14, "bold"),fg="green", state="disabled", command=reconocer_persona)
# btnTomarFoto.grid(row=1,column=3, padx=20)
# btnReiniciar = Button(frmBotones,text="Reiniciar",font=("calibri", 14, "bold"),fg="red", state="disabled", command=reiniciar)
# btnReiniciar.grid(row=1,column=4, padx=20)


# Ventana.mainloop()



lbl_0 = Label(Ventana, text="", font = ("calibri", 20, "bold"), bg="#F8EDEB")
lbl_0.grid(row=0, column=1, columnspan=4)

# logo
img = ImageTk.PhotoImage(Image.open("./Logo/L3_3.png"))
label = Label(Ventana, image = img, bg="#F8EDEB")
label.grid(row=1, column=1, columnspan=4)

# Información
# lblInfo0 = Label(Ventana, text="Reconocimiento facial", font = ("calibri", 22, "italic", "bold"), fg="#168AAD", justify="center", bg="#F8EDEB")
# lblInfo0.grid(row=0, column=1, columnspan=3)


lbl_1 = Label(Ventana, text="", font = ("calibri", 12, "bold"), bg="#F8EDEB")
lbl_1.grid(row=2, column=1, columnspan=3)

msg_inicial = 'Coloque su rostro en el recuadro de abajo, tratando de que todas sus facciones se distingan\nperfectamente y espere la confirmación del reconocimiento.'
lblInfo2 = Label(Ventana, text=msg_inicial, font=("calibri", 14, "bold"), fg="Black", justify="center", bg="#F8EDEB")
lblInfo2.grid(row=3, column=1, columnspan=3)

lbl_3 = Label(Ventana, text="", font = ("calibri", 12, "bold"), bg="#F8EDEB")
lbl_3.grid(row=4, column=1, columnspan=3)

# Ventana video
frmBorde = Frame(Ventana,bg="#FFB5A7",height=500,width=200, padx=20, pady=20)
frmBorde.grid(row=5, column=1)

frmTabla = Frame(Ventana,bg="#FCD5CE",height=620, width=820, padx=20, pady=20)
frmTabla.grid(row=5, column=2)

frmBorde2 = Frame(Ventana,bg="#FFB5A7",height=500,width=200, padx=20, pady=20)
frmBorde2.grid(row=5, column=3)

lblVideo = Label(Ventana, text="", font=("calibri", 14, "italic", "bold"), fg="Black", justify="center", bg="#FCD5CE")
lblVideo.grid(row=5, column=2)

# Botones
lbl_4 = Label(Ventana, text="", font = ("calibri", 7, "bold"), bg="#F8EDEB")
lbl_4.grid(row=6, column=1, columnspan=3)

frmBotones = Frame(Ventana,bg="#F8EDEB",height=100,width=100,padx=5,pady=5)
frmBotones.grid(row=7, column=1, columnspan=3)

# grid botones:
btnIniciarCamara = Button(frmBotones,text="Activar cámara",font=("calibri", 14, "bold"),fg="blue", state="active", command=capturar_video)
btnIniciarCamara.grid(row=1,column=2, padx=20)
btnTomarFoto = Button(frmBotones,text="Capturar rostro",font=("calibri", 14, "bold"),fg="green", state="disabled", command=reconocer_persona)
btnTomarFoto.grid(row=1,column=3, padx=20)
btnReiniciar = Button(frmBotones,text="Reiniciar",font=("calibri", 14, "bold"),fg="red", state="disabled", command=reiniciar)
btnReiniciar.grid(row=1,column=4, padx=20)

# Cuadro buscar padre


frmBusqueda = Frame(Ventana, bg="#F8EDEB",height=230,width=400,padx=15,pady=15)
frmBusqueda.grid(row=5, column=5, columnspan=3)

msg_label = Label(frmBusqueda, text="Buscar padre/tutor:", bg="#F8EDEB", fg='#168AAD', font=("calibri", 14, "bold"))
msg_label.grid(row=0, column=2, padx=20, pady=20)
mensajeTxt = Text(frmBusqueda, width=45 , height=1, font=("calibri", 12, "bold"), padx=40, pady=10)
mensajeTxt.grid(row=1, column=2)

botonEnviar = Button(frmBusqueda, text="Buscar", fg="black", font=("calibri",14, "bold"), command=enviarDatos)
botonEnviar.grid(row=2, column=2, padx=20, pady=20)


# Espacios
lbl_5 = Label(Ventana, text="        ", font = ("calibri", 14, "bold"), bg="#F8EDEB")
lbl_5.grid(row=5, column=4, columnspan=1)

Ventana.mainloop()