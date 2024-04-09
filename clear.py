#clear the txt files generated and (tested pic)
filepathtxt="runs\detect\predict\labels" #path to txt
filepathimg="path\to\verifiedimg"   #path to verified images
FreeSpaceInDisk= 256 * 1024 * 1024 

# Keep free space above given level (img+txt)
def keepimgDiskSpaceFree(bytesToReserve): 
    if (getFreeSpace() < bytesToReserve):
        #clear txt
        for filename in sorted(os.listdir(filepathtxt + "/")):
            if filename.startswith(filenamePrefix) and filename.endswith(".txt"):
                os.remove(filepathtxt + "/" + filename)
                print "Deleted %s/%s to avoid filling disk" % (filepathtxt,filename)
                if (getFreeSpace() > bytesToReserve):
                    return
        #clear img
        for filename in sorted(os.listdir(filepathimg + "/")):
            if filename.startswith(filenamePrefix) and filename.endswith(".txt"):
                os.remove(filepathimg + "/" + filename)
                print "Deleted %s/%s to avoid filling disk" % (filepathimg,filename)
                if (getFreeSpace() > bytesToReserve):
                    return
 
# Get available disk space
def getFreeSpace():
    st = os.statvfs(filepath + "/")
    du = st.f_bavail * st.f_frsize
    return du