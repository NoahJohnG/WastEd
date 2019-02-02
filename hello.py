import io
import os
import serial
import time

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

def main():

	# Instantiates a client
	client = vision.ImageAnnotatorClient()

	# The name of the image file to annotate
	file_name = os.path.join(
		os.path.dirname(__file__),
		'bread.jpg')

	ard = serial.Serial('/dev/cu.usbmodem1141', 9600, timeout=5)

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

	# CONFIDENCE VALUE, UPDATE IF NECESSARY

	labels = [x for x in labels if x.score > .5]

	if len(labels) == 0:
		print("Unable to determine item!")
		quit()

	trash = True
	for item in labels:
		if (item.description + "\n") in recycle_list:
			print("Recyclable!") # recycle 2
			recycle_val = int_to_byte(2)
			write_to_arduino(recycle_val, ard)
			trash = False
			break;
		elif (item.description + "\n") in compost_list:
			print("Compostable!") # compost 1
			compost_val = int_to_byte(1)
			write_to_arduino(compost_val, ard)
			trash = False
			break;
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
	time.sleep(.5)
	msg = ard.readline()
	print(msg)
