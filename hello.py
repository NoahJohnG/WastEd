import io
import os
import serial
import time
import numpy as np
import cv2 as cv
import math

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

def main():
	# Instantiates a client
	client = vision.ImageAnnotatorClient()

		ard = serial.Serial("/dev/cu.usbmodem1411", 9600, timeout=2)
	time.sleep(2)

	with io.open("recycle.txt", "r") as recycle_file:
		recycle_list = recycle_file.readlines()
	with io.open("compost.txt", "r") as compost_file:
		compost_list = compost_file.readlines()

	file_name = os.path.join(os.path.dirname(__file__),'THING.jpg')

	while True:
		wait_trash()

		# Loads the image into memory
		with io.open(file_name, 'rb') as image_file:
			content = image_file.read()

		image = types.Image(content=content)

		# Performs label detection on the image file
		response = client.label_detection(image=image)
		labels = response.label_annotations

		# CONFIDENCE VALUE, UPDATE IF NECESSARY

		labels = [x for x in labels if x.score > .5]

		trash = True
		for item in labels:
			if (item.description + "\n") in recycle_list:
				print("Recyclable!") # recycle 2
				recycle_val = int_to_byte(2)
				write_to_arduino(recycle_val, ard)
				trash = False
				break
			elif (item.description + "\n") in compost_list:
				print("Compostable!") # compost 1
				compost_val = int_to_byte(1)
				write_to_arduino(compost_val, ard)
				trash = False
				break
		if trash:
			print("Trash!") # trash 3
			trash_val = int_to_byte(1)
			write_to_arduino(trash_val, ard)



def int_to_byte(x):
    if(x ==1):
        return b'1'
    elif(x == 2):
        return  b'2'
    elif(x==3):
        return b'3'
    else:
        return b'0'

def write_to_arduino(x, ard):
	ard.write(x)
	time.sleep(2)
	msg = ard.readline()
	print(msg)

def wait_trash():
	cap = cv.VideoCapture(0)

	while(True):
		dist = ard.readline()
		if dist < threshhold:
			break

	# Capture frame-by-frame
	ret, frame = cap.read()

	if ret == True:
		cv.imwrite('THING.jpg', frame)

	cap.release()

if __name__ == "__main__":
	main()