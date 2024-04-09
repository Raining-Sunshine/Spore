from ultralytics import YOLO
'''from PIL import Image
import cv2'''

model = YOLO(r"path/to /your/file")
# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
results = model.predict(source="/home/pi/picam", show=True, save_txt=True, save=True) # Display preds. Accepts all YOLO predict arguments
#saving to runs\detect\predict\labels. txt format is:[class] [x_center] [y_center] [width] [height] [confidence]

'''# from PIL
im1 = Image.open("bus.jpg")
results = model.predict(source=im1, save=True)  # save plotted images

# from ndarray
im2 = cv2.imread("bus.jpg")
results = model.predict(source=im2, save=True, save_txt=True)  # save predictions as labels

# from list of PIL/ndarray
results = model.predict(source=[im1, im2])'''

txtfolderpath="path to txt folder"

def calcgermrate():
    tempfile = f"{txtfolderpath}/{filenamePrefix}-%04d%02d%02d-%02d%02d%02d.txt" % (
        time.year, time.month, time.day, time.hour, time.minute, time.second)
    temparea = areacount(tempfile)
    GerminationRate = temparea / iniarea
    return GerminationRate

def areacount(pathTotxt):
    total_area = 0
    try:
        with open(pathTotxt, 'r') as file:
            for line in file:
                components = line.split()
                if len(components) == 6:  # Ensure there are enough components to avoid errors
                    area = float(components[3]) * float(components[4])
                    total_area += area
    except FileNotFoundError:
        print(f"File not found: {pathTotxt}")
        # Handle the file not found error or return a default value
        return 0
    return total_area


    
# Example usage:
germrate = calcgermrate()  # Assume you get this value from somewhere
alarm(germrate) #trigger alarm

keepimgDiskSpaceFree(FreeSpaceInDisk) #clear generated files of yolo