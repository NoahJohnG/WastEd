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
	cap = cv.VideoCapture(0)

	fgbg = cv.createBackgroundSubtractorMOG2()
	# Setup fbgb paramaters
	fgbg.setVarThreshold(200)

	# Setup initial location of window
	r,h,c,w = 250,int(cap.get(4)/1.75),400,int(cap.get(3)/1.75) # simply hardcoded the values
	track_window = (c,r,w,h)

	# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
	term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )

	# Setup stage
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
				# Output frame after waiting a second and a half
				cv.waitKey(1500)
				cv.imwrite('THING.jpg', frame)
				break
			x,y,w,h = track_window
			center = (int(x + w/2), int(y + h/2))
			img2 = cv.circle(fgmask, stage, 50, 100, 2)
			img2 = cv.circle(img2, center, 5, 255,2)
			cv.imshow('waiting', img2)

			k =  cv.waitKey(1) & 0xFF
			if k == ord('q'):
				break
		else:
			break
	# When everything done, release the capture
	cap.release()



if __name__ == "__main__":
	main()