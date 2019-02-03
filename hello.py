import io
import os
import serial
import time
import numpy as np
import cv2 as cv
import math
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "slo-hacks-wasted",
})

db = firestore.client()
users_ref = db.collection(u'names').document(u'wastEd OG bin')

def main():

	# Instantiates a client
	client = vision.ImageAnnotatorClient()

	wait_trash()

	# The name of the image file to annotate
	file_name = os.path.join(
		os.path.dirname(__file__),'THING.jpg')

	ard = serial.Serial("/dev/cu.usbmodem1411", 9600, timeout=2)
	time.sleep(2)

	with io.open("recycle.txt", "r") as recycle_file:
		recycle_list = recycle_file.readlines()
	with io.open("compost.txt", "r") as compost_file:
		compost_list = compost_file.readlines()

	# Loads the image into memory
	with io.open(file_name, 'rb') as image_file:
		content = image_file.read()

	image = types.Image(content=content)

	# Performs label detection on the image file
	response = client.label_detection(image=image)
	labels = response.label_annotations


	for x in labels:
		print(x.description)

	# CONFIDENCE VALUE, UPDATE IF NECESSARY

	labels = [x for x in labels if x.score > .5]

	if len(labels) == 0:
		print("Unable to determine item!")
		quit()

	transaction = db.transaction()
	snapshot = users_ref.get()

	@firestore.transactional
	def update_in_transaction(transaction, users_ref, x):
		snapshot = users_ref.get(transaction=transaction)
		if(x ==1):
			transaction.update(users_ref, {
				u'Compost': snapshot.get(u'Compost') + 1
			})
			transaction.update(users_ref, {
				u'Score': (snapshot.get(u'Recycling')*2) + (snapshot.get(u'Compost')*3) - (snapshot.get(u'Trash'))
			})
		elif(x==2):
			transaction.update(users_ref, {
				u'Recycling': snapshot.get(u'Recycling') + 1
			})
			transaction.update(users_ref, {
				u'Score': (snapshot.get(u'Recycling')*2) + (snapshot.get(u'Compost')*3) - (snapshot.get(u'Trash'))
			})
		else:
			transaction.update(users_ref, {
				u'Trash': snapshot.get(u'Trash') + 1
			})
			transaction.update(users_ref, {
				u'Score': (snapshot.get(u'Recycling')*2) + (snapshot.get(u'Compost')*3) - (snapshot.get(u'Trash'))
			})

	trash = True
	for item in labels:
		if (item.description + "\n") in recycle_list:
			print("Recyclable!") # recycle 2
			recycle_val = int_to_byte(2)
			write_to_arduino(recycle_val, ard)
			update_in_transaction(transaction, users_ref, 2)
			trash = False
			break
		elif (item.description + "\n") in compost_list:
			print("Compostable!") # compost 1
			compost_val = int_to_byte(1)
			write_to_arduino(compost_val, ard)
			update_in_transaction(transaction, users_ref, 1)
			trash = False
			break
	if trash:
		print("Trash!") # trash 3
		trash_val = int_to_byte(3)
		write_to_arduino(trash_val, ard)
		update_in_transaction(transaction, users_ref, 3)

def int_to_byte(x):
    if(x ==1):
        return b'C'
    elif(x == 2):
        return  b'R'
    elif(x==3):
        return b'T'
    else:
        return b'0'

def write_to_arduino(x, ard):
	ard.write(x)
	time.sleep(2)
	msg = ard.readline()
	print(msg)

def wait_trash():
	cap = cv.VideoCapture(1)

	with open('calibration.json') as f:
		params = json.load(f)

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

#			cv.imshow("blak", inv_thresh)
			k = cv.waitKey(1) & 0xFF
			if k == ord('q') or count > (size / 4):
				cv.imwrite('THING.jpg', crop_img)
				break
		else:
			break
	cap.release()
	cv.destroyAllWindows()



if __name__ == "__main__":
	main()