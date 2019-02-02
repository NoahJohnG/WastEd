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
fgbg.setVarThreshold(300)

# setup initial location of window
r,h,c,w = 250,90,400,125  # simply hardcoded the values
track_window = (c,r,w,h)
# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi =  cv.cvtColor(roi, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv.normalize(roi_hist,roi_hist,0,255,cv.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )

frame_cnt = 0
frame_limit = 10
prev_pos = track_window[:2]
dist = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    #Inc frame counter
    frame_cnt += 1
    if frame_cnt == frame_limit:
        dist = math.sqrt((prev_pos[0]-track_window[0])**2 + (prev_pos[1] - track_window[1])**2)
        prev_pos = track_window[:2]
        frame_cnt = 0

    if ret == True:
        # Apply Mask
        fgmask = fgbg.apply(frame)

        # apply meanshift to get the new location
        ret, track_window = cv.meanShift(fgmask, track_window, term_crit)

        if dist > 100:
            # Draw it on image
            x,y,w,h = track_window
            img2 = cv.rectangle(fgmask, (x,y), (x+w,y+h), 255,2)
        else:
            img2 = fgmask

        #Display image
        cv.imshow('img2',img2)
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