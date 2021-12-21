import numpy as np
import cv2
image = cv2.imread("./img/rayas_exten_3.jpg")
original = cv2.resize(image, (740, 411))
#b,g,r = cv2.split(original)
cv2.imshow("original", original)
gris = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
# #cv2.imshow("blue", b)
gauss = cv2.GaussianBlur(gris, (11,11), 0)
cv2.imshow("gauss", gauss)
canny = cv2.Canny(gauss, 50, 150)
cv2.imshow("canny", canny)
(contornos,_) = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#cnt = sorted(contornos, key=cv2.contourArea, reverse=True)[:1][0]
cv2.drawContours(original,contornos, -1, (0, 0, 255), 2)
# lines = cv2.HoughLinesP(canny, 1, np.pi/180, 100, minLineLength=100, maxLineGap=5)
# for line in lines:
#     x1, y1, x2, y2 = line[0]
#     cv2.line(original, (x1,y1), (x2,y2), (0,255,0), 1, cv2.LINE_AA)
cv2.imshow("lineas", original)   
cv2.waitKey(0)
