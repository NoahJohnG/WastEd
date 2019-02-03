# WastEd

## wasted.ino
  * receives serial data from hello.py
  * interprets bytes as compost, trash or recycling using defined constants
    * ```COMPOST == 1```
    * ```RECYCLE == 2```
    * ```TRASH == 3```
## hello.py
  * waits for camera to detect motion and centered object
  * captures image
  * analyzes image with google cloud vision
  * based on image analysis confidence, sorts as compost, recylce or (default) trash
  * sends classification to arduino 
  * receives message back from arduino indicating waste category
  
## Site/site.py
 * runs website 
 * css, js, scss, and img in /static
 * html files in /templates

## compost.txt
  * key words indicating waste category is compost
  
## recycle.txt
  * key words indicating waste category is recycling 

## vidCap.py  
  * ?? now combined with hello.py ...? i think
  * records motion tracking video
  * saves a jpeg photo of an object placed onto staging area
