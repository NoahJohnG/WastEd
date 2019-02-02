import numpy as np
import cv2 as cv
import math

def draw_keypoints(vis, keypoints, color = (0, 0, 255)):
    for kp in keypoints:
            x, y = kp.pt
            cv.circle(vis, (int(x), int(y)), int(kp.size/2), color)

cap = cv.VideoCapture(0)

# take first frame of the video
ret,frame = cap.read()

fgbg = cv.createBackgroundSubtractorMOG2()
# Setup fbgb paramaters
fgbg.setVarThreshold(200)

# setup initial location of window
r,h,c,w = 250,int(cap.get(4)/1.75),400,int(cap.get(3)/1.75) # simply hardcoded the values
track_window = (c,r,w,h)
# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi =  cv.cvtColor(roi, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv.normalize(roi_hist,roi_hist,0,255,cv.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )

stage = (int(cap.get(3)/2), int(cap.get(4)/2))
dist = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    dist = math.sqrt((stage[0]-int(track_window[0] + track_window[2]/2))**2 + (stage[1] - int(track_window[1] + track_window[3]/2))**2)

    if ret == True:
        # Apply Mask
        fgmask = fgbg.apply(frame)

        # apply meanshift to get the new location
        ret, track_window = cv.meanShift(fgmask, track_window, term_crit)

        if dist < 100:
            # Output frame after waiting half a second
            cv.waitKey(1500)
            cv.imwrite('THING.JPG', frame)
            break
        x,y,w,h = track_window
        center = (int(x + w/2), int(y + h/2))
        img2 = cv.circle(fgmask, stage, 50, 100, 2)
        img2 = cv.circle(img2, center, 5, 255,2)
        cv.imshow("Empty", fgmask)

        k =  cv.waitKey(1) & 0xFF
        if k == ord('q'):
            break
    else:
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
while cv.waitKey(1) & 0xFF != ord('q'):
    cv.imshow('MOVEMENT', frame)