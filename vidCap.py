import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

retval = cv.SimpleBlobDetector_create()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        # Detect blobs.
        keypoints = retval.detect(frame)

        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        im_with_keypoints = cv.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # Display the resulting frame
        cv.imshow('img', frame)
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