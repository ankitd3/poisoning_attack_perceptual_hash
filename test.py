import os
from imutils import paths
import argparse
import time
import sys
import cv2
import time
import json

def dhash(image, hashSize=8):
    # resize the input image, adding a single column (width) so we
    # can compute the horizontal gradient
    resized = cv2.resize(image, (hashSize + 1, hashSize))

    # compute the (relative) horizontal gradient between adjacent
    # column pixels
    diff = resized[:, 1:] > resized[:, :-1]

    # convert the difference image to a hash
    hash=sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
    #print(hash)
    return hash

def showimage(destination):
    print("in showimage function")
    image = cv2.imread(destination,0)
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

def review(im,magic,imageHash):
    if(magic==2):
        showimage('buffer/'+im)
        response=input("Enter response:")
        if(int(response)==1):
            print("[info]Moving to imp")
            os.rename('buffer/'+im,'important/'+im)
        else:
            with open('hash_count.json') as yo:
                data=json.load(yo)
            data[imageHash]=0
            
            with open('hash_count.json', 'w') as fi:
                json.dump(data, fi)
    if(magic==1):
        showimage('buffer/'+im)
        response=input("Enter response:")
        if(int(response)==1):
            print("[info]Moving to imp and deleting poison image hash in db")
            os.rename('buffer/'+im,'important/'+im)

            with open('hash_count.json') as yo:
                data=json.load(yo)
            del data[str(imageHash)]
            with open('hash_count.json', 'w') as fi:
                json.dump(data, fi)
        else:
            print("[info]Count reduced to 1")
            with open('hash_count.json') as yo:
                data=json.load(yo)
            data[str(imageHash)]=1
            with open('hash_count.json', 'w') as fi:
                json.dump(data, fi)


def stage1(image_path):
    im=cv2.imread('buffer/'+image_path)
    imageHash = dhash(im)

    with open('hash_count.json') as f:
        data = json.load(f)

    if str(imageHash) in data:

        data[str(imageHash)]+=1
        with open('hash_count.json', 'w') as fi:
            json.dump(data, fi)

        if(data[str(imageHash)]>5):
            review(image_path,1,imageHash)
        else:
            os.remove('buffer/'+image_path)
    else:
        review(image_path,2,imageHash)

    return True


while(True):
    time.sleep(1)
    print("In while")
    paths = os.listdir("./buffer")
    print(paths)
    #print(im.endswith('.jpg'))
    for im in paths:
        print("In for loop")
        #print(im)
        if im.endswith('.jpg'):
            stage1(im)
        else:
            os.remove('buffer/'+im)
            continue