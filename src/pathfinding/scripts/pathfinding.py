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


imageOut = True


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

def mini2global(pos,xmin, xmax, ymin , ymax):
    return pos[0] + xmin, pos[1] +ymin

def global2mini(pos,xmin, xmax, ymin , ymax):
    if( pos[0]>xmax or pos[0]<xmin or pos[1]>ymax or pos[0]<ymin ):
        return None
    return pos[0] - xmin, pos[1] -ymin

def pix2m(pos,origin,resolution):
    return origin[0] + (resolution * pos[0]), origin[1] + (resolution * pos[1])

def smooth(path, map, div = 10):
    _div = 1./div
    subpath= [path[0]]
    prevpoint = path[0]
    for point in path[1:]:
        for i in range(1,div+1):
            diffx = point[0] - prevpoint[0]
            diffy = point[1] - prevpoint[1]

            subpath.append((int(prevpoint[0]+ diffx*i*_div),int(prevpoint[1]+ diffy*i*_div)))
        prevpoint = point

    res = [subpath[0]]
    current = 0
    point = 1
    while True :
        if(point == len(subpath)-1):
            res.append(subpath[point])
            break
        if (collide(subpath[current],subpath[point],map)):
            res.append(subpath[point-1])
            current= point - 1
        point += 1

    return res


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


    if imageOut:
        cv2.imwrite("1-map.jpg",255 -cropped)

    img = np.array(cropped,'uint8')



    kernel = np.ones((8,8),'uint8')

    img = cv2.dilate(img,kernel)

    if imageOut:
        cv2.imwrite("2-dilate8.jpg",255 -img)
    img = cv2.erode(img,kernel)

    if imageOut:
        cv2.imwrite("3-erode8.jpg",255 -img)

    img = cv2.medianBlur(np.float32(img),5)
    if imageOut:
        cv2.imwrite("4-mBlur3.jpg",255 -img)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(20,20))

    final = cv2.dilate(img,kernel)
    if imageOut:
        cv2.imwrite("5-final.jpg",255 -final)

    final = 255-final

    prm = algo.PRM(final,100,10)

    cv2.imwrite("linkedmap.jpg",prm.returnLinkedMap())

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
