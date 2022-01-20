from turtle import width
import cv2 as cv
import aruco_detec
import trace_image
image_width = 740
image_height = 411

original = cv.imread("./aruco_tela.png")
image = cv.resize(original, (image_width, image_height))
points = aruco_detec.Detect(image)
dst = trace_image.Align(image,points,image_width,image_height)
cv.imshow("resultado",image)
cv.imshow("alineada",dst)
cv.waitKey(0)
cv.destroyAllWindows