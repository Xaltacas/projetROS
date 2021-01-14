#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.srv import GetMap
import math
import time
import numpy as np
import cv2
import prm as algo
from utils import getAOI

imageName ="reel"


if __name__ == "__main__":

    rospy.wait_for_service("dynamic_map")
    service = rospy.ServiceProxy("dynamic_map",GetMap)
    map = service().map

    vect = np.array(map.data)


    data = np.reshape(vect,(map.info.height,map.info.width))

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
    print("cropped")

    cv2.imwrite(imageName+"_1-map.jpg",255 -cropped)


    kernel = np.ones((8,8),'uint8')
    img = cv2.dilate(img,kernel)
    print("dilate")

    cv2.imwrite(imageName+"_2-dilate8.jpg",255 -img)

    img = cv2.erode(img,kernel)
    print("erode")

    cv2.imwrite(imageName+"_3-erode8.jpg",255 -img)

    img = cv2.medianBlur(np.float32(img),5)
    print("blur")

    cv2.imwrite(imageName+"_4-mBlur3.jpg",255 -img)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(20,20))
    final = cv2.dilate(img,kernel)
    print("final")

    cv2.imwrite(imageName+"_5-final.jpg",255 -final)

    final = 255-final
    print("debutPRM")
    prm = algo.PRM(final,100,10)

    cv2.imwrite(imageName+"_linkedmap.jpg",prm.returnLinkedMap())

    print("ok")
