import numpy as np
import cv2 as cv


cap = cv.VideoCapture(0, cv.CAP_DSHOW)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
print("camera opened")
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    #     # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Display the resulting frame
    cv.imshow('frame', frame)
    # except:
    #     pass
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()