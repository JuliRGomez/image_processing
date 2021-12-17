import cv2 as cv
import numpy as np
from scipy.spatial import distance as dist
kernel = np.ones((3,3),np.uint8)
# Definir el cálculo de coordenadas del punto medio
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
def measure(img):
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    #ret, thresh = cv.threshold(gray, 127, 255, 0)
    gauss = cv.GaussianBlur(gray, (5, 5), 0)
    ret, thresh = cv.threshold(gauss, 127, 255, 0)
    opening = cv.morphologyEx(thresh,cv.MORPH_CLOSE, kernel)
    canny = cv.Canny(opening, 50, 150)
    cv.imshow("canny",canny)
    contours, hierarchy = cv.findContours(canny, 1, 2)
    print(len(contours))
    cnts = sorted(contours, key=cv.contourArea,reverse=True)[:1]
    for cnt in cnts:
	#  # Encuentra la distancia geométrica del contorno   
        M = cv.moments(cnt)
    # 	     # Obtenga el rectángulo circunscrito del contorno, x, y son las coordenadas de píxeles de la esquina superior izquierda del marco verde, w, h son la longitud y el ancho del marco verde
        x, y, w, h = cv.boundingRect(cnt)
    # 	     # Calcule el contorno mínimo, cuadro rojo
        rect = cv.minAreaRect(cnt)
    # 	     # Calcula las coordenadas de la imagen de las 4 esquinas del cuadro rojo
        box = cv.boxPoints(rect)
    # 	     # El número de la imagen es un número entero, así que convierta las coordenadas en un número entero
        box = np.int0(box)


        if M['m00'] != 0:
        	# print(M)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
        	         #Según el punto central obtenido por la distancia geométrica, dibuje el círculo central, que está bloqueado por la línea azul, por lo que no se puede ver
            cv.circle(img,(int(cx),int(cy)),2,(0,255,255),-1) 
         	         #     Marco
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        	         #Pintando cuadro rojo 4 esquinas
            cv.drawContours(img, [box], 0, (0, 0, 255), 2)
            for (x, y) in box:
                cv.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
            	             # tl coordenadas del número de la imagen de la esquina superior izquierda, tr coordenadas del número de la imagen de la esquina superior derecha, br coordenadas del número de la imagen de la esquina inferior derecha, bl coordenadas del número de la imagen de la esquina inferior izquierda
                (tl, tr, br, bl) = box
             	             # Calcule los puntos centrales de los 4 lados del cuadro rojo
                (tltrX, tltrY) = midpoint(tl, tr)
                (blbrX, blbrY) = midpoint(bl, br)
                (tlblX, tlblY) = midpoint(tl, bl)
                (trbrX, trbrY) = midpoint(tr, br)
                    # Dibuja algunos
                cv.circle(img, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
                cv.circle(img, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
                cv.circle(img, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
                cv.circle(img, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)
            	             # Dibuja una línea para conectar 4 puntos, es decir, 2 líneas azules en la imagen.

                cv.line(img, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                    (255, 0, 0), 2)
                cv.line(img, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                      (255, 0, 0), 2)
                                  # Calcula las coordenadas del punto central
                dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
                dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
    #         	             # Convierta la longitud del número de imagen a la longitud real, 6.5 equivale a la escala, yo uso la unidad mm, es decir, 1 mm equivale a 6.5 imágenes

                dimA = dA / 6.5
                dimB = dB / 6.5
    #         	             # Imprima el resultado del cálculo en la imagen original, que es el contenido amarillo

                cv.putText(img, "{:.1f}mm".format(dimA),
                        (int(tltrX - 15), int(tltrY - 10)), cv.FONT_HERSHEY_SIMPLEX,
                         0.65, (0, 255, 255), 2)
                cv.putText(img, "{:.1f}mm".format(dimB),
                         (int(trbrX + 10), int(trbrY)), cv.FONT_HERSHEY_SIMPLEX,
                         0.65, (0, 255, 255), 2)
    cv.imshow("mo", img)
 # Enciende la cámara, configura la resolución
img = cv.imread("./img/tela_rayas_1.png")
measure(img)
cv.waitKey(0)