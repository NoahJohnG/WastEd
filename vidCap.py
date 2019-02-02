import numpy as np
import cv2 as cv
cap = cv.VideoCapture(1)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame',frame)
    k = cv.waitKey(1)
    if k == ord('q'):
        break
    elif k == ord('c'):
        cv.imwrite('capture.jpg', frame)
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()