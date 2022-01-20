import cv2 as cv

def Detect(image):
    points_dict = {}
    arucoDict = cv.aruco.Dictionary_get(cv.aruco.DICT_5X5_100)
    arucoParams = cv.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv.aruco.detectMarkers(image, arucoDict,parameters=arucoParams)
    if len (corners) > 0:
        ids =  ids.flatten()
        for (markerCorner,markerID) in zip(corners,ids):
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            points_dict[str(markerID)] = {'tl':topLeft,'tr':topRight,'bl':bottomLeft,'br':bottomRight}
            cv.circle(image, (cX, cY), 4, (0, 0, 255), -1)
        return [points_dict['1'].get('tr'),points_dict['2'].get('tl'),points_dict['3'].get('br'),points_dict['4'].get('bl')] 