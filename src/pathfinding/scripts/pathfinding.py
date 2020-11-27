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

    cv2.imwrite("map.jpg",255-cropped)
    #cv2.imshow("sacree map",data)
    #cv2.waitKey(0)

    #print(map.type)
    print(type(map.data))
    print(len(map.data))
    print("coucou")
