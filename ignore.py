import numpy as np
import cv2 as cv
import json

cap = cv.VideoCapture(1)

with open('calibration.json') as f:
	params = json.load(f)

#	while(True):
#		if ard.readline():
#			break

while True:
    ret, img = cap.read()

    if ret == True:
        crop_img = img[params["y2"]:params["y1"], params["x1"]:params["x2"]]
        hsv_crop = cv.cvtColor(crop_img, cv.COLOR_BGR2HSV)
        thresh_hsv = cv.inRange(hsv_crop, (params["h_low"], params["s_low"], params["v_low"]), (params["h_high"], params["s_high"], params["v_high"]))
        inv_thresh = 255 - thresh_hsv

        #Count number of white pixels
        size = inv_thresh.size
        count = cv.countNonZero(inv_thresh)

        cv.imshow("blak", inv_thresh)
        k = cv.waitKey(1) & 0xFF
        if k == ord('q') or count > (size / 4):
            cv.imwrite('THING.jpg', crop_img)
            cv.imshow("bakchoi", crop_img)
    else:
        break
cap.release()
cv.destroyAllWindows()
