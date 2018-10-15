import os
from imutils import paths
import argparse
import time
import sys
import cv2

def showimage(destination):
	print("in showimage function")
	image = cv2.imread(destination,0)
	cv2.imshow('image',image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

while(True):
	paths = os.listdir("./buffer")
	for im in paths:
		if im.endswith('.jpg'):
			showimage('buffer/'+im)
			response=input("Enter response:")
			if(int(response)==1):
				print("cool")
				os.remove('buffer/'+im)
			else:
				print("not cool")
		else:
			continue

#showimage("buffer/20181006_224440.jpg")

def dhash(image, hashSize=8):
    # resize the input image, adding a single column (width) so we
    # can compute the horizontal gradient
    resized = cv2.resize(image, (hashSize + 1, hashSize))

    # compute the (relative) horizontal gradient between adjacent
    # column pixels
    diff = resized[:, 1:] > resized[:, :-1]

    # convert the difference image to a hash
    hash=sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
    print(hash)
    return hash

def hashyo():
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--dataset", required=True,
        help="dataset of images to search through (i.e., the haytack)")
    args = vars(ap.parse_args())
    # grab the paths to both the haystack and needle images 
    print("[INFO] computing hashes for haystack...")
    haystackPaths = list(paths.list_images(args["haystack"]))
    # remove the `\` character from any filenames containing a space
    # (assuming you're executing the code on a Unix machine)
    if sys.platform != "win32":
        haystackPaths = [p.replace("\\", "") for p in haystackPaths]
    haystack = {}
    start = time.time()
    # loop over the haystack paths
    for p in haystackPaths:
        # load the image from disk
        image = cv2.imread(p)

        # if the image is None then we could not load it from disk (so
        # skip it)
        if image is None:
            continue

        # convert the image to grayscale and compute the hash
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imageHash = dhash(image)

        # update the haystack dictionary
        l = haystack.get(imageHash, [])
        l.append(p)
        haystack[imageHash] = l
        #print(haystack)

