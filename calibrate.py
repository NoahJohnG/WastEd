from __future__ import print_function
import cv2 as cv
import argparse
import json

max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'
left_x=0
right_x=1280
low_y=720
high_y=0
def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)
def on_low_y_trackbar(val):
    global low_y
    global high_y
    low_y=val
    high_y=min(high_y, low_y-1)

def on_high_y_trackbar(val):
    global low_y
    global high_y
    high_y = val
    low_y = max(high_y+1, low_y)
def on_left_x_trackbar(val):
    global left_x
    global right_x
    left_x = val
    right_x=max(right_x, left_x+1)
def on_right_x_trackbar(val):
    global left_x
    global right_x
    right_x=val
    left_x=min(right_x-1, left_x)
cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name)
cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)
cv.createTrackbar("Topmost Crop Boundary", window_capture_name, high_y, 720, on_high_y_trackbar)
cv.createTrackbar("Lower Crop Boundary", window_capture_name, low_y, 720, on_low_y_trackbar)
cv.createTrackbar("Leftmost Crop Boundary", window_capture_name, left_x, 1280, on_left_x_trackbar)
cv.createTrackbar("Rightmost Crop Boundary", window_capture_name, right_x, 1280, on_right_x_trackbar)
calibration={}
while True:

    frame=cv.imread("calibration.jpg")
    if frame is None:
        break
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    frame_inverted = 255 - frame_threshold

    cv.line(frame, (left_x,0), (left_x,720), (0,255,0))
    cv.line(frame, (right_x,0), (right_x,720), (0,255,0))
    cv.line(frame, (0,high_y), (1280,high_y), (0,255,0))
    cv.line(frame, (0,low_y), (1280,low_y), (0,255,0))
    cv.imshow(window_capture_name, frame)

    cv.imshow(window_detection_name, frame_threshold)
    cv.imshow("Inverted", frame_inverted)

    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        with open('calibration.json', 'w') as outfile:
            calibration['h_high']=high_H
            calibration['h_low']=low_H
            calibration['s_high']=high_S
            calibration['s_low']=low_S
            calibration['v_high']=high_V
            calibration['v_low']=low_V
            calibration['x1']=left_x
            calibration['x2']=right_x
            calibration['y1']=low_y
            calibration['y2']=high_y

            json.dump(calibration, outfile)
        break
