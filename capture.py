#!/usr/bin/python
 
import subprocess
import io
import os
import time
from datetime import datetime,timedelta
from PIL import Image
import socket
#import verify.py



# Motion detection settings:
# Threshold          - how much a pixel has to change by to be marked as "changed"
# Sensitivity        - how many changed pixels before capturing an image, needs to be higher if noisy view
# ForceCapture       - whether to force an image to be captured every forceCaptureTime seconds, values True or False
# filepath           - location of folder to save photos
# filenamePrefix     - string that prefixes the file name for easier identification of files.
# diskSpaceToReserve - Delete oldest images to avoid filling disk. How much byte to keep free on disk.
# cameraSettings     - "" = no extra settings; "-hf" = Set horizontal flip of image; "-vf" = Set vertical flip; "-hf -vf" = both horizontal and vertical flip
threshold = 10
sensitivity = 20
focus= 17
forceCapture = True
forceCaptureTime = 60*60 # Once an hour
filepath = "/home/yuyang/picam"
hostname = socket.gethostname()
#get hostname to define which host sent alarm
filenamePrefix = hostname
diskSpaceToReserve = 256 * 1024 * 1024 # Keep 40 mb free on disk
#use imx477 config and open auto focus
cameraSettings = "--autofocus-mode auto --tuning-file /usr/share/libcamera/ipa/rpi/pisp/imx477.json " 
 
# settings of the photos to save
saveWidth   = 1600
saveHeight  = 1200
saveQuality = 100 # Set jpeg quality (0 to 100)

#from below is test mode setting

# Test-Image settings
testWidth = 100
testHeight = 76
 
# this is the default setting, if the whole image should be scanned for changed pixel
testAreaCount = 1
testBorders = [ [[1,testWidth],[1,testHeight]] ]  # [ [[start pixel on left side,end pixel on right side],[start pixel on top side,stop pixel on bottom side]] ]
# testBorders are NOT zero-based, the first pixel is 1 and the last pixel is testWith or testHeight
 
# with "testBorders", you can define areas, where the script should scan for changed pixel
# for example, if your picture looks like this:
#
#     ....XXXX
#     ........
#     ........
#
# "." is a street or a house, "X" are trees which move arround like crazy when the wind is blowing
# because of the wind in the trees, there will be taken photos all the time. to prevent this, your setting might look like this:
 
# testAreaCount = 2
# testBorders = [ [[1,50],[1,75]], [[51,100],[26,75]] ] # area y=1 to 25 not scanned in x=51 to 100
 
# even more complex example
# testAreaCount = 4
# testBorders = [ [[1,39],[1,75]], [[40,67],[43,75]], [[68,85],[48,75]], [[86,100],[41,75]] ]
 
# in debug mode, a file debug.bmp is written to disk with marked changed pixel an with marked border of scan-area
# debug mode should only be turned on while testing the parameters above
debugMode = False # False or True
 
# Capture a small test image (for motion detection)
def captureTestImage(settings, width, height):
    # Constructing the command with the provided settings, width, and height.
    command = f"rpicam-still {settings} --width {width} --height {height} -t 500 -e bmp -n -o -"

    # Execute the command and capture the output as binary data.
    imageData = io.BytesIO(subprocess.check_output(command, shell=True))

    # Use PIL to open the image from the binary data in memory.
    im = Image.open(imageData)
    buffer = im.load()
    imageData.close()
    return im, buffer


#from below is defining all functions

 
# Save a full size image to disk
def saveImage(settings, width, height, quality, diskSpaceToReserve):
    global filename
    keepDiskSpaceFree(diskSpaceToReserve)
    time = datetime.now()
    filename = filepath + "/" + filenamePrefix + "-%04d%02d%02d-%02d%02d%02d.jpg" % (time.year, time.month, time.day, time.hour, time.minute, time.second)
    subprocess.call("rpicam-still %s --width %s --height %s -t 1000 -e jpg -q %s -n -o %s" % (settings, width, height, quality, filename), shell=True)
    print ("Captured %s" % filename)
 
