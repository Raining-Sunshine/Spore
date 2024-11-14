import argparse
import json
import subprocess
import io
import logging
import os
import time
import shlex
from pathlib import Path
from subprocess import Popen, PIPE
from time import sleep
import cv2
import requests
from gpiozero import LED  # type: ignore
from picamera2 import Picamera2, MappedArray  # type: ignore
from datetime import datetime,timedelta
from PIL import Image
import socket
from motor import MotorControl
from roboflow import Roboflow

filepath = "/home/pi/picam"
hostname = socket.gethostname()
#get hostname to define which host sent alarm
filenamePrefix = hostname
diskSpaceToReserve = 256 * 1024 * 1024 # Keep 40 mb free on disk
max_file_count = 10
#use imx477 config and open auto focus
cameraSettings = "--autofocus-mode auto --tuning-file /home/pi/Arducam-477P-Pi5.json " 
 
# settings of the photos to save
saveWidth   = 1600
saveHeight  = 1200
saveQuality = 100 # Set jpeg quality (0 to 100)

# Initialize the Roboflow object with your API key
rf = Roboflow(api_key="CeEPhbziMVE60CsewDGS")
workspaceId = 'yuyang-zhang-vhs3j'
projectId = 'yellow-rust-cu5jk'
project = rf.workspace(workspaceId).project(projectId)

logging.basicConfig(
    filename='script.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# Get available disk space
def getFreeSpace():
    st = os.statvfs(filepath + "/")
    du = st.f_bavail * st.f_frsize
    return du

def manageFileCount(directory, max_count):
    """
    Deletes the oldest files in the directory until the file count is within the allowed limit.
    """
    # Get list of all files in the directory with their full paths
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".jpg")]

    # If file count exceeds the maximum limit
    if len(files) > max_count:
        # Sort files by modification time (oldest first)
        files.sort(key=os.path.getmtime)
        
        # Calculate how many files need to be deleted
        files_to_delete = len(files) - max_count
        
        # Delete the oldest files
        for i in range(files_to_delete):
            try:
                os.remove(files[i])
                print(f"Deleted {files[i]} to maintain file count limit.")
            except Exception as e:
                print(f"Error deleting file {files[i]}: {e}")


def keepDiskSpaceFree(bytesToReserve):
    manageFileCount(filepath, max_file_count)
    if (getFreeSpace() < bytesToReserve):
        for filename in sorted(os.listdir(filepath + "/")):
            if filename.startswith(filenamePrefix) and filename.endswith(".jpg"):
                os.remove(filepath + "/" + filename)
                print ("Deleted %s/%s to avoid filling disk" % (filepath,filename))
                if (getFreeSpace() > bytesToReserve):
                    return
                

def saveImage(settings, width, height, quality, diskSpaceToReserve):
    keepDiskSpaceFree(diskSpaceToReserve)
    time = datetime.now()
    filenameSuffix = filenamePrefix + "-%04d%02d%02d-%02d%02d%02d" % (time.year, time.month, time.day, time.hour, time.minute, time.second)
    filename = filepath + "/" + filenameSuffix + ".jpg"
    subprocess.call("rpicam-still %s --width %s --height %s -t 1000 -e jpg -q %s -n -o %s" % (settings, width, height, quality, filename), shell=True)
    print ("Captured %s" % filename)
    return filename, filenameSuffix

def uploadimage(filename):
    try:
        response = project.upload(filename)
        print(f"Uploaded {filename}, response: {response}")
    except Exception as e:
        logging.error(f"Failed to upload {filename}: {e}")




while (True):
    takepicture=True
    upload=True
    if takepicture:
     try:
        captured_name, captured_nameSuffix = saveImage(cameraSettings, saveWidth, saveHeight, saveQuality, diskSpaceToReserve)
     except Exception as e:
        logging.error(f"Error capturing image: {e}")
    

    if upload:
        uploadimage(captured_name)
