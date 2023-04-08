import cv2
import numpy as np

faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

image = cv2.imread('./Rostros Personas/Bale_before.png')
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

faces = faceClassif.detectMultiScale(gray,
                    scaleFactor = 1.1,
                    minNeighbors = 5,
                    minSize = (20,20),
                    maxSize = (500,500))

for (x,y,w,h) in faces:
    cv2.rectangle(image(x,y), (x+w, y+h), (0,255,0), 2)

cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows