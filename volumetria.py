import numpy as np
import cv2
import math

#Capturando o vídeo e reduzindo a escala da imagem
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

while True:
    #atribuindo a imagem em variaveis e dando zoom na imagem
    ret, img = cap.read()
    img = img[100:500, 100:500]

    #verificação de o vídeo possui imagem
    if img is None:
        break

    #pré-processamento da imagem
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray,(3,3))
    edges = cv2.Canny(blur, 100, 120)
    kernel = np.ones((3,3),np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)
    lines = cv2.HoughLinesP(dilated, 1, math.pi/180, 30, None, 2, 480)

    #verificação se existe a linha
    if lines is not None:
        dot1 = (lines[0][0][0],lines[0][0][1])
        dot2 = (lines[0][0][2],lines[0][0][3])
        dot = max([lines[0][0][1],lines[0][0][3]])
        cv2.line(img, dot1, dot2, (255,0,0), 3)
        length = lines[0][0][1] - lines[0][0][3]

        #calculo do volume
        volume = math.pi * math.pow(2.75,2) * (13 - dot/30.77)

        #print dos dados no console
        print(f" Line Length = {abs(dot)}  Volume = {abs(volume):.1f}")

    #saída da imagem
    cv2.imshow("output", img)

    #macro pro esc fechar a imagem
    key = cv2.waitKey(10)
    if key == 27:
        break

#desligar a câmera
cv2.destroyAllWindows()
cv2.VideoCapture(0).release()