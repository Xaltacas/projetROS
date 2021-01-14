#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.srv import GetMap
import math
import time
import numpy as np
import cv2
import prm as algo
from bresenham import collide
from utils import *

imageOut = True





if __name__ == "__main__":

    rospy.wait_for_service("dynamic_map")
    service = rospy.ServiceProxy("dynamic_map",GetMap)
    map = service().map

    vect = np.array(map.data)

    #print(np.histogram(vect,bins = 255))

    data = np.reshape(vect,(1600,1600))

    xmin, xmax, ymin , ymax = getAOI(data)

    print("AOI",xmin, xmax, ymin , ymax)

    cropped = data[xmin:xmax,ymin:ymax]

    height,width = cropped.shape
    for x in range(height):
        for y in range(width):
            if cropped[x][y] == -1:
                cropped[x][y] = 255
            elif cropped[x][y] == 0:
                cropped[x][y] = 0
            else:
                cropped[x][y] = 255
    img = np.array(cropped,'uint8')



    kernel = np.ones((8,8),'uint8')
    img = cv2.dilate(img,kernel)

    img = cv2.erode(img,kernel)

    img = cv2.medianBlur(np.float32(img),5)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(20,20))
    final = cv2.dilate(img,kernel)

    final = 255-final

    prm = algo.PRM(final,100,10)


    miniPath = prm.path((74,769),(215,157))
    print("minipath : \n")
    print(miniPath)

    print("smoothmini")
    print(smooth(miniPath,4))

    origin = (map.info.origin.position.x,map.info.origin.position.y)
    resolution = map.info.resolution

    globalPathPix = []
    globalPathPos = []
    for elem in miniPath:
        gElem = mini2global(elem,xmin, xmax, ymin , ymax)
        globalPathPix.append(gElem)
        globalPathPos.append(pix2m(gElem,origin,resolution))


    print("global")
    print(globalPathPix)
    print("pos")
    print(globalPathPos)



    print("is oke")
