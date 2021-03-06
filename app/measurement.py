#TODO el script mas avanzado se encuentra en lines.py 
import numpy as np
import cv2
from operator import itemgetter
from scipy.spatial import distance as dist

kernel = np.ones((5,5),np.uint8)

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


image = cv2.imread("../img/cut_fabric.png")
original = cv2.resize(image, (740, 411))
cv2.imshow("original", original)
b,g,r = cv2.split(original)
gris = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
gauss = cv2.GaussianBlur(gris, (11, 11), 0)
canny = cv2.Canny(gauss, 50, 150)
cv2.imshow("canny", canny)
lines = cv2.HoughLinesP(canny, 1, np.pi/180, 100, minLineLength=100, maxLineGap=5)
filter_lines = []
for line in lines:
    x1, y1, x2, y2 = line[0]
    filter_lines.append({"x1":x1,"y1":y1,"x2":x2,"y2":y2})
sorted_up = sorted(filter_lines,key=itemgetter("y1"))[:1][0]
sorted_down = sorted(filter_lines,key=itemgetter("y1"),reverse=True)[:1][0]
mid_point_up =[ int( (sorted_up.get("x1") + sorted_up.get("x2")) / 2 ),int ( (sorted_up.get("y1") + sorted_up.get("y2")) / 2 ) ]
mid_point_down =[ int ( (sorted_down.get("x1") + sorted_down.get("x2")) / 2 ),int ( (sorted_down.get("y1") + sorted_down.get("y2")) / 2 )  ]
contours = [np.array([[sorted_up.get("x2"),sorted_up.get("y2")],[sorted_up.get("x1"),sorted_up.get("y1")],[sorted_down.get("x1"),sorted_down.get("y1")],[sorted_down.get("x2"),sorted_down.get("y2")]], dtype=np.int32)]
x, y, w, h = cv2.boundingRect(contours[0])
rect = cv2.minAreaRect(contours[0])
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(original, [box], 0, (255, 0, 0), 2)
for (x, y) in box:
    (tl, tr, br, bl) = box
    (tltrX, tltrY) = midpoint(tl, tr)
    (blbrX, blbrY) = midpoint(bl, br)
    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)
    cv2.line(original, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                    (0, 255, 0), 2)
    cv2.line(original, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                      (0, 255, 0), 2)
    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
    #nvierta la longitud del n??mero de imagen a la longitud real, 6.5 equivale a la escala, yo uso la unidad mm, es decir, 1 mm equivale a 6.5 im??genes
    dimA = (dA / 0.3) / 10
    dimB = (dB / 0.3) /10
    cv2.putText(original, "{:.2f} cm".format(dimA),
                        (int(tltrX + 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                         0.65, (0, 255, 255), 2)
    cv2.putText(original, "{:.2f} cm".format(dimB),
                         (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                         0.65, (0, 255, 255), 2)
    
cv2.imshow("contornos", original)
cv2.waitKey(0)
