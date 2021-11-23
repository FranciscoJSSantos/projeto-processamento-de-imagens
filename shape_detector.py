import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

#captura do vídeo
cam = cv2.VideoCapture(0)

#captura da imagem
img = cv2.imread("formas_geometricas.png")

while True:
    # atribuindo a imagem em variaveis e dando zoom na imagem
    ret, frame = cam.read()
    frame = frame[0:300, 200:600]

    #verificação de o vídeo possui imagem
    if not ret:
        break

    #para caso for usar a imagem
    #frame = img


    #pré-processamento da imagem
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)

    #função para pegar os contornos da imagem
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #atribuição de variaveis para o processamento
    i = 0
    x = 0
    y = 0

    for contour in contours:

        #condicional para ignorar o primeiro contorno
        if i == 0:
            i = 1
            continue

        #função para aproximar as formas
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)

        #função para desenhar os contornos
        cv2.drawContours(frame, [contour], 0, (0, 0, 255), 5)

        #encontrando o centro da forma geométrica
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10'] / M['m00'])
            y = int(M['m01'] / M['m00'])

        #condicional para adição de texto da forma geométrica
        if len(approx) == 3:
            cv2.putText(frame, 'Triangulo', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        elif len(approx) == 4:
            cv2.putText(frame, 'Quadrilatero', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        elif len(approx) == 5:
            cv2.putText(frame, 'Pentagono', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        elif len(approx) == 6:
            cv2.putText(frame, 'Hexagono', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        else:
            cv2.putText(frame, 'Circulo', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    #saída da imagem
    cv2.imshow("threshold", threshold)
    cv2.imshow("Camera", frame)

    # macro pro esc fechar a imagem
    key = cv2.waitKey(10)
    if key == 27:
        break

    #sleep para travar variação da imagem por causa do loop
    #time.sleep(300)

#desligar a câmera
cam.release()
cv2.destroyAllWindows()