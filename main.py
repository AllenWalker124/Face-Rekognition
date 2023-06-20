from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import os
import rekognition
import ctypes
import actualizar_datos
from time import sleep

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# CAPTURAR FOTOGRAFÍAS USANDO LA CÁMARA
def crearCarpetaFotos():
    if not os.path.exists('Rostros encontrados'):
        print('Carpeta creada: Rostros encontrados')
        os.makedirs('Rostros encontrados')

# FUNCIÓN PARA BOTÓN 'BUSCAR PADRE'
def mostrarFotoTutor(nombreTutor):
    tutor_existe = actualizar_datos.validarRegistroTutor(nombreTutor)
    if tutor_existe:
        actualizar_datos.actualizarBD(nombreTutor)
        msg = 'Persona encontrada, su(s) hijo(s) esta(n) \nen camino a la puerta de salida, por favor espere su llegada.'
        notif_label_busqueda.configure(text=msg)
        
    else:
        msg = 'La persona no se encuentra registrada en la base de datos, por favor inténtelo de nuevo cuidando errores ortográficos.'
        notif_label_busqueda.configure(text=msg)
        

def enviarDatos():
    lbl_foto_tutor.configure(image="")
    lbl_foto_tutor.image = ""
    notif_label_busqueda.configure(text="")
    nombreTutor = mensajeTxt.get(1.0, "end-1c")
    print(nombreTutor)
    mostrarFotoTutor(nombreTutor)
    Ventana.after(5000, limpiarBusqueda)
    # Ventana.destroy()
    
# INTERFAZ            
def visualizar():
    global cap
    ret, frame = cap.read()
    
    if ret == True:
        frame = imutils.resize(frame, width=800)
        frame = deteccion_facilal(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)

        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, visualizar)
    else:
        lblVideo.image = ""
        btnIniciarCamara.configure(state="active")
        btnTomarFoto.configure(state="disabled")
        cap.release()

def capturar_video():
    global cap
    
    btnIniciarCamara.configure(state="disabled")
    btnTomarFoto.configure(state="active")
    btnReiniciar.configure(state="active")
    
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)                        ### 0 para webcam, 1 para cámara externa
    visualizar()
    
def tomar_foto(count, rostro):
    cv2.imwrite('Rostros encontrados/rostro_{}.jpg'.format(count), rostro)
    # cv2.imshow('rostro_{}'.format(count), rostro)

def deteccion_facilal(frame):
    # frame = cv2.flip(frame, 1)
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

def reiniciarVentana():
    lblInfo2.configure(text=msg_inicial, fg="Black", justify="center")
    btnIniciarCamara.configure(state="active")
    btnTomarFoto.configure(state="disabled")
    btnReiniciar.configure(state="disabled")

def initComparation():
    ruta_img = './Rostros encontrados/rostro_0.jpg'
    type_msg, msg_notif = rekognition.actualizacionStatus(ruta_img)      # Lista de alumnos que tienen permitido salir

    if type_msg == 1:
        lblInfo2.configure(text=msg_notif, fg="#29BF12", justify="center")
        Ventana.after(5000, reiniciarVentana)
        
    else:
        lblInfo2.configure(text=msg_notif, fg="#F21B3F", justify="center")
        Ventana.after(5000, reiniciarVentana)

def reconocer_persona():
    # UNA VEZ TENEMOS LA FOTO, REALIZAMOS LA COMPARACIÓN DE ROSTROS Y MODIFICAMOS EL LABEL DE VIDEO
    
    # mostrarGif()
    
    lblVideo.configure(image="")
    lblVideo.image = ""
    cap.release()
    
    msg_procesando = "Buscando rostro en la base de datos.\nPor favor espere un momento..."
    lblInfo2.configure(text=msg_procesando, fg="#168AAD", justify="center")
    
    Ventana.after(500, initComparation)
    
def reiniciar():
    lblInfo2.configure(text=msg_inicial, fg="Black", justify="center")
    lblVideo.image = ""
    cap.release()
    cv2.destroyAllWindows()
    # limpiarBusqueda()
    btnIniciarCamara.configure(state="active")
    btnTomarFoto.configure(state="disabled")
    btnReiniciar.configure(state="disabled")
    
def limpiarBusqueda():
    lbl_foto_tutor.configure(image="")
    lbl_foto_tutor.image = ""
    notif_label_busqueda.configure(text="")
    mensajeTxt.delete("1.0","end")
    
# INICIALIZAMOS DATOS
crearCarpetaFotos()
cap = None 

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
ancho, alto = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# print(ancho, alto)

alto = alto - 100
dim_window = str(ancho) + 'x' + str(alto)

# CREAMOS INTERFAZ
Ventana=Tk()
Ventana.title("Face 2 Pick Up")
Ventana.configure(bg="#F8EDEB")
Ventana.geometry(dim_window)


lbl_0 = Label(Ventana, text="", font = ("calibri", 20, "bold"), bg="#F8EDEB")
lbl_0.grid(row=0, column=1, columnspan=4)

