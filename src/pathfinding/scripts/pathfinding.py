#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.srv import GetMap
import math
import time
import numpy as np
import cv2

def getAOI(map):
    height,width = map.shape

    xmin = height
    xmax = 0

    ymin = width
    ymax = 0

    for x in range(height):
        for y in range(width):
            if( data[x][y] != -1):
                xmin = min(xmin,x)
                xmax = max(xmax,x)
                ymin = min(ymin,y)
                ymax = max(ymax,y)

    return xmin, xmax, ymin , ymax



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


    cv2.imwrite("1-map.jpg",255 -cropped)

    img = np.array(cropped,'uint8')



    kernel = np.ones((8,8),'uint8')

    img = cv2.dilate(img,kernel)

    cv2.imwrite("2-dilate8.jpg",255 -img)
    img = cv2.erode(img,kernel)

    cv2.imwrite("3-erode8.jpg",255 -img)

    img = cv2.medianBlur(np.float32(img),3)
    cv2.imwrite("4-mBlur3.jpg",255 -img)

    kernel = np.ones((10,10),'uint8')

    final = cv2.dilate(img,kernel)
    cv2.imwrite("5-final.jpg",255 -final)

    print("is oke")