# Keep free space above given level
def keepDiskSpaceFree(bytesToReserve):
    if (getFreeSpace() < bytesToReserve):
        for filename in sorted(os.listdir(filepath + "/")):
            if filename.startswith(filenamePrefix) and filename.endswith(".jpg"):
                os.remove(filepath + "/" + filename)
                print ("Deleted %s/%s to avoid filling disk" % (filepath,filename))
                if (getFreeSpace() > bytesToReserve):
                    return
 
# Get available disk space
def getFreeSpace():
    st = os.statvfs(filepath + "/")
    du = st.f_bavail * st.f_frsize
    return du

#use pretrained model to classify all objects
def predictImage():
    global filename
    model = YOLO(r"path/to /your/file")
    # accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
    results = model.predict(source=filename, show=True, save_txt=True, save=True) 
    # Display preds. Accepts all YOLO predict arguments
    #saving to runs\detect\predict\labels. txt format is:[class] [x_center] [y_center] [width] [height] [confidence]
    return results


#Start running the program
 
# Get first image
image1, buffer1 = captureTestImage(cameraSettings, testWidth, testHeight)
 
# Reset last capture time
lastCapture = datetime.now()

# define the txt file of test img (first img)
#initxt = '~/runs/detect/predict/labels' + "/" + filenamePrefix + "-%04d%02d%02d-%02d%02d%02d.txt" % (lastCapture.year, lastCapture.month, lastCapture.day, lastCapture.hour, lastCapture.minute, lastCapture.second)
#iniarea= verify.areacount(initxt)

while (True):
 
    # Get comparison image
    image2, buffer2 = captureTestImage(cameraSettings, testWidth, testHeight)
 
    # Count changed pixels
    changedPixels = 0
    takePicture = False
 
    if (debugMode): # in debug mode, save a bitmap-file with marked changed pixels and with visible testarea-borders
        debugimage = Image.new("RGB",(testWidth, testHeight))
        debugim = debugimage.load()
     
 #area calculation
    for z in range(0, testAreaCount): # = xrange(0,1) with default-values = z will only have the value of 0 = only one scan-area = whole picture
        for x in range(testBorders[z][0][0]-1, testBorders[z][0][1]): # = xrange(0,100) with default-values
            for y in range(testBorders[z][1][0]-1, testBorders[z][1][1]):   # = xrange(0,75) with default-values; testBorders are NOT zero-based, buffer1[x,y] are zero-based (0,0 is top left of image, testWidth-1,testHeight-1 is botton right)
                if (debugMode):
                    debugim[x,y] = buffer2[x,y]
                    if ((x == testBorders[z][0][0]-1) or (x == testBorders[z][0][1]-1) or (y == testBorders[z][1][0]-1) or (y == testBorders[z][1][1]-1)):
                        # print "Border %s %s" % (x,y)
                        debugim[x,y] = (0, 0, 255) # in debug mode, mark all border pixel to blue
                # Just check green channel as it's the highest quality channel
                pixdiff = abs(buffer1[x,y][1] - buffer2[x,y][1])
                if pixdiff > threshold:
                    changedPixels += 1
                    if (debugMode):
                        debugim[x,y] = (0, 255, 0) # in debug mode, mark all changed pixel to green
                # Save an image if pixels changed
                if (changedPixels > sensitivity):
                    takePicture = True # will shoot the photo later
                if ((debugMode == False) and (changedPixels > sensitivity)):
                    break  # break the y loop
            if ((debugMode == False) and (changedPixels > sensitivity)):
                break  # break the x loop
        if ((debugMode == False) and (changedPixels > sensitivity)):
            break  # break the z loop
 
    if (debugMode):
        debugimage.save(filepath + "/debug.bmp") # save debug image as bmp
        print ("debug.bmp saved, %s changed pixel" % changedPixels)
    # else:
    #     print "%s changed pixel" % changedPixels
 
    # Check force capture
    if forceCapture:
        if datetime.now() - lastCapture > timedelta(seconds=forceCaptureTime):
            takePicture = True
 
    if takePicture:
        lastCapture = datetime.now()
        saveImage(cameraSettings, saveWidth, saveHeight, saveQuality, diskSpaceToReserve)

    #Predict objects
    results = predictImage()

    # Swap comparison buffers
    image1 = image2
    buffer1 = buffer2