## logo
img = ImageTk.PhotoImage(Image.open("./Logo/L3_3.png"))
label = Label(Ventana, image = img, bg="#F8EDEB")
label.grid(row=1, column=1, columnspan=4)

lbl_1 = Label(Ventana, text="", font = ("calibri", 12, "bold"), bg="#F8EDEB")
lbl_1.grid(row=2, column=1, columnspan=3)

## Información
msg_inicial = 'Coloque su rostro en el recuadro de abajo, tratando de que todas sus facciones se distingan\nperfectamente y espere la confirmación del reconocimiento.'
lblInfo2 = Label(Ventana, text=msg_inicial, font=("calibri", 14, "bold"), fg="Black", justify="center", bg="#F8EDEB")
lblInfo2.grid(row=3, column=1, columnspan=3)

lbl_3 = Label(Ventana, text="", font = ("calibri", 12, "bold"), bg="#F8EDEB")
lbl_3.grid(row=4, column=1, columnspan=3)

## Ventana video
frmBorde = Frame(Ventana,bg="#FFB5A7",height=500,width=200, padx=20, pady=20)
frmBorde.grid(row=5, column=1)

frmTabla = Frame(Ventana,bg="#FCD5CE",height=620, width=820, padx=20, pady=20)
frmTabla.grid(row=5, column=2)

frmBorde2 = Frame(Ventana,bg="#FFB5A7",height=500,width=200, padx=20, pady=20)
frmBorde2.grid(row=5, column=3)

lblVideo = Label(Ventana, text="", font=("calibri", 14, "italic", "bold"), fg="#168AAD", justify="center", bg="#FCD5CE")
lblVideo.grid(row=5, column=2)


# Botones
lbl_4 = Label(Ventana, text="", font = ("calibri", 7, "bold"), bg="#F8EDEB")
lbl_4.grid(row=6, column=1, columnspan=3)

frmBotones = Frame(Ventana,bg="#F8EDEB",height=100,width=100,padx=5,pady=5)
frmBotones.grid(row=7, column=1, columnspan=3)

# grid botones:
btnIniciarCamara = Button(frmBotones,text="Activar cámara",font=("calibri", 14, "bold"), state="active", command=capturar_video)  # command=pantallaCarga
btnIniciarCamara.grid(row=1,column=2, padx=20)
btnTomarFoto = Button(frmBotones,text="Capturar rostro",font=("calibri", 14, "bold"), state="disabled", command=reconocer_persona)
btnTomarFoto.grid(row=1,column=3, padx=20)
btnReiniciar = Button(frmBotones,text="Reiniciar",font=("calibri", 14, "bold"), state="disabled", command=reiniciar)
btnReiniciar.grid(row=1,column=4, padx=20)

# Cuadro buscar padre
frmBusqueda = Frame(Ventana, bg="#F8EDEB",height=620,width=400,padx=15,pady=15)
frmBusqueda.grid(row=5, column=5, columnspan=3)

msg = "Buscar padre/tutor (empezando por apellidos):"
msg_label = Label(frmBusqueda, text=msg, bg="#F8EDEB", fg='#168AAD', font=("calibri", 14, "bold"))
msg_label.grid(row=0, column=2, padx=20, pady=20)
mensajeTxt = Text(frmBusqueda, width=45 , height=1, font=("calibri", 12, "bold"), padx=40, pady=10)
mensajeTxt.grid(row=1, column=2)

frmBotonesBusqueda = Frame(frmBusqueda, bg="#F8EDEB",height=200,width=400,padx=15,pady=15)
frmBotonesBusqueda.grid(row=2, column=2, columnspan=3)

botonEnviar = Button(frmBotonesBusqueda, text="Buscar", fg="black", font=("calibri",14, "bold"), command=enviarDatos)
botonEnviar.grid(row=1, column=0, padx=20, pady=20)

botonLimpiar = Button(frmBotonesBusqueda, text="Limpiar", fg="black", font=("calibri",14, "bold"), command=limpiarBusqueda)
botonLimpiar.grid(row=1, column=1, padx=20, pady=20)

# hay que agregar un label para la notificación y otro para mostrar la foto del padre:000
notif_label_busqueda = Label(frmBusqueda, text="", bg="#F8EDEB", fg='#168AAD', font=("calibri", 12, "bold"))
notif_label_busqueda.grid(row=4, column=2, padx=20, pady=20, columnspan=3)

# img_tutor = ImageTk.PhotoImage(Image.open("./Rostros Personas/Estrada Crespo Karla Julieta.jpg"))
lbl_foto_tutor = Label(frmBusqueda, image="", bg="#F8EDEB")
lbl_foto_tutor.grid(row=5, column=2, columnspan=3)

for i in range(6):
    # Espacios
    lbl_5 = Label(frmBusqueda, text="           ", font = ("calibri", 14, "bold"), bg="#F8EDEB")
    lbl_5.grid(row=i, column=1)

Ventana.mainloop()