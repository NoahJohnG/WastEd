import numpy as np
import cv2 as cv

def draw_keypoints(vis, keypoints, color = (0, 0, 255)):
    for kp in keypoints:
            x, y = kp.pt
            cv.circle(vis, (int(x), int(y)), int(kp.size/2), color)

cap = cv.VideoCapture(0)

fgbg = cv.createBackgroundSubtractorMOG2()

retval = cv.SimpleBlobDetector_create()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        # Apply Mask
        fgmask = fgbg.apply(frame)

        # Detect blobs.
        keypoints = retval.detect(fgmask)

        # Draw detected blobs as red circles.
        draw_keypoints(fgmask, keypoints, (0,0,255))

        # Display the resulting frame
        cv.imshow('img', fgmask)
        k =  cv.waitKey(1) & 0xFF
        if k == ord('q'):
            break
        elif k == ord('c'):
            cv.imwrite('capture.jpg', frame)
    else:
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()