# WastEd

## wasted.ino
  * receives serial data from hello.py
  * interprets bytes as compost, trash or recycling using defined constants
    * ```COMPOST == 1```
    * ```RECYCLE == 2```
    * ```TRASH == 3```
## hello.py
  * receives image data 
  * analyzes image with google cloud vision
  * based on image analysis confidence, sorts as compost, recylce or (default) trash
  * sends classification to arduino 
  * receives message back from arduino indicating waste category
  
## .json
  * credentials for google cloud vision

## compost.txt
  * key words indicating waste category is compost
  
## recycle.txt
  * key words indicating waste category is compost 

## vidCap.py  
  * records motion tracking video
  * saves a jpeg photo of an object placed onto staging area
