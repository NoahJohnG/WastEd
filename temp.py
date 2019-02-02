import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'bread.jpg')

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
		print("Recyclable!")
		trash = False
		break;
	elif (item.description + "\n") in compost_list:
		print("Compostable!")
		trash = False
		break;
if trash:
	print("Trash!")